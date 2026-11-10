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
    names = ("bad.json", "quarantine.json")  # hatalı bildirimler + şüpheli (çözüm verisinden) sorular
    files = [os.path.join(bad_dir, n) for n in names]
    pd = os.path.join(bad_dir, "profiles")
    if os.path.isdir(pd):
        files += [os.path.join(pd, p, n) for p in os.listdir(pd) for n in names]
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


def collect_liked(bad_dir):
    """data/liked.json ve data/profiles/*/liked.json: beğenilen sorular (üretimde tarz örneği olur)."""
    out = []
    if not bad_dir or not os.path.isdir(bad_dir):
        return out
    files = [os.path.join(bad_dir, "liked.json")]
    pd = os.path.join(bad_dir, "profiles")
    if os.path.isdir(pd):
        files += [os.path.join(pd, p, "liked.json") for p in os.listdir(pd)]
    for fp in files:
        try:
            with open(fp, encoding="utf-8") as f:
                out += [x for x in json.load(f) if isinstance(x, dict)]
        except Exception:
            pass
    return out


def load_passages(root):
    """sources/<sınıf>/turkce_metinler.json: {ünite: [{id, baslik, metin}]}"""
    out = {}
    base = os.path.join(root, "sources")
    if os.path.isdir(base):
        for g in os.listdir(base):
            fp = os.path.join(base, g, "turkce_metinler.json")
            try:
                with open(fp, encoding="utf-8") as f:
                    out[g] = (json.load(f) or {}).get("units", {})
            except Exception:
                pass
    return out


def _norm_txt(t):
    return re.sub(r"\s+", " ", str(t or "").strip().lower())


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


def _ls_txt(ai):
    d = getattr(ai, "LAST_STRICT", None) or {}
    return f"şık tutmadı {d.get('mismatch', 0)}, hatalı(X) {d.get('x', 0)}, ÇÖZÜCÜYE ULAŞILAMADI {d.get('unreach', 0)}"


