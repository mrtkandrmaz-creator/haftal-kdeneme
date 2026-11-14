"""Ünite içi kazanım kapsamı: her ünite için 3 zorlukta istenen adet üretilmeli ve kazanımların en az %60 ortalamayla karşılanmalı."""
import os as _os, sys, re, time, collections, tempfile
_ROOT = _os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
APP = _os.path.join(_ROOT, "app.py")
sys.path.insert(0, _os.path.join(_ROOT, "tools"))
_os.environ["DENEMEMATIK_DATA"] = tempfile.mkdtemp()
import build_pool as bp
ai, cur, store = bp.load_pkg(APP)
D = cur.DIFFICULTIES
C = cur.C["5"]
SUBJ = ["Matematik", "Fen Bilimleri", "Sosyal Bilgiler", "Türkçe", "Din Kültürü ve Ahlak Bilgisi", "İngilizce"]

IT = {}
for reg in (ai._FF_GENS, ai._SF_GENS, ai._TF_GENS, ai._DF_GENS, ai._EF_GENS):
    for f, k in reg:
        if getattr(f, "ITEM", None):
            IT[f.__name__] = f.ITEM
FN = {f.__name__: f for f, k, g in ai._MF_GENS}
fails = []
for sj in SUBJ:
    tot = cnt = 0.0
    for u, t in cur.units("5", sj):
        tops = u + ": " + "; ".join(t)
        items = ai._topic_items(sj, "5. Sınıf", tops)
        if len(items) < 2:
            continue
        n = 14 if sj == "Matematik" else 12
        for di in (1, 3, 5):
            qs, err = ai.generate_mc([{"subject": sj, "n": n, "topics": tops}], "5. Sınıf", D[di], "t", avoid={}, use_bank=False, deposit=False, verify=False, count=False)
            if len(qs) != n:
                fails.append((sj, u[:24], di, "adet", len(qs)))
            c = collections.Counter((items.index(IT[q["tpl"]]) if IT.get(q.get("tpl")) in items else ai._fam_item(q.get("tpl"), FN.get(q.get("tpl")), sj, items) if q.get("tpl") in FN else ai._q_item(q, items)) for q in qs)
            cov = len([k for k in c if k >= 0]) / len(items)
            tot += cov
            cnt += 1
    avg = tot / max(1, cnt)
    print(sj, "ort. kapsam %.0f%%" % (100 * avg))
    if avg < 0.60:
        fails.append((sj, "ort. kapsam", round(avg, 2)))
assert not fails, fails[:10]
print("OK")
