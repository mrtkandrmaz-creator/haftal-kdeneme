import time
import streamlit as st
import json
import io
import matplotlib.pyplot as plt
import numpy as np

# Matplotlib Türkçe ve Düzgün Görünüm Ayarları
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

# Sayfa Yapılandırması
st.set_page_config(
    page_title="MEB Müfredatı 80 Soruluk Deneme Paneli",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern UI ve Özel CSS Stilleri
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    
    div.stButton > button:first-child {
        width: 100%;
        border-radius: 14px;
        font-weight: 800;
        font-size: 1.1rem;
        padding: 1.0rem 1.2rem;
        background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
        color: white;
        border: none;
        box-shadow: 0 6px 12px -2px rgba(249, 115, 22, 0.3);
        transition: all 0.3s ease;
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px -4px rgba(249, 115, 22, 0.5);
    }
    
    .nav-btn-container div.stButton > button:first-child {
        font-size: 1.25rem !important;
        padding: 1.1rem 1.5rem !important;
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%) !important;
        box-shadow: 0 6px 15px -2px rgba(2, 132, 199, 0.35) !important;
    }
    .nav-btn-container div.stButton > button:first-child:hover {
        box-shadow: 0 8px 22px -4px rgba(2, 132, 199, 0.55) !important;
    }

    .question-card {
        background: white;
        padding: 2.2rem;
        border-radius: 16px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05);
        border: 1px solid #e2e8f0;
        margin-bottom: 1.5rem;
    }
    
    .question-title {
        font-size: 1.45rem !important;
        font-weight: 800 !important;
        color: #1e293b !important;
        line-height: 1.65 !important;
        margin-top: 1rem;
        margin-bottom: 1.2rem;
    }
    .passage-box {
        background: #f1f5f9;
        border-left: 5px solid #0284c7;
        padding: 1.2rem;
        border-radius: 8px;
        font-size: 1.1rem;
        color: #334155;
        margin-bottom: 1.2rem;
        line-height: 1.7;
    }
    .timer-box {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        color: #38bdf8;
        padding: 1.2rem;
        border-radius: 16px;
        text-align: center;
        font-size: 2.2rem;
        font-weight: 900;
        box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.3);
        border: 2px solid #38bdf8;
        letter-spacing: 2px;
    }
    .badge {
        background-color: #e0f2fe;
        color: #0369a1;
        padding: 0.4rem 0.9rem;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.9rem;
    }
    
    /* Geliştirilmiş Modern Tablo Stili */
    .custom-table-container {
        overflow-x: auto;
        margin: 15px 0;
        border-radius: 12px;
        box-shadow: 0 4px 15px -3px rgba(0, 0, 0, 0.08);
        border: 1px solid #e2e8f0;
    }
    .custom-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 0.95rem;
        background-color: #ffffff;
        text-align: left;
    }
    .custom-table th {
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
        color: white;
        padding: 14px 18px;
        font-weight: 700;
        letter-spacing: 0.3px;
        border-bottom: 2px solid #0284c7;
    }
    .custom-table td {
        padding: 12px 18px;
        border-bottom: 1px solid #f1f5f9;
        color: #334155;
    }
    .custom-table tr:last-child td {
        border-bottom: none;
    }
    .custom-table tr:nth-child(even) {
        background-color: #f8fafc;
    }
    .custom-table tr:hover {
        background-color: #f1f5f9;
    }
    </style>
