#!/usr/bin/env python3
"""Havuz kapsam raporu: ders/ünite/kazanım (Matematik) ve alt konu bazında soru sayısı, kalıp sayısı, şekilli oranı; ince alanları işaretler.
Kullanım: python tools/kapsam_raporu.py [sınıf=5] [çıktı.md]"""
import os, sys, collections, tempfile
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
os.environ.setdefault("DENEMEMATIK_DATA", tempfile.mkdtemp())
os.environ.setdefault("DENEMEMATIK_POOL_DIR", os.path.join(ROOT, "pool"))
import build_pool as bp
ai, cur, store = bp.load_pkg(os.path.join(ROOT, "app.py"))
g = sys.argv[1] if len(sys.argv) > 1 else "5"
out = sys.argv[2] if len(sys.argv) > 2 else None
GL = f"{g}. Sınıf"
SUBJ = ["Matematik", "Fen Bilimleri", "Türkçe", "Sosyal Bilgiler", "Din Kültürü ve Ahlak Bilgisi", "İngilizce"]
MIN_UNIT, MIN_KZ, MIN_TOPIC, MIN_FAM, MIN_SHAPE = 400, 250, 25, 3, 0.25
L, thin = [], []


def pct(a, b):
    return f"%{round(100 * a / b)}" if b else "–"


def row(name, qs, minq):
    fam = {q.get("fam") for q in qs}
    sh = sum(1 for q in qs if q.get("shape"))
    flag = ""
    if len(qs) < minq or len(fam) < MIN_FAM:
        flag = " ⚠"
    elif qs and sh / len(qs) < MIN_SHAPE:
        flag = " 🖼 görsel az"
    return f"| {name} | {len(qs)} | {len(fam)} | {pct(sh, len(qs))}{flag} |", bool(flag)


L.append(f"# Havuz kapsam raporu — {GL}\n")
L.append(f"İnce alan eşikleri: ünite < {MIN_UNIT} soru, Matematik kazanımı < {MIN_KZ}, alt konu < {MIN_TOPIC} soru ya da kalıp < {MIN_FAM} ⚠ ile işaretlenir.\n")
for sj in SUBJ:
    _, qs = bp.read_pool(ai, GL, sj)
    if not qs:
        continue
    sh = sum(1 for q in qs if q.get("shape"))
    L.append(f"\n## {sj} — {len(qs)} soru, {len({q.get('fam') for q in qs})} kalıp, şekilli/tablolu {pct(sh, len(qs))}\n")
    if sj == "Matematik":
        L.append("### Kazanım bazında\n\n| Kazanım | Soru | Kalıp | Şekilli |\n|---|---|---|---|")
        kz = collections.defaultdict(list)
        for q in qs:
            for k in q.get("kz") or ["(kodsuz)"]:
                kz[k].append(q)
        for k in sorted(kz):
            r, t = row(k, kz[k], MIN_KZ)
            L.append(r)
            t and thin.append((sj, k, len(kz[k])))
    L.append("\n### Ünite bazında\n\n| Ünite | Soru | Kalıp | Şekilli |\n|---|---|---|---|")
    un = collections.defaultdict(list)
    for q in qs:
        un[q["unit"]].append(q)
    for u, l in sorted(un.items()):
        r, t = row(u, l, MIN_UNIT)
        L.append(r)
        t and thin.append((sj, u, len(l)))
    if sj != "Matematik":
        L.append("\n### Alt konu etiketi bazında (yaklaşık; aynı konunun farklı yazımları birleştirildi, yalnızca ince olanlar)\n\n| Ünite · alt konu | Soru | Kalıp | Şekilli |\n|---|---|---|---|")
        tp = collections.defaultdict(list)
        for q in qs:
            tp[(q["unit"], " ".join(str(q.get("topic") or "(konusuz)").casefold().split()))].append(q)
        n = 0
        for (u, t_), l in sorted(tp.items(), key=lambda x: len(x[1])):
            r, t = row(f"{u} · {t_}", l, MIN_TOPIC)
            if t:
                L.append(r)
                thin.append((sj, f"{u} · {t_}", len(l)))
                n += 1
        if not n:
            L.append("| (ince alt konu yok) | | | |")
L.append(f"\n## Özet: {len(thin)} ince alan\n")
for sj in SUBJ:
    x = [(a, b) for s, a, b in thin if s == sj]
    if x:
        L.append(f"- **{sj}:** " + "; ".join(f"{a} ({b})" for a, b in x[:25]) + (f" … +{len(x) - 25}" if len(x) > 25 else ""))
txt = "\n".join(L) + "\n"
if out:
    open(out, "w", encoding="utf-8").write(txt)
print(txt)
