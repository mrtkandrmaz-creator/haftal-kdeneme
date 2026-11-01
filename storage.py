"""Yerel JSON ilerleme kaydı: denemeler, yanlış arşivi, rozetler. (Streamlit'ten bağımsız)
Not: Streamlit Cloud'da dosya sistemi kalıcı değildir; kalıcılık için Supabase/Firestore ile değiştirilebilir."""
import json
import os
import threading
import uuid
from datetime import datetime, timedelta

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
FILE = os.path.join(DATA_DIR, "progress.json")
_lock = threading.Lock()


def _empty():
    return {"profile": {"name": ""}, "attempts": [], "wrongs": [], "stems": []}


def load():
    try:
        with open(FILE, "r", encoding="utf-8") as f:
            d = json.load(f)
        for k, v in _empty().items():
            d.setdefault(k, v)
        return d
    except Exception:
        return _empty()


def save(d):
    with _lock:
        os.makedirs(DATA_DIR, exist_ok=True)
        tmp = FILE + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False)
        os.replace(tmp, FILE)


def set_name(name):
    d = load(); d["profile"]["name"] = name; save(d)


def add_attempt(a):
    d = load(); a["id"] = uuid.uuid4().hex[:10]; a["ts"] = datetime.now().isoformat(timespec="seconds")
    d["attempts"].append(a); save(d); return a


def add_wrongs(grade, items):
    d = load()
    have = {w["q"]["question"][:80] for w in d["wrongs"] if not w.get("mastered")}
    for q, user in items:
        if q["question"][:80] in have:
            continue
        d["wrongs"].append({"id": uuid.uuid4().hex[:10], "ts": datetime.now().isoformat(timespec="seconds"),
                            "grade": grade, "subject": q["subject"], "unit": q.get("unit", ""), "user": user,
                            "mastered": False, "q": q})
    save(d)


def update_wrong(wid, **kw):
    d = load()
    for w in d["wrongs"]:
        if w["id"] == wid:
            w.update(kw)
    save(d)


def delete_wrong(wid):
    d = load(); d["wrongs"] = [w for w in d["wrongs"] if w["id"] != wid]; save(d)


def remember_stems(qs):
    d = load()
    d["stems"] = (d["stems"] + [q["question"][:90] for q in qs])[-300:]
    save(d)


def recent_stems(subject_questions=None, k=25):
    return load()["stems"][-k:]


# ---------------------------------------------------------------- ROZETLER
BADGES = [
    ("first", "🥇", "İlk Adım", "İlk denemeni tamamla", lambda s: s["n"] >= 1),
    ("five", "🔥", "Istıkrarlı", "5 deneme tamamla", lambda s: s["n"] >= 5),
    ("ten", "🚀", "Deneme Ustası", "10 deneme tamamla", lambda s: s["n"] >= 10),
    ("q100", "💯", "100 Soru", "Toplam 100 soru çöz", lambda s: s["q"] >= 100),
    ("q500", "🏔️", "500 Soru", "Toplam 500 soru çöz", lambda s: s["q"] >= 500),
    ("perfect", "⭐", "Kusursuz Ders", "Bir derste (≥8 soru) %100 başarı", lambda s: s["perfect"]),
    ("allsub", "🎓", "Tam Kadro", "6 farklı dersten soru çöz", lambda s: s["subjects"] >= 6),
    ("rise", "📈", "Yükselen Grafik", "Üst üste 3 denemede başarıyı artır", lambda s: s["rise"]),
    ("streak", "📅", "3 Gün Serisi", "Üst üste 3 gün deneme çöz", lambda s: s["streak"] >= 3),
    ("clean", "🧹", "Yanlış Avcısı", "10 yanlışı arşivden öğrenildi işaretle", lambda s: s["mastered"] >= 10),
    ("lgs", "🏆", "LGS Yolcusu", "Bir LGS formatı denemesi çöz", lambda s: s["lgs"]),
    ("oyss", "📝", "OYSS Hazır", "Bir OYSS sınavı tamamla", lambda s: s["oyss"]),
]


def stats(d=None):
    d = d or load()
    A = d["attempts"]
    subj, perfect = set(), False
    for a in A:
        for s, v in a.get("subjects", {}).items():
            subj.add(s)
            if v["n"] >= 8 and v["d"] == v["n"]:
                perfect = True
    pcts = [a["pct"] for a in A]
    rise = any(pcts[i] < pcts[i + 1] < pcts[i + 2] for i in range(len(pcts) - 2))
    days = sorted({a["ts"][:10] for a in A})
    best = streak = 0
    prev = None
    for ds in days:
        cur = datetime.fromisoformat(ds)
        streak = streak + 1 if prev and cur - prev == timedelta(days=1) else 1
        best = max(best, streak); prev = cur
    return {"n": len(A), "q": sum(a["total"] for a in A), "perfect": perfect, "subjects": len(subj), "rise": rise,
            "streak": best, "mastered": sum(1 for w in d["wrongs"] if w.get("mastered")),
            "lgs": any(a["mode"] in ("lgs80", "lgs90") for a in A), "oyss": any(a["mode"] == "oyss" for a in A)}


def earned_badges(d=None):
    s = stats(d)
    return [(k, ic, t, desc, bool(fn(s))) for k, ic, t, desc, fn in BADGES]


def unit_summary(d=None, min_q=10):
    """(grade, subject, unit) -> n, d  — sertifika için."""
    d = d or load()
    agg = {}
    for a in d["attempts"]:
        for key, v in a.get("units", {}).items():
            k = (a["grade"],) + tuple(key.split("||", 1))
            x = agg.setdefault(k, {"n": 0, "d": 0}); x["n"] += v["n"]; x["d"] += v["d"]
    return agg
