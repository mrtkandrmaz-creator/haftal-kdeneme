import time
import streamlit as st
import json

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

# %100 Hata Korumalı ve Hassas SVG / Tablo Motoru
def draw_geometry_shape(shape_data):
    if not isinstance(shape_data, dict):
        return ""
        
    st_type = str(shape_data.get("type", "triangle")).strip().lower()
    
    # 1. ÜÇGENLER
    if st_type == "triangle":
        sub_type = str(shape_data.get("sub_type", "scalene")).strip().lower()
        a_label = str(shape_data.get("A", "A"))
        b_label = str(shape_data.get("B", "B"))
        c_label = str(shape_data.get("C", "C"))
        ab_len = str(shape_data.get("ab", ""))
        bc_len = str(shape_data.get("bc", ""))
        ac_len = str(shape_data.get("ac", ""))
        angle_a = str(shape_data.get("angle_a", ""))
        angle_b = str(shape_data.get("angle_b", ""))
        angle_c = str(shape_data.get("angle_c", ""))
        
        if sub_type == "right":
            polygon_points = "65,30 65,185 240,185"
            right_angle_svg = '<rect x="65" y="160" width="25" height="25" fill="none" stroke="#1e293b" stroke-width="2.5"/>'
            a_pos, b_pos, c_pos = (65, 18), (50, 200), (248, 200)
            ab_pos, bc_pos, ac_pos = (40, 110), (152, 207), (160, 100)
        elif sub_type == "equilateral":
            polygon_points = "155,22 45,190 265,190"
            right_angle_svg = ''
            a_pos, b_pos, c_pos = (155, 10), (30, 202), (280, 202)
            ab_pos, bc_pos, ac_pos = (85, 100), (155, 210), (225, 100)
        else:
            polygon_points = "155,25 50,185 260,185"
            right_angle_svg = ''
            a_pos, b_pos, c_pos = (155, 15), (35, 198), (275, 198)
            ab_pos, bc_pos, ac_pos = (88, 100), (155, 205), (220, 100)

        return f'''<div style="display: flex; justify-content: center; margin: 15px 0;">
            <svg width="320" height="225" viewBox="0 0 320 225" style="background: #ffffff; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.06); border: 1px solid #e2e8f0;">
                <polygon points="{polygon_points}" fill="#f8fafc" stroke="#1e293b" stroke-width="3.5" stroke-linejoin="round"/>
                {right_angle_svg}
                <text x="{a_pos[0]}" y="{a_pos[1]}" font-family="sans-serif" font-size="15" font-weight="900" fill="#1e293b" text-anchor="middle">{a_label}</text>
                <text x="{b_pos[0]}" y="{b_pos[1]}" font-family="sans-serif" font-size="15" font-weight="900" fill="#1e293b" text-anchor="middle">{b_label}</text>
                <text x="{c_pos[0]}" y="{c_pos[1]}" font-family="sans-serif" font-size="15" font-weight="900" fill="#1e293b" text-anchor="middle">{c_label}</text>
                <text x="{ab_pos[0]}" y="{ab_pos[1]}" font-family="sans-serif" font-size="13" font-weight="700" fill="#ea580c" text-anchor="middle">{ab_len}</text>
                <text x="{bc_pos[0]}" y="{bc_pos[1]}" font-family="sans-serif" font-size="13" font-weight="700" fill="#ea580c" text-anchor="middle">{bc_len}</text>
                <text x="{ac_pos[0]}" y="{ac_pos[1]}" font-family="sans-serif" font-size="13" font-weight="700" fill="#ea580c" text-anchor="middle">{ac_len}</text>
                <text x="155" y="52" font-family="sans-serif" font-size="12" font-weight="700" fill="#0284c7" text-anchor="middle">{angle_a}</text>
                <text x="80" y="165" font-family="sans-serif" font-size="12" font-weight="700" fill="#0284c7" text-anchor="middle">{angle_b}</text>
                <text x="230" y="165" font-family="sans-serif" font-size="12" font-weight="700" fill="#0284c7" text-anchor="middle">{angle_c}</text>
            </svg>
        </div>'''
        
    # 2. ÇEMBER / DAİRE
    elif st_type == "circle":
        center_label = str(shape_data.get("center", "O"))
        radius_label = str(shape_data.get("radius", ""))
        show_diameter = bool(shape_data.get("show_diameter", False))
        
        diameter_line = f'<line x1="55" y1="112" x2="265" y2="112" stroke="#cbd5e1" stroke-width="2" stroke-dasharray="4"/>' if show_diameter else ''
        
        return f'''<div style="display: flex; justify-content: center; margin: 15px 0;">
            <svg width="320" height="225" viewBox="0 0 320 225" style="background: #ffffff; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.06); border: 1px solid #e2e8f0;">
                <circle cx="160" cy="112" r="88" fill="#f8fafc" stroke="#1e293b" stroke-width="3.5"/>
                <circle cx="160" cy="112" r="4.5" fill="#ea580c"/>
                {diameter_line}
                <line x1="160" y1="112" x2="248" y2="112" stroke="#0284c7" stroke-width="2.5"/>
                <text x="168" y="102" font-family="sans-serif" font-size="15" font-weight="900" fill="#ea580c">{center_label}</text>
                <text x="204" y="102" font-family="sans-serif" font-size="13" font-weight="700" fill="#0284c7" text-anchor="middle">{radius_label}</text>
            </svg>
        </div>'''

    # 3. KARE VE DİKDÖRTGEN
    elif st_type in ["square", "rectangle"]:
        title = str(shape_data.get("title", "Geometrik Şekil"))
        w_label = str(shape_data.get("width", ""))
        h_label = str(shape_data.get("height", ""))
        is_square = (st_type == "square")
        
        rect_w, rect_h = (160, 160) if is_square else (210, 130)
        rect_x, rect_y = (160 - rect_w//2), (112 - rect_h//2)
        
        return f'''<div style="display: flex; justify-content: center; margin: 15px 0;">
            <svg width="320" height="225" viewBox="0 0 320 225" style="background: #ffffff; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.06); border: 1px solid #e2e8f0;">
                <rect x="{rect_x}" y="{rect_y}" width="{rect_w}" height="{rect_h}" fill="#f8fafc" stroke="#1e293b" stroke-width="3.5" rx="4"/>
                <text x="160" y="{rect_y - 12}" font-family="sans-serif" font-size="14" font-weight="800" fill="#ea580c" text-anchor="middle">{w_label}</text>
                <text x="{rect_x - 22}" y="118" font-family="sans-serif" font-size="14" font-weight="800" fill="#0284c7" text-anchor="middle">{h_label}</text>
                <text x="160" y="208" font-family="sans-serif" font-size="13" font-weight="700" fill="#334155" text-anchor="middle">{title}</text>
            </svg>
        </div>'''
        
    # 4. FEN BİLİMLERİ & MATEMATİK ÇUBUK / SÜTUN GRAFİK
    elif st_type in ["bar_chart", "science_chart"]:
        labels = shape_data.get("labels", ["A", "B", "C", "D"])
        values = shape_data.get("values", [10, 25, 15, 30])
        title = str(shape_data.get("title", "Veri Analizi"))
        
        clean_values = []
        for v in values:
            try:
                clean_values.append(float(v))
            except:
                clean_values.append(10.0)
                
        max_v = max(clean_values) if clean_values and max(clean_values) > 0 else 30.0
        
        bars_html = ""
        x_start = 35
        total_bars = len(labels) if len(labels) > 0 else 4
        bar_width = min(42, max(18, int(230 / total_bars)))
        spacing = bar_width + 14
        
        for i, (l, v) in enumerate(zip(labels, clean_values)):
            h = int((v / max_v) * 120) if max_v > 0 else 10
            y = 165 - h
            bx = x_start + i * spacing
            bars_html += f'''
                <rect x="{bx}" y="{y}" width="{bar_width}" height="{h}" fill="#0284c7" rx="4"/>
                <text x="{bx + bar_width//2}" y="{y - 6}" font-family="sans-serif" font-size="11" font-weight="700" fill="#1e293b" text-anchor="middle">{v:g}</text>
                <text x="{bx + bar_width//2}" y="185" font-family="sans-serif" font-size="11" font-weight="800" fill="#334155" text-anchor="middle">{str(l)}</text>
            '''
        
        return f'''<div style="display: flex; justify-content: center; margin: 15px 0;">
            <svg width="330" height="215" viewBox="0 0 330 215" style="background: #ffffff; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.06); border: 1px solid #e2e8f0;">
                <text x="165" y="24" font-family="sans-serif" font-size="14" font-weight="800" fill="#1e293b" text-anchor="middle">{title}</text>
                <line x1="25" y1="165" x2="305" y2="165" stroke="#cbd5e1" stroke-width="2"/>
                {bars_html}
            </svg>
        </div>'''

    # 5. FEN BİLİMLERİ TABLO / DENEY SONUÇ MATRİSİ
    elif st_type == "science_table":
        title = str(shape_data.get("title", "Deney Veri Tablosu"))
        headers = shape_data.get("headers", ["Grup", "Değişken 1", "Değişken 2"])
        rows = shape_data.get("rows", [["1. Grup", "Arttı", "Sabit"], ["2. Grup", "Azaldı", "Arttı"]])
        
        th_html = "".join([f'<th style="border: 1px solid #cbd5e1; padding: 8px; background: #f1f5f9; color: #1e293b; font-size: 13px;">{h}</th>' for h in headers])
        tr_html = ""
        for row in rows:
            tds = "".join([f'<td style="border: 1px solid #cbd5e1; padding: 7px; text-align: center; color: #334155; font-size: 12px;">{cell}</td>' for cell in row])
            tr_html += f'<tr>{tds}</tr>'
            
        return f'''<div style="margin: 15px auto; max-width: 380px; background: #ffffff; padding: 12px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.06); border: 1px solid #e2e8f0;">
            <div style="font-weight: 800; text-align: center; color: #1e293b; margin-bottom: 8px; font-size: 13px;">{title}</div>
            <table style="width: 100%; border-collapse: collapse; font-family: sans-serif;">
                <thead><tr>{th_html}</tr></thead>
                <tbody>{tr_html}</tbody>
            </table>
        </div>'''
        
    return ""

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
st.markdown(f"<p style='text-align: center; color: #64748b; font-size: 1.1rem;'>Seçilen Kapsam: <b>{selected_scope}</b> | Zorluk Modu: <b>{difficulty_level}</b></p>", unsafe_allow_html=True)
st.markdown("---")

def call_groq_with_key(api_key, prompt_text):
    from groq import Groq
    client = Groq(api_key=api_key)
    completion = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": "Sen kıdemli bir MEB müfredat ve LGS soru hazırlama uzmanısın. Grafikleri ve şekilleri asla ham kod olarak metin içinde yazdırma, JSON objesi olarak 'shape' alanında ver. Eksiksiz JSON formatında yanıt ver."},
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

# Soru Üretim Mantığı (80 Soru Sabit ve İngilizce Dahil)
if generate_btn:
    with st.spinner(f"✨ Çoklu API havuzu taranıyor: {selected_grade} için harita, grafik, tablo uyumlu tam 80 yeni nesil soru hazırlanıyor..."):
        prompt = (
            f"Türkiye Cumhuriyeti Millî Eğitim Bakanlığı (MEB) {selected_grade} {term} dönemi resmi öğretim programı "
            f"ve '{selected_scope}' kapsamındaki gerçek haftalık kazanımlarına tam uygun olarak toplam KESİNLİKLE VE EKSİKSİZ olarak tam 80 adet yeni nesil soru hazırla.\n\n"
            f"ZORLUK SEVİYESİ VE KALİTE TALİMATI: '{difficulty_level}'. (Sorular net, anlaşılır ve MEB beceri temelli sınav formatına uygun olmalıdır!)\n\n"
            "LGS VE MERKEZİ SINAV DERS DAĞILIMI VE KESİN SORU SAYILARI (TOPLAM TAM 80 SORU):\n"
            "1. Türkçe: 15 Soru (1-15 arası) - Uzun metinli, eleştirel okuma, mantık muhakemesi.\n"
            "2. Matematik: 15 Soru (16-30 arası) - Günlük hayat problemleri, şekil ve işlem yoğun.\n"
            "3. Fen Bilimleri: 15 Soru (31-45 arası) - Deney yorumlama, grafik analizi veya tablo matrisli.\n"
            "4. Sosyal Bilgiler: 15 Soru (46-60 arası) - Öncüllü yorum, belge analizi.\n"
            "5. Din Kültürü ve Ahlak Bilgisi: 10 Soru (61-70 arası) - Ayet/hadis yorumu.\n"
            "6. İngilizce (English): 10 Soru (71-80 arası) - Diyalog tamamlama, paragraf okuma, görsel/durum analizi ve vocabulary (kelime bilgisi) ağırlıklı.\n\n"
            "HAYATİ ÖNEM TAŞIYAN GÖRSEL VE TABLO KURALLARI (ASLA HATA YAPMA):\n"
            "1. Fen Bilimleri ve Matematik sorularında grafik, tablo veya geometrik şekil (üçgen, çember, kare, dikdörtgen) gerektiren durumlarda ASLA metin içinde açık kod veya ham metin yazma; bunun yerine `shape` alanına eksiksiz JSON objesi ekle.\n"
            "2. Çember/Üçgen/Kare/Dikdörtgen için `shape` formatları doğru olmalıdır.\n"
            "3. Fen Bilimleri Tablo formatı: `{\"type\": \"science_table\", \"title\": \"Deney Sonuçları\", \"headers\": [\"Kaplar\", \"Sıcaklık\", \"Süre\"], \"rows\": [[\"1. Kap\", \"20°C\", \"10 dk\"], [\"2. Kap\", \"40°C\", \"5 dk\"]]}`\n"
            "4. Grafik formatı: `{\"type\": \"bar_chart\", \"title\": \"Grafik Analizi\", \"labels\": [\"A\", \"B\", \"C\", \"D\"], \"values\": [15, 30, 20, 40]}`\n"
            "5. Geometrik şekil formatları:\n"
            "   - Üçgen: `{\"type\": \"triangle\", \"sub_type\": \"right\", \"A\": \"A\", \"B\": \"B\", \"C\": \"C\", \"ab\": \"3 cm\", \"bc\": \"4 cm\", \"ac\": \"5 cm\"}`\n"
            "   - Çember: `{\"type\": \"circle\", \"center\": \"O\", \"radius\": \"r = 6 cm\"}`\n"
            "   - Kare/Dikdörtgen: `{\"type\": \"rectangle\", \"title\": \"ABCD Dikdörtgeni\", \"width\": \"12 cm\", \"height\": \"5 cm\"}`\n\n"
            "Her sorunun 4 şıkkı (A, B, C, D) ve doğru cevabı ('A', 'B', 'C' veya 'D') olmalıdır. 'subject' alanına ilgili dersin adını tam yaz.\n"
            "Çıktıyı KESİNLİKLE aşağıdaki JSON formatında ver, başka hiçbir açıklama ekleme:\n"
            "{\n"
            "    \"questions\": [\n"
            "        {\n"
            "            \"id\": 1,\n"
            "            \"subject\": \"Türkçe\",\n"
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
        st.markdown(f"### 📋 {selected_grade} - {term} ({selected_scope}) 80 Soruluk LGS Denemesi")
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
        shape_html = draw_geometry_shape(q['shape'])
        st.markdown(shape_html, unsafe_allow_html=True)

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
            if st.button("➡️️ Sonraki Soru"):
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
                    st.markdown(draw_geometry_shape(q_item['shape']), unsafe_allow_html=True)
                st.markdown(f"**Soru {i + 1} ({q_item.get('subject', '')}):**\n\n{q_item['question']}")
                st.markdown(f"Seçiminiz: **{user_ans}** | Doğru Cevap: **{q_item['answer']}** {status}")
                st.markdown("---")
