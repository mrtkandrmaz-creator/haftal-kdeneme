# -*- coding: utf-8 -*-
"""Denemematik — soru havuzu hazırlayıcı.

Sınav ANINDA değil, önceden (gece / elle) soru üretir; kural kontrolü + çapraz model doğrulamasından
geçenleri repodaki pool/<sınıf>/<ders>.json dosyalarına yazar. Uygulama sınavı bu havuzdan kurar (API kotası harcamaz).

Kullanım (repo kökünden):
  python tools/build_pool.py --grades 5,6,7,8 --per-unit 6 --minutes 40
Anahtarlar ortam değişkenlerinden okunur: GROQ_API_KEYS, GEMINI_API_KEYS (virgülle ayrılmış),
CEREBRAS_API_KEYS, OPENROUTER_API_KEYS, MISTRAL_API_KEYS, SAMBANOVA_API_KEYS, NVIDIA_API_KEYS, GITHUB_API_KEYS.
En az dolu olan (sınıf, ders, ünite) hedefleri önce işlenir; böylece her çalıştırma açığı kapatır.
"""
import argparse, json, os, random, re, sys, time, types

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEEP_DROP = ("_gp", "id", "local", "seed", "vfd", "tpl", "pool")


def load_pkg(app_py):
    """app.py içindeki MODULES sözlüğünü geçici bir core/ paketine açar (Streamlit gerekmez)."""
    import tempfile
    sys.modules.setdefault("streamlit", types.SimpleNamespace(secrets={}))
    src = open(app_py, encoding="utf-8").read()
    tmp = tempfile.mkdtemp(prefix="dm_pkg_")
    os.makedirs(os.path.join(tmp, "core"))
    open(os.path.join(tmp, "core", "__init__.py"), "w").write("")
    for name, body in re.findall(r"MODULES\['core/(\w+)'\] = r'''(.*?)\n'''", src, re.S):
        open(os.path.join(tmp, "core", name + ".py"), "w", encoding="utf-8").write(body)
    sys.path.insert(0, tmp)
    from core import ai_engine, curriculum, store
    store.DATA = os.path.join(tmp, "data")
    os.makedirs(store.DATA, exist_ok=True)
    return ai_engine, curriculum, store


def read_pool(ai, g, subject):
    path = ai._pool_path(subject, g)
    try:
        with open(path, encoding="utf-8") as f:
            return path, (json.load(f) or {}).get("qs", [])
    except Exception:
        return path, []


def write_pool(path, qs):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump({"v": 1, "qs": qs}, f, ensure_ascii=False, indent=0)
    os.replace(tmp, path)


def collect_bad(bad_dir):
    """data/bad.json ve data/profiles/*/bad.json içindeki 'hatalı' bildirilen soru gövdeleri."""
    out = set()
    if not bad_dir or not os.path.isdir(bad_dir):
        return out
    files = [os.path.join(bad_dir, "bad.json")]
    pd = os.path.join(bad_dir, "profiles")
    if os.path.isdir(pd):
        files += [os.path.join(pd, p, "bad.json") for p in os.listdir(pd)]
    for fp in files:
        try:
            with open(fp, encoding="utf-8") as f:
                for st in json.load(f):
                    out.add(st)
                    out.add(re.sub(r"\W+", " ", re.sub(r"\d+", "0", st)).strip())
        except Exception:
            pass
    return out


def purge_bad(ai, root, bad):
    """Hatalı bildirilen soruları tüm havuz dosyalarından kalıcı siler. -> silinen sayısı"""
    removed = 0
    if not bad:
        return 0
    for dp, _dn, fns in os.walk(root):
        for fn in fns:
            if not fn.endswith(".json"):
                continue
            path = os.path.join(dp, fn)
            try:
                with open(path, encoding="utf-8") as f:
                    qs = (json.load(f) or {}).get("qs", [])
            except Exception:
                continue
            keep = [q for q in qs if ai._stem(q) not in bad]
            if len(keep) != len(qs):
                removed += len(qs) - len(keep)
                write_pool(path, keep)
    return removed


def targets(cur, ai, grades, subjects):
    out = []
    for g in grades:
        label = cur.GRADE_LABELS.get(g, g + ". Sınıf")
        for sj in cur.subjects_for(g):
            if subjects and sj not in subjects:
                continue
            _p, have = read_pool(ai, label, sj)
            for unit, topics in cur.units(g, sj):
                cnt = sum(1 for q in have if q.get("unit") == unit)
                out.append((cnt, random.random(), g, label, sj, unit, topics))
    out.sort(key=lambda t: t[:2])
    return out


