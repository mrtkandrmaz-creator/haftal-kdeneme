#!/usr/bin/env python3
"""Havuz açıklamalarındaki işlemleri (a + b × c = d) bağımsız hesaplayıp doğrular; son sonucun doğru şıkta bulunmasını da denetler.
Kullanım: python tools/aritmetik_dogrulama.py [sınıf=5] [ders=Matematik]"""
import collections, os, re, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DENEMEMATIK_DATA", tempfile.mkdtemp())
import build_pool as bp  # noqa
from fractions import Fraction

EXPR = re.compile(r"(?<![\w.,/])((?:\(?\d+(?:[.,]\d+)?\)?\s*[+\-−×÷*]\s*)+\(?\d+(?:[.,]\d+)?\)?)\s*=\s*(\d+(?:[.,]\d+)?)(?![\d,./]|\s*[×÷+\-−*/(]|\s*\(?kalan|\s*\d)")
THOU = re.compile(r"(?<![\d.,])(\d{1,3})((?: \d{3})+)(?![\d])")
NUMTOK = re.compile(r"\d+(?:[.,]\d+)?")


def val(s):
    t = s.replace("−", "-").replace("×", "*").replace("÷", "/").replace("x", "*")
    t = re.sub(r"(\d+),(\d+)", r"\1.\2", t)
    t = re.sub(r"(\d+(?:\.\d+)?)", lambda m: f"Fraction('{m.group(1)}')", t)
    return eval(t, {"Fraction": Fraction, "__builtins__": {}})


def main():
    g = sys.argv[1] if len(sys.argv) > 1 else "5"
    sj = sys.argv[2] if len(sys.argv) > 2 else "Matematik"
    os.environ["DENEMEMATIK_POOL_DIR"] = os.path.join(bp.ROOT, "pool")
    ai, cur, store = bp.load_pkg(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "app.py"))
    _, qs = bp.read_pool(ai, cur.GRADE_LABELS[g], sj)
    tot = chk = 0
    bad = collections.defaultdict(list)
    nolast = collections.Counter()
    for q in qs:
        ex = THOU.sub(lambda m: m.group(1) + m.group(2).replace(" ", ""), str(q.get("explanation") or ""))
        for m in EXPR.finditer(ex):
            try:
                a = val(m.group(1))
                b = Fraction(m.group(2).replace(",", "."))
            except Exception:
                continue
            chk += 1
            if a != b:
                bad[q.get("fam", "?")].append((m.group(0), q["question"][:70].replace("\n", " ")))
        tot += 1
    print(f"{sj}: {tot} soru, {chk} işlem denetlendi, hatalı işlem içeren aile: {len(bad)}")
    for f, v in sorted(bad.items(), key=lambda kv: -len(kv[1]))[:30]:
        print(" ", f, len(v), "→", v[0])
    return len(bad)


if __name__ == "__main__":
    sys.exit(1 if main() else 0)
