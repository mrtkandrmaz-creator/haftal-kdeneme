#!/usr/bin/env python3
"""Sınav bazında benzerlik/tekrar ölçümü: python tools/sinav_benzerlik.py [sınıf=5] [sınav_sayısı=6] [soru=20]
Her ders ve ünite için ardışık sınavlar kurar; sınav içinde ve sınavlar arasında tekrarları, aynı kalıp yığılmasını,
aynı şekil/tablo içeriğini ve cevap harfi dağılımını ölçer."""
import collections, json, os, re, sys, tempfile, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DENEMEMATIK_DATA", tempfile.mkdtemp())
os.environ.setdefault("DENEMEMATIK_POOL_DIR", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "pool"))
import build_pool as bp  # noqa

G = sys.argv[1] if len(sys.argv) > 1 else "5"
NEX = int(sys.argv[2]) if len(sys.argv) > 2 else 6
NQ = int(sys.argv[3]) if len(sys.argv) > 3 else 20
ai, cur, store = bp.load_pkg(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "app.py"))
LAB = cur.GRADE_LABELS[G]
D = cur.DIFFICULTIES
SUBJ = sys.argv[4].split(",") if len(sys.argv) > 4 else ["Matematik", "Fen Bilimleri", "Türkçe", "Sosyal Bilgiler", "Din Kültürü ve Ahlak Bilgisi", "İngilizce"]
mask = lambda t: re.sub(r"\s+", " ", re.sub(r"\d+", "#", str(t).lower())).strip()


def fp(q):  # içerik parmak izi: soru + şıklar + şekil
    return mask(q.get("question")) + "|" + json.dumps(sorted(map(str, (q.get("options") or {}).values())), ensure_ascii=False) + "|" + json.dumps(q.get("shape"), sort_keys=True, ensure_ascii=False, default=str)[:300]


def exact(q):
    return str(q.get("question")) + json.dumps(q.get("options"), sort_keys=True, ensure_ascii=False) + json.dumps(q.get("shape"), sort_keys=True, ensure_ascii=False, default=str)


tot = collections.Counter()
rows = []
letters = collections.defaultdict(collections.Counter)
for sj in SUBJ:
    units = cur.C[G][sj]
    cases = [("karışık", "; ".join(u + ": " + "; ".join(t) for u, t in units))] + [(u[:34], u + ": " + "; ".join(t)) for u, t in units]
    for name, tops in cases:
        prev_exact, prev_form = set(), collections.Counter()
        os.environ["DENEMEMATIK_DATA"] = tempfile.mkdtemp()  # her ünite temiz geçmişle (gerçek kullanıcı son sınavları görür, yüzlercesini değil)
        store.DATA = os.environ["DENEMEMATIK_DATA"]
        st = collections.Counter()
        for r in range(NEX):
            try:
                qs, err = ai.generate_mc([{"subject": sj, "n": NQ, "topics": tops}], LAB, D[r % 3], "t", avoid={k: list(v) for k, v in store.recent_stems().items()}, use_bank=False, deposit=False, verify=False, count=False)
            except Exception as e:  # noqa
                st["hata"] += 1
                continue
            store.add_stems(qs)
            store.add_styles(qs)
            st["sınav"] += 1
            st["eksik_adet"] += max(0, NQ - len(qs))
            ex = [exact(q) for q in qs]
            fm = [mask(q.get("question")) for q in qs]
            fps = [fp(q) for q in qs]
            fam = collections.Counter(q.get("fam") or q.get("tpl") for q in qs if (q.get("fam") or q.get("tpl")))
            st["iç_aynı_soru"] += len(ex) - len(set(ex))
            st["iç_aynı_içerik"] += len(fps) - len(set(fps))
            st["iç_aynı_kök"] += len(fm) - len(set(fm))
            st["en_çok_aynı_kalıp"] = max(st["en_çok_aynı_kalıp"], max(fam.values()) if fam else 0)
            st["arada_aynı_soru"] += sum(1 for e in ex if e in prev_exact)
            st["arada_aynı_kök"] += sum(1 for f in fm if prev_form[f])
            prev_exact |= set(ex)
            prev_form.update(fm)
            for q in qs:
                letters[sj][str(q.get("answer"))[:1]] += 1
        rows.append((sj, name, dict(st)))
        for k in ("iç_aynı_soru", "iç_aynı_içerik", "arada_aynı_soru", "eksik_adet", "hata"):
            tot[(sj, k)] += st[k]
        tot[(sj, "sınav")] += st["sınav"]
    print(f"== {sj}", {k: v for (s, k), v in tot.items() if s == sj}, "cevap harfleri", dict(sorted(letters[sj].items())), flush=True)
    for s, n, d in rows[-(len(cases)):]:
        bad = {k: v for k, v in d.items() if k in ("iç_aynı_soru", "iç_aynı_içerik", "arada_aynı_soru", "eksik_adet", "hata") and v} | ({"en_çok_aynı_kalıp": d["en_çok_aynı_kalıp"]} if d.get("en_çok_aynı_kalıp", 0) > 4 else {})
        if bad:
            print("   ", n, bad)
