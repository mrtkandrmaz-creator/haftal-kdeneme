"""Banka bütünlüğü + öz denetim: sorun listesi boş olmalı; tüm aileler çökmeden üretmeli."""
import os as _os, sys, tempfile, collections
_ROOT = _os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
APP = _os.path.join(_ROOT, "app.py")
sys.path.insert(0, _os.path.join(_ROOT, "tools"))
_os.environ["DENEMEMATIK_DATA"] = tempfile.mkdtemp()
import build_pool as bp
ai, cur, store = bp.load_pkg(APP)
bi = ai.bank_integrity()
assert not bi, bi
au = ai.self_audit()
assert not au.get("problems"), au["problems"]
crash = []
regs = {"Matematik": [(f, k) for f, k, *_ in ai._MF_GENS], "Fen Bilimleri": ai._FF_GENS, "Sosyal Bilgiler": ai._SF_GENS,
        "Türkçe": ai._TF_GENS, "Din Kültürü ve Ahlak Bilgisi": ai._DF_GENS, "İngilizce": ai._EF_GENS}
n = 0
for subj, reg in regs.items():
    for f, _k in reg:
        for _ in range(15):
            try:
                r = f(subj)
                if r:
                    ai._norm_q(r, subj)
                n += 1
            except Exception as e:
                crash.append((subj, f.__name__, repr(e)[:80]))
                break
assert not crash, crash[:10]
print("OK", n)
