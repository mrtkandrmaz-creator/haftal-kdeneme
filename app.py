import time
import streamlit as json_import
import json

# Sayfa Yapılandırması
json_import.set_page_config(
    page_title="MEB Müfredatı 80 Soruluk Deneme Paneli",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern UI ve Özel CSS Stilleri
json_import.markdown("""
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

# %100 Kararlı ve Korumalı Kesin SVG / Tablo Motoru
def draw_geometry_shape(shape_data):
    if not isinstance(shape_data, dict):
        return ""
        
    st_type = str(shape_data.get("type", "triangle")).strip().lower()
    
    # 1. ÜÇGENLER (Güvenli Koordinat Yapısı)
    if st_type == "triangle":
        sub_type = str(shape_data.get("sub_type", "scalene")).strip().lower()
        a_label = str(shape_data.get("A", "A"))
        b_label = str(shape_data.get("B", "B"))
        c_label = str(shape_data.get("C", "C"))
        ab_len = str(shape_data.get("ab", ""))
        bc_len = str(shape_data.get("bc", ""))
        ac_len = str(shape_data.get("ac", ""))
        
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
            </svg>
        </div>'''
        
    # 2. ÇEMBER / DAİRE (Kusursuz Kararlı Çizim)
    elif st_type == "circle":
        center_label = str(shape_data.get("center", "O"))
        radius_label = str(shape_data.get("radius", "r"))
        show_diameter = bool(shape_data.get("show_diameter", False))
        
        diameter_line = f'<line x1="60" y1="112" x2="260" y2="112" stroke="#cbd5e1" stroke-width="2" stroke-dasharray="4"/>' if show_diameter else ''
        
        return f'''<div style="display: flex; justify-content: center; margin: 15px 0;">
            <svg width="320" height="225" viewBox="0 0 320 225" style="background: #ffffff; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.06); border: 1px solid #e2e8f0;">
                <circle cx="160" cy="112" r="80" fill="#f8fafc" stroke="#1e293b" stroke-width="3.5"/>
                <circle cx="160" cy="112" r="4.5" fill="#ea580c"/>
                {diameter_line}
                <line x1="160" y1="112" x2="240" y2="112" stroke="#0284c7" stroke-width="2.5"/>
                <text x="168" y="102" font-family="sans-serif" font-size="15" font-weight="900" fill="#ea580c">{center_label}</text>
                <text x="200" y="102" font-family="sans-serif" font-size="13" font-weight="700" fill="#0284c7" text-anchor="middle">{radius_label}</text>
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
        
    # 4. FEN BİLİMLERİ & MATEMATİK ÇUBUK / SÜTUN GRAFİK (Kesin Çözüm)
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

    # 5. FEN BİLİMLERİ & DİĞER DERSLER TABLO / DENEY SONUÇ MATRİSİ
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
    GROQ_KEYS = json_import.secrets["api_keys"].get("groq_keys", [])
    GEMINI_KEYS = json_import.secrets["api_keys"].get("gemini_keys", [])
except Exception:
    GROQ_KEYS = []
    GEMINI_KEYS = []

if not GROQ_KEYS and not GEMINI_KEYS:
    json_import.error("⚠️ `.streamlit/secrets.toml` dosyasında `groq_keys` veya `gemini_keys` bulunamadı!")
    json_import.stop()

# Oturum Durumları
if "questions" not in json_import.session_state:
    json_import.session_state.questions = []
if "quiz_ready" not in json_import.session_state:
    json_import.session_state.quiz_ready = False
if "quiz_started" not in json_import.session_state:
    json_import.session_state.quiz_started = False
if "start_time" not in json_import.session_state:
    json_import.session_state.start_time = None
if "selected_answers" not in json_import.session_state:
    json_import.session_state.selected_answers = {}
if "current_page" not in json_import.session_state:
    json_import.session_state.current_page = 0

# Yan Menü Ayarları
json_import.sidebar.markdown("## ⚙ MEB Müfredat & Sınav Ayarları")
json_import.sidebar.markdown("---")

selected_grade = json_import.sidebar.selectbox("🎓 Sınıf Seviyesi", ["5. Sınıf", "6. Sınıf", "7. Sınıf", "8. Sınıf (LGS)"])
term = json_import.sidebar.selectbox("📚 Eğitim Dönemi", ["1. Dönem (18 Hafta)", "2. Dönem (18 Hafta)"])

weeks_options = [f"Hafta {i}" for i in range(1, 19)]
weeks_options.extend([
    "4. Hafta Kapsamlı Değerlendirme ve Tekrar", 
    "8. Hafta Kapsamlı Değerlendirme ve Tekrar", 
    "12. Hafta Kapsamlı Değerlendirme ve Tekrar", 
    "16. Hafta Kapsamlı Değerlendirme ve Tekrar", 
    "18. Hafta Genel Dönem Bitirme Sınavı"
])

selected_scope = json_import.sidebar.selectbox("📅 Hafta / Kazanım Kapsamı", weeks_options)

# Manuel Konu / Kazanım Arama Motoru
json_import.sidebar.markdown("---")
json_import.sidebar.markdown("### 🔍 Manuel Konu & Kazanım Ekle")
custom_topic_search = json_import.sidebar.text_input(
    "Özel Konu / Alt Başlık / Soru Kriteri",
    placeholder="Örn: Basınç, Hücre Bölünmesi, Çemberde Açılar...",
    help="Buraya yazacağınız özel konu veya detay, üretilecek 80 sorunun içeriğine doğrudan kılavuzluk edecektir."
)

difficulty_level = json_import.sidebar.selectbox(
    "📊 Soru Zorluk Derecesi",
    [
        "🎯 MEB Standart & Beceri Temelli (LGS İdeal Düzey)",
        "🔥 Güçlendirilmiş Orta / Seçici Düzey",
        "🚀 Üst Düzey Zor / LGS Seçici (Çok Aşamalı Muhakeme)",
        "⚡ Çok Zor / Olimpiyat & Beceri Odaklı"
    ]
)

question_count = 80

json_import.sidebar.markdown("---")
json_import.sidebar.markdown("### 🚀 Soru İşlemleri")
generate_btn = json_import.sidebar.button("Soruları Üret")

# Ana Ekran Başlığı
json_import.markdown(f"<h1 style='text-align: center; color: #1e293b; font-weight: 900;'>🎯 {selected_grade} 80 Soruluk Deneme Paneli</h1>", unsafe_allow_html=True)
custom_info_str = f" | Özel Konu/Kriter: <b>{custom_topic_search}</b>" if custom_topic_search.strip() else ""
json_import.markdown(f"<p style='text-align: center; color: #64748b; font-size: 1.1rem;'>Seçilen Kapsam: <b>{selected_scope}</b>{custom_info_str} | Zorluk Modu: <b>{difficulty_level}</b></p>", unsafe_allow_html=True)
json_import.markdown("---")

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
    
    with json_import.spinner(f"✨ Çoklu API havuzu taranıyor: {selected_grade} için kararlı grafik, tablo ve şekil motoruyla tam 80 yeni nesil soru hazırlanıyor..."):
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
            "4. Üçgen: `{\"type\": \"triangle\", \"sub_type\": \"right\", \"A\": \"A\", \"B\": \"B\", \"C\": \"C\", \"ab\": \"3 cm\", \"bc\": \"4 cm\", \"ac\": \"5 cm\"}`\n"
            "5. Çember: `{\"type\": \"circle\", \"center\": \"O\", \"radius\": \"6 cm\", \"show_diameter\": true}`\n\n"
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
                json_import.session_state.questions = data.get("questions", [])
                json_import.session_state.quiz_ready = True
                json_import.session_state.quiz_started = False
                json_import.session_state.selected_answers = {}
                json_import.session_state.current_page = 0
                json_import.sidebar.success(f"✅ Toplam {len(json_import.session_state.questions)} soru başarıyla üretildi!")
            except json.JSONDecodeError:
                json_import.error("Yapay zeka yanıtı geçerli JSON formatına dönüştürülemedi.")
                json_import.code(raw_json)
        else:
            json_import.error(f"❌ Tanımlı API anahtarları ile bağlantı kurulamadı. Hata: {error_message}")

# Sınavı Başlat Butonu
if json_import.session_state.quiz_ready and not json_import.session_state.quiz_started:
    json_import.markdown("---")
    sc1, sc2, sc3 = json_import.columns([1, 2, 1])
    with sc2:
        if json_import.button("🎯 Sınavı Şimdi Başlat"):
            json_import.session_state.quiz_started = True
            json_import.session_state.start_time = time.time()
            json_import.rerun()

# Sınav Ekranı
if json_import.session_state.quiz_started and json_import.session_state.questions:
    total_questions = len(json_import.session_state.questions)
    total_time_seconds = total_questions * 90
    
    elapsed_time = int(time.time() - json_import.session_state.start_time)
    remaining_time = max(0, total_time_seconds - elapsed_time)
    
    hours = remaining_time // 3600
    minutes = (remaining_time % 3600) // 60
    seconds = remaining_time % 60

    json_import.markdown("---")
    header_col1, header_col2 = json_import.columns([2, 1])
    with header_col1:
        json_import.markdown(f"### 📋 {selected_grade} - {term} ({selected_scope}) 80 Soruluk Deneme")
        json_import.markdown(f"<span class='badge'>Soru: {json_import.session_state.current_page + 1} / {total_questions}</span> <span class='badge'>Zorluk Modu: {difficulty_level}</span>", unsafe_allow_html=True)
    with header_col2:
        json_import.markdown(f"<div class='timer-box'>⏳ {hours:02d}:{minutes:02d}:{seconds:02d}</div>", unsafe_allow_html=True)

    json_import.markdown("---")

    idx = json_import.session_state.current_page
    q = json_import.session_state.questions[idx]

    json_import.markdown(f"<div class='question-card'>", unsafe_allow_html=True)
    sub_badge = f"[{q.get('subject', 'Genel')}]" if 'subject' in q else ""
    
    if 'passage' in q and q['passage'] and str(q['passage']).strip() != "":
        json_import.markdown(f"<div class='passage-box'><b>📖 Metin / Öncül / Diyalog:</b><br>{q['passage']}</div>", unsafe_allow_html=True)

    if 'shape' in q and q['shape'] and isinstance(q['shape'], dict):
        shape_html = draw_geometry_shape(q['shape'])
        json_import.markdown(shape_html, unsafe_allow_html=True)

    json_import.markdown(f"<p class='question-title'>Soru {idx + 1} {sub_badge}:\n\n{q['question']}</p>", unsafe_allow_html=True)

    options = q['options']
    
    current_val = json_import.session_state.selected_answers.get(idx)
    default_index = None
    if current_val in list(options.keys()):
        default_index = list(options.keys()).index(current_val)

    choice = json_import.radio(
        f"**Soru {idx + 1} Şıkları:**",
        options=list(options.keys()),
        index=default_index,
        format_func=lambda x: f"{x}) {options[x]}",
        key=f"q_{idx}"
    )
    if choice:
        json_import.session_state.selected_answers[idx] = choice
        
    json_import.markdown(f"</div>", unsafe_allow_html=True)

    # Navigasyon Butonları
    json_import.markdown("<div class='nav-btn-container'>", unsafe_allow_html=True)
    nav_col1, nav_col2, nav_col3 = json_import.columns([1, 2, 1])
    with nav_col1:
        if json_import.session_state.current_page < total_questions - 1:
            if json_import.button("➡ Sonraki Soru"):
                json_import.session_state.current_page += 1
                json_import.rerun()
                
    with nav_col3:
        if json_import.session_state.current_page > 0:
            if json_import.button("⬅️ Önceki Soru"):
                json_import.session_state.current_page -= 1
                json_import.rerun()
    json_import.markdown("</div>", unsafe_allow_html=True)

    json_import.markdown("---")
    if json_import.button("🏁 Deneme Sınavını Tamamla ve Sonuçları Gör"):
        correct_count, wrong_count = 0, 0
        for i, q_item in enumerate(json_import.session_state.questions):
            if json_import.session_state.selected_answers.get(i) == q_item['answer']:
                correct_count += 1
            else:
                wrong_count += 1

        score = (correct_count / total_questions) * 100
        json_import.balloons()
        json_import.success("🎉 Deneme sınavı başarıyla tamamlandı!")
        
        res_col1, res_col2, res_col3 = json_import.columns(3)
        res_col1.metric("✅ Doğru Sayısı", correct_count)
        res_col2.metric("❌ Yanlış Sayısı", wrong_count)
        res_col3.metric("🎯 Genel Başarı Puanı", f"{score:.1f} Puan")

        with json_import.expander("📖 Detaylı Soru Çözüm ve Cevap Anahtarını İncele"):
            for i, q_item in enumerate(json_import.session_state.questions):
                user_ans = json_import.session_state.selected_answers.get(i, "Boş")
                status = "✅" if user_ans == q_item['answer'] else "❌"
                if 'passage' in q_item and q_item['passage'] and str(q_item['passage']).strip() != "":
                    json_import.markdown(f"**Metin:** {q_item['passage']}")
                if 'shape' in q_item and q_item['shape'] and isinstance(q_item['shape'], dict):
                    json_import.markdown(draw_geometry_shape(q_item['shape']), unsafe_allow_html=True)
                json_import.markdown(f"**Soru {i + 1} ({q_item.get('subject', '')}):**\n\n{q_item['question']}")
                json_import.markdown(f"Seçiminiz: **{user_ans}** | Doğru Cevap: **{q_item['answer']}** {status}")
                json_import.markdown("---")