""", unsafe_allow_html=True)

# Gelişmiş Dinamik Görselleştirme, Tablo ve Şema Motoru (Kusursuz Görsel Kalite)
def draw_geometry_shape(shape_data):
    if not isinstance(shape_data, dict):
        return
        
    st_type = str(shape_data.get("type", "")).strip().lower()
    if not st_type:
        return

    # Gelişmiş HTML Tablo Motoru
    if st_type == "table":
        headers = shape_data.get("headers", ["Veri", "Değer"])
        rows = shape_data.get("rows", [["Örnek 1", "10"], ["Örnek 2", "20"]])
        title = str(shape_data.get("title", "Veri Tablosu"))
        
        st.markdown(f"<p style='font-weight: 700; color: #1e293b; margin-bottom: 0.4rem; font-size: 1.05rem;'>📊 {title}</p>", unsafe_allow_html=True)
        table_html = "<div class='custom-table-container'><table class='custom-table'><thead><tr>"
        for h in headers:
            table_html += f"<th>{h}</th>"
        table_html += "</tr></thead><tbody>"
        for row in rows:
            table_html += "<tr>"
            for cell in row:
                table_html += f"<td>{cell}</td>"
            table_html += "</tr>"
        table_html += "</tbody></table></div>"
        st.markdown(table_html, unsafe_allow_html=True)
        return

    # Matplotlib görselleri için profesyonel boyutlandırma ve çakışma önleyici layout optimizasyonu
    fig, ax = plt.subplots(figsize=(6.8, 4.0))
    fig.subplots_adjust(top=0.82, bottom=0.18, left=0.12, right=0.92)
    ax.set_aspect('equal')
    ax.axis('off')
    
    try:
        # 1. GEOMETRİ / ÜÇGEN ÇİZİMİ
        if st_type == "triangle":
            sub_type = str(shape_data.get("sub_type", "scalene")).strip().lower()
            a_label = str(shape_data.get("A", "A"))
            b_label = str(shape_data.get("B", "B"))
            c_label = str(shape_data.get("C", "C"))
            side_ab = str(shape_data.get("side_ab", ""))
            side_bc = str(shape_data.get("side_bc", ""))
            side_ac = str(shape_data.get("side_ac", ""))
            angle_a = str(shape_data.get("angle_a", ""))
            
            if sub_type == "right":
                pts = np.array([[0, 0], [4, 0], [0, 3]])
                ax.plot([0, 0.35, 0.35, 0], [0, 0, 0.35, 0.35], color='#1e293b', linewidth=1.2)
            elif sub_type == "equilateral":
                h = np.sqrt(3) / 2 * 4
                pts = np.array([[0, 0], [4, 0], [2, h]])
            else:
                pts = np.array([[0, 0], [5, 0], [2, 4.2]])
                
            triangle = plt.Polygon(pts, closed=True, facecolor='#f8fafc', edgecolor='#1e293b', linewidth=2)
            ax.add_patch(triangle)
            
            offsets = [[-0.5, -0.5], [0.4, -0.5], [0, 0.35]]
            labels = [b_label, c_label, a_label]
            for i, p in enumerate(pts):
                ax.text(p[0] + offsets[i][0], p[1] + offsets[i][1], labels[i], fontsize=10, fontweight='bold', color='#1e293b')
            
            if side_ab:
                ax.text(-0.8, 1.5, f"AB: {side_ab}", fontsize=8.5, color='#0284c7', fontweight='bold', ha='right')
            if side_bc:
                ax.text(2.5, -0.7, f"BC: {side_bc}", fontsize=8.5, color='#0284c7', fontweight='bold', ha='center')
            if side_ac:
                ax.text(2.8, 2.3, f"AC: {side_ac}", fontsize=8.5, color='#0284c7', fontweight='bold')
            if angle_a:
                ax.text(2.0, 3.8, f"Â={angle_a}", fontsize=8.5, color='#ea580c', fontweight='bold', ha='center')
                
            ax.set_xlim(-3.5, 7.5)
            ax.set_ylim(-2.5, 5.8)

        # 2. ÇEMBER VE DAİRE
        elif st_type == "circle":
            center_label = str(shape_data.get("center", "O"))
            radius_label = str(shape_data.get("radius", "r"))
            show_diameter = bool(shape_data.get("show_diameter", False))
            chord = str(shape_data.get("chord", ""))
            
            circle = plt.Circle((0, 0), 2.2, facecolor='#f8fafc', edgecolor='#1e293b', linewidth=2)
            ax.add_patch(circle)
            ax.plot(0, 0, 'o', color='#ea580c', markersize=5)
            ax.text(0.18, -0.38, center_label, fontsize=10, fontweight='bold', color='#ea580c')
            
            if show_diameter:
                ax.plot([-2.2, 2.2], [0, 0], linestyle='--', color='#94a3b8', linewidth=1.4)
                ax.text(0, 0.25, f"Çap: {radius_label}", fontsize=8.5, fontweight='bold', color='#0284c7', ha='center')
            else:
                ax.plot([0, 2.2], [0, 0], color='#0284c7', linewidth=1.8)
                ax.text(1.1, 0.2, f"r = {radius_label}", fontsize=8.5, fontweight='bold', color='#0284c7')
                
            if chord:
                ax.plot([-1.8, 1.8], [-1.3, -1.3], color='#10b981', linewidth=1.8)
                ax.text(0, -1.75, f"Kiriş: {chord}", fontsize=8.5, fontweight='bold', color='#10b981', ha='center')
                
            ax.set_xlim(-3.2, 3.2)
            ax.set_ylim(-3.2, 3.2)

        # 3. ÇUBUK / GRAFİK ANALİZİ
        elif st_type in ["bar_chart", "science_chart"]:
            ax.set_aspect('auto')
            labels = shape_data.get("labels", ["A", "B", "C", "D"])
            values = shape_data.get("values", [10, 25, 15, 30])
            title = str(shape_data.get("title", "Veri ve Grafik Analizi"))
            
            clean_vals = [float(v) if str(v).replace('.','',1).isdigit() else 10.0 for v in values]
            bars = ax.bar(labels, clean_vals, color='#0284c7', width=0.45, edgecolor='#1e293b', linewidth=1, alpha=0.9)
            
            ax.set_title(title, fontsize=11, fontweight='bold', color='#1e293b', pad=18)
            ax.tick_params(axis='x', rotation=15, labelsize=9)
            ax.tick_params(axis='y', labelsize=9)
            
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_color('#cbd5e1')
            ax.spines['bottom'].set_color('#cbd5e1')
            
            max_val = max(clean_vals) if clean_vals else 10
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + (max_val * 0.03), f'{height:g}',
                        ha='center', va='bottom', fontsize=9, fontweight='bold', color='#1e293b')
            
            ax.set_ylim(0, max_val * 1.35)
            ax.set_xlim(-0.8, len(labels) - 0.2)

        # 4. TREND / ÇİZGİ GRAFİĞİ
        elif st_type == "line_chart":
            ax.set_aspect('auto')
            labels = shape_data.get("labels", ["Oca", "Şub", "Mar", "Nis", "May"])
            values = shape_data.get("values", [12, 18, 15, 22, 30])
            title = str(shape_data.get("title", "Değişim ve Çizgi Grafiği"))
            
            clean_vals = [float(v) if str(v).replace('.','',1).isdigit() else 10.0 for v in values]
            
            ax.plot(labels, clean_vals, marker='o', color='#ea580c', linewidth=2.5, markersize=7, markerfacecolor='#0284c7', markeredgecolor='#ffffff')
            ax.set_title(title, fontsize=11, fontweight='bold', color='#1e293b', pad=18)
            ax.tick_params(axis='x', rotation=15, labelsize=9)
            ax.tick_params(axis='y', labelsize=9)
            
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_color('#cbd5e1')
            ax.spines['bottom'].set_color('#cbd5e1')
            
            max_val = max(clean_vals) if clean_vals else 10
            for x_pos, y_val in enumerate(clean_vals):
                ax.text(x_pos, y_val + (max_val * 0.04), f'{y_val:g}', ha='center', va='bottom', fontsize=9, fontweight='bold', color='#1e293b')
                
            ax.set_ylim(0, max_val * 1.40)
            ax.set_xlim(-0.5, len(labels) - 0.5)

        # 5. FEN BİLİMLERİ: UZAY, DÜNYA, GÜNEŞ, AY EVRELERİ VE TUTULMALAR
        elif st_type in ["science_space", "space_orbit", "eclipse", "moon_phases"]:
            sub_sub = str(shape_data.get("sub_type", "orbit")).strip().lower()
            title = str(shape_data.get("title", "Fen Bilimleri Sistem Şeması"))
            
            if sub_sub == "moon_phases":
                sun_indicator = plt.Circle((-3.5, 0), 0.6, facecolor='#f59e0b', edgecolor='#d97706', linewidth=1.2)
                ax.add_patch(sun_indicator)
                ax.text(-3.5, -0.9, "Güneş Işığı", fontsize=7.5, fontweight='bold', color='#d97706', ha='center')
                
                earth_center = plt.Circle((0, 0), 0.7, facecolor='#0284c7', edgecolor='#0369a1', linewidth=1.5)
                ax.add_patch(earth_center)
                ax.text(0, -0.2, "Dünya", fontsize=8, fontweight='bold', color='white', ha='center', va='center')
                
                moon_positions = [
                    (0, 1.8, "Yeni Ay"), (1.8, 0, "İlk Dördün"),
                    (0, -1.8, "Dolunay"), (-1.8, 0, "Son Dördün")
                ]
                for mx, my, mlabel in moon_positions:
                    m_circle = plt.Circle((mx, my), 0.3, facecolor='#cbd5e1', edgecolor='#64748b', linewidth=1)
                    ax.add_patch(m_circle)
                    ax.text(mx, my - 0.6, mlabel, fontsize=7, fontweight='bold', color='#334155', ha='center')
                    
                ax.set_xlim(-4.5, 4.5)
                ax.set_ylim(-3.0, 3.0)
                
            elif sub_sub == "solar_eclipse":
                sun_p = plt.Circle((-2.5, 0), 0.75, facecolor='#f59e0b', edgecolor='#d97706', linewidth=1.5)
                ax.add_patch(sun_p)
                ax.text(-2.5, -1.0, "Güneş", fontsize=8, fontweight='bold', color='#d97706', ha='center')
                
                moon_p = plt.Circle((-0.7, 0), 0.25, facecolor='#cbd5e1', edgecolor='#64748b', linewidth=1)
                ax.add_patch(moon_p)
                ax.text(-0.7, -0.5, "Ay", fontsize=8, fontweight='bold', color='#64748b', ha='center')
                
                earth_p = plt.Circle((1.5, 0), 0.55, facecolor='#0284c7', edgecolor='#0369a1', linewidth=1.5)
                ax.add_patch(earth_p)
                ax.text(1.5, -0.8, "Dünya", fontsize=8, fontweight='bold', color='#0284c7', ha='center')
                
                ax.set_xlim(-3.8, 3.0)
                ax.set_ylim(-2.0, 2.0)
                
            elif sub_sub == "lunar_eclipse":
                sun_p = plt.Circle((-2.5, 0), 0.75, facecolor='#f59e0b', edgecolor='#d97706', linewidth=1.5)
                ax.add_patch(sun_p)
                ax.text(-2.5, -1.0, "Güneş", fontsize=8, fontweight='bold', color='#d97706', ha='center')
                
                earth_p = plt.Circle((-0.5, 0), 0.55, facecolor='#0284c7', edgecolor='#0369a1', linewidth=1.5)
                ax.add_patch(earth_p)
                ax.text(-0.5, -0.8, "Dünya", fontsize=8, fontweight='bold', color='#0284c7', ha='center')
                
                moon_p = plt.Circle((1.5, 0), 0.25, facecolor='#cbd5e1', edgecolor='#64748b', linewidth=1)
                ax.add_patch(moon_p)
                ax.text(1.5, -0.5, "Ay", fontsize=8, fontweight='bold', color='#64748b', ha='center')
                
                ax.set_xlim(-3.8, 3.0)
                ax.set_ylim(-2.0, 2.0)
                
            else:
                sun = plt.Circle((-2.0, 0), 0.8, facecolor='#f59e0b', edgecolor='#d97706', linewidth=1.5)
                ax.add_patch(sun)
                ax.text(-2.0, -1.2, "Güneş", fontsize=8.5, fontweight='bold', color='#d97706', ha='center')
                
                orbit = plt.Circle((0, 0), 2.1, fill=False, edgecolor='#94a3b8', linestyle='--', linewidth=1.2)
                ax.add_patch(orbit)
                
                earth = plt.Circle((2.1, 0), 0.4, facecolor='#0284c7', edgecolor='#0369a1', linewidth=1.2)
                ax.add_patch(earth)
                ax.text(2.1, -0.7, "Dünya", fontsize=8.5, fontweight='bold', color='#0284c7', ha='center')
                
                ax.set_xlim(-3.8, 3.5)
                ax.set_ylim(-2.5, 2.5)

            ax.set_title(title, fontsize=11, fontweight='bold', color='#1e293b', pad=18)

        plt.tight_layout()
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', dpi=180)
        buf.seek(0)
        st.image(buf, width=380)
        plt.close(fig)
    except Exception as e:
        plt.close(fig)
        st.info("📊 Soru görsel şeması hazırlanıyor...")

# API Anahtarları
try:
    GROQ_KEYS = st.secrets["api_keys"].get("groq_keys", [])
    GEMINI_KEYS = st.secrets["api_keys"].get("gemini_keys", [])
except Exception:
    GROQ_KEYS = []
    GEMINI_KEYS = []

if not GROQ_KEYS and not GEMINI_KEYS:
    st.error("⚠️ `.streamlit/secrets.toml` dosyasında API anahtarları bulunamadı!")
    st.stop()

# Oturum Durumları
if "questions" not in st.session_state:
    st.session_state.questions = []
if "quiz_ready" not in st.session_state:
    st.session_state.quiz_ready = False
if "quiz_started" not in st.session_state:
    st.session_state.quiz_started = False
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "selected_answers" not in st.session_state:
    st.session_state.selected_answers = {}
if "current_page" not in st.session_state:
    st.session_state.current_page = 0
if "custom_topic_input" not in st.session_state:
    st.session_state.custom_topic_input = ""

# Yan Menü Ayarları
st.sidebar.markdown("## ⚙ MEB Müfredat & Sınav Ayarları")
st.sidebar.markdown("---")

selected_grade = st.sidebar.selectbox("🎓 Sınıf Seviyesi", ["5. Sınıf", "6. Sınıf", "7. Sınıf", "8. Sınıf (LGS)"])
term = st.sidebar.selectbox("📚 Eğitim Dönemi", ["1. Dönem (18 Hafta)", "2. Dönem (18 Hafta)"])

weeks_options = [f"Hafta {i}" for i in range(1, 19)]
weeks_options.extend([
    "4. Hafta Kapsamlı Değerlendirme ve Tekrar", 
    "8. Hafta Kapsamlı Değerlendirme ve Tekrar", 
    "12. Hafta Kapsamlı Değerlendirme ve Tekrar", 
    "16. Hafta Kapsamlı Değerlendirme ve Tekrar", 
    "18. Hafta Genel Dönem Bitirme Sınavı"
])

selected_scope = st.sidebar.selectbox("📅 Hafta / Kazanım Kapsamı", weeks_options)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔍 Manuel Ek Konu / Odak Kriteri")

def update_custom_topic():
    st.session_state.custom_topic_input = st.session_state.widget_custom_topic

st.sidebar.text_input(
    "Özel Konu / Alt Başlık (Opsiyonel)",
    value=st.session_state.custom_topic_input,
    key="widget_custom_topic",
    on_change=update_custom_topic,
    placeholder="Örn: Açılar, Hücre, Paragraf...",
    help="Belirttiğiniz konu soruların yaklaşık 1/3'ünde dengeli odak olarak yer alır, kalanı genel müfredat kazanımlarından oluşur."
)

difficulty_level = st.sidebar.selectbox(
    "📊 Soru Zorluk Derecesi (Kademe Seçimi)",
    [
        "🟢 1. Çok Kolay / Temel Kazanım Düzeyi",
        "🔵 2. Kolay / Bilgiyi Hatırlama ve Kavrama",
        "🟡 3. Orta / MEB Standart & Beceri Temelli (İdeal LGS)",
        "🟠 4. Güçlendirilmiş / Seçici ve Yorum Odaklı",
        "🔴 5. Üst Düzey Zor / LGS Seçici (Çok Aşamalı Muhakeme)",
        "⚡ 6. Çok Zor / Olimpiyat & Üst Düzey Beceri Odaklı"
    ]
)

question_count = 80

st.sidebar.markdown("---")
st.sidebar.markdown("### 🚀 Soru İşlemleri")
generate_btn = st.sidebar.button("Soruları Üret")

if generate_btn:
    st.sidebar.info("⏳ Sorular hazırlanıyor, çoklu API havuzu taranıyor...")

# GÜNCELLENDİ: Seçilen Hafta/Kazanım Kapsamına Uygun Dinamik Kazanım Haritası Paneli
st.sidebar.markdown("---")
st.sidebar.markdown(f"### 📋 Kazanım Haritası ({selected_scope})")

# Haftalık veya genel döneme göre dinamik içerik üretici mantık
def get_dynamic_syllabus(grade, scope):
    s_lower = scope.lower()
    if "hafta 1" in s_lower or "1. hafta" in s_lower:
        return [
            ("**Türkçe (15 Soru)**", "Sözcükte Anlam, Temel Kavramlar, Ses Bilgisi"),
            ("**Matematik (15 Soru)**", "Doğal Sayılar ve Milyonlar, Sayı Örüntüleri"),
            ("**Fen Bilimleri (15 Soru)**", "Gezegenimiz Dünya ve Temel Katmanları"),
            ("**Sosyal Bilgiler (15 Soru)**", "Birey ve Toplum, Rol ve Sorumluluklar"),
            ("**Din Kültürü (10 Soru)**", "Yaratılış ve Evrendeki Düzen"),
            ("**İngilizce (10 Soru)**", "Hello! - Karşılama ve Tanışma İfadeleri")
        ]
    elif "hafta 4" in s_lower:
        return [
            ("**Türkçe (15 Soru)**", "Cümlede Anlam İlişkileri, Neden-Sonuç, Amaç-Sonuç"),
            ("**Matematik (15 Soru)**", "Doğrtusal İşlemler, Toplama ve Çıkarma Problemleri"),
            ("**Fen Bilimleri (15 Soru)**", "Güneş'in Yapısı ve Kendi Eksenindeki Dönme Hareketi"),
            ("**Sosyal Bilgiler (15 Soru)**", "Kültürel Mirasımız ve Çocuk Hakları"),
            ("**Din Kültürü (10 Soru)**", "Allah'ın Evrene Koyduğu Yasalar"),
            ("**İngilizce (10 Soru)**", "My Town - Yönler ve Konum Belirtme")
        ]
    elif "hafta 8" in s_lower:
        return [
            ("**Türkçe (15 Soru)**", "Paragrafın Ana Düşüncesi ve Yardımcı Düşünceler"),
            ("**Matematik (15 Soru)**", "Çarpanlar, Katlar veya Kesirler Temel İşlemler"),
            ("**Fen Bilimleri (15 Soru)**", "Ay'ın Evreleri, Dönme ve Dolanma Hareketleri"),
            ("**Sosyal Bilgiler (15 Soru)**", "Tarihi İpek Yolu ve Türk Devletleri"),
            ("**Din Kültürü (10 Soru)**", "İbadet Bilinci ve Namaz İbadeti"),
            ("**İngilizce (10 Soru)**", "Games and Hobbies - Boş Zaman Aktiviteleri")
        ]
    elif "hafta 12" in s_lower or "12. hafta" in s_lower:
        return [
            ("**Türkçe (15 Soru)**", "Metin Türleri (Hikaye, Masal, Bilgilendirici Metinler)"),
            ("**Matematik (15 Soru)**", "Cebirsel İfadeler / Oran ve Orantı Başlangıcı"),
            ("**Fen Bilimleri (15 Soru)**", "Canlılar Dünyası: Hücre Yapısı ve Organeller"),
            ("**Sosyal Bilgiler (15 Soru)**", "Orta Çağ'da Türk Dünyası ve İslam Tarihi"),
            ("**Din Kültürü (10 Soru)**", "Peygamberlerin Özellikleri ve İlahi Kitaplar"),
            ("**İngilizce (10 Soru)**", "Daily Routine - Günlük Rutinler ve Saatler")
        ]
    elif "hafta 16" in s_lower or "16. hafta" in s_lower:
        return [
            ("**Türkçe (15 Soru)**", "Fiilimsiler / Ek Fiil / Söz Sanatları Kapsamı"),
            ("**Matematik (15 Soru)**", "Veri Analizi ve Olasılık Temelleri"),
            ("**Fen Bilimleri (15 Soru)**", "Kuvvet ve Enerji Dönüşümleri, Basit Makineler"),
            ("**Sosyal Bilgiler (15 Soru)**", "Osmanlı Devleti'nin Kuruluş Dönemi ve Siyasi Gelişmeler"),
            ("**Din Kültürü (10 Soru)**", "Kader İnancı ve Zekat / Sadaka Kurumları"),
            ("**İngilizce (10 Soru)**", "In The Kitchen - Yemek Tarifleri ve İfadeler")
        ]
    else:
        # Genel / Standart Sınıf Müfredat Haritası
        base_map = {
            "5. Sınıf": [
                ("**Türkçe (15 Soru)**", f"{selected_scope} - Sözcükte/Cümlede Anlam ve Paragraf"),
                ("**Matematik (15 Soru)**", f"{selected_scope} - Temel İşlemler ve Geometrik Açılar"),
                ("**Fen Bilimleri (15 Soru)**", f"{selected_scope} - Güneş, Dünya, Ay ve Kuvvet"),
                ("**Sosyal Bilgiler (15 Soru)**", f"{selected_scope} - Birey, Toplum ve Kültürel Miras"),
                ("**Din Kültürü (10 Soru)**", f"{selected_scope} - Allah İnancı ve İbadetler"),
                ("**İngilizce (10 Soru)**", f"{selected_scope} - Ünite Kelime ve Diyaloglar")
            ],
            "6. Sınıf": [
                ("**Türkçe (15 Soru)**", f"{selected_scope} - Deyimler, Paragraf Yapısı ve Dil Bilgisi"),
                ("**Matematik (15 Soru)**", f"{selected_scope} - Üslü Sayılar, Ortaklar ve Tam Sayılar"),
                ("**Fen Bilimleri (15 Soru)**", f"{selected_scope} - Güneş Sistemi, Sistemler ve Kuvvet"),
                ("**Sosyal Bilgiler (15 Soru)**", f"{selected_scope} - Türk Devletleri ve İslam Tarihi"),
                ("**Din Kültürü (10 Soru)**", f"{selected_scope} - Peygamberler ve Namaz"),
                ("**İngilizce (10 Soru)**", f"{selected_scope} - Life, Breakfast & Downtown")
            ],
            "7. Sınıf": [
                ("**Türkçe (15 Soru)**", f"{selected_scope} - Fiiller, Zarflar ve Sözel Mantık"),
                ("**Matematik (15 Soru)**", f"{selected_scope} - Rasyonel Sayılar ve Cebirsel İfadeler"),
                ("**Fen Bilimleri (15 Soru)**", f"{selected_scope} - Hücre Bölünmeleri ve Saf Maddeler"),
                ("**Sosyal Bilgiler (15 Soru)**", f"{selected_scope} - Osmanlı Beylikten İmparatorluğa"),
                ("**Din Kültürü (10 Soru)**", f"{selected_scope} - Melek, Ahiret ve Kader"),
                ("**İngilizce (10 Soru)**", f"{selected_scope} - Appearance, Sports & Biographies")
            ],
            "8. Sınıf (LGS)": [
                ("**Türkçe (15 Soru)**", f"{selected_scope} - Fiilimsiler, Ögeler ve Yeni Nesil Paragraf"),
                ("**Matematik (15 Soru)**", f"{selected_scope} - Çarpanlar, Köklü İfadeler ve Olasılık"),
                ("**Fen Bilimleri (15 Soru)**", f"{selected_scope} - Mevsimler, DNA, Basınç ve Asit-Baz"),
                ("**Sosyal Bilgiler (İnkılap) (15 Soru)**", f"{selected_scope} - Bir Kahraman Doğuyor & Milli Mücadele"),
                ("**Din Kültürü (10 Soru)**", f"{selected_scope} - Kader, Zekat ve Din-Hayat"),
                ("**İngilizce (10 Soru)**", f"{selected_scope} - Friendship, Teen Life & Kitchen")
            ]
        }
        return base_map.get(selected_grade, base_map["5. Sınıf"])

active_syllabus = get_dynamic_syllabus(selected_grade, selected_scope)
for sub_title, content_desc in active_syllabus:
    st.sidebar.markdown(f"• {sub_title}<br><span style='font-size:0.8rem; color:#64748b;'>&nbsp;&nbsp;&nbsp;{content_desc}</span>", unsafe_allow_html=True)

# Ana Ekran Başlığı
st.markdown(f"<h1 style='text-align: center; color: #1e293b; font-weight: 900;'>🎯 {selected_grade} 80 Soruluk Deneme Paneli</h1>", unsafe_allow_html=True)
custom_info_str = f" | Odak Kriter: <b>{st.session_state.custom_topic_input}</b>" if st.session_state.custom_topic_input.strip() else ""
st.markdown(f"<p style='text-align: center; color: #64748b; font-size: 1.1rem;'>Seçilen Kapsam: <b>{selected_scope}</b>{custom_info_str} | Zorluk Kademesi: <b>{difficulty_level}</b></p>", unsafe_allow_html=True)
st.markdown("---")

def call_groq_with_key(api_key, prompt_text):
    from groq import Groq
    client = Groq(api_key=api_key)
    completion = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": "Sen MEB müfredatı soru hazırlama uzmanısın. Paragraf, metin, tablo ve fen bilimleri grafik/şema sorularında asla kesinti yapmaz, eksiksiz üretirsin."},
            {"role": "user", "content": prompt_text}
        ],
        temperature=0.75,
        max_tokens=8000,
        response_format={"type": "json_object"}
    )
    return completion.choices[0].message.content

def call_gemini_with_key(api_key, prompt_text):
    from google import genai
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt_text,
    )
    text = response.text
    if "```json" in text:
        text = text.split("```json")[1].split("```")[0].strip()
    elif "```" in text:
        text = text.split("```")[1].split("```")[0].strip()
    return text

def multi_pool_generate(prompt_text):
    attempts = []
    for i, key in enumerate(GROQ_KEYS):
        if key.strip():
            attempts.append(("Groq", i+1, key, call_groq_with_key))
            
    for i, key in enumerate(GEMINI_KEYS):
        if key.strip():
            attempts.append(("Gemini", i+1, key, call_gemini_with_key))

    if not attempts:
        return None, "Geçerli API anahtarı bulunamadı!"

    last_error = None
    for provider, index, key, func in attempts:
        try:
            result = func(key, prompt_text)
            if result:
                return result, None
        except Exception as e:
            last_error = e
            continue

    return None, str(last_error)

# Soru Üretim Mantığı
if generate_btn:
    current_topic_val = st.session_state.custom_topic_input
    custom_prompt_addon = f"\nDENGELİ ODAK KONU: '{current_topic_val}'\n(Soruların üçte birlik bölümünde bu konuya odaklan, kalanı haftanın diğer tüm kazanımlarından eşit dağılımla üretilsin.)" if current_topic_val.strip() else ""
    
    with st.spinner(f"✨ Çoklu API havuzu taranıyor: {selected_grade} ({selected_scope}) için eksiksiz metinler, gelişmiş matematik grafik kütüphaneleri ve konuya özel fen şemalarıyla 80 soru hazırlanıyor..."):
        prompt = (
            f"Türkiye Cumhuriyeti Millî Eğitim Bakanlığı (MEB) {selected_grade} {term} dönemi resmi öğretim programı "
            f"ve '{selected_scope}' kapsamındaki gerçek haftalık kazanımlarına tam uygun olarak toplam KESİNLİKLE VE EKSİKSİZ olarak tam 80 adet yeni nesil soru hazırla."
            f"{custom_prompt_addon}\n\n"
            f"ZORLUK KADEMESİ VE KALİTE KRİTERİ: '{difficulty_level}'.\n\n"
            "DERS DAĞILIMI VE KESİN SORU SAYILARI VE İÇERİK KURALLARI (TOPLAM TAM 80 SORU):\n"
            "1. Türkçe: 15 Soru (1-15 arası) - Kesinlikle Türkçe dersine ait (Sözel mantık, paragrafta anlam, uzun metinler, dil bilgisi, görsel okuma, deyimler/atasözleri). Metinleri ASLA KISALTMA, eksiksiz tam yaz.\n"
            "2. Matematik: 15 Soru (16-30 arası) - Kesinlikle Matematik dersine ait (Geometri, açılar, üçgenler, çember, veri analizi, çizgi grafikleri, oran-orantı, problemler). Grafik sorularında çubuk ('bar_chart') veya çizgi grafiği ('line_chart') kütüphane şemalarını mutlaka kullan.\n"
            "3. Fen Bilimleri: 15 Soru (31-45 arası) - Kesinlikle Fen Bilimleri dersine ait (Kuvvet ve hareket, Güneş/Dünya/Ay hareketleri, evreler, tutulmalar, hücre, maddeler). Dünya, Güneş, Ay sorularında hep aynı şemayı ASLA kullanma; sorunun konusuna göre 'moon_phases' (evrecikler), 'solar_eclipse' (güneş tutulması), 'lunar_eclipse' (ay tutulması) veya yörünge şemalarından soruya en uygun olanını seç.\n"
            "4. Sosyal Bilgiler: 15 Soru (46-60 arası) - Kesinlikle Sosyal Bilgiler dersine ait (Tarih, coğrafya, harita okuma, kültürel miras, hak ve sorumluluklar).\n"
            "5. Din Kültürü ve Ahlak Bilgisi: 10 Soru (61-70 arası) - Kesinlikle Din Kültürü dersine ait (Ayet ve hadis yorumlama, İslam kültürü, değerler eğitimi).\n"
            "6. İngilizce (English): 10 Soru (71-80 arası) - Kesinlikle İngilizce dersine ait (Diyalog tamamlama, kartlar, tablo eşleştirme, kelime bilgisi).\n\n"
            "🚨 KESİN GÖRSEL VE ŞEMA KURALLARI (`shape` nesnesi):\n"
            "Soruların matematik, fen ve veri okuma bölümlerinde 'shape' alanını boş bırakma; uygun şema parametresini ekle:\n"
            "- Üçgen için: {\"type\": \"triangle\", \"sub_type\": \"right/scalene/equilateral\", \"A\": \"A\", \"B\": \"B\", \"C\": \"C\", \"side_ab\": \"...\", \"angle_a\": \"...\"}\n"
            "- Çember için: {\"type\": \"circle\", \"center\": \"O\", \"radius\": \"5 cm\", \"show_diameter\": true}\n"
            "- Çubuk Grafik için: {\"type\": \"bar_chart\", \"labels\": [\"A\", \"B\", \"C\", \"D\"], \"values\": [10, 25, 15, 30], \"title\": \"Grafik Başlığı\"}\n"
            "- Çizgi Grafik için: {\"type\": \"line_chart\", \"labels\": [\"Oca\", \"Şub\", \"Mar\", \"Nis\"], \"values\": [12, 18, 15, 22], \"title\": \"Trend Grafik Başlığı\"}\n"
            "- Tablo için: {\"type\": \"table\", \"title\": \"Veri Tablosu Başlığı\", \"headers\": [\"Sütun 1\", \"Sütun 2\"], \"rows\": [[\"Satır 1A\", \"Satır 1B\"], [\"Satır 2A\", \"Satır 2B\"]]}\n"
            "- Fen / Uzay / Ay Evreleri için: {\"type\": \"science_space\", \"sub_type\": \"moon_phases\" (veya solar_eclipse, lunar_eclipse, orbit), \"title\": \"Sistem Şeması Başlığı\"}\n"
            "Görsel gerekmeyen metin/dil bilgisi sorularında 'shape' değerini null bırak.\n\n"
            "Her sorunun 4 şıkkı (A, B, C, D) ve doğru cevabı olmalıdır. 'subject' alanına ilgili dersin adını tam yaz.\n"
            "Çıktıyı KESİNLİKLE aşağıdaki JSON formatında ver, başka hiçbir açıklama ekleme:\n"
            "{\n"
            "    \"questions\": [\n"
            "        {\n"
            "            \"id\": 1,\n"
            "            \"subject\": \"Matematik\",\n"
            "            \"passage\": \"Metin veya paragraf içeriği burada eksiksiz yer alacak...\",\n"
            "            \"question\": \"Soru metni...\",\n"
            "            \"shape\": {\"type\": \"triangle\", \"sub_type\": \"right\", \"A\": \"A\", \"B\": \"B\", \"C\": \"C\"},\n"
            "            \"options\": {\n"
            "                \"A\": \"A şıkkı\",\n"
            "                \"B\": \"B şıkkı\",\n"
            "                \"C\": \"C şıkkı\",\n"
            "                \"D\": \"D şıkkı\"\n"
            "            },\n"
            "            \"answer\": \"A\"\n"
            "        }\n"
            "    ]\n"
            "}"
        )
        
        raw_json, error_message = multi_pool_generate(prompt)
        if raw_json:
            try:
                data = json.loads(raw_json)
                st.session_state.questions = data.get("questions", [])
                st.session_state.quiz_ready = True
                st.session_state.quiz_started = False
                st.session_state.selected_answers = {}
                st.session_state.current_page = 0
                st.session_state.custom_topic_input = ""
                st.sidebar.success(f"✅ Toplam {len(st.session_state.questions)} soru başarıyla üretildi!")
                st.rerun()
            except json.JSONDecodeError:
                st.error("Yapay zeka yanıtı geçerli JSON formatına dönüştürülemedi.")
                st.code(raw_json)
        else:
            st.error(f"❌ Bağlantı kurulamadı. Hata: {error_message}")

# Sınavı Başlat Butonu
if st.session_state.quiz_ready and not st.session_state.quiz_started:
    st.markdown("---")
    sc1, sc2, sc3 = st.columns([1, 2, 1])
    with sc2:
        if st.button("🎯 Sınavı Şimdi Başlat"):
            st.session_state.quiz_started = True
            st.session_state.start_time = time.time()
            st.rerun()

# Sınav Ekranı
if st.session_state.quiz_started and st.session_state.questions:
    total_questions = len(st.session_state.questions)
    total_time_seconds = total_questions * 90
    
    elapsed_time = int(time.time() - st.session_state.start_time)
    remaining_time = max(0, total_time_seconds - elapsed_time)
    
    hours = remaining_time // 3600
    minutes = (remaining_time % 3600) // 60
    seconds = remaining_time % 60

    st.markdown("---")
    header_col1, header_col2 = st.columns([2, 1])
    with header_col1:
        st.markdown(f"### 📋 {selected_grade} - {term} ({selected_scope}) 80 Soruluk Deneme")
        st.markdown(f"<span class='badge'>Soru: {st.session_state.current_page + 1} / {total_questions}</span> <span class='badge'>Kademe: {difficulty_level}</span>", unsafe_allow_html=True)
    with header_col2:
        st.markdown(f"<div class='timer-box'>⏳ {hours:02d}:{minutes:02d}:{seconds:02d}</div>", unsafe_allow_html=True)

    st.markdown("---")

    idx = st.session_state.current_page
    q = st.session_state.questions[idx]

    st.markdown(f"<div class='question-card'>", unsafe_allow_html=True)
    sub_badge = f"[{q.get('subject', 'Genel')}]" if 'subject' in q else ""
    
    passage_text = str(q.get('passage', '')).strip()
    if passage_text and passage_text.lower() != "null" and passage_text != "":
        st.markdown(f"<div class='passage-box'><b>📖 Metin / Öncül / Diyalog:</b><br>{passage_text}</div>", unsafe_allow_html=True)

    if 'shape' in q and q['shape'] and isinstance(q['shape'], dict):
        draw_geometry_shape(q['shape'])

    st.markdown(f"<p class='question-title'>Soru {idx + 1} {sub_badge}:\n\n{q['question']}</p>", unsafe_allow_html=True)

    options = q['options'] # Örn: {"A": "Seçenek 1", "B": "Seçenek 2", ...}
    option_keys = list(options.keys())

    # Daha önce bu soruya verilmiş bir cevap var mı kontrol edelim
    current_val = st.session_state.selected_answers.get(idx)
    
    # Eğer daha önce cevap verilmişse index'ini bulalım, verilmemişse None yapalım ki boş gelsin
    default_index = None
    if current_val in option_keys:
        default_index = option_keys.index(current_val)

    # st.radio içerisindeki key ile session_state çakışmasını önlemek için 
    # widget'ın kendi state'ini dikkatli yönetiyoruz:
    widget_key = f"q_{idx}"
    
    # Eğer widget state'i daha önce oluşmadıysa ve hafızada cevap varsa atayalım
    if widget_key not in st.session_state:
        if current_val in option_keys:
            st.session_state[widget_key] = current_val
        else:
            st.session_state[widget_key] = None

    def update_answer():
        selected = st.session_state.get(widget_key)
        if selected:
            st.session_state.selected_answers[idx] = selected

    choice = st.radio(
        f"**Soru {idx + 1} Şıkları:**",
        options=option_keys,
        index=default_index,
        format_func=lambda x: f"{x}) {options[x]}",
        key=widget_key,
        on_change=update_answer,
        placeholder="Bir şık seçiniz..." # Streamlit'in boş bırakabilmeyi destekleyen yapısı için
    )
    
    # Kullanıcı tıkladığında anında kaydet
    if choice:
        st.session_state.selected_answers[idx] = choice
        
    st.markdown(f"</div>", unsafe_allow_html=True)

    # Navigasyon Butonları
    st.markdown("<div class='nav-btn-container'>", unsafe_allow_html=True)
    nav_col1, nav_col2, nav_col3 = st.columns([1, 2, 1])
    with nav_col1:
        if st.session_state.current_page < total_questions - 1:
            if st.button("➡ Sonraki Soru"):
                st.session_state.current_page += 1
                st.rerun()
                
    with nav_col3:
        if st.session_state.current_page > 0:
            if st.button("⬅️ Önceki Soru"):
                st.session_state.current_page -= 1
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    if st.button("🏁 Deneme Sınavını Tamamla ve Sonuçları Gör"):
        correct_count, wrong_count = 0, 0
        for i, q_item in enumerate(st.session_state.questions):
            if st.session_state.selected_answers.get(i) == q_item['answer']:
                correct_count += 1
            else:
                wrong_count += 1

        score = (correct_count / total_questions) * 100
        st.balloons()
        st.success("🎉 Deneme sınavı başarıyla tamamlandı!")
        
        res_col1, res_col2, res_col3 = st.columns(3)
        res_col1.metric("✅ Doğru Sayısı", correct_count)
        res_col2.metric("❌ Yanlış Sayısı", wrong_count)
        res_col3.metric("🎯 Genel Başarı Puanı", f"{score:.1f} Puan")

        with st.expander("📖 Detaylı Soru Çözüm, Cevap Anahtarı ve Tüm Şıkları İncele", expanded=True):
            for i, q_item in enumerate(st.session_state.questions):
                u_ans = st.session_state.selected_answers.get(i, "Boş")
                c_ans = q_item['answer']
                status_icon = "✅" if u_ans == c_ans else "❌"
                st.markdown(f"**Soru {i+1} [{q_item.get('subject', '')}]:** {status_icon} (Sizin Cevabınız: **{u_ans}** | Doğru Cevap: **{c_ans}**)")
