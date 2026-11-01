# -*- coding: utf-8 -*-
"""Denemematik — MEB Maarif Modeli yapay zekâ deneme platformu.
Çalıştırma:  streamlit run app.py
Anahtarlar:  .streamlit/secrets.toml  ->  [api_keys]  groq_keys=[".."]  gemini_keys=[".."]
"""
import os
import sys
import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # core/ ve ui/ her zaman bulunsun

st.set_page_config(page_title="Denemematik • MEB Deneme Platformu", page_icon="🎓", layout="wide", initial_sidebar_state="expanded")

from core import ai_engine, curriculum as cur
from ui import theme, state, setup, exam, reports, extras

theme.inject()
state.init()

GROQ_KEYS, GEMINI_KEYS = ai_engine.load_keys()
if not GROQ_KEYS and not GEMINI_KEYS and not ai_engine.demo_mode():
    st.error("⚠️ `.streamlit/secrets.toml` dosyasında API anahtarları bulunamadı!")
    st.code('[api_keys]\ngroq_keys = ["gsk_..."]\ngemini_keys = ["AIza..."]', language="toml")
    st.stop()

# ------------------------------------------------------------------ kenar çubuğu
with st.sidebar:
    st.markdown("<div class='brand'>🎓 Deneme<span>matik</span></div>", unsafe_allow_html=True)
    st.caption("MEB Maarif Modeli • AI ile sınırsız deneme")
    st.markdown("---")
    st.button("🏠 Ana Sayfa", key="nv_home", on_click=lambda: (state.reset_exam(), state.nav("home")))
    st.button("📄 Yaprak Test", key="nv_leaf", on_click=setup._tool_go, args=("leaf_start",))
    st.button("📊 Performans & Raporlar", key="nv_rep", on_click=state.nav, args=("reports",))
    st.button("🗂️ Yanlış Arşivim", key="nv_arc", on_click=state.nav, args=("archive",))
    st.button("🏅 Rozet & Sertifika", key="nv_bdg", on_click=state.nav, args=("badges",))
    st.markdown("---")
    g = st.session_state.grade
    if g:
        st.markdown(f"<div class='side-chip'>🎓 <b>{cur.GRADE_LABELS[g]}</b><br>Seçili tür: {st.session_state.mode or '—'}</div>", unsafe_allow_html=True)
    mode_txt = "DEMO (çevrimdışı)" if ai_engine.demo_mode() else f"Groq {len(GROQ_KEYS)} • Gemini {len(GEMINI_KEYS)}"
    st.markdown(f"<div class='side-chip'>🤖 API havuzu<br><b>{mode_txt}</b><br><small>Önce Groq, sonra Gemini</small></div>", unsafe_allow_html=True)

# ------------------------------------------------------------------ yönlendirme
PAGE = st.session_state.page
ROUTES = {
    "home": setup.home, "modes": setup.modes, "setup": setup.setup, "pre": setup.pre,
    "exam": exam.exam, "selfscore": exam.selfscore, "result": exam.result,
    "reports": reports.reports, "archive": extras.archive, "badges": extras.badges,
}
ROUTES.get(PAGE, setup.home)()
