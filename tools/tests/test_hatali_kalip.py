"""Hatalı bildirilen soru kalıbı (sayılar değişse de) bir daha hiçbir kaynaktan gelmemeli; zorluk bir kademe yükselmeli."""
import os as _os, sys, tempfile
_ROOT = _os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
sys.path.insert(0, _os.path.join(_ROOT, "tools"))
_os.environ["DENEMEMATIK_DATA"] = tempfile.mkdtemp()
import build_pool as bp
ai, cur, store = bp.load_pkg(_os.path.join(_ROOT, "app.py"))
f = [x for x in ai._MF_GENS if x[0].__name__ == "_mf_yn_nufus"][0][0] if any(x[0].__name__ == "_mf_yn_nufus" for x in ai._MF_GENS) else ai._MF_GENS[0][0]
q = None
for _ in range(50):
    r = f("Matematik")
    q = ai._norm_q(r, "Matematik") if r else None
    if q:
        break
assert q, "örnek soru üretilemedi"
store.report_bad({**q, "local": True}, "test")
ai._BADX["t"] = 0
back = 0
for _ in range(200):
    r = f("Matematik")
    x = ai._norm_q(r, "Matematik") if r else None
    if x and store.form_key(x) == store.form_key(q):
        back += 1
assert back == 0, f"hatalı kalıp {back} kez geri geldi"
L = cur.DIFFICULTIES
assert ai._bump_diff(L[2]) == L[3] and ai._bump_diff(L[5]) == L[5]
print("OK")
