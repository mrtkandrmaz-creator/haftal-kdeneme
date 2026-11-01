"""Performans & Raporlar, Yanlış Arşivi ve Rozet/Sertifika ekranları."""
import io
import math

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

import curriculum as C
import pdf_export
import storage
import theme

MODE_NAMES = {"weekly": "Haftalık Deneme", "oyss": "OYSS", "genel": "Genel Deneme", "konu": "Konu Tarama", "yaprak": "Yaprak Test",
              "bank": "Soru Bankası", "lgs80": "LGS 80 Soru", "lgs90": "LGS 90 Soru", "wrongs": "Yanlış Testi"}
PAL = ["#0284c7", "#ea580c", "#16a34a", "#7c3aed", "#e11d48", "#0891b2", "#ca8a04", "#64748b"]


def _pct(v):
    return 100.0 * v["d"] / v["n"] if v and v.get("n") else None


def _kpi(label, value, sub=""):
    return f"<div class='kpi'><div class='l'>{label}</div><div class='v'>{value}</div><div class='d'>{sub}</div></div>"


def _style(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.grid(axis="y", color="#e2e8f0"); ax.set_axisbelow(True)
    ax.tick_params(labelsize=8)


def _short(a):
    return a["ts"][5:10].replace("-", ".") + "\n" + MODE_NAMES.get(a["mode"], a["mode"])[:12]


def performance():
    d = storage.load(); A = d["attempts"]
    st.markdown("<div class='hero'><h1>📊 Performans & Raporlar</h1><p>Denemelerini ders, ünite ve zaman bazında karşılaştır; güçlü ve zayıf yönlerini gör.</p></div>", unsafe_allow_html=True)
    if not A:
        st.info("Henüz tamamlanmış deneme yok. İlk denemeni çözdükten sonra tüm raporların burada görünecek. 🚀")
        return
    f1, f2 = st.columns(2)
    gsel = f1.selectbox("Sınıf filtresi", ["Tümü"] + [C.GRADES[g]["label"] for g in C.GRADES if any(a["grade"] == g for a in A)])
    msel = f2.selectbox("Sınav türü", ["Tümü"] + sorted({MODE_NAMES.get(a["mode"], a["mode"]) for a in A}))
    inv = {v["label"]: k for k, v in C.GRADES.items()}
    F = [a for a in A if (gsel == "Tümü" or a["grade"] == inv.get(gsel)) and (msel == "Tümü" or MODE_NAMES.get(a["mode"], a["mode"]) == msel)]
    if not F:
        st.warning("Filtreye uyan deneme yok."); return
    last, prev = F[-1], (F[-2] if len(F) > 1 else None)
    avg = np.mean([a["pct"] for a in F]); best = max(F, key=lambda a: a["pct"])
    dl = None if not prev else last["pct"] - prev["pct"]
    k = st.columns(5)
    k[0].markdown(_kpi("Deneme", len(F), f"toplam {sum(a['total'] for a in F)} soru"), unsafe_allow_html=True)
    k[1].markdown(_kpi("Son Başarı", f"%{last['pct']:.1f}", theme.delta(dl, " puan")), unsafe_allow_html=True)
    k[2].markdown(_kpi("Ortalama", f"%{avg:.1f}", f"{len(F)} denemenin ort."), unsafe_allow_html=True)
    k[3].markdown(_kpi("En İyi", f"%{best['pct']:.1f}", best["ts"][:10]), unsafe_allow_html=True)
    k[4].markdown(_kpi("Son Net", f"{last['net']:.2f}", theme.delta(None if not prev else last["net"] - prev["net"])), unsafe_allow_html=True)

    st.markdown("<div class='sec-title'>🆚 Son Deneme ↔ Önceki Deneme (Ders Bazlı)</div>", unsafe_allow_html=True)
    rows = []
    for s, v in last["subjects"].items():
        p_now = _pct(v); p_old = _pct(prev["subjects"].get(s)) if prev else None
        rows.append([f"<b>{s}</b>", f"{v['d']} / {v['y']} / {v['b']}", f"%{p_now:.0f}",
                     "—" if p_old is None else f"%{p_old:.0f}", theme.delta(None if p_old is None else p_now - p_old, " puan"),
                     theme.bar(p_now)])
    st.markdown(theme.html_table(["Ders", "D / Y / B", "Son", "Önceki", "Değişim", "Başarı"], rows), unsafe_allow_html=True)

    st.markdown("<div class='sec-title'>📈 Gelişim Grafiği</div>", unsafe_allow_html=True)
    subs_all = sorted({s for a in F for s in a["subjects"]})
    pick = st.multiselect("Grafikte gösterilecek dersler", subs_all, default=subs_all[:4])
    c1, c2 = st.columns([3, 2])
    with c1:
        fig, ax = plt.subplots(figsize=(7.2, 3.6)); x = list(range(len(F)))
        ax.plot(x, [a["pct"] for a in F], "-o", color="#0f172a", lw=3, ms=7, label="Genel", zorder=5)
        for i, s in enumerate(pick):
            ys = [(_pct(a["subjects"].get(s)) if a["subjects"].get(s) else np.nan) for a in F]
            ax.plot(x, ys, "-o", color=PAL[i % len(PAL)], lw=1.8, ms=4, label=s, alpha=.9)
        ax.set_xticks(x); ax.set_xticklabels([_short(a) for a in F], fontsize=7); ax.set_ylim(0, 105); ax.set_ylabel("Başarı %", fontsize=9)
        ax.legend(fontsize=7, ncol=3, loc="lower center", bbox_to_anchor=(.5, 1.0), frameon=False); _style(ax)
        st.pyplot(fig); plt.close(fig)
    with c2:
        if subs_all:
            fig = plt.figure(figsize=(4, 3.6)); ax = fig.add_subplot(111, polar=True)
            ang = np.linspace(0, 2 * math.pi, len(subs_all), endpoint=False).tolist(); ang += ang[:1]
            def ser(a):
                return [(_pct(a["subjects"].get(s)) or 0) for s in subs_all]
            sets = [("Ortalama", [np.mean([(_pct(a["subjects"].get(s)) or 0) for a in F]) for s in subs_all], "#94a3b8"), ("Son", ser(last), "#ea580c")]
            if prev: sets.insert(1, ("Önceki", ser(prev), "#0284c7"))
            for nm, vals, col in sets:
                v = list(vals) + [vals[0]]; ax.plot(ang, v, color=col, lw=2, label=nm); ax.fill(ang, v, color=col, alpha=.08)
            ax.set_xticks(ang[:-1]); ax.set_xticklabels([s.split(" ")[0][:9] for s in subs_all], fontsize=7); ax.set_ylim(0, 100)
            ax.tick_params(axis="y", labelsize=6); ax.legend(fontsize=7, loc="upper right", bbox_to_anchor=(1.3, 1.15), frameon=False)
            st.pyplot(fig); plt.close(fig)

    st.markdown("<div class='sec-title'>🔎 Ders Karşılaştırması: Tüm Denemeler</div>", unsafe_allow_html=True)
    subj = st.selectbox("Ders seç", subs_all)
    rows = []; prev_p = None
    for a in F:
        v = a["subjects"].get(subj)
        if not v: continue
        p = _pct(v)
        rows.append([a["ts"][:10], MODE_NAMES.get(a["mode"], a["mode"]), a.get("scope", ""), f"{v['d']} / {v['y']} / {v['b']}", f"{v['d'] - v['y'] / 3:.2f}", f"%{p:.0f}", theme.delta(None if prev_p is None else p - prev_p, " puan"), theme.bar(p)])
        prev_p = p
    st.markdown(theme.html_table(["Tarih", "Tür", "Kapsam", "D / Y / B", "Net", "Başarı", "Önceki Denemeye Göre", ""], rows[::-1]), unsafe_allow_html=True)

    st.markdown("<div class='sec-title'>🧩 Ünite / Kazanım Analizi</div>", unsafe_allow_html=True)
    agg = {}
    for a in F:
        for key, v in a.get("units", {}).items():
            s, u = key.split("||", 1)
            x = agg.setdefault((s, u), [0, 0]); x[0] += v["n"]; x[1] += v["d"]
    if agg:
        items = sorted(((s, u, n, dd, 100 * dd / n) for (s, u), (n, dd) in agg.items() if n), key=lambda t: t[4])
        w, g = items[:6], items[::-1][:6]
        cw, cg = st.columns(2)
        cw.markdown("**⚠️ Önce Çalışılması Gerekenler**")
        cw.markdown(theme.html_table(["Ders · Ünite", "D/Soru", "Başarı"], [[f"{s} · {u}", f"{dd}/{n}", theme.bar(p)] for s, u, n, dd, p in w]), unsafe_allow_html=True)
        cg.markdown("**💪 En Güçlü Alanların**")
        cg.markdown(theme.html_table(["Ders · Ünite", "D/Soru", "Başarı"], [[f"{s} · {u}", f"{dd}/{n}", theme.bar(p)] for s, u, n, dd, p in g]), unsafe_allow_html=True)

    st.markdown("<div class='sec-title'>🗂️ Deneme Geçmişi</div>", unsafe_allow_html=True)
    rows = [[a["ts"].replace("T", " "), C.GRADES.get(a["grade"], {}).get("label", a["grade"]), MODE_NAMES.get(a["mode"], a["mode"]), a.get("scope", ""),
             a["correct"], a["wrong"], a["blank"], f"{a['net']:.2f}", f"%{a['pct']:.1f}", f"{a.get('duration_sec', 0) // 60} dk"] for a in F[::-1]]
    st.markdown(theme.html_table(["Tarih", "Sınıf", "Tür", "Kapsam", "D", "Y", "B", "Net", "Başarı", "Süre"], rows), unsafe_allow_html=True)
    csv = "tarih,sinif,tur,kapsam,dogru,yanlis,bos,net,basari\n" + "\n".join(
        f"{a['ts']},{a['grade']},{a['mode']},\"{a.get('scope', '')}\",{a['correct']},{a['wrong']},{a['blank']},{a['net']:.2f},{a['pct']:.1f}" for a in F)
    st.download_button("⬇️ Geçmişi CSV indir", csv.encode("utf-8-sig"), "denemematik_gecmis.csv", "text/csv")


def wrongs():
    """Dönüş: yeni test için seçilen soru listesi (veya None)."""
    d = storage.load(); W = d["wrongs"]
    st.markdown("<div class='hero'><h1>🧠 Yanlış Yaptığım Sorular Arşivi</h1><p>Yanlışların otomatik burada birikir. Öğrendiklerini işaretle, kalanlardan yeni test üret.</p></div>", unsafe_allow_html=True)
    if not W:
        st.info("Arşiv boş. Bir deneme çözdüğünde yanlışların buraya otomatik eklenir."); return None
    open_w = [w for w in W if not w.get("mastered")]
    subs = sorted({w["subject"] for w in W})
    c1, c2, c3 = st.columns([2, 2, 2])
    sel = c1.selectbox("Ders", ["Tümü"] + subs)
    show = c2.radio("Göster", ["Öğrenilmeyenler", "Öğrenilenler", "Hepsi"], horizontal=True)
    c3.markdown(_kpi("Arşiv", f"{len(open_w)} açık", f"{len(W) - len(open_w)} öğrenildi"), unsafe_allow_html=True)
    L = [w for w in W if (sel == "Tümü" or w["subject"] == sel) and (show == "Hepsi" or (show == "Öğrenilenler") == bool(w.get("mastered")))]
    result = None
    if [w for w in L if not w.get("mastered")]:
        st.markdown("<div class='primary-btn'>", unsafe_allow_html=True)
        if st.button(f"🎯 Bu {len([w for w in L if not w.get('mastered')])} yanlışımdan test oluştur"):
            result = [dict(w["q"], _wid=w["id"]) for w in L if not w.get("mastered")]
        st.markdown("</div>", unsafe_allow_html=True)
    for w in L[::-1]:
        q = w["q"]
        with st.expander(f"{'✅' if w.get('mastered') else '❌'} [{w['subject']}] {w.get('unit', '')} — {q['question'][:90]}"):
            if q.get("passage"): st.markdown(f"<div class='passage-box'>{q['passage']}</div>", unsafe_allow_html=True)
            import visuals
            if visuals.is_table(q.get("shape")):
                st.markdown(theme.html_table(q["shape"].get("headers", []), q["shape"].get("rows", [])), unsafe_allow_html=True)
            elif q.get("shape"):
                png = visuals.render_png(dict(q["shape"]))
                if png: st.image(png, width=360)
            st.markdown(f"**{q['question']}**")
            for k, v in q["options"].items():
                m = " 🟢 **doğru**" if k == q["answer"] else (" 🔴 **seçtiğin**" if k == w.get("user") else "")
                st.markdown(f"- **{k})** {v}{m}")
            if q.get("explanation"): st.info(f"💡 {q['explanation']}")
            b1, b2 = st.columns(2)
            if b1.button("✅ Öğrendim" if not w.get("mastered") else "↩️ Geri al", key=f"m_{w['id']}"):
                storage.update_wrong(w["id"], mastered=not w.get("mastered")); st.rerun()
            if b2.button("🗑️ Sil", key=f"d_{w['id']}"):
                storage.delete_wrong(w["id"]); st.rerun()
    return result


def badges():
    d = storage.load()
    st.markdown("<div class='hero'><h1>🏅 Ünite Başarı Sertifikaları & Rozetler</h1><p>Düzenli çalıştıkça rozet kazan, ünitede %80 başarıya ulaşınca sertifikanı indir.</p></div>", unsafe_allow_html=True)
    name = st.text_input("Sertifikada görünecek ad", value=d["profile"].get("name", ""), placeholder="Adın Soyadın")
    if name != d["profile"].get("name", ""):
        storage.set_name(name)
    B = storage.earned_badges(d)
    st.markdown(f"<div class='sec-title'>Rozetler ({sum(1 for b in B if b[4])}/{len(B)})</div>", unsafe_allow_html=True)
    cols = st.columns(4)
    for i, (k, ic, t, ds, ok) in enumerate(B):
        cols[i % 4].markdown(f"<div class='badge-card {'' if ok else 'off'}'><div class='ic'>{ic}</div><div class='t'>{t}</div><div class='ds'>{ds}</div></div>", unsafe_allow_html=True)
    st.markdown("<div class='sec-title'>📜 Ünite Başarı Sertifikaları</div>", unsafe_allow_html=True)
    agg = storage.unit_summary(d)
    ok = [(g, s, u, v) for (g, s, u), v in agg.items() if v["n"] >= 10 and v["d"] / v["n"] >= .8]
    near = [(g, s, u, v) for (g, s, u), v in agg.items() if v["n"] >= 1 and (v["n"] < 10 or v["d"] / v["n"] < .8)]
    if not ok:
        st.info("Sertifika için bir ünitede en az 10 soru çözmeli ve %80 başarıya ulaşmalısın.")
    for i, (g, s, u, v) in enumerate(ok):
        p = 100 * v["d"] / v["n"]
        c1, c2 = st.columns([4, 1])
        c1.markdown(f"🎓 **{C.GRADES[g]['label']} · {s} · {u}** — %{p:.0f} ({v['d']}/{v['n']})")
        pdf = pdf_export.build_certificate(name, s, u, C.GRADES[g]["label"], p)
        c2.download_button("PDF", pdf, f"sertifika_{i}.pdf", "application/pdf", key=f"cert_{i}")
    if near:
        st.markdown("**Yolda olduğun üniteler**")
        rows = [[f"{C.GRADES[g]['label']} · {s} · {u}", f"{v['d']}/{v['n']}", theme.bar(100 * v["d"] / v["n"])] for g, s, u, v in sorted(near, key=lambda t: -t[3]["d"] / t[3]["n"])[:12]]
        st.markdown(theme.html_table(["Ünite", "Doğru/Soru", "Başarı"], rows), unsafe_allow_html=True)
