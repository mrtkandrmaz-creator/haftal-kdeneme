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

# Modern UI ve Özel CSS Stilleri (Daha Uzatılmış / Büyük Butonlar ve Sabit Boyutlar)
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    
    /* Çok Daha Uzun, Geniş ve Ultra Modern Soru Üret Butonu */
    div.stButton > button:first-child {
        width: 100%;
        border-radius: 18px;
        font-weight: 900;
        font-size: 1.35rem;
        padding: 1.4rem 1.8rem;
        background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
        color: white;
        border: none;
        box-shadow: 0 10px 25px -4px rgba(249, 115, 22, 0.45);
        transition: all 0.3s ease;
        letter-spacing: 0.8px;
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 30px -6px rgba(249, 115, 22, 0.65);
        background: linear-gradient(135deg, #fb923c 0%, #f97316 100%);
    }
    
    .nav-btn-container div.stButton > button:first-child {
        font-size: 1.2rem !important;
        padding: 1rem 1.4rem !important;
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
        background: #f0f9ff;
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
    .solution-box {
        background: #f8fafc;
        border: 1px solid #cbd5e1;
        border-left: 4px solid #10b981;
        padding: 1.2rem;
        border-radius: 8px;
        margin-top: 1rem;
        margin-bottom: 1.2rem;
        color: #1e293b;
        line-height: 1.6;
    }
    .info-display-box {
        background: white;
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 0 15px 35px -5px rgba(0,0,0,0.08);
        border: 1px solid #e2e8f0;
        text-align: center;
        margin-top: 2rem;
    }
    
    /* Kusursuz, İdeal Boyutlu ve Modern Tablo Stili */
    .custom-table-container {
        max-width: 100%;
        overflow-x: auto;
        margin: 15px 0;
        border-radius: 12px;
        box-shadow: 0 4px 15px -3px rgba(2, 132, 199, 0.12);
        border: 1px solid #bae6fd;
    }
    .custom-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 0.95rem;
        background-color: #ffffff;
        text-align: left;
    }
    .custom-table th {
        background: linear-gradient(135deg, #0284c7 0%, #2563eb 100%);
        color: white;
        padding: 12px 16px;
        font-weight: 700;
        border-bottom: 3px solid #0284c7;
    }
    .custom-table td {
        padding: 10px 16px;
        border-bottom: 1px solid #e0f2fe;
        color: #1e293b;
    }
    .custom-table tr:last-child td {
        border-bottom: none;
    }
    .custom-table tr:nth-child(even) {
        background-color: #f0f9ff;
    }
    .custom-table tr:hover {
        background-color: #e0f2fe;
    }
    </style>
""", unsafe_allow_html=True)

# Görsel ve Tablo İşleme Motoru (Boyut Sorunları Giderilmiş)
def draw_geometry_shape(shape_data):
    if not isinstance(shape_data, dict):
        return
        
    st_type = str(shape_data.get("type", "")).strip().lower()
    if not st_type:
        return

    # Modern ve Boyut Kısıtlamalı Tablo Motoru
    if st_type in ["table", "line_chart"]:
        headers = shape_data.get("headers", ["Kategori / Zaman", "Değer"])
        rows = shape_data.get("rows", [])
        if not rows and "labels" in shape_data and "values" in shape_data:
            rows = [[str(l), str(v)] for l, v in zip(shape_data.get("labels", []), shape_data.get("values", []))]
        if not rows:
            rows = [["Örnek 1", "10"], ["Örnek 2", "20"]]
        title = str(shape_data.get("title", "Veri ve Değer Tablosu"))
        
        st.markdown(f"<p style='font-weight: 700; color: #0284c7; margin-bottom: 0.4rem; font-size: 1.05rem;'>📊 {title}</p>", unsafe_allow_html=True)
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

    # Kompakt Matplotlib Görsel Motoru (Sabit ve Taşma Yapmayan Boyutlar)
    fig, ax = plt.subplots(figsize=(3.2, 2.2), dpi=150)
    ax.set_aspect('equal')
    ax.axis('off')
    
    try:
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
                ax.plot([0, 0.35, 0.35, 0], [0, 0, 0.35, 0.35], color='#0284c7', linewidth=1.5)
            elif sub_type == "equilateral":
                h = np.sqrt(3) / 2 * 4
                pts = np.array([[0, 0], [4, 0], [2, h]])
            else:
                pts = np.array([[0, 0], [5, 0], [2, 4.2]])
                
            triangle = plt.Polygon(pts, closed=True, facecolor='#f0f9ff', edgecolor='#0284c7', linewidth=2.0)
            ax.add_patch(triangle)
            
            offsets = [[-0.5, -0.5], [0.4, -0.5], [0, 0.35]]
            labels = [b_label, c_label, a_label]
            for i, p in enumerate(pts):
                ax.text(p[0] + offsets[i][0], p[1] + offsets[i][1], labels[i], fontsize=9, fontweight='bold', color='#1e293b')
            
            if side_ab:
                ax.text(-0.8, 1.5, f"AB: {side_ab}", fontsize=7, color='#2563eb', fontweight='bold', ha='right')
            if side_bc:
                ax.text(2.5, -0.7, f"BC: {side_bc}", fontsize=7, color='#2563eb', fontweight='bold', ha='center')
            if side_ac:
                ax.text(2.8, 2.3, f"AC: {side_ac}", fontsize=7, color='#2563eb', fontweight='bold')
            if angle_a:
                ax.text(2.0, 3.8, f"Â={angle_a}", fontsize=7, color='#ea580c', fontweight='bold', ha='center')
                
            ax.set_xlim(-3.5, 7.5)
            ax.set_ylim(-2.5, 5.8)

        elif st_type == "circle":
            center_label = str(shape_data.get("center", "O"))
            radius_val_str = str(shape_data.get("radius", "5 cm"))
            show_diameter = bool(shape_data.get("show_diameter", False))
            chord = str(shape_data.get("chord", ""))
            
            r_num = 2.1
            circle = plt.Circle((0, 0), r_num, facecolor='#f0f9ff', edgecolor='#0284c7', linewidth=2.0)
            ax.add_patch(circle)
            ax.plot(0, 0, 'o', color='#ea580c', markersize=5)
            ax.text(0.18, -0.38, center_label, fontsize=9, fontweight='bold', color='#ea580c')
            
            if show_diameter:
                ax.plot([-r_num, r_num], [0, 0], linestyle='--', color='#94a3b8', linewidth=1.3)
                ax.text(0, 0.25, f"Çap: {radius_val_str}", fontsize=7.5, fontweight='bold', color='#2563eb', ha='center')
            else:
                ax.plot([0, r_num], [0, 0], color='#2563eb', linewidth=1.8)
                display_r = "5 cm" if ("10" in radius_val_str or "10" in chord) else radius_val_str
                ax.text(r_num/2, 0.2, f"r = {display_r}", fontsize=7.5, fontweight='bold', color='#2563eb')
                
            if chord:
                ax.plot([-1.8, 1.8], [-1.3, -1.3], color='#10b981', linewidth=1.8)
                ax.text(0, -1.75, f"Kiriş: {chord}", fontsize=7.5, fontweight='bold', color='#10b981', ha='center')
                
            ax.set_xlim(-3.0, 3.0)
            ax.set_ylim(-3.0, 3.0)

        elif st_type in ["bar_chart", "science_chart"]:
            labels = shape_data.get("labels", ["A", "B", "C", "D"])
            values = shape_data.get("values", [10, 25, 15, 30])
            title = str(shape_data.get("title", "Veri Analizi"))
            
            clean_vals = [float(v) if str(v).replace('.','',1).isdigit() else 10.0 for v in values]
            colors = ['#0284c7', '#2563eb', '#06b6d4', '#3b82f6']
            bar_colors = [colors[i % len(colors)] for i in range(len(labels))]
            
            bars = ax.bar(labels, clean_vals, color=bar_colors, width=0.5, edgecolor='#1e293b', linewidth=1.0, alpha=0.95)
            ax.set_title(title, fontsize=9.5, fontweight='bold', color='#1e293b', pad=15)
            
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_color('#cbd5e1')
            ax.spines['bottom'].set_color('#cbd5e1')
            
            max_val = max(clean_vals) if clean_vals else 10
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + (max_val * 0.04), f'{height:g}',
                        ha='center', va='bottom', fontsize=7.5, fontweight='bold', color='#1e293b')
            
            ax.set_ylim(0, max_val * 1.3)
            ax.set_xlim(-0.8, len(labels) - 0.2)

        elif st_type in ["science_space", "space_orbit", "eclipse", "moon_phases"]:
            sub_sub = str(shape_data.get("sub_type", "orbit")).strip().lower()
            title = str(shape_data.get("title", "Fen Bilimleri Şeması"))
            
            if sub_sub == "moon_phases":
                sun_indicator = plt.Circle((-3.5, 0), 0.5, facecolor='#f59e0b', edgecolor='#d97706', linewidth=1.0)
                ax.add_patch(sun_indicator)
                ax.text(-3.5, -0.8, "Güneş", fontsize=6.5, fontweight='bold', color='#d97706', ha='center')
                
                earth_center = plt.Circle((0, 0), 0.6, facecolor='#0284c7', edgecolor='#0369a1', linewidth=1.2)
                ax.add_patch(earth_center)
                ax.text(0, -0.15, "Dünya", fontsize=7, fontweight='bold', color='white', ha='center', va='center')
                
                moon_positions = [
                    (0, 1.7, "Yeni Ay"), (1.7, 0, "İlk Dördün"),
                    (0, -1.7, "Dolunay"), (-1.7, 0, "Son Dördün")
                ]
                for mx, my, mlabel in moon_positions:
                    m_circle = plt.Circle((mx, my), 0.25, facecolor='#e2e8f0', edgecolor='#64748b', linewidth=0.8)
                    ax.add_patch(m_circle)
                    ax.text(mx, my - 0.55, mlabel, fontsize=6, fontweight='bold', color='#334155', ha='center')
                    
                ax.set_xlim(-4.2, 4.2)
                ax.set_ylim(-2.8, 2.8)
                
            elif sub_sub == "solar_eclipse":
                sun_p = plt.Circle((-2.5, 0), 0.7, facecolor='#f59e0b', edgecolor='#d97706', linewidth=1.2)
                ax.add_patch(sun_p)
                ax.text(-2.5, -0.9, "Güneş", fontsize=7, fontweight='bold', color='#d97706', ha='center')
                
                moon_p = plt.Circle((-0.7, 0), 0.22, facecolor='#e2e8f0', edgecolor='#64748b', linewidth=0.8)
                ax.add_patch(moon_p)
                ax.text(-0.7, -0.45, "Ay", fontsize=6.5, fontweight='bold', color='#64748b', ha='center')
                
                earth_p = plt.Circle((1.5, 0), 0.5, facecolor='#0284c7', edgecolor='#0369a1', linewidth=1.2)
                ax.add_patch(earth_p)
                ax.text(1.5, -0.75, "Dünya", fontsize=7, fontweight='bold', color='#0284c7', ha='center')
                
                ax.set_xlim(-3.6, 2.8)
                ax.set_ylim(-1.8, 1.8)
                
            elif sub_sub == "lunar_eclipse":
                sun_p = plt.Circle((-2.5, 0), 0.7, facecolor='#f59e0b', edgecolor='#d97706', linewidth=1.2)
                ax.add_patch(sun_p)
                ax.text(-2.5, -0.9, "Güneş", fontsize=7, fontweight='bold', color='#d97706', ha='center')
                
                earth_p = plt.Circle((-0.5, 0), 0.5, facecolor='#0284c7', edgecolor='#0369a1', linewidth=1.2)
                ax.add_patch(earth_p)
                ax.text(-0.5, -0.75, "Dünya", fontsize=7, fontweight='bold', color='#0284c7', ha='center')
                
                moon_p = plt.Circle((1.5, 0), 0.22, facecolor='#e2e8f0', edgecolor='#64748b', linewidth=0.8)
                ax.add_patch(moon_p)
                ax.text(1.5, -0.45, "Ay", fontsize=6.5, fontweight='bold', color='#64748b', ha='center')
                
                ax.set_xlim(-3.6, 2.8)
                ax.set_ylim(-1.8, 1.8)
                
            else:
                sun = plt.Circle((-2.0, 0), 0.7, facecolor='#f59e0b', edgecolor='#d97706', linewidth=1.2)
                ax.add_patch(sun)
                ax.text(-2.0, -1.0, "Güneş", fontsize=7, fontweight='bold', color='#f59e0b', ha='center')
                
                orbit = plt.Circle((0, 0), 2.0, fill=False, edgecolor='#94a3b8', linestyle='--', linewidth=1.0)
                ax.add_patch(orbit)
                
                earth = plt.Circle((2.0, 0), 0.35, facecolor='#0284c7', edgecolor='#0369a1', linewidth=1.0)
                ax.add_patch(earth)
                ax.text(2.0, -0.6, "Dünya", fontsize=7, fontweight='bold', color='#0284c7', ha='center')
                
                ax.set_xlim(-3.5, 3.2)
                ax.set_ylim(-2.2, 2.2)

            ax.set_title(title, fontsize=9.5, fontweight='bold', color='#1e293b', pad=15)

        plt.tight_layout()
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', dpi=180)
        buf.seek(0)
        st.image(buf, width=280)
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
if "is_generating" not in st.session_state:
    st.session_state.is_generating = False

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
st.sidebar.markdown("### 🔍 Manuel Özel Ünite / Konu Ekleme")

def update_custom_topic():
    st.session_state.custom_topic_input = st.session_state.widget_custom_topic

st.sidebar.text_input(
    "Özel Ünite / İçerik (Opsiyonel)",
    value=st.session_state.custom_topic_input,
    key="widget_custom_topic",
    on_change=update_custom_topic,
    placeholder="Örn: Açılar, Hücre, Paragraf...",
    help="Buraya yazdığınız ünite/konu ilgili dersin kazanımlarıyla eşit şekilde paylaştırılır."
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

# Uzatılmış ve Büyük Soru Üret Butonu
generate_btn = st.sidebar.button("🎯 SORULARI ÜRET")

# Ana Ekran Başlığı
st.markdown(f"<h1 style='text-align: center; color: #1e293b; font-weight: 900;'>🎯 {selected_grade} 80 Soruluk Deneme Paneli</h1>", unsafe_allow_html=True)
custom_info_str = f" | Manuel Ekleme Odak Ünitesi: <b>{st.session_state.custom_topic_input}</b>" if st.session_state.custom_topic_input.strip() else ""
st.markdown(f"<p style='text-align: center; color: #64748b; font-size: 1.1rem;'>Seçilen Kapsam: <b>{selected_scope}</b>{custom_info_str} | Zorluk Kademesi: <b>{difficulty_level}</b></p>", unsafe_allow_html=True)
st.markdown("---")

def call_groq_with_key(api_key, prompt_text):
    from groq import Groq
    client = Groq(api_key=api_key)
    completion = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": "Sen MEB müfredatı soru hazırlama uzmanısın. Paragraf, tablo ve fen bilimleri grafik/şema sorularında asla kesinti yapmazsın."},
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

# Soru Üretim Tetikleyicisi
if generate_btn:
    st.session_state.is_generating = True

# Üretim Yapılırken Sağ Ekranda Ünite/Ders Detayları Bilgisi ve Sol Sidebar'da Spinner
if st.session_state.is_generating:
    with st.sidebar:
        st.info("🔄 Yapay zeka havuzu aktif: Sorular, veriler ve çözümler üretiliyor...")
        
    st.markdown(
        f"""
        <div class='info-display-box'>
            <h2 style='color: #0284c7; margin-bottom: 1rem;'>🚀 Deneme Sınavı Hazırlanıyor...</h2>
            <p style='font-size: 1.15rem; color: #334155; line-height: 1.8;'>
                Seçmiş olduğunuz <b>{selected_grade}</b> seviyesi ve <b>{selected_scope}</b> kapsamındaki MEB resmi kazanımları taranıyor.<br><br>
                <b>📚 Denemede Yer Alan Dersler ve Üniteler:</b><br>
                • <b>Türkçe (14 Soru):</b> Sözcükte Anlam, Paragraf, Sözel Mantık, Dil Bilgisi<br>
                • <b>Matematik (14 Soru):</b> Geometri, Üçgenler, Çember, Veri Analizi ve Tablo Yorumlama<br>
                • <b>Fen Bilimleri (14 Soru):</b> Güneş, Dünya ve Ay, Evreler, Tutulmalar, Kuvvet ve Hareket<br>
                • <b>Sosyal Bilgiler (14 Soru):</b> Tarih, Coğrafya, Harita Okuma ve Haklar<br>
                • <b>Din Kültürü ve Ahlak Bilgisi (12 Soru):</b> Ayet/Hadis Yorumlama ve Değerler Eğitimi<br>
                • <b>İngilizce (12 Soru):</b> Diyalog Tamamlama, Kelime ve Tablo Eşleştirme<br><br>
                Toplam 80 adet yeni nesil soru, şema ve detaylı çözüm açıklamaları derlenmektedir. Lütfen bekleyiniz...
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    current_topic_val = st.session_state.custom_topic_input
    if current_topic_val.strip():
        custom_prompt_addon = (
            f"\n\n🚨 MANUEL ÖZEL ÜNİTE / KONU EKLENDİ: '{current_topic_val}'\n"
            f"TALİMAT: Bu girdiğin üniteyi ilgili dersin kazanımlarıyla eşit şekilde paylaştırarak sorulara yansıt."
        )
    else:
        custom_prompt_addon = ""

    prompt = (
        f"Türkiye Cumhuriyeti Millî Eğitim Bakanlığı (MEB) {selected_grade} {term} dönemi resmi öğretim programı "
        f"ve '{selected_scope}' kapsamındaki resmi kazanımlara tam uygun olarak toplam KESİNLİKLE VE EKSİKSİZ olarak tam 80 adet yeni nesil soru hazırla."
        f"{custom_prompt_addon}\n\n"
        f"ZORLUK KADEMESİ VE KALİTE KRİTERİ: '{difficulty_level}'.\n\n"
        "DERS DAĞILIMI VE KESİN SORU SAYILARI VE İÇERİK KURALLARI (TOPLAM TAM 80 SORU):\n"
        "1. Türkçe: 14 Soru (1-14 arası) - Sözel mantık, paragrafta anlam, uzun metinler, dil bilgisi, görsel okuma. Metinleri ASLA KISALTMA, tam yaz.\n"
        "2. Matematik: 14 Soru (15-28 arası) - Geometri, açılar, üçgenler, çember, veri analizi, tablo gösterimleri, oran-orantı, problemler. Çizgi grafiklerini ASLA KULLANMA; tüm verileri ve trendleri 'table' formatında göster. Örneğin dondurma satış tablosu gibi veri tablolarını soru yapısına dahil et. Çember sorularında çap ve yarıçap ilişkisinde (Örn: Çap 10 cm ise yarıçap 5 cm olarak) metin ile görselin birebir uyuşmasına dikkat et.\n"
        "3. Fen Bilimleri: 14 Soru (29-42 arası) - Kuvvet ve hareket, Güneş/Dünya/Ay hareketleri, evreler, tutulmalar, hücre, maddeler. Konuya göre 'moon_phases', 'solar_eclipse', 'lunar_eclipse' veya yörünge şemalarından en uygununu seç.\n"
        "4. Sosyal Bilgiler: 14 Soru (43-56 arası) - Tarih, coğrafya, harita okuma, kültürel miras, hak ve sorumluluklar.\n"
        "5. Din Kültürü ve Ahlak Bilgisi: 12 Soru (57-68 arası) - Ayet ve hadis yorumlama, İslam kültürü, değerler eğitimi.\n"
        "6. İngilizce (English): 12 Soru (69-80 arası) - Diyalog tamamlama, kartlar, tablo eşleştirme, kelime bilgisi.\n\n"
        "🚨 KESİN GÖRSEL VE ŞEMA KURALLARI (`shape` nesnesi):\n"
        "- Üçgen için: {\"type\": \"triangle\", \"sub_type\": \"right/scalene/equilateral\", \"A\": \"A\", \"B\": \"B\", \"C\": \"C\", \"side_ab\": \"...\", \"angle_a\": \"...\"}\n"
        "- Çember için: {\"type\": \"circle\", \"center\": \"O\", \"radius\": \"5 cm\", \"show_diameter\": true}\n"
        "- Çubuk Grafik için: {\"type\": \"bar_chart\", \"labels\": [\"A\", \"B\", \"C\", \"D\"], \"values\": [10, 25, 15, 30], \"title\": \"Grafik Başlığı\"}\n"
        "- Tablo için: {\"type\": \"table\", \"title\": \"Tablo Başlığı\", \"headers\": [\"Gün\", \"Adet\"], \"rows\": [[\"Pazartesi\", \"12\"], [\"Salı\", \"15\"]]}\n"
        "- Fen / Uzay için: {\"type\": \"science_space\", \"sub_type\": \"moon_phases\", \"title\": \"Sistem Şeması\"}\n"
        "Her sorunun 4 şıkkı (A, B, C, D), doğru cevabı (`answer`) ve neden doğru olduğunu açıklayan detaylı çözüm adımları (`explanation`) olmalıdır. 'subject' alanına ilgili dersin adını tam yaz.\n"
        "Çıktıyı KESİNLİKLE aşağıdaki JSON formatında ver, başka hiçbir açıklama ekleme:\n"
        "{\n"
        "    \"questions\": [\n"
        "        {\n"
        "            \"id\": 1,\n"
        "            \"subject\": \"Matematik\",\n"
        "            \"passage\": \"Metin veya paragraf içeriği burada eksiksiz yer alacak...\",\n"
        "            \"question\": \"Soru metni...\",\n"
        "            \"shape\": {\"type\": \"table\", \"title\": \"Dondurma Satış Tablosu\", \"headers\": [\"Gün\", \"Adet\"], \"rows\": [[\"Pazartesi\", \"12\"], [\"Salı\", \"15\"]]},\n"
        "            \"options\": {\n"
        "                \"A\": \"A şıkkı\",\n"
        "                \"B\": \"B şıkkı\",\n"
        "                \"C\": \"C şıkkı\",\n"
        "                \"D\": \"D şıkkı\"\n"
        "            },\n"
        "            \"answer\": \"A\",\n"
        "            \"explanation\": \"Doğru cevap A şıkkıdır çünkü... (detaylı çözüm açıklaması)\"\n"
        "        }\n"
        "    ]\n"
        "}"
    )
    
    raw_json, error_message = multi_pool_generate(prompt)
    st.session_state.is_generating = False
    
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
if st.session_state.quiz_ready and not st.session_state.quiz_started and not st.session_state.is_generating:
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

    options = q['options']
    
    current_val = st.session_state.selected_answers.get(idx)
    default_index = None
    if current_val in list(options.keys()):
        default_index = list(options.keys()).index(current_val)

    choice = st.radio(
        f"**Soru {idx + 1} Şıkları:**",
        options=list(options.keys()),
        index=default_index,
        format_func=lambda x: f"{x}) {options[x]}",
        key=f"q_{idx}"
    )
    if choice:
        st.session_state.selected_answers[idx] = choice
        
    st.markdown(f"</div>", unsafe_allow_html=True)

    # Navigasyon Butonları
    st.markdown("<div class='nav-btn-container'>", unsafe_allow_html=True)
    nav_col1, nav_col2, nav_col3 = st.columns([1, 2, 1])
    with nav_col1:
        if st.session_state.current_page > 0:
            if st.button("⬅ Önceki Soru"):
                st.session_state.current_page -= 1
                st.rerun()
    with nav_col3:
        if st.session_state.current_page < total_questions - 1:
            if st.button("➡ Sonraki Soru"):
                st.session_state.current_page += 1
                st.rerun()
        else:
            if st.button("🏁 Sınavı Tamamla"):
                st.session_state.quiz_started = False
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# Sonuç ve Karne Ekranı (Detaylı Doğru Şık ve Çözüm Gerekçeleri İle)
elif not st.session_state.quiz_started and st.session_state.quiz_ready and not st.session_state.is_generating:
    st.markdown("---")
    st.markdown("<h2 style='text-align: center; color: #1e293b;'>📊 Sınav Sonuç ve Detaylı Karne Raporu</h2>", unsafe_allow_html=True)
    
    correct_count = 0
    wrong_count = 0
    empty_count = 0
    
    for i, q in enumerate(st.session_state.questions):
        user_ans = st.session_state.selected_answers.get(i)
        correct_ans = str(q.get("answer", "")).strip().upper()
        if not user_ans:
            empty_count += 1
        elif user_ans.strip().upper() == correct_ans:
            correct_count += 1
        else:
            wrong_count += 1
            
    total_q = len(st.session_state.questions)
    net_score = correct_count - (wrong_count * 0.25)
    success_percent = (correct_count / total_q) * 100 if total_q > 0 else 0
    
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Toplam Soru", total_q)
    m2.metric("Doğru", correct_count, delta_color="normal")
    m3.metric("Yanlış", wrong_count, delta_color="inverse")
    m4.metric("Boş", empty_count)
    m5.metric("Başarı Oranı", f"%{success_percent:.1f}")
    
    st.markdown("---")
    st.markdown("### 📝 Soru Çözümleri, Doğru Yanıt Analizi ve Gerekçeler")
    
    for i, q in enumerate(st.session_state.questions):
        user_ans = st.session_state.selected_answers.get(i, "Boş")
        correct_ans = str(q.get("answer", "")).strip().upper()
        is_correct = (user_ans.strip().upper() == correct_ans) if user_ans != "Boş" else False
        
        status_icon = "✅" if is_correct else ("❌" if user_ans != "Boş" else "⚠️")
        explanation_text = q.get('explanation', f"Doğru seçenek <b>{correct_ans}</b> şıkkıdır. Bu soruda MEB kazanımları çerçevesinde temel kavramlar ve mantıksal işlem adımları uygulanarak doğru sonuca ulaşılmıştır.")
        
        with st.expander(f"{status_icon} Soru {i+1} [{q.get('subject', 'Genel')}] - Sizin Cevabınız: {user_ans} | Doğru Cevap: {correct_ans}"):
            st.markdown(f"**Soru Metni:** {q['question']}")
            options = q.get('options', {})
            for opt_key, opt_val in options.items():
                prefix = "👉 " if opt_key == correct_ans else "   "
                st.markdown(f"{prefix}**{opt_key})** {opt_val}")
            
            st.markdown(f"""
                <div class='solution-box'>
                    <b>💡 Doğru Cevap ve Detaylı Gerekçeli Çözüm:</b><br>
                    Doğru Yanıt: <b>{correct_ans}</b><br><br>
                    <b>Neden Doğru / Çözüm Analizi:</b><br>
                    {explanation_text}
                </div>
            """, unsafe_allow_html=True)
            
    st.markdown("---")
    if st.button("🔄 Yeni Sınav Başlat / Başa Dön"):
        st.session_state.quiz_ready = False
        st.session_state.quiz_started = False
        st.session_state.questions = []
        st.session_state.selected_answers = {}
        st.session_state.current_page = 0
        st.rerun()
