# -*- coding: utf-8 -*-
"""Denemematik — yerel soru ailelerinden havuz doldurucu (API anahtarı gerekmez).

Kodla üretilen (cevabı hesaplanan) soru ailelerinden ünite başına çeşitli, tekrarsız, kural filtrelerinden
geçmiş soruları pool/<sınıf>/<ders>.json içine yazar. Yapay zekâ havuz kayıtlarına dokunmaz; yalnızca
önceki 'src':'local' kayıtlarını yeniler.
Kullanım:  python tools/build_local_pool.py --grades 5 --max-per-unit 3000
"""
import argparse, collections, json, os, random, re, sys, tempfile, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DENEMEMATIK_DATA", tempfile.mkdtemp())
import build_pool as bp

ROOT = bp.ROOT


_UNIT_KZ = {"Temel Geometrik Çizimler": ["MAT.5.3.1", "MAT.5.3.2"], "Açı Ölçme": ["MAT.5.3.3", "MAT.5.3.4"], "Açı İlişkileri": ["MAT.5.3.4"],
            "Çokgenler ve Çember": ["MAT.5.3.5", "MAT.5.3.6", "MAT.5.3.7"], "Basamak Değerlerini": ["MAT.5.1.1"], "Doğal Sayılarla Dört İşlem": ["MAT.5.1.2"],
            "Dikdörtgenin Çevre": ["MAT.5.4.1", "MAT.5.4.2", "MAT.5.4.3", "MAT.5.4.4"], "Kesirler": ["MAT.5.1.3", "MAT.5.1.4"], "Ondalık Gösterim": ["MAT.5.1.3"],
            "Veri Toplama": ["MAT.5.5.1", "MAT.5.5.2"], "İşlemlerle Cebirsel": ["MAT.5.2.1", "MAT.5.2.2", "MAT.5.2.3", "MAT.5.2.4"], "Veriden Olasılığa": ["MAT.5.6.1", "MAT.5.6.2"]}
_UNIT_KZ_EXTRA = {"Veri Toplama": ["MAT.5.2.3"]}  # örüntü kalıpları (yalnız kendi kalıp kodu 5.2.3 ise bu kazanıma bağlanır)


def _kz_of(ai, unit, fam):
    """Soru, doğrulandığı ünitenin kazanımlarına bağlanır; kalıbın kendi kazanım kodu varsa onunla kesişimi (daha dar) alınır."""
    uk, ex = [], []
    for k, v in _UNIT_KZ.items():
        if unit.startswith(k):
            uk, ex = list(v), list(_UNIT_KZ_EXTRA.get(k, []))
    fk = list((getattr(ai, "_MF_ITEMCODE", {}) or {}).get(fam) or [])
    both = [c for c in fk if c in uk or c in ex]
    return both or fk or uk


