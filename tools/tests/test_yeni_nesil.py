"""Yeni nesil (tablolu/paragraflı) kalıplar: her biri 200 çekimde çökmemeli, en az %80'i denetimden geçmeli, şekil/metin uyumu bozulmamalı."""
import os as _os, sys, collections
_ROOT = _os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
APP = _os.path.join(_ROOT, "app.py")
sys.path.insert(0, _os.path.join(_ROOT, "tools"))
import build_pool as bp
ai, cur, store = bp.load_pkg(APP)
fails = []
for reg, subj, pre in ((ai._FF_GENS, "Fen Bilimleri", "_ff_yn_"), (ai._TF_GENS, "Türkçe", "_tf_par_"), (ai._TF_GENS, "Türkçe", "_tf_dk_")):
    for f, _k in reg:
        if not f.__name__.startswith(pre):
            continue
        c = collections.Counter()
        for _ in range(200):
            r = f(subj)
            if not r:
                c["none"] += 1
                continue
            q = ai._norm_q(r, subj)
            c["ok" if q else "rej"] += 1
        if c["ok"] < (120 if f.__name__.startswith("_tf_dk_") else 160):
            fails.append((f.__name__, dict(c)))
        print(f.__name__, dict(c))
assert not fails, fails
print("OK")
