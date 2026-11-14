#!/usr/bin/env python3
"""Tüm regresyon testlerini sırayla çalıştırır. Kullanım: python tools/run_checks.py [-k ad] [--hizli]
Çıkış kodu: hepsi geçtiyse 0, değilse 1. CI'da her push'ta çalışır."""
import os, subprocess, sys, time, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TESTS = sorted(glob.glob(os.path.join(ROOT, "tools", "tests", "test_*.py")))
args = sys.argv[1:]
flt = args[args.index("-k") + 1] if "-k" in args else ""
res = []
for t in TESTS:
    name = os.path.basename(t)[5:-3]
    if flt and flt not in name:
        continue
    t0 = time.time()
    try:
        p = subprocess.run([sys.executable, t], capture_output=True, text=True, timeout=900, cwd=ROOT)
        ok, out = p.returncode == 0, (p.stdout + p.stderr)
    except subprocess.TimeoutExpired:
        ok, out = False, "ZAMAN AŞIMI"
    res.append((name, ok, time.time() - t0, out))
    print(("GEÇTİ " if ok else "KALDI "), f"{name:24s} {res[-1][2]:5.1f} sn", flush=True)
    if not ok:
        print("   " + "\n   ".join(out.strip().splitlines()[-8:]))
bad = [r for r in res if not r[1]]
print(f"\n{len(res) - len(bad)}/{len(res)} test geçti")
sys.exit(1 if bad else 0)
