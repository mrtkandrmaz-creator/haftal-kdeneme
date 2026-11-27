"""Yeni kalıpların görsel inceleme sayfası: her kalıptan N örnek; şekil çizilir, tablo HTML olarak gösterilir, doğru şık işaretlenir.
Kullanım: python3 tools/gorsel_inceleme.py <çıktı.html> <örnek> <önek1,önek2,...>   (önek: kalıp adının başı, örn. _ff_dh_,_mf6n_)"""
import base64, html, io, os, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DENEMEMATIK_DATA", tempfile.mkdtemp())
import build_pool as bp
import importlib
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT, N, PRE = sys.argv[1], int(sys.argv[2]), tuple(sys.argv[3].split(","))
ai, cur, store = bp.load_pkg(os.path.join(_ROOT, "app.py"))
vis = importlib.import_module(ai.__name__.rsplit(".", 1)[0] + ".visuals")
SUBJ = {"_ff": "Fen Bilimleri", "_mf": "Matematik", "_sf": "Sosyal Bilgiler", "_tf": "Türkçe", "_df": "Din Kültürü ve Ahlak Bilgisi"}


def png(shape):
    t = vis.shape_type(shape)
    if not t or t not in vis._DISPATCH:
        return None
    plt = vis.plt
    fig, ax = plt.subplots(figsize=(6.2, 3.8))
    try:
        ax.axis("off"); ax.set_aspect("equal")
        vis._DISPATCH[t](ax, dict(shape))
        buf = io.BytesIO(); fig.savefig(buf, format="png", bbox_inches="tight", dpi=90, facecolor="white", pad_inches=.1)
        return base64.b64encode(buf.getvalue()).decode()
    except Exception:
        return None
    finally:
        plt.close(fig)


names = sorted(n for n in dir(ai) if n.startswith(PRE) and callable(getattr(ai, n)))
out = ["<meta charset=utf-8><style>body{font:14px system-ui;margin:16px;max-width:1100px}.f{border:1px solid #ccc;border-radius:8px;padding:10px;margin:10px 0;display:grid;grid-template-columns:1fr 1fr;gap:12px}h3{margin:18px 0 0}img{max-width:100%}table{border-collapse:collapse}td,th{border:1px solid #999;padding:3px 8px}.ok{color:#0a7d28;font-weight:600}.bad{color:#b00}</style><h1>Görsel inceleme</h1>"]
cnt = 0
for n in names:
    subj = SUBJ.get(n[:3], "Matematik")
    out.append(f"<h3>{n}</h3>")
    got = 0
    for _ in range(N * 6):
        if got >= N:
            break
        try:
            r = getattr(ai, n)(subj)
            q = ai._norm_q(dict(r), subj) if r else None
        except Exception:
            q = None
        if not q:
            continue
        got += 1; cnt += 1
        sh = q.get("shape"); fig = ""
        if isinstance(sh, dict):
            if sh.get("type") == "table":
                fig = f"<b>{html.escape(str(sh.get('title','')))}</b><table><tr>" + "".join(f"<th>{html.escape(str(h))}</th>" for h in sh.get("headers", [])) + "</tr>" + "".join("<tr>" + "".join(f"<td>{html.escape(str(c))}</td>" for c in row) + "</tr>" for row in sh.get("rows", [])) + "</table>"
            else:
                b = png(sh)
                fig = f"<img src='data:image/png;base64,{b}'>" if b else "<i class=bad>ŞEKİL ÇİZİLEMEDİ</i>"
        else:
            fig = "<i>(şekilsiz)</i>"
        opts = "".join(f"<div class={'ok' if k == q['answer'] else ''}>{k}) {html.escape(str(v))}{' ✓' if k == q['answer'] else ''}</div>" for k, v in q["options"].items())
        out.append(f"<div class=f><div>{html.escape(q.get('passage') or '')}<p>{html.escape(q['question']).replace(chr(10), '<br>')}</p>{opts}<small>{html.escape(str(q.get('explanation',''))[:200])}</small></div><div>{fig}</div></div>")
open(OUT, "w", encoding="utf-8").write("".join(out))
print(len(names), "kalıp", cnt, "örnek", OUT)
