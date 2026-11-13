# -*- coding: utf-8 -*-
"""Bilgi bankasını bağımsız yapay zekâ ile doğrular (gece, GitHub Actions).
Sonuç: pool/bank_checks.json  ->  {"v":1,"ok":[anahtarlar],"bad":[anahtarlar]}; uygulama 'bad' girdileri kullanmaz.
Kullanım: python tools/verify_bank.py --max-q 240"""
import argparse, json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_pool as bp


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-q", type=int, default=240)
    ap.add_argument("--batch", type=int, default=12)
    ap.add_argument("--app", default=os.path.join(bp.ROOT, "app.py"))
    ap.add_argument("--out", default=os.path.join(bp.ROOT, "pool", "bank_checks.json"))
    a = ap.parse_args()
    os.environ["DENEMEMATIK_POOL_DIR"] = os.path.dirname(a.out)
    ai, cur, store = bp.load_pkg(a.app)
    gk, mk = ai.load_keys()
    if not gk and not mk and not ai.extra_keys():
        print("API anahtarı yok; doğrulama atlandı.")
        return
    r = ai.verify_bank(gk, mk, max_q=a.max_q, batch=a.batch)
    done = store._load("bank_verified.json", {})
    ok_, bad_ = ai._bank_checks()
    ok = sorted((ok_ | {k for k, v in done.items() if v == "ok"}) - {k for k, v in done.items() if v == "bad"})
    bad = sorted(bad_ | {k for k, v in done.items() if v == "bad"})
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    with open(a.out, "w", encoding="utf-8") as f:
        json.dump({"v": 1, "ok": ok, "bad": bad}, f, ensure_ascii=False, indent=0)
    print(f"denenen soru: {r['checked']} • doğrulanan toplam: {len(ok)} • reddedilen toplam: {len(bad)} • henüz sorulmamış: {r['left']}")
    for k in r["bad"][:20]:
        print("  reddedildi:", k)


if __name__ == "__main__":
    main()
