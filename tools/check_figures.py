"""Şekilli soruların görsel denetimi.
import os
Her şekilli soru kalıbından örnek üretir, şekli gerçekten çizer (uygulamanın kendi çizicisiyle),
şekil üzerindeki yazıları toplar ve sorunun metninde geçen sayıların şekilde de yazılı olduğunu kontrol eder.
Sonuç: rapor (stdout) + inceleme sayfası (HTML, şekiller gömülü).

Kullanım:  python3 tools/check_figures.py [app.py] [çıktı.html] [kalıp başına örnek]
"""
import base64, collections, html, io, os, re, sys, tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DENEMEMATIK_DATA", tempfile.mkdtemp())
import build_pool as bp  # noqa: E402


# Bu dosya tools/ içinde olduğu için bir üst klasöre (ana dizine) çıkar
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP = os.path.join(ROOT_DIR, "app.py")

OUT = sys.argv[2] if len(sys.argv) > 2 else "/home/claude/figure_check.html"
PER = int(sys.argv[3]) if len(sys.argv) > 3 else 12
ai, cur, store = bp.load_pkg(APP)
import importlib  # noqa: E402
vis = importlib.import_module(ai.__name__.rsplit(".", 1)[0] + ".visuals")

NUM = re.compile(r"(?<![\w.,])(\d+(?:[.,]\d+)?)(?![\w])")
# soru metninde geçip şekilde yazılması gerekmeyen sayılar: fiyat/oran/adım/sıra bilgileri
EXEMPT_AFTER = re.compile(r"^\s*(TL|kuruş|N'luk|N’luk|N\b|g’lık|g'lık|kg’lık|\.\s*(adım|sıra|gün)|’lik|’lık|’ü|’i|’u|’ı|tane|kez|sıra|katı|kat\b|öğrenci|kişi|yıl|ay\b)")


def fig_texts(shape):
    """Şekli çizer; PNG ve şekil üzerindeki tüm yazıları döndürür."""
    t = vis.shape_type(shape)
    if not t or t == "table" or t not in vis._DISPATCH:
        return None, None
    plt = vis.plt
    sh = dict(shape)
    if t == "moon_phases" and "sub_type" not in sh:
        sh["sub_type"] = "moon_phases"
    fig, ax = plt.subplots(figsize=(6.2, 3.8))
    try:
        ax.axis("off")
        ax.set_aspect("equal")
        vis._DISPATCH[t](ax, sh)
        txt = [x.get_text() for x in ax.texts] + [ax.get_title()] + [x.get_text() for x in ax.get_xticklabels()] + [x.get_text() for x in ax.get_yticklabels()]
        for x in fig.texts:
            txt.append(x.get_text())
        leg = ax.get_legend()
        if leg:
            txt += [x.get_text() for x in leg.get_texts()]
        buf = io.BytesIO()
        fig.savefig(buf, format="png", bbox_inches="tight", dpi=110, facecolor="white", pad_inches=.12)
        return buf.getvalue(), " | ".join(x for x in txt if x)
    except Exception as e:  # noqa
        return None, "HATA: %r" % (e,)
    finally:
        plt.close(fig)


def digits(s):
    return {x.replace(",", ".") for x in NUM.findall(s)}


def check(q, figtxt, shape):
    """Şekilde bulunması gereken ama bulunmayan sayıları döndürür."""
    text = str(q.get("question", ""))
    need = []
    for m in NUM.finditer(text):
        n = m.group(1).replace(",", ".")
        if EXEMPT_AFTER.match(text[m.end():m.end() + 14]):
            continue
        # tanım sayıları: "toplamı 90° olan", "3 kenarlı", "9 eş küçük üçgen" (şekilde yazılması gerekmez)
        if re.search(r"toplamı\s*$", text[max(0, m.start() - 12):m.start()]) or re.match(r"\s*(kenarlı|kenarı|eş\b|köşeli|bölüm)", text[m.end():m.end() + 10]):
            continue
        need.append(n)
    # şekil sayıları: yazılar + shape sözlüğündeki değerler
    have = digits(figtxt or "")
    have |= {str(x) for x in re.findall(r"\d+(?:\.\d+)?", str(shape))}
    miss = [n for n in need if n not in have and n.rstrip("0").rstrip(".") not in have]
    return sorted(set(miss))