def _bkey(ai, q):
    """Yineleme anahtarı. Açılış cümlesi ve harf/rakam değişimleri soruyu 'farklı' yapmaz; içerik (şekildeki sözcükler,
    sorulan öge, doğru cevabın sözcüğü) farklıysa farklı soru sayılır. Yalnızca 'Konu:' açılışlı şekilli sorulara uygulanır."""
    import json as _j
    qt = str(q.get("question") or "")
    sh = q.get("shape")
    if not sh:
        ps = str(q.get("passage") or "")
        if len(ps) >= 20:  # öncüllü/metinli soru: kök aynı olsa da önculler (içerik) farklıysa farklı soru
            import hashlib as _h0
            ans0 = str((q.get("options") or {}).get(str(q.get("answer", "")).upper()[:1], ""))
            return "p:" + _h0.md5((re.sub(r"\d+", "0", qt.lower()) + "|" + ps + "|" + ans0).encode()).hexdigest()[:16]
        return ai._stem(q)
    core = qt
    if core.startswith("Konu:"):
        core = "\n".join(core.split("\n")[1:]) or core
    for e in getattr(ai, "_VY_EN", []):  # İngilizce açılış cümlesi
        if core.startswith(e + " "):
            core = core[len(e) + 1:]
            break
    ls = core.split("\n")
    if len(ls) > 1 and any(ls[0].endswith(x) for x in getattr(ai, "_VY_SUF", [])):  # Türkçe açılış satırı
        core = "\n".join(ls[1:])
    core = re.sub(r"\b[A-ZÇĞİÖŞÜ]\b", "X", core)
    core = re.sub(r"\d+", "0", core.lower())
    ans = str((q.get("options") or {}).get(str(q.get("answer", "")).upper()[:1], ""))
    if isinstance(sh, dict) and sh.get("type") == "bar_chart":  # grafikte soruyla ilgisiz çubuklar soruyu farklı yapmaz
        import hashlib as _h
        ops = "|".join(sorted(str(v) for v in (q.get("options") or {}).values()))
        return "k:" + _h.md5((core + "|" + ans + "|" + ops).encode()).hexdigest()[:16]
    js = _j.dumps(sh, ensure_ascii=False, sort_keys=True)
    if len(ans) == 1:  # cevap bir harf: şekilde o harfle gösterilen sözcüğü anahtara kat
        for m in re.finditer(r'"h": "(.)", "w": "([^"]+)"', js):
            if m.group(1) == ans:
                ans = "w:" + m.group(2)
    js = re.sub(r'"(h|harf|k)": "[A-ZÇĞİÖŞÜ]"', '"h": "X"', js)
    words = ",".join(sorted(re.findall(r'"(?:w|k)": "([^"]+)"', js)))
    rows = js if sh.get("type") != "dil" else ""
    import hashlib
    return "k:" + hashlib.md5((core + "|" + ans + "|" + words + "|" + rows).encode()).hexdigest()[:16]


