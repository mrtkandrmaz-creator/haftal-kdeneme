#!/usr/bin/env python3
"""Havuz tutarlılık taraması: python tools/tutarlilik_taramasi.py [sınıf=5] [ders|hepsi] [çıktı.json]
Her soru için: yapı (4 tekil şık, cevap şıkta), güncel kalite kapıları (_norm_q), şekil–metin uyumu,
metindeki sayıların şekilde yazılı olması, cevabın şekilde/tabloda aynen görünmemesi, yinelenen soru."""
import collections, json, os, re, sys, tempfile, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DENEMEMATIK_DATA", tempfile.mkdtemp())
import build_pool as bp  # noqa

NUM = re.compile(r"\d+(?:[.,]\d+)?")
SUBJ = ["Matematik", "Fen Bilimleri", "Türkçe", "Sosyal Bilgiler", "Din Kültürü ve Ahlak Bilgisi", "İngilizce"]


def nums(t):
    return {x.replace(",", ".") for x in NUM.findall(str(t))}


def scan(ai, qs, subject, lab):
    bad = collections.defaultdict(list)
    seen = {}
    for i, q in enumerate(qs):
        qt, ps, o, a, sh = str(q.get("question") or ""), str(q.get("passage") or ""), q.get("options"), str(q.get("answer") or "").upper()[:1], q.get("shape")
        tag = f"{q.get('fam','?')}|{(q.get('unit') or '')[:30]}"
        if not isinstance(o, dict) or sorted(o) != list("ABCD") or a not in "ABCD" or len({str(v).strip().lower() for v in o.values()}) < 4 or not str(o.get(a, "")).strip():
            bad["yapı"].append((tag, qt[:90]))
            continue
        k = hashlib.md5((qt + ps + json.dumps(o, sort_keys=True, ensure_ascii=False) + json.dumps(sh, sort_keys=True, ensure_ascii=False, default=str)).encode()).hexdigest()
        if k in seen:
            bad["yinelenen"].append((tag, qt[:90]))
        seen[k] = 1
        clean = {x: v for x, v in q.items() if x not in ("unit", "topics", "d", "ts", "pool", "local", "seed", "vfd", "_gp", "id", "tpl", "pid", "listen", "kz", "fam")}
        try:
            r = ai._norm_q(clean, subject)
        except Exception as e:  # noqa
            r = None
        if not r:
            bad["kapı"].append((tag, qt[:90]))
        elif str((r.get("options") or {}).get(r.get("answer"), "")).strip() != str(o.get(a, "")).strip():
            bad["kapı-cevap-değişti"].append((tag, qt[:90]))
        if isinstance(sh, dict):
            js = json.dumps(sh, ensure_ascii=False, default=str)
            if sh.get("type") in ("geo", "m6", "prob", "orun", "number_line", "bar_chart", "line_chart", "pie_chart", "table", "kes") and subject == "Matematik":
                miss = [n for n in nums(qt.split("\n")[0] + " " + qt) if n not in nums(js) and n not in nums(ps) and n not in nums(" ".join(map(str, o.values())))]
                miss = [n for n in miss if n not in ("0", "1", "2", "90", "180", "360", "100", "1000")]
                if miss:
                    bad["sayı-şekilde-yok"].append((tag, f"{miss[:4]} | {qt[:80]}"))
            try:
                if ai.leaks_answer({"question": qt, "options": o, "answer": a, "shape": sh, "passage": ps}):
                    bad["cevap-sızıntı"].append((tag, qt[:90]))
            except Exception:
                pass
    return bad


def main():
    g = sys.argv[1] if len(sys.argv) > 1 else "5"
    which = sys.argv[2] if len(sys.argv) > 2 else "hepsi"
    out = sys.argv[3] if len(sys.argv) > 3 else ""
    os.environ["DENEMEMATIK_POOL_DIR"] = os.path.join(bp.ROOT, "pool") if hasattr(bp, "ROOT") else "pool"
    ai, cur, store = bp.load_pkg(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "app.py"))
    lab = cur.GRADE_LABELS[g]
    res = {}
    for sj in (SUBJ if which == "hepsi" else [which]):
        _, qs = bp.read_pool(ai, lab, sj)
        b = scan(ai, qs, sj, lab)
        res[sj] = {"n": len(qs), **{k: len(v) for k, v in b.items()}}
        print(sj, res[sj], flush=True)
        for k, v in b.items():
            c = collections.Counter(t.split("|")[0] for t, _ in v)
            print("   ", k, c.most_common(12))
            for t, s in v[:3]:
                print("      ·", t, "→", s)
        res[sj]["_ornek"] = {k: v[:400] for k, v in b.items()}
    if out:
        json.dump(res, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
