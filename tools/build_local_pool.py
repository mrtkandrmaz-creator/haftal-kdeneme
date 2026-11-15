# -*- coding: utf-8 -*-
"""Denemematik — yerel soru ailelerinden havuz doldurucu (API anahtarı gerekmez).

Kodla üretilen (cevabı hesaplanan) soru ailelerinden ünite başına çeşitli, tekrarsız, kural filtrelerinden
geçmiş soruları pool/<sınıf>/<ders>.json içine yazar. Yapay zekâ havuz kayıtlarına dokunmaz; yalnızca
önceki 'src':'local' kayıtlarını yeniler.
Kullanım:  python tools/build_local_pool.py --grades 5 --max-per-unit 80
"""
import argparse, collections, json, os, random, re, sys, tempfile, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DENEMEMATIK_DATA", tempfile.mkdtemp())
import build_pool as bp

ROOT = bp.ROOT


def _mask(q):
    t = re.sub(r"\d+([.,]\d+)?", "0", str(q.get("question") or ""))
    sh = q.get("shape") or {}
    return re.sub(r"\s+", " ", t.lower()).strip() + "|" + str(sh.get("type") or "") + "|" + re.sub(r"\d+", "0", str(sh.get("title") or ""))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--grades", default="5")
    ap.add_argument("--subjects", default="")
    ap.add_argument("--max-per-unit", type=int, default=80)
    ap.add_argument("--tries", type=int, default=160, help="aile başına üretim denemesi")
    ap.add_argument("--per-form", type=int, default=3, help="aynı kalıptan (sayılar maskeli) en çok kaç soru")
    ap.add_argument("--per-family", type=int, default=14, help="bir ünitede aile başına en çok soru")
    args = ap.parse_args()
    random.seed()
    os.environ["DENEMEMATIK_NO_POOL"] = "1"
    os.environ["DENEMEMATIK_POOL_DIR"] = os.path.join(ROOT, "pool")
    os.environ["DENEMEMATIK_SRC_DIR"] = os.path.join(ROOT, "sources")
    ai, cur, _st = bp.load_pkg(os.path.join(ROOT, "app.py"))
    D = cur.DIFFICULTIES
    want = [s.strip() for s in args.subjects.split(",") if s.strip()]
    tot = 0
    for g in [x.strip() for x in args.grades.split(",") if x.strip()]:
        label = cur.GRADE_LABELS.get(g, g + ". Sınıf")
        C = cur.C[g]
        reg = {"Matematik": [(f, k) for f, k, gr in ai._MF_GENS if int(g) in gr], "Fen Bilimleri": ai._FF_GENS, "Sosyal Bilgiler": ai._SF_GENS,
               "Türkçe": ai._TF_GENS, "Din Kültürü ve Ahlak Bilgisi": ai._DF_GENS, "İngilizce": ai._EF_GENS}
        for sj, fams in reg.items():
            if want and sj not in want:
                continue
            path, have = bp.read_pool(ai, label, sj)
            keep = [q for q in have if q.get("src") != "local"]
            stems = {ai._stem(q) for q in keep}
            new = []
            for unit, topics in C[sj]:
                utxt = unit + ": " + "; ".join(topics)
                per = []
                for f, kw in fams:
                    if not any(ai._kw_hit(utxt.lower(), k) for k in kw):
                        continue
                    item = getattr(f, "ITEM", None)
                    got, forms = [], collections.Counter()
                    for _ in range(args.tries):
                        if len(got) >= args.per_family:
                            break
                        try:
                            r = f(sj)
                            q = ai._norm_q(r, sj) if r else None
                        except Exception:
                            q = None
                        if not q or not ai._on_topic(q, utxt, sj, label):
                            continue
                        s, m = ai._stem(q), _mask(q)
                        if not s or s in stems or forms[m] >= args.per_form:
                            continue
                        stems.add(s)
                        forms[m] += 1
                        got.append(q)
                    per.append((f.__name__, got))
                pick, i = [], 0
                while len(pick) < args.max_per_unit and any(i < len(x[1]) for x in per):
                    for fn, gl in per:
                        if i < len(gl) and len(pick) < args.max_per_unit:
                            pick.append((fn, gl[i]))
                    i += 1
                for fn, q in pick:
                    d = ai._DIFF_OF.get(fn, 2)
                    d = d if isinstance(d, int) else 2
                    clean = {k: v for k, v in q.items() if k not in bp.KEEP_DROP}
                    try:
                        json.dumps(clean, ensure_ascii=False)
                    except Exception:
                        continue
                    new.append({**clean, "unit": unit, "topics": ", ".join(topics)[:160], "d": d, "ts": int(time.time()), "src": "local", "fam": fn})
                print(f"{label} | {sj} | {unit[:42]} | {len(pick)} soru ({len(per)} aile)")
            bp.write_pool(path, keep + new)
            tot += len(new)
    print("TOPLAM yerel havuz sorusu:", tot)


if __name__ == "__main__":
    main()