def _mask(q):
    t = re.sub(r"\d+([.,]\d+)?", "0", str(q.get("question") or ""))
    sh = q.get("shape") or {}
    ps = str(q.get("passage") or "")
    if len(ps) >= 20 and not sh:
        t += "|" + re.sub(r"\s+", " ", ps.lower())[:400]
    return re.sub(r"\s+", " ", t.lower()).strip() + "|" + str(sh.get("type") or "") + "|" + re.sub(r"\d+", "0", str(sh.get("title") or ""))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--grades", default="5")
    ap.add_argument("--subjects", default="")
    ap.add_argument("--max-per-unit", type=int, default=3000)
    ap.add_argument("--tries", type=int, default=250, help="aile başına üretim denemesi")
    ap.add_argument("--per-form", type=int, default=3, help="aynı kalıptan (sayılar maskeli) en çok kaç soru")
    ap.add_argument("--bad-dir", default="", help="userdata dalındaki data/ klasörü: hatalı bildirilen soru/kalıplar havuza girmez ve eski kayıtlardan silinir")
    ap.add_argument("--per-family", type=int, default=60, help="bir ünitede aile başına en çok soru")
    args = ap.parse_args()
    random.seed()
    os.environ["DENEMEMATIK_NO_POOL"] = "1"
    os.environ["DENEMEMATIK_POOL_DIR"] = os.path.join(ROOT, "pool")
    os.environ["DENEMEMATIK_SRC_DIR"] = os.path.join(ROOT, "sources")
    ai, cur, _st = bp.load_pkg(os.path.join(ROOT, "app.py"))
    D = cur.DIFFICULTIES
    import shutil
    bd = args.bad_dir
    dirs = [bd] if bd else []
    if bd and os.path.isdir(os.path.join(bd, "profiles")):
        dirs += [os.path.join(bd, "profiles", p) for p in os.listdir(os.path.join(bd, "profiles"))]
    for fn in ("bad.json", "bad_keys.json", "bad_forms.json", "quarantine.json", "bad_facts.json"):  # tüm profillerin hatalı bildirimleri birleştirilir
        acc = []
        for d_ in dirs:
            try:
                with open(os.path.join(d_, fn), encoding="utf-8") as f:
                    acc += [x for x in json.load(f) if isinstance(x, str)]
            except Exception:
                pass
        if acc:
            with open(os.path.join(_st.DATA, fn), "w", encoding="utf-8") as f:
                json.dump(sorted(set(acc)), f, ensure_ascii=False)
    want = [s.strip() for s in args.subjects.split(",") if s.strip()]
    tot = 0
    for g in [x.strip() for x in args.grades.split(",") if x.strip()]:
        label = cur.GRADE_LABELS.get(g, g + ". Sınıf")
        C = cur.C[g]
        reg = {"Matematik": [(f, k) for f, k, gr in ai._MF_GENS if int(g) in gr], "Fen Bilimleri": ai._FF_GENS, "Sosyal Bilgiler": ai._SF_GENS,
               "Türkçe": ai._TF_GENS, "Din Kültürü ve Ahlak Bilgisi": ai._DF_GENS, "İngilizce": ai._EF_GENS}
        _g6 = getattr(ai, "_G6_ONLY", set())
        reg = {k: (v if k == "Matematik" else [(f, kw) for f, kw in v if (f.__name__ in _g6) == (str(g) == "6") or (f.__name__ not in _g6)]) for k, v in reg.items()}
        for sj, fams in reg.items():
            if want and sj not in want:
                continue
            path, have = bp.read_pool(ai, label, sj)
            keep = [q for q in have if q.get("src") != "local"]
            _n0 = len(keep)
            keep = [q for q in keep if not ai._is_bad(ai._stem(q)) and not ai._is_bad_form(q) and not ai._is_bad_exact(q.get("question"), (q.get("options") or {}).get(str(q.get("answer", "")).upper()[:1]))]
            if len(keep) != _n0:
                print(f"   hatalı bildirimlerden silinen (yapay zekâ kayıtları): {_n0 - len(keep)}")
            stems = {_bkey(ai, q) for q in keep}
            new = []
            _tsets = bp.unit_topic_sets(C[sj])
            for unit, topics in C[sj]:
                utxt = unit + ": " + "; ".join(topics)
                per = []
                for f, kw in fams:
                    if not any(ai._kw_hit(utxt.lower(), k) for k in kw):
                        continue
                    item = getattr(f, "ITEM", None)
                    got, forms = [], collections.Counter()
                    for _ in range(args.tries):
                        if len(got) >= args.per_family:
                            break
                        try:
                            r = f(sj)
                            q = ai._norm_q(r, sj) if r else None
                        except Exception:
                            q = None
                        if not q or not ai._on_topic(q, utxt, sj, label):
                            continue
                        if bp.topic_other_unit(q, unit, _tsets):
                            continue
                        s, m = _bkey(ai, q), _mask(q)
                        if not s or s in stems or forms[m] >= args.per_form:
                            continue
                        stems.add(s)
                        forms[m] += 1
                        got.append(q)
                    per.append((f.__name__, got))
                pick, i = [], 0
                while len(pick) < args.max_per_unit and any(i < len(x[1]) for x in per):
                    for fn, gl in per:
                        if i < len(gl) and len(pick) < args.max_per_unit:
                            pick.append((fn, gl[i]))
                    i += 1
                for fn, q in pick:
                    d = ai._DIFF_OF.get(fn, 2)
                    d = d if isinstance(d, int) else 2
                    clean = {k: v for k, v in q.items() if k not in bp.KEEP_DROP}
                    try:
                        json.dumps(clean, ensure_ascii=False)
                    except Exception:
                        continue
                    kz = _kz_of(ai, unit, fn) if sj == "Matematik" else []
                    new.append({**clean, **({"kz": kz} if kz else {}), "unit": unit, "topics": ", ".join(topics)[:160], "d": d, "ts": int(time.time()), "src": "local", "fam": fn})
                print(f"{label} | {sj} | {unit[:42]} | {len(pick)} soru ({len(per)} aile)")
            bp.write_pool(path, keep + new)
            tot += len(new)
    print("TOPLAM yerel havuz sorusu:", tot)


if __name__ == "__main__":
    main()