_ROWS = []


def main():
    regs = [("Matematik", [(f, k) for f, k, g in ai._MF_GENS if 5 in g]), ("Fen Bilimleri", list(ai._FF_GENS))]
    rows, stat = [], collections.Counter()
    for subj, reg in regs:
        for f, kw in reg:
            n = f.__name__
            got = 0
            for _ in range(PER * 6):
                if got >= PER:
                    break
                try:
                    r = f(subj)
                except Exception:
                    continue
                if not r:
                    continue
                q = ai._norm_q(r, subj)
                if not q or not q.get("shape"):
                    continue
                got += 1
                sh = vis.normalize_shape(q["shape"]) or q["shape"]
                png, ft = fig_texts(sh)
                st_ = "ok"
                miss = []
                if png is None and vis.shape_type(sh) != "table":
                    st_ = "ÇİZİLEMEDİ"
                elif png is not None:
                    miss = check(q, ft, sh)
                    if miss:
                        st_ = "EKSİK"
                stat[(subj, st_)] += 1
                rows.append((subj, n, st_, miss, q, png, ft))
    _ROWS.extend(rows)
    bad = [r for r in rows if r[2] != "ok"]
    print("Şekilli soru:", len(rows), "| sorunlu:", len(bad))
    for k, v in sorted(stat.items()):
        print("  ", k, v)
    byf = collections.Counter((r[1], r[2]) for r in bad)
    for (n, s), c in byf.most_common(40):
        ex = next(r for r in bad if r[1] == n and r[2] == s)
        print(f"  {n:22s} {s:10s} x{c}  eksik={ex[3]}  | {ex[4]['question'][:90]!r}")
    # inceleme sayfası: önce sorunlular, sonra her kalıptan bir örnek
    seen, pick = set(), list(bad)
    for r in rows:
        if r[1] not in seen and r[2] == "ok":
            seen.add(r[1])
            pick.append(r)
    h = ["<meta charset=utf-8><style>body{font:14px sans-serif;margin:16px;background:#f6f7f9}.c{background:#fff;border:1px solid #d8dde3;border-radius:8px;padding:10px;margin:10px 0;display:flex;gap:14px}.c.bad{border-color:#d33;background:#fff5f5}img{max-width:340px;height:auto}.m{font-size:12px;color:#555}</style>",
         f"<h2>Şekil–metin denetimi: {len(rows)} şekilli soru, {len(bad)} sorunlu</h2>"]
    for subj, n, st_, miss, q, png, ft in pick:
        img = f"<img src='data:image/png;base64,{base64.b64encode(png).decode()}'>" if png else "<i>çizilemedi / tablo</i>"
        opts = " &nbsp;|&nbsp; ".join(f"<b>{k}</b>) {html.escape(str(v))}" for k, v in q["options"].items())
        h.append(f"<div class='c{' bad' if st_ != 'ok' else ''}'><div>{img}</div><div><div class=m>{html.escape(n)} · {subj} · <b>{st_}</b>{' · eksik: ' + ', '.join(miss) if miss else ''}</div>"
                 f"<p>{html.escape(q['question'])}</p><div>{opts}</div><div class=m>Cevap: {q['answer']} · Şekildeki yazılar: {html.escape(ft or '')}</div></div></div>")
    open(OUT, "w", encoding="utf-8").write("\n".join(h))
    print("Sayfa:", OUT)
    return len(bad)


if __name__ == "__main__":
    main()
    # çizilemeyen şekil = metni var, görseli yok: gece denetiminde hata say
    sys.exit(1 if any(r[2] == "ÇİZİLEMEDİ" for r in _ROWS) else 0)
