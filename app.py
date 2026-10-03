import time
import streamlit as st
import json
import io

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

# Görseller ve Grafikler Yerine Tablo Kullanım Motoru
def draw_geometry_shape(shape_data):
    if not isinstance(shape_data, dict):
        return
        
    st_type = str(shape_data.get("type", "")).strip().lower()
    if not st_type:
        return

    # Tüm soru türleri ve grafikler için profesyonel HTML Tablo Dönüşümü
    title = str(shape_data.get("title", "Soru Veri ve Bilgi Tablosu"))
    headers = shape_data.get("headers", [])
    rows = shape_data.get("rows", [])

    # Eğer AI özel headers/rows göndermediyse, gelen verilere göre dinamik tablo üret
    if not headers or not rows:
        if "labels" in shape_data and "values" in shape_data:
            headers = ["Kategori / Veri", "Değer"]
            rows = [[str(l), str(v)] for l, v in zip(shape_data.get("labels", []), shape_data.get("values", []))]
        elif st_type == "triangle":
            headers = ["Geometri Öğe", "Parametre / Değer"]
            rows = [
                ["Üçgen Çeşitleri / Kenarlar", f"AB: {shape_data.get('side_ab', 'Belirtilmemiş')} | BC: {shape_data.get('side_bc', 'Belirtilmemiş')} | AC: {shape_data.get('side_ac', 'Belirtilmemiş')}"],
                ["Açı Bilgileri", f"Açılar: {shape_data.get('angle_a', 'Standart Açı Değerleri')}"]
            ]
            title = "Üçgen Analiz Tablosu"
        elif st_type == "circle":
            headers = ["Çember Öğe", "Ölçü / Değer"]
            rows = [
                ["Merkez ve Yarıçap", f"Merkez: {shape_data.get('center', 'O')} | Yarıçap (r): {shape_data.get('radius', 'r')}"],
                ["Ek Parametreler", f"Çap Gösterimi: {shape_data.get('show_diameter', 'Yok')} | Kiriş: {shape_data.get('chord', 'Yok')}"]
            ]
            title = "Çember ve Daire Bilgi Tablosu"
        else:
            headers = ["Özellik", "Açıklama"]
            rows = [["Durum", "Soru Bilgi ve Veri Kümeleri"]]

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
            {"role": "system", "content": "Sen MEB müfredatı soru hazırlama uzmanısın. Tüm veri, grafik ve şema gerektiren soruları görsel yerine profesyonel tablolarla (table formatında) eksiksiz üretirsin."},
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
    
    with st.spinner(f"✨ Çoklu API havuzu taranıyor: {selected_grade} için eksiksiz metinler ve konuya özel veri tablolarıyla 80 soru hazırlanıyor..."):
        prompt = (
            f"Türkiye Cumhuriyeti Millî Eğitim Bakanlığı (MEB) {selected_grade} {term} dönemi resmi öğretim programı "
            f"ve '{selected_scope}' kapsamındaki gerçek haftalık kazanımlarına tam uygun olarak toplam KESİNLİKLE VE EKSİKSİZ olarak tam 80 adet yeni nesil soru hazırla."
            f"{custom_prompt_addon}\n\n"
            f"ZORLUK KADEMESİ VE KALİTE KRİTERİ: '{difficulty_level}'.\n\n"
            "DERS DAĞILIMI VE KESİN SORU SAYILARI VE İÇERİK KURALLARI (TOPLAM TAM 80 SORU):\n"
            "1. Türkçe: 15 Soru (1-15 arası) - Kesinlikle Türkçe dersine ait (Sözel mantık, paragrafta anlam, uzun metinler, dil bilgisi, deyimler/atasözleri). Metinleri ASLA KISALTMA, eksiksiz tam yaz.\n"
            "2. Matematik: 15 Soru (16-30 arası) - Kesinlikle Matematik dersine ait (Geometri, açılar, üçgenler, çember, veri analizi, oran-orantı, problemler). Grafik sorularında resim/grafik yerine 'table' şemalarını kullanarak verileri tablolarda sun.\n"
            "3. Fen Bilimleri: 15 Soru (31-45 arası) - Kesinlikle Fen Bilimleri dersine ait (Kuvvet ve hareket, Güneş/Dünya/Ay hareketleri, evreler, tutulmalar, hücre, maddeler). Dünya, Güneş, Ay veya deney aşamalarını 'table' şemalarıyla ver.\n"
            "4. Sosyal Bilgiler: 15 Soru (46-60 arası) - Kesinlikle Sosyal Bilgiler dersine ait (Tarih, coğrafya, kültürel miras, hak ve sorumluluklar).\n"
            "5. Din Kültürü ve Ahlak Bilgisi: 10 Soru (61-70 arası) - Kesinlikle Din Kültürü dersine ait (Ayet ve hadis yorumlama, İslam kültürü, değerler eğitimi).\n"
            "6. İngilizce (English): 10 Soru (71-80 arası) - Kesinlikle İngilizce dersine ait (Diyalog tamamlama, kartlar, tablo eşleştirme, kelime bilgisi).\n\n"
            "🚨 KESİN TABLO VE ŞEMA KURALLARI (`shape` nesnesi):\n"
            "Soruların matematik, fen ve veri okuma bölümlerinde resim/grafik yerine KESİNLİKLE tablo ('table') şemasını kullan:\n"
            "- Tablo için: {\"type\": \"table\", \"title\": \"Veri Tablosu Başlığı\", \"headers\": [\"Sütun 1\", \"Sütun 2\"], \"rows\": [[\"Satır 1A\", \"Satır 1B\"], [\"Satır 2A\", \"Satır 2B\"]]}\n"
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
            "            \"shape\": {\"type\": \"table\", \"title\": \"Veri Analizi\", \"headers\": [\"A\", \"B\"], \"rows\": [[\"10\", \"20\"]]},\n"
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