def build(ai, cur, args, gen=None, strict=None):
    """gen(plan, label, difficulty, scope) -> (qs, err); testte sahte üretici verilebilir."""
    gen = gen or (lambda plan, label, diff, scope, avoid: ai.generate_mc(
        plan, label, diff, scope, avoid=avoid, use_bank=False, deposit=False, verify=True, count=False))
    if strict is None:
        _gk, _mk = ai.load_keys()
        strict = lambda qs: ai.verify_strict(qs, _gk, _mk)
    t0 = time.time()
    bad = collect_bad(getattr(args, "bad_dir", ""))
    if bad:
        print("hatalı bildirimlerden silinen:", purge_bad(ai, os.environ["DENEMEMATIK_POOL_DIR"], bad))
    grades = [g.strip() for g in args.grades.split(",") if g.strip()]
    subjects = [s.strip() for s in args.subjects.split(",") if s.strip()] if args.subjects else []
    added_total = 0
    for cnt, _r, g, label, sj, unit, topics in targets(cur, ai, grades, subjects):
        if time.time() - t0 > args.minutes * 60 or cnt >= args.max_per_unit:
            continue
        path, have = read_pool(ai, label, sj)
        stems = {ai._stem(q) for q in have}
        di = random.choice(args.difficulty_idx)
        diff = cur.DIFFICULTIES[di]
        plan = [{"subject": sj, "n": args.per_unit, "topics": f"{unit}: " + ", ".join(topics), "short": unit}]
        try:
            qs, err = gen(plan, label, diff, unit, {sj: list(stems)[-80:]})
        except Exception as e:
            print(f"! {label} {sj} {unit}: {type(e).__name__}: {str(e)[:80]}")
            continue
        new = []
        for q in qs or []:
            if q.get("local") or q.get("seed") or q.get("pool"):
                continue  # havuz yalnızca yapay zekâ kaynaklı sorular içerir (hazır/fabrika sorular uygulamada ayrıca eklenir)
            s = ai._stem(q)
            if not s or s in stems:
                continue
            if any(ai._qwords(q) and ai._qwords(k) and len(ai._qwords(q) & ai._qwords(k)) / len(ai._qwords(q) | ai._qwords(k)) > 0.6 for k in have + new):
                continue
            if s in bad:
                continue
            stems.add(s)
            new.append(q)
        before = len(new)
        new = strict(new) if new else []  # sıkı doğrulama: iki bağımsız çözüm de anahtarla aynı olmalı
        rejected_strict = before - len(new)
        new = [{**{k: v for k, v in q.items() if k not in KEEP_DROP}, "unit": unit, "topics": ", ".join(topics)[:160], "d": di, "ts": int(time.time())} for q in new]
        if new:
            write_pool(path, have + new)
            added_total += len(new)
        print(f"{label} | {sj} | {unit[:40]} | +{len(new)} (sıkı doğrulamada elenen {rejected_strict}) (havuz {len(have) + len(new)})" + (f" | {err}" if err and not new else ""))
    print("TOPLAM eklenen:", added_total)
    return added_total


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--grades", default="5")
    ap.add_argument("--subjects", default="")
    ap.add_argument("--per-unit", type=int, default=10)
    ap.add_argument("--max-per-unit", type=int, default=80, help="bir ünitede bu kadar soruya ulaşılınca atlanır")
    ap.add_argument("--minutes", type=float, default=40)
    ap.add_argument("--bad-dir", default="", help="userdata dalındaki data/ klasörü (bad.json içerir); bildirilen sorular havuzdan silinir")
    ap.add_argument("--difficulty-idx", default="1,2,3,4", help="curriculum.DIFFICULTIES indeksleri (0-5), virgülle")
    args = ap.parse_args()
    args.difficulty_idx = [int(x) for x in args.difficulty_idx.split(",")]
    os.environ["DENEMEMATIK_NO_FACTORY"] = "1"
    os.environ["DENEMEMATIK_NO_POOL"] = "1"
    os.environ["DENEMEMATIK_POOL_DIR"] = os.path.join(ROOT, "pool")
    ai, cur, _store = load_pkg(os.path.join(ROOT, "app.py"))
    gk, mk = ai.load_keys()
    if not gk and not mk and not ai.extra_keys():
        sys.exit("API anahtarı yok (GROQ_API_KEYS / GEMINI_API_KEYS ...)")
    build(ai, cur, args)


if __name__ == "__main__":
    main()
