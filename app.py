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
        padding: 1rem 1.2rem;
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
    </style>
""", unsafe_allow_html=True)

# %100 Kararlı Matplotlib Tabanlı Çizim ve Görsel Motoru
def draw_geometry_shape(shape_data):
    if not isinstance(shape_data, dict):
        return
        
    st_type = str(shape_data.get("type", "")).strip().lower()
    if not st_type:
        return

    fig, ax = plt.subplots(figsize=(5, 4))
    ax.set_aspect('equal')
    ax.axis('off')
    
    try:
        # 1. ÜÇGEN ÇİZİMİ
        if st_type == "triangle":
            sub_type = str(shape_data.get("sub_type", "scalene")).strip().lower()
            a_label = str(shape_data.get("A", "A"))
            b_label = str(shape_data.get("B", "B"))
            c_label = str(shape_data.get("C", "C"))
            
            if sub_type == "right":
                pts = np.array([[0, 0], [4, 0], [0, 3]])
                ax.plot([0, 0.4, 0.4, 0], [0, 0, 0.4, 0.4], color='#1e293b', linewidth=1.5)
            elif sub_type == "equilateral":
                h = np.sqrt(3) / 2 * 4
                pts = np.array([[0, 0], [4, 0], [2, h]])
            else:
                pts = np.array([[0, 0], [5, 0], [2, 4]])
                
            triangle = plt.Polygon(pts, closed=True, facecolor='#f8fafc', edgecolor='#1e293b', linewidth=3)
            ax.add_patch(triangle)
            
            offsets = [[-0.3, -0.3], [0.2, -0.3], [0, 0.2]]
            labels = [b_label, c_label, a_label]
            for i, p in enumerate(pts):
                ax.text(p[0] + offsets[i][0], p[1] + offsets[i][1], labels[i], fontsize=13, fontweight='bold', color='#1e293b')
                
            ax.set_xlim(-1, 6)
            ax.set_ylim(-1, 5)

        # 2. ÇEMBER ÇİZİMİ
        elif st_type == "circle":
            center_label = str(shape_data.get("center", "O"))
            radius_label = str(shape_data.get("radius", "r"))
            show_diameter = bool(shape_data.get("show_diameter", False))
            
            circle = plt.Circle((0, 0), 3, facecolor='#f8fafc', edgecolor='#1e293b', linewidth=3)
            ax.add_patch(circle)
            ax.plot(0, 0, 'o', color='#ea580c', markersize=8)
            ax.text(0.2, -0.3, center_label, fontsize=13, fontweight='bold', color='#ea580c')
            
            if show_diameter:
                ax.plot([-3, 3], [0, 0], linestyle='--', color='#cbd5e1', linewidth=2)
            else:
                ax.plot([0, 3], [0, 0], color='#0284c7', linewidth=2.5)
                ax.text(1.5, 0.2, radius_label, fontsize=11, fontweight='bold', color='#0284c7')
                
            ax.set_xlim(-4, 4)
            ax.set_ylim(-4, 4)

        # 3. KARE VE DİKDÖRTGEN ÇİZİMİ
        elif st_type in ["square", "rectangle"]:
            title = str(shape_data.get("title", "Şekil"))
            w_label = str(shape_data.get("width", "w"))
            h_label = str(shape_data.get("height", "h"))
            is_sq = (st_type == "square")
            
            w, h_dim = (3, 3) if is_sq else (4, 2.5)
            rect = plt.Rectangle((-w/2, -h_dim/2), w, h_dim, facecolor='#f8fafc', edgecolor='#1e293b', linewidth=3)
            ax.add_patch(rect)
            
            ax.text(0, h_dim/2 + 0.3, w_label, fontsize=11, fontweight='bold', color='#ea580c', ha='center')
            ax.text(-w/2 - 0.5, 0, h_label, fontsize=11, fontweight='bold', color='#0284c7', va='center')
            ax.text(0, -h_dim/2 - 0.5, title, fontsize=11, fontweight='bold', color='#334155', ha='center')
            
            ax.set_xlim(-3.5, 3.5)
            ax.set_ylim(-3, 3)

        # 4. SÜTUN / ÇUBUK GRAFİK
        elif st_type in ["bar_chart", "science_chart"]:
            labels = shape_data.get("labels", ["A", "B", "C", "D"])
            values = shape_data.get("values", [10, 25, 15, 30])
            title = str(shape_data.get("title", "Grafik Analizi"))
            
            clean_vals = []
            for v in values:
                try:
                    clean_vals.append(float(v))
                except:
                    clean_vals.append(10.0)
                    
            bars = ax.bar(labels, clean_vals, color='#0284c7', width=0.55, edgecolor='#1e293b', linewidth=1.5)
            ax.set_title(title, fontsize=12, fontweight='bold', color='#1e293b', pad=10)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_color('#cbd5e1')
            ax.spines['bottom'].set_color('#cbd5e1')
            
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.5, f'{height:g}',
                        ha='center', va='bottom', fontsize=10, fontweight='bold', color='#1e293b')
            
            max_y = max(clean_vals) if clean_vals else 10
            ax.set_ylim(0, max_y * 1.25)

        # 5. FEN BİLİMLERİ TABLO / MATRİS
        elif st_type == "science_table":
            title = str(shape_data.get("title", "Deney Veri Tablosu"))
            headers = shape_data.get("headers", ["Grup", "Değişken 1", "Değişken 2"])
            rows = shape_data.get("rows", [["1. Grup", "Arttı", "Sabit"], ["2. Grup", "Azaldı", "Arttı"]])
            
            table_data = [headers] + rows
            table = ax.table(cellText=table_data, loc='center', cellLoc='center')
            table.auto_set_font_size(False)
            table.set_fontsize(10)
            table.scale(1, 1.6)
            
            for (row, col), cell in table.get_celld().items():
                if row == 0:
                    cell.set_facecolor('#0284c7')
                    cell.set_text_props(weight='bold', color='white')
                else:
                    cell.set_facecolor('#f8fafc')
                    cell.set_text_props(color='#334155')
                    
            ax.set_title(title, fontsize=12, fontweight='bold', color='#1e293b', pad=15)
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)

        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', dpi=150)
        buf.seek(0)
        st.image(buf, use_container_width=True)
        plt.close(fig)
    except Exception as e:
        plt.close(fig)
        st.info("📊 Grafik veya görsel veri işleniyor...")

# API Anahtarlarını Okuma
try:
    GROQ_KEYS = st.secrets["api_keys"].get("groq_keys", [])
    GEMINI_KEYS = st.secrets["api_keys"].get("gemini_keys", [])
except Exception:
    GROQ_KEYS = []
    GEMINI_KEYS = []

if not GROQ_KEYS and not GEMINI_KEYS:
    st.error("⚠️ `.streamlit/secrets.toml` dosyasında `groq_keys` veya `gemini_keys` bulunamadı!")
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
st.sidebar.markdown("### 🔍 Manuel Konu & Kazanım Ekle")
custom_topic_search = st.sidebar.text_input(
    "Özel Konu / Alt Başlık / Soru Kriteri",
    placeholder="Örn: Basınç, Hücre Bölünmesi, Çemberde Açılar...",
    help="Buraya yazacağınız özel konu veya detay, üretilecek 80 sorunun içeriğine doğrudan kılavuzluk edecektir."
)

difficulty_level = st.sidebar.selectbox(
    "📊 Soru Zorluk Derecesi",
    [
        "🎯 MEB Standart & Beceri Temelli (LGS İdeal Düzey)",
        "🔥 Güçlendirilmiş Orta / Seçici Düzey",
        "🚀 Üst Düzey Zor / LGS Seçici (Çok Aşamalı Muhakeme)",
        "⚡ Çok Zor / Olimpiyat & Beceri Odaklı"
    ]
)

question_count = 80

st.sidebar.markdown("---")
st.sidebar.markdown("### 🚀 Soru İşlemleri")
generate_btn = st.sidebar.button("Soruları Üret")

# Ana Ekran Başlığı
st.markdown(f"<h1 style='text-align: center; color: #1e293b; font-weight: 900;'>🎯 {selected_grade} 80 Soruluk Deneme Paneli</h1>", unsafe_allow_html=True)
custom_info_str = f" | Özel Konu/Kriter: <b>{custom_topic_search}</b>" if custom_topic_search.strip() else ""
st.markdown(f"<p style='text-align: center; color: #64748b; font-size: 1.1rem;'>Seçilen Kapsam: <b>{selected_scope}</b>{custom_info_str} | Zorluk Modu: <b>{difficulty_level}</b></p>", unsafe_allow_html=True)
st.markdown("---")

def call_groq_with_key(api_key, prompt_text):
    from groq import Groq
    client = Groq(api_key=api_key)
    completion = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": "Sen MEB müfredatı soru hazırlama uzmanısın. Fen Bilimleri, Matematik veya diğer derslerdeki grafikler, tablolar, üçgenler ve çemberler ASLA soru metninde ham kod veya metin olarak yazılamaz; KESİNLİKLE 'shape' JSON nesnesi olarak eksiksiz doldurulmalıdır."},
            {"role": "user", "content": prompt_text}
        ],
        temperature=0.7,
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
        return None, "Havuzda geçerli API anahtarı bulunamadı!"

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
    custom_prompt_addon = f"\nMANUEL EKLENEN ÖZEL KONU / KRİTER: {custom_topic_search}\n(Soruların hazırlanmasında bu özel konuya ve odak noktasına da ağırlık ver.)" if custom_topic_search.strip() else ""
    
    with st.spinner(f"✨ Çoklu API havuzu taranıyor: {selected_grade} için kararlı grafik, tablo ve şekil motoruyla tam 80 yeni nesil soru hazırlanıyor..."):
        prompt = (
            f"Türkiye Cumhuriyeti Millî Eğitim Bakanlığı (MEB) {selected_grade} {term} dönemi resmi öğretim programı "
            f"ve '{selected_scope}' kapsamındaki gerçek haftalık kazanımlarına tam uygun olarak toplam KESİNLİKLE VE EKSİKSİZ olarak tam 80 adet yeni nesil soru hazırla."
            f"{custom_prompt_addon}\n\n"
            f"ZORLUK SEVİYESİ VE KALİTE TALİMATI: '{difficulty_level}'.\n\n"
            "DERS DAĞILIMI VE KESİN SORU SAYILARI (TOPLAM TAM 80 SORU):\n"
            "1. Türkçe: 15 Soru (1-15 arası)\n"
            "2. Matematik: 15 Soru (16-30 arası)\n"
            "3. Fen Bilimleri: 15 Soru (31-45 arası) - Fen bilimlerindeki tüm deneyler, sütun grafikler ve veri tabloları KESİNLİKLE 'shape' alanı içinde bar_chart, science_chart veya science_table olarak verilmelidir!\n"
            "4. Sosyal Bilgiler: 15 Soru (46-60 arası)\n"
            "5. Din Kültürü ve Ahlak Bilgisi: 10 Soru (61-70 arası)\n"
            "6. İngilizce (English): 10 Soru (71-80 arası)\n\n"
            "🚨 KESİN GÖRSEL, ŞEKİL VE GRAFİK KURALLARI (ASLA AÇIK KOD VEYA METİNSEL ÇİZİM YAPMA):\n"
            "1. Soru metni içinde asla ASCII art, markdown tablo kodu veya düz metin grafiği yazma. Bütün çizimler KESİNLİKLE JSON içinde `shape` anahtarı altında nesne olarak verilmelidir.\n"
            "2. Sütun Grafik (Fen/Matematik): `{\"type\": \"bar_chart\", \"title\": \"Sıcaklık Değişimi\", \"labels\": [\"1. Dakika\", \"2. Dakika\", \"3. Dakika\", \"4. Dakika\"], \"values\": [10, 25, 40, 60]}`\n"
            "3. Deney Tablosu (Fen): `{\"type\": \"science_table\", \"title\": \"Deney Sonuç Matrisi\", \"headers\": [\"Kaplar\", \"Sıvı Cinsi\", \"Sıcaklık\"], \"rows\": [[\"K Kabı\", \"Su\", \"20°C\"], [\"L Kabı\", \"Alkol\", \"20°C\"]]}`\n"
            "4. Üçgen: `{\"type\": \"triangle\", \"sub_type\": \"right\", \"A\": \"A\", \"B\": \"B\", \"C\": \"C\"}`\n"
            "5. Çember: `{\"type\": \"circle\", \"center\": \"O\", \"radius\": \"r\", \"show_diameter\": true}`\n\n"
            "Her sorunun 4 şıkkı (A, B, C, D) ve doğru cevabı ('A', 'B', 'C' veya 'D') olmalıdır. 'subject' alanına ilgili dersin adını tam yaz.\n"
            "Çıktıyı KESİNLİKLE aşağıdaki JSON formatında ver, başka hiçbir açıklama ekleme:\n"
            "{\n"
            "    \"questions\": [\n"
            "        {\n"
            "            \"id\": 1,\n"
            "            \"subject\": \"Fen Bilimleri\",\n"
            "            \"passage\": \"Paragraf veya metin içeriği (gerekmiyorsa boş bırakılabilir).\",\n"
            "            \"question\": \"Soru metni...\",\n"
            "            \"shape\": null,\n"
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
                st.sidebar.success(f"✅ Toplam {len(st.session_state.questions)} soru başarıyla üretildi!")
            except json.JSONDecodeError:
                st.error("Yapay zeka yanıtı geçerli JSON formatına dönüştürülemedi.")
                st.code(raw_json)
        else:
            st.error(f"❌ Tanımlı API anahtarları ile bağlantı kurulamadı. Hata: {error_message}")

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
        st.markdown(f"<span class='badge'>Soru: {st.session_state.current_page + 1} / {total_questions}</span> <span class='badge'>Zorluk Modu: {difficulty_level}</span>", unsafe_allow_html=True)
    with header_col2:
        st.markdown(f"<div class='timer-box'>⏳ {hours:02d}:{minutes:02d}:{seconds:02d}</div>", unsafe_allow_html=True)

    st.markdown("---")

    idx = st.session_state.current_page
    q = st.session_state.questions[idx]

    st.markdown(f"<div class='question-card'>", unsafe_allow_html=True)
    sub_badge = f"[{q.get('subject', 'Genel')}]" if 'subject' in q else ""
    
    if 'passage' in q and q['passage'] and str(q['passage']).strip() != "":
        st.markdown(f"<div class='passage-box'><b>📖 Metin / Öncül / Diyalog:</b><br>{q['passage']}</div>", unsafe_allow_html=True)

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

        with st.expander("📖 Detaylı Soru Çözüm ve Cevap Anahtarını İncele"):
            for i, q_item in enumerate(st.session_state.questions):
                user_ans = st.session_state.selected_answers.get(i, "Boş")
                status = "✅" if user_ans == q_item['answer'] else "❌"
                if 'passage' in q_item and q_item['passage'] and str(q_item['passage']).strip() != "":
                    st.markdown(f"**Metin:** {q_item['passage']}")
                if 'shape' in q_item and q_item['shape'] and isinstance(q_item['shape'], dict):
                    draw_geometry_shape(q_item['shape'])
                st.markdown(f"**Soru {i + 1} ({q_item.get('subject', '')}):**\n\n{q_item['question']}")
                st.markdown(f"Seçiminiz: **{user_ans}** | Doğru Cevap: **{q_item['answer']}** {status}")
                st.markdown("---")
