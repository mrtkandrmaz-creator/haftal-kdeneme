"""Üç ardışık sınav: istenen soru adedi üretilmeli, önceki sınavla aynı soru kökü tekrar etmemeli, aynı kalıp sınavı doldurmamalı."""
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

fails = []
for sj in SUBJ:
    tops = "; ".join(u + ": " + "; ".join(t) for u, t in C[sj][:3])
    prev = []
    for r in range(3):
        qs, err = ai.generate_mc([{"subject": sj, "n": 10, "topics": tops}], "5. Sınıf", D[2], "t", avoid={}, use_bank=False, deposit=False, verify=False, count=False)
        st = [re.sub(r"\d+", "#", q["question"])[:70] for q in qs]
        rep = sum(1 for s in st if s in prev)
        tp = collections.Counter(q.get("tpl") for q in qs)
        print(sj, r, len(qs), "tekrar", rep, "aynı kalıp max", max(tp.values()))
        if len(qs) != 10:
            fails.append((sj, r, "adet", len(qs)))
        if rep > 3:
            fails.append((sj, r, "önceki sınavla aynı kök", rep))
        if max(tp.values()) > 5:
            fails.append((sj, r, "tek kalıp baskın", max(tp.values())))
        prev += st
        store.add_stems(qs)
        store.add_styles(qs)
assert not fails, fails
print("OK")
