"""Havuz aritmetik/yapı denetimi (5. sınıf): açıklamalardaki tüm işlemler bağımsız hesapla doğru olmalı; her soruda 4 tekil şık ve şıklar arasında cevap bulunmalı."""
import os, sys
_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(_ROOT, "tools"))
import aritmetik_dogrulama as ad
import build_pool as bp

fail = 0
for sj in ("Matematik", "Fen Bilimleri", "Sosyal Bilgiler"):
    sys.argv = ["x", "5", sj]
    fail += ad.main()
ai, cur, store = bp.load_pkg(os.path.join(_ROOT, "app.py"))
for sj in ("Matematik", "Fen Bilimleri", "Türkçe", "Sosyal Bilgiler", "Din Kültürü ve Ahlak Bilgisi", "İngilizce"):
    _, qs = bp.read_pool(ai, "5. Sınıf", sj)
    for q in qs:
        o = q.get("options")
        if not isinstance(o, dict) or sorted(o) != list("ABCD") or str(q.get("answer")) not in "ABCD" or len({str(v).strip().lower() for v in o.values()}) < 4:
            print("YAPI", sj, q.get("fam"), str(q.get("question"))[:80])
            fail += 1
sys.exit(1 if fail else 0)
