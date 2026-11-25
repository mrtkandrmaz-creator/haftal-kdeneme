"""Konu saflığı (5. sınıf havuzu): hiçbir soru kendi ünitesi/kazanımı dışında çıkmamalı.
1) Matematik: havuzdaki kazanım kodları, kalıbın güncel kazanım eşlemesinin (_MF_ITEMCODE) dışına taşmaz;
   MAT.5.1.1 (çok basamaklı sayılar) altında kapsam dışı kalıplar (yuvarlama, tablodan toplam, örüntü) yoktur.
2) Diğer dersler: soru, kalıbının anahtar sözcüklerinin eşleştiği ünitelerin dışında bir ünitede bulunmaz;
   bilgi bankası kalıbı (_bk…) yalnızca kendi ünitesinde bulunur.
3) Fen/Sosyal/Din: ünite denetimi (_unit_guard) hiçbir havuz sorusunu reddetmez."""
import os as _os, sys, tempfile, collections
_ROOT = _os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
APP = _os.path.join(_ROOT, "app.py")
sys.path.insert(0, _os.path.join(_ROOT, "tools"))
_os.environ["DENEMEMATIK_DATA"] = tempfile.mkdtemp()
_os.environ["DENEMEMATIK_POOL_DIR"] = _os.path.join(_ROOT, "pool")
import build_pool as bp
ai, cur, store = bp.load_pkg(APP)
G = "5. Sınıf"
problems = []

# --- 1) Matematik
_, qs = bp.read_pool(ai, G, "Matematik")
assert qs, "Matematik havuzu boş"
OFF_11 = {"_mf_say_yuvar", "_mf_say_yuvarla2", "_mf_yv_yakin", "_mf_yv_hangisine", "_mf6s_sd_yuvarla", "_mf6s_sd_topla",
          "_mf_yn_nufus", "_mf_yn_nufus_fark", "_mf6s_makine"}
for q in qs:
    f = q.get("fam")
    code = ai._MF_ITEMCODE.get(f)
    kz = set(q.get("kz") or [])
    if code and kz and not kz <= set(code):
        problems.append(("mat-kz", f, sorted(kz), code))
    if "MAT.5.1.1" in kz and f in OFF_11:
        problems.append(("mat-5.1.1-kapsam-disi", f))
    if f == "_mf_market" and kz & {"MAT.5.6.1", "MAT.5.6.2", "MAT.5.4.4"}:
        problems.append(("mat-market", sorted(kz)))
    if len(kz) != 1:
        problems.append(("mat-tek-kazanim-degil", f, sorted(kz)))  # her kalıp tek kazanıma bağlı olmalı

# --- 2) Diğer dersler
REG = {"Fen Bilimleri": (ai._FF_GENS, ai._FFACTS), "Sosyal Bilgiler": (ai._SF_GENS, ai._SFACTS), "Türkçe": (ai._TF_GENS, ai._TFACTS),
       "Din Kültürü ve Ahlak Bilgisi": (ai._DF_GENS, ai._DFACTS), "İngilizce": (ai._EF_GENS, ai._EFACTS)}


def _norm(t):
    return t.replace("İ", "i").replace("I", "ı").lower()


for sj, (gens, facts) in REG.items():
    _, qs = bp.read_pool(ai, G, sj)
    assert qs, sj + " havuzu boş"
    kwmap = {}
    for f, kw in gens:
        kwmap.setdefault(f.__name__, kw)
    ut = {u: _norm(u + " " + " ".join(ks)) for u, ks in cur.units("5", sj)}
    order = list(facts)
    tag = {"Fen Bilimleri": "f", "Sosyal Bilgiler": "s", "Türkçe": "t", "İngilizce": "e", "Din Kültürü ve Ahlak Bilgisi": "d"}[sj]
    seen = set()
    for q in qs:
        f, u = q.get("fam"), q.get("unit")
        if (f, u) in seen:
            continue
        seen.add((f, u))
        if f.startswith("_bk" + tag):
            try:
                own = order[int(f[3 + 1:].split("_")[0])]
            except Exception:
                own = None
            if own and own != u:
                problems.append(("banka-baska-unite", sj, f, u, own))
            continue
        kw = kwmap.get(f)
        if kw and u in ut and not any(ai._kw_hit(ut[u], k) for k in kw):
            problems.append(("anahtar-eslesmiyor", sj, f, u))

# --- 2b) Etiketi başka ünitenin kazanımı olan soru yok
for sj in REG:
    _, qs = bp.read_pool(ai, G, sj)
    sets = bp.unit_topic_sets(cur.units("5", sj))
    for q in qs:
        if bp.topic_other_unit(q, q["unit"], sets):
            problems.append(("etiket-baska-unite", sj, q.get("fam"), q["unit"], q.get("topic")))

# --- 3) _unit_guard
for sj in ("Fen Bilimleri", "Sosyal Bilgiler", "Din Kültürü ve Ahlak Bilgisi"):
    _, qs = bp.read_pool(ai, G, sj)
    for q in qs:
        if not ai._unit_guard(q, q["unit"], sj, G):
            problems.append(("unit_guard", sj, q.get("fam"), q["unit"]))

assert not problems, f"{len(problems)} sorun: {problems[:12]}"
print("OK konu saflığı")