def build(ai, cur, args, gen=None, strict=None):
    """gen(plan, label, difficulty, scope) -> (qs, err); testte sahte üretici verilebilir."""
    gen = gen or (lambda plan, label, diff, scope, avoid: ai.generate_mc(
        plan, label, diff, scope, avoid=avoid, use_bank=False, deposit=False, verify=True, count=False))
    _gk, _mk = [], []
    if strict is None:
        _gk, _mk = ai.load_keys()
        strict = lambda qs, facts=None: ai.verify_strict(qs, _gk, _mk, facts=facts)
    t0 = time.time()
    bad = collect_bad(getattr(args, "bad_dir", ""))
    liked = collect_liked(getattr(args, "bad_dir", ""))
    passages = load_passages(os.environ.get("DENEMEMATIK_ROOT", ROOT))
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
        topics_txt = f"{unit}: " + ", ".join(topics)
        n_ask = args.per_unit
        chosen = None
        ps = (passages.get(g) or {}).get(unit) if sj == "Türkçe" else None
        if ps:  # Türkçe: onaylı okuma metni seç (en az kullanılan); sorular yalnızca bu metne dayanır
            used = {p["id"]: sum(1 for q in have if q.get("pid") == p["id"]) for p in ps}
            chosen = min(ps, key=lambda p: (used[p["id"]], random.random()))
            if used[chosen["id"]] >= args.max_per_passage:
                continue
            n_ask = min(n_ask, 4)
            topics_txt += (f"\n📖 KAYNAK METİN (başlık: {chosen['baslik']}):\n{chosen['metin']}\n"
                           "KURAL: Soruların TAMAMI yalnızca bu metne dayansın (ana fikir, konu, başlık, çıkarım, neden-sonuç, sözcük/deyim anlamı, anlatım özellikleri). "
                           "'passage' alanına bu metni AYNEN, hiç değiştirmeden yaz. Metinde olmayan bilgiyi sorma; doğru cevap metinden kesin olarak çıkarılabilsin ve tek bir şık doğru olsun. "
                           "Her soru farklı bir beceriyi ölçsün.")
        listening = False
        if sj == "İngilizce" and random.random() < args.listen_ratio:  # dinleme sorusu: metin ekranda gizlenir, sesli çalınır
            listening = True
            n_ask = min(n_ask, 4)
            topics_txt += ("\n🎧 DİNLEME SORUSU KURALI: 'passage' alanına bu ünite konusunda 40-70 kelimelik, 5. sınıf düzeyinde, kısa bir İNGİLİZCE diyalog yaz "
                           "(her konuşma ayrı satırda, 'Ali: ...' / 'Mia: ...' biçiminde, iki konuşmacı). Sorular ve şıklar İngilizce olsun; cevap YALNIZCA diyalogda söylenenlerden kesin çıkarılabilsin, "
                           "yalnızca ezbere ya da genel bilgiye dayanmasın; sorularda 'text/dialogue' kelimelerine atıf yapma, 'In the conversation, ...' biçimini kullan.")
        ex = [x["q"] for x in liked if (x.get("q") or {}).get("subject") == sj and x.get("grade_label") == label and isinstance(x.get("q"), dict)]
        ai.STYLE_EXAMPLES[sj] = ex
        plan = [{"subject": sj, "n": n_ask, "topics": topics_txt, "short": unit}]
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
            if sj in ("Matematik", "Fen Bilimleri", "Sosyal Bilgiler", "Din Kültürü ve Ahlak Bilgisi") and not ai._on_topic(q, f"{unit}: {topics_txt}", sj, label):
                print(f"   ✗ ünite dışı: {str(q.get('question'))[:70]}")
                continue
            if chosen:  # metni değiştirmiş ya da metinden bağımsız soruları ele; metni AYNEN kaynak metinle değiştir
                import difflib
                if difflib.SequenceMatcher(None, _norm_txt(q.get("passage")), _norm_txt(chosen["metin"])).ratio() < 0.85:
                    continue
                q["passage"] = chosen["metin"]
                q["pid"] = chosen["id"]
            if listening:
                if len(str(q.get("passage") or "").split()) < 25 or str(q.get("passage")).count(":") < 2:
                    continue  # dinleme için yeterli diyalog yok
                q["listen"] = True
            stems.add(s)
            new.append(q)
        if new and (_gk or _mk) and os.environ.get("DENEMEMATIK_NO_CRITIC") != "1":
            n0 = len(new)
            try:
                new = ai.critique_fix(new, _gk, _mk)  # uzman-eleştirmen: hata/muğlaklık/olumsuz kök düzelt ya da ele
            except Exception as e:
                print(f"   ! eleştirmen atlandı: {type(e).__name__}")
            if len(new) != n0 or any(q.get("crit") for q in new):
                print(f"   🔎 eleştirmen: {n0} → {len(new)} (düzeltilen {sum(1 for q in new if q.get('crit'))})")
        ai.LAST_STRICT = {}
        before = len(new)
        facts = ai.src_facts(sj, label, f"{unit}: " + ", ".join(topics))
        try:
            new = strict(new, facts=facts) if new else []
        except TypeError:
            new = strict(new) if new else []  # sıkı doğrulama: iki bağımsız çözüm de anahtarla aynı olmalı
        rejected_strict = before - len(new)
        new = [{**{k: v for k, v in q.items() if k not in KEEP_DROP}, "unit": unit, "topics": ", ".join(topics)[:160], "d": di, "ts": int(time.time())} for q in new]
        if new:
            write_pool(path, have + new)
            added_total += len(new)
        print(f"{label} | {sj} | {unit[:40]} | +{len(new)} (elenen {rejected_strict}: {_ls_txt(ai)}) (havuz {len(have) + len(new)})" + (f" | {err}" if err and not new else ""))
    print("TOPLAM eklenen:", added_total)
    return added_total


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--grades", default="5")
    ap.add_argument("--subjects", default="Matematik,Fen Bilimleri")
    ap.add_argument("--per-unit", type=int, default=1)
    ap.add_argument("--max-per-unit", type=int, default=80, help="bir ünitede bu kadar soruya ulaşılınca atlanır")
    ap.add_argument("--minutes", type=float, default=40)
    ap.add_argument("--listen-ratio", type=float, default=0.4, help="İngilizce hedeflerinin dinleme sorusu olma olasılığı")
    ap.add_argument("--max-per-passage", type=int, default=12, help="bir okuma metninden bu kadar soruya ulaşılınca metin atlanır")
    ap.add_argument("--bad-dir", default="", help="userdata dalındaki data/ klasörü (bad.json içerir); bildirilen sorular havuzdan silinir")
    ap.add_argument("--difficulty-idx", default="1,2,3,4", help="curriculum.DIFFICULTIES indeksleri (0-5), virgülle")
    args = ap.parse_args()
    args.difficulty_idx = [int(x) for x in args.difficulty_idx.split(",")]
    os.environ["DENEMEMATIK_NO_FACTORY"] = "1"
    os.environ["DENEMEMATIK_NO_POOL"] = "1"
    os.environ["DENEMEMATIK_POOL_DIR"] = os.path.join(ROOT, "pool")
    os.environ["DENEMEMATIK_SRC_DIR"] = os.path.join(ROOT, "sources")
    ai, cur, _store = load_pkg(os.path.join(ROOT, "app.py"))
    gk, mk = ai.load_keys()
    if not gk and not mk and not ai.extra_keys():
        sys.exit("API anahtarı yok (GROQ_API_KEYS / GEMINI_API_KEYS ...)")
    build(ai, cur, args)


if __name__ == "__main__":
    main()
