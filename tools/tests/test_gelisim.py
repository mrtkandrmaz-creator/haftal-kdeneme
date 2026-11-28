"""Öğrenci gelişim raporu: coach.mastery (kazanım karnesi) durum ve değişim kuralları."""
import os as _os, sys, tempfile
_ROOT = _os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
sys.path.insert(0, _os.path.join(_ROOT, "tools"))
_os.environ["DENEMEMATIK_DATA"] = tempfile.mkdtemp()
import build_pool as bp
ai, cur, store = bp.load_pkg(_os.path.join(_ROOT, "app.py"))
from core import coach

def ex(**kw):  # tek sınav: {ders: {kazanım: [doğru, toplam]}}
    return {"topics": {"Fen": {k: list(v) for k, v in kw.items()}}}

H = [ex(A=(1, 4), B=(5, 5), C=(2, 2), D=(1, 5)),
     ex(A=(2, 4), B=(5, 5), D=(2, 5)),
     ex(A=(4, 4), B=(5, 5), D=(1, 5)),
     ex(A=(4, 4), B=(5, 5), D=(0, 5))]
rows = {r["topic"]: r for r in coach.mastery(H)}
errs = []
def chk(c, m):
    if not c:
        errs.append(m)
chk(rows["B"]["status"] == "Ustalaştı", "B ustalaşmalı")
chk(rows["A"]["status"] == "Gelişiyor" and rows["A"]["change"] > 40, "A: düşük başlayıp yükseldi, değişim >40 olmalı (%.0f)" % (rows["A"]["change"] or -1))
chk(rows["D"]["status"] == "Zayıf" and rows["D"]["change"] < 0, "D zayıf ve düşüşte olmalı")
chk(rows["C"]["status"] == "Yeni" and rows["C"]["change"] is None, "C yeni (2 soru, tek sınav)")
order = [r["status"] for r in coach.mastery(H)]
chk(order == sorted(order, key=["Zayıf", "Gelişiyor", "Yeni", "Ustalaştı"].index), "sıralama: zayıflar önce")
chk(coach.mastery([]) == [], "boş geçmiş boş döner")
chk(coach.mastery([{"topics": {"Fen": {"Genel": [3, 4]}}}]) == [], "'Genel' kazanım sayılmaz")
if errs:
    print("\n".join(errs)); sys.exit(1)
print("kazanım karnesi tamam")
