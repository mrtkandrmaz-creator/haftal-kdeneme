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
    .solution-box {
        background: #f8fafc;
        border: 1px solid #cbd5e1;
        border-left: 4px solid #10b981;
        padding: 1rem;
        border-radius: 6px;
        margin-top: 0.8rem;
        margin-bottom: 1.2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Gelişmiş Dinamik Görselleştirme ve Şema Motoru (Üst üste binmeleri önleyen optimize edilmiş sürüm)
def draw_geometry_shape(shape_data):
    if not isinstance(shape_data, dict):
        return
        
    st_type = str(shape_data.get("type", "")).strip().lower()
    if not st_type:
        return

    fig, ax = plt.subplots(figsize=(5.5, 4.2))
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
                ax.text(p[0] + offsets[i][0], p[1] + offsets[i][1], labels[i], fontsize=11, fontweight='bold', color='#1e293b')
            
            if side_ab:
                ax.text(-0.8, 1.5, f"AB: {side_ab}", fontsize=8.5, color='#0284c7', fontweight='bold', ha='right')
            if side_bc:
                ax.text(2.5, -0.7, f"BC: {side_bc}", fontsize=8.5, color='#0284c7', fontweight='bold', ha='center')
            if side_ac:
                ax.text(2.8, 2.3, f"AC: {side_ac}", fontsize=8.5, color='#0284c7', fontweight='bold')
            if angle_a:
                ax.text(2.0, 3.8, f"Â={angle_a}", fontsize=8.5, color='#ea580c', fontweight='bold', ha='center')
                
            ax.set_xlim(-2.5, 6.8)
            ax.set_ylim(-2.0, 5.5)

        # 2. ÇEMBER VE DAİRE
        elif st_type == "circle":
            center_label = str(shape_data.get("center", "O"))
            radius_label = str(shape_data.get("radius", "r"))
            show_diameter = bool(shape_data.get("show_diameter", False))
            chord = str(shape_data.get("chord", ""))
            
            circle = plt.Circle((0, 0), 2.2, facecolor='#f8fafc', edgecolor='#1e293b', linewidth=2)
            ax.add_patch(circle)
            ax.plot(0, 0, 'o', color='#ea580c', markersize=6)
            ax.text(0.18, -0.38, center_label, fontsize=11, fontweight='bold', color='#ea580c')
            
            if show_diameter:
                ax.plot([-2.2, 2.2], [0, 0], linestyle='--', color='#94a3b8', linewidth=1.4)
                ax.text(0, 0.25, f"Çap: {radius_label}", fontsize=9, fontweight='bold', color='#0284c7', ha='center')
            else:
                ax.plot([0, 2.2], [0, 0], color='#0284c7', linewidth=1.8)
                ax.text(1.1, 0.2, f"r = {radius_label}", fontsize=9, fontweight='bold', color='#0284c7')
                
            if chord:
                ax.plot([-1.8, 1.8], [-1.3, -1.3], color='#10b981', linewidth=1.8)
                ax.text(0, -1.75, f"Kiriş: {chord}", fontsize=9, fontweight='bold', color='#10b981', ha='center')
                
            ax.set_xlim(-3.5, 3.5)
            ax.set_ylim(-3.5, 3.5)

        # 3. SÜTUN / MATEMATİK & FEN GRAFİĞİ (Üst marjlar ve eksen payları optimize edildi)
        elif st_type in ["bar_chart", "science_chart"]:
            labels = shape_data.get("labels", ["A", "B", "C", "D"])
            values = shape_data.get("values", [10, 25, 15, 30])
            title = str(shape_data.get("title", "Veri ve Grafik Analizi"))
            
            clean_vals = [float(v) if str(v).replace('.','',1).isdigit() else 10.0 for v in values]
            bars = ax.bar(labels, clean_vals, color='#0284c7', width=0.45, edgecolor='#1e293b', linewidth=1)
            
            ax.set_title(title, fontsize=11, fontweight='bold', color='#1e293b', pad=22)
            
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_color('#cbd5e1')
            ax.spines['bottom'].set_color('#cbd5e1')
            
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + (max(clean_vals)*0.06), f'{height:g}',
                        ha='center', va='bottom', fontsize=9.5, fontweight='bold', color='#1e293b')
            
            max_y = max(clean_vals) if clean_vals else 10
            ax.set_ylim(0, max_y * 1.65)
            ax.set_xlim(-0.8, len(labels)-0.2)

        # 4. FEN BİLİMLERİ / UZAY / KUVVET ŞEMASI
        elif st_type in ["science_space", "space_orbit", "eclipse", "physics_force"]:
            title = str(shape_data.get("title", "Fen Bilimleri Sistem Şeması"))
            
            sun = plt.Circle((-2.2, 0), 0.85, facecolor='#f59e0b', edgecolor='#d97706', linewidth=1.5)
            ax.add_patch(sun)
            ax.text(-2.2, -1.4, "Kaynak / Odak", fontsize=8.5, fontweight='bold', color='#d97706', ha='center')
            
            orbit = plt.Circle((0, 0), 2.0, fill=False, edgecolor='#94a3b8', linestyle='--', linewidth=1)
            ax.add_patch(orbit)
            
            earth = plt.Circle((0, 0), 0.45, facecolor='#0284c7', edgecolor='#0369a1', linewidth=1.5)
            ax.add_patch(earth)
            ax.text(0, -0.8, "Cisim 1", fontsize=8.5, fontweight='bold', color='#0284c7', ha='center')
            
            moon = plt.Circle((1.4, 1.4), 0.2, facecolor='#cbd5e1', edgecolor='#64748b', linewidth=1)
            ax.add_patch(moon)
            ax.text(1.4, 1.9, "Cisim 2", fontsize=8, fontweight='bold', color='#64748b', ha='center')
            
            ax.set_title(title, fontsize=11, fontweight='bold', color='#1e293b', pad=22)
            ax.set_xlim(-4.0, 3.5)
            ax.set_ylim(-2.8, 2.8)

        plt.tight_layout()
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', dpi=180)
        buf.seek(0)
        st.image(buf, width=420)
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
            {"role": "system", "content": "Sen MEB müfredatı soru hazırlama uzmanısın. Paragraf, metin ve fen bilimleri grafik sorularında asla kesinti yapmaz, eksiksiz üretirsin."},
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
    
    with st.spinner(f"✨ Çoklu API havuzu taranıyor: {selected_grade} için eksiksiz metinler ve optimize edilmiş fen grafik şemalarıyla 80 soru hazırlanıyor..."):
        prompt = (
            f"Türkiye Cumhuriyeti Millî Eğitim Bakanlığı (MEB) {selected_grade} {term} dönemi resmi öğretim programı "
            f"ve '{selected_scope}' kapsamındaki gerçek haftalık kazanımlarına tam uygun olarak toplam KESİNLİKLE VE EKSİKSİZ olarak tam 80 adet yeni nesil soru hazırla."
            f"{custom_prompt_addon}\n\n"
            f"ZORLUK KADEMESİ VE KALİTE KRİTERİ: '{difficulty_level}'.\n\n"
            "DERS DAĞILIMI VE KESİN SORU SAYILARI VE İÇERİK KURALLARI (TOPLAM TAM 80 SORU):\n"
            "1. Türkçe: 15 Soru (1-15 arası) - Kesinlikle Türkçe dersine ait (Sözel mantık, paragrafta anlam, uzun metinler, dil bilgisi, görsel okuma, deyimler/atasözleri). Metinleri ASLA KISALTMA, eksiksiz tam yaz.\n"
            "2. Matematik: 15 Soru (16-30 arası) - Kesinlikle Matematik dersine ait (Geometri, açılar, üçgenler, çember, veri analizi, oran-orantı, problemler). Geometri ve veri sorularında mutlaka 'shape' json objesi ile şema görseli ekle.\n"
            "3. Fen Bilimleri: 15 Soru (31-45 arası) - Kesinlikle Fen Bilimleri dersine ait (Kuvvet ve hareket, Güneş/Dünya/Ay, hücre, maddeler, elektrik devreleri, ekosistem). Grafik ve deney şemaları için mutlaka 'shape' json objesi kullan.\n"
            "4. Sosyal Bilgiler: 15 Soru (46-60 arası) - Kesinlikle Sosyal Bilgiler dersine ait (Tarih, coğrafya, harita okuma, kültürel miras, hak ve sorumluluklar).\n"
            "5. Din Kültürü ve Ahlak Bilgisi: 10 Soru (61-70 arası) - Kesinlikle Din Kültürü dersine ait (Ayet ve hadis yorumlama, İslam kültürü, değerler eğitimi).\n"
            "6. İngilizce (English): 10 Soru (71-80 arası) - Kesinlikle İngilizce dersine ait (Diyalog tamamlama, kartlar, tablo eşleştirme, kelime bilgisi).\n\n"
            "🚨 KESİN GÖRSEL VE ŞEMA KURALLARI (`shape` nesnesi):\n"
            "Soruların matematik, fen ve bazı görsel okuma bölümlerinde 'shape' alanını boş bırakma; şemaya uygun parametreleri ekle:\n"
            "- Üçgen için: {\"type\": \"triangle\", \"sub_type\": \"right/scalene/equilateral\", \"A\": \"A\", \"B\": \"B\", \"C\": \"C\", \"side_ab\": \"...\", \"angle_a\": \"...\"}\n"
            "- Çember için: {\"type\": \"circle\", \"center\": \"O\", \"radius\": \"5 cm\", \"show_diameter\": true}\n"
            "- Grafik/Veri için: {\"type\": \"bar_chart\", \"labels\": [\"A\", \"B\", \"C\", \"D\"], \"values\": [10, 25, 15, 30], \"title\": \"Grafik Başlığı\"}\n"
            "- Fen/Sistem için: {\"type\": \"science_space\", \"title\": \"Deney / Sistem Şeması\"}\n"
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
                user_ans = st.session_state.selected_answers.get(i, "Boş")
                correct_ans = q_item['answer']
                status = "✅ Doğru" if user_ans == correct_ans else "❌ Yanlış / Boş"
                
                st.markdown(f"### Soru {i + 1} [{q_item.get('subject', '')}] — {status}")
                
                p_text = str(q_item.get('passage', '')).strip()
                if p_text and p_text.lower() != "null" and p_text != "":
                    st.markdown(f"**Metin / Öncül:** {p_text}")
                    
                if 'shape' in q_item and q_item['shape'] and isinstance(q_item['shape'], dict):
                    draw_geometry_shape(q_item['shape'])
                    
                st.markdown(f"**Soru Kökü:** {q_item['question']}")
                
                # Tüm Şıkları Listeleme
                st.markdown("**Tüm Şıklar:**")
                opts = q_item.get('options', {})
                for key_opt, text_opt in opts.items():
                    is_correct_marker = " 🎯 **(Doğru Cevap)**" if key_opt == correct_ans else ""
                    is_user_marker = " 👈 *(Sizin Cevabınız)*" if key_opt == user_ans else ""
                    st.markdown(f"- **{key_opt})** {text_opt}{is_correct_marker}{is_user_marker}")
                
                # Çözüm / Açıklama Alanı (Eğer model açıklama döndüyse gösterir, dönmediyse şık bazlı özet sunar)
                explanation = q_item.get('explanation', '')
                if explanation:
                    st.markdown(f"<div class='solution-box'>💡 <b>Çözüm Açıklaması:</b> {explanation}</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='solution-box'>💡 <b>Doğru Cevap:</b> {correct_ans} şıkkıdır. Sizin tercihiniz: <b>{user_ans}</b></div>", unsafe_allow_html=True)
                
                st.markdown("---")
