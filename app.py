import time
import streamlit as st
import json

# Sayfa Yapılandırması
st.set_page_config(
    page_title="MEB Müfredatı 60 Soruluk Deneme Paneli",
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
    .question-card {
        background: white;
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05);
        border: 1px solid #e2e8f0;
        margin-bottom: 1.5rem;
    }
    .question-title {
        font-size: 1.35rem !important;
        font-weight: 800 !important;
        color: #1e293b !important;
        line-height: 1.6 !important;
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

# Kusursuz Vektörel Üçgen Çizim Motoru (Kesin Düzeltilmiş ve HTML Render Garantili)
def draw_triangle_svg(a_label="A", b_label="B", c_label="C", ab_len="", bc_len="", ac_len="", is_right=False):
    right_angle_svg = '<rect x="30" y="145" width="25" height="25" fill="none" stroke="#1e293b" stroke-width="2.5"/>' if is_right else ''
    
    # Çok satırlı metin hatasını önlemek için tek satırlık XML string yapısı
    svg_code = f'<div style="display: flex; justify-content: center; margin: 15px 0;"><svg width="260" height="210" viewBox="0 0 260 210" style="background: #ffffff; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.06); border: 1px solid #e2e8f0;"><polygon points="130,25 30,170 230,170" fill="#f8fafc" stroke="#1e293b" stroke-width="3.5" stroke-linejoin="round"/>{right_angle_svg}<text x="130" y="18" font-family="sans-serif" font-size="16" font-weight="900" fill="#1e293b" text-anchor="middle">{a_label}</text><text x="15" y="188" font-family="sans-serif" font-size="16" font-weight="900" fill="#1e293b" text-anchor="middle">{b_label}</text><text x="245" y="188" font-family="sans-serif" font-size="16" font-weight="900" fill="#1e293b" text-anchor="middle">{c_label}</text><text x="68" y="90" font-family="sans-serif" font-size="14" font-weight="700" fill="#ea580c" text-anchor="middle">{ab_len}</text><text x="130" y="193" font-family="sans-serif" font-size="14" font-weight="700" fill="#ea580c" text-anchor="middle">{bc_len}</text><text x="192" y="90" font-family="sans-serif" font-size="14" font-weight="700" fill="#ea580c" text-anchor="middle">{ac_len}</text></svg></div>'
    return svg_code

# API Anahtarlarını secrets.toml'dan Güvenli Okuma
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

# Yan Menü - Sınıf, Dönem ve Kapsam Ayarları
st.sidebar.markdown("## ⚙️ Müfredat & Çoklu API Havuzu")
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
question_count = 60

st.sidebar.markdown("---")
st.sidebar.markdown("### 🚀 Soru İşlemleri")
generate_btn = st.sidebar.button("Soruları Üret")

st.sidebar.markdown("---")
st.sidebar.info(f"🔑 **Aktif API Havuzu:** {len(GROQ_KEYS)} Groq | {len(GEMINI_KEYS)} Gemini anahtarı yüklendi.")

# Ana Ekran Başlığı
st.markdown(f"<h1 style='text-align: center; color: #1e293b; font-weight: 900;'>🎯 {selected_grade} 60 Soruluk Deneme Paneli</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748b; font-size: 1.1rem;'>Seçilen haftaya ait MEB konu kazanımları ve eşit oranlı (%25) yeni nesil beceri temelli soru tipleriyle.</p>", unsafe_allow_html=True)
st.markdown("---")

# Groq Çağrı Fonksiyonu
def call_groq_with_key(api_key, prompt_text):
    from groq import Groq
    client = Groq(api_key=api_key)
    completion = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": "Sen kıdemli bir MEB müfredat, Ölçme-Değerlendirme ve LGS sınav hazırlama uzmanısın. Yalnızca eksiksiz ve geçerli JSON formatında yanıt ver."},
            {"role": "user", "content": prompt_text}
        ],
        temperature=0.7,
        max_tokens=8000,
        response_format={"type": "json_object"}
    )
    return completion.choices[0].message.content

# Gemini Çağrı Fonksiyonu
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

# Arka Planda Çalışan Akıllı Dağıtıcı
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
    with st.spinner(f"✨ Çoklu API havuzu taranıyor: {selected_grade} için '{selected_scope}' kazanımlarına tam uygun, %25 eşit oranlı 60 yeni nesil soru hazırlanıyor..."):
        prompt = (
            f"Türkiye Cumhuriyeti Millî Eğitim Bakanlığı (MEB) {selected_grade} {term} dönemi '{selected_scope}' resmi öğretim programı "
            f"ve kazanımlarına birebir uygun olacak şekilde toplam KESİNLİKLE VE EKSİKSİZ olarak tam {question_count} adet yeni nesil soru hazırla.\n\n"
            "ZORUNLU SORU TİPİ DAĞILIMI (%25 EŞİT ORAN):\n"
            "60 sorunun tamamı şu 4 soru tipine tam olarak eşit (15'er adet) oranla dağıtılmalıdır:\n"
            "1. Günlük Hayat Bağlamı / Gerçek Yaşam Problemi Kurma (%25)\n"
            "2. Grafik, Tablo ve Görsel Okuma / Veri Yorumlama (%25)\n"
            "3. Sözel Mantık / Muhakeme ve Eleştirel Düşünme (%25)\n"
            "4. Deney / Hipotez Analizi ve Çıkarım Yapma / Mantıksal Çözümleme (%25)\n\n"
            "DERS DAĞILIMI:\n"
            "Sorular sırasıyla Türkçe, Matematik, Fen Bilimleri, Sosyal Bilgiler (veya İnkılap Tarihi), Din Kültürü ve İngilizce derslerinden oluşsun.\n\n"
            "GEOMETRİ VE ÜÇGEN KURALLARI:\n"
            "Eğer matematik/geometri sorularında üçgen bulunuyorsa, metin içinde asla ASCII çizim kullanılmamalı ve JSON içinde mutlaka şu formatta bir 'shape' nesnesi tanımlanmalıdır:\n"
            "{\n"
            "    \"type\": \"triangle\",\n"
            "    \"A\": \"A\", \"B\": \"B\", \"C\": \"C\",\n"
            "    \"ab\": \"3 cm\", \"bc\": \"4 cm\", \"ac\": \"5 cm\",\n"
            "    \"is_right\": true\n"
            "}\n\n"
            "Her sorunun 4 şıkkı (A, B, C, D) ve doğru cevabı ('A', 'B', 'C' veya 'D') olmalıdır. 'subject' alanına ilgili dersin adını yaz.\n"
            "Çıktıyı KESİNLİKLE aşağıdaki JSON formatında ver, başka hiçbir açıklama metni ekleme:\n"
            "{\n"
            "    \"questions\": [\n"
            "        {\n"
            "            \"id\": 1,\n"
            "            \"subject\": \"Türkçe\",\n"
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
            st.error(f"❌ Tanımlı tüm API anahtarları arka planda denendi fakat yanıt alınamadı. Detay: {error_message}")

# Sorular Üretildikten Sonra Görünen "Sınavı Başlat" Butonu
if st.session_state.quiz_ready and not st.session_state.quiz_started:
    st.markdown("---")
    sc1, sc2, sc3 = st.columns([1, 2, 1])
    with sc2:
        if st.button("🎯 Sınavı Şimdi Başlat"):
            st.session_state.quiz_started = True
            st.session_state.start_time = time.time()
            st.rerun()

# Sınav Ekranı (Her Sayfada 1 Soru)
if st.session_state.quiz_started and st.session_state.questions:
    total_questions = len(st.session_state.questions)
    total_time_seconds = total_questions * 80  
    
    elapsed_time = int(time.time() - st.session_state.start_time)
    remaining_time = max(0, total_time_seconds - elapsed_time)
    
    hours = remaining_time // 3600
    minutes = (remaining_time % 3600) // 60
    seconds = remaining_time % 60

    st.markdown("---")
    header_col1, header_col2 = st.columns([2, 1])
    with header_col1:
        st.markdown(f"### 📋 {selected_grade} - {term} ({selected_scope}) Deneme Sınavı")
        st.markdown(f"<span class='badge'>Soru: {st.session_state.current_page + 1} / {total_questions}</span> <span class='badge'>Soru Başı Süre: 80 Saniye</span>", unsafe_allow_html=True)
    with header_col2:
        st.markdown(f"<div class='timer-box'>⏳ {hours:02d}:{minutes:02d}:{seconds:02d}</div>", unsafe_allow_html=True)

    st.markdown("---")

    idx = st.session_state.current_page
    q = st.session_state.questions[idx]

    st.markdown(f"<div class='question-card'>", unsafe_allow_html=True)
    sub_badge = f"[{q.get('subject', 'Genel')}]" if 'subject' in q else ""
    
    st.markdown(f"<p class='question-title'>Soru {idx + 1} {sub_badge}:\n\n{q['question']}</p>", unsafe_allow_html=True)
    
    # Geometrik şekil (üçgen vb.) varsa düzeltilmiş SVG fonksiyonu ile çağır
    if 'shape' in q and q['shape'] and isinstance(q['shape'], dict):
        s = q['shape']
        if s.get('type') == 'triangle':
            svg_html = draw_triangle_svg(
                a_label=s.get('A', 'A'),
                b_label=s.get('B', 'B'),
                c_label=s.get('C', 'C'),
                ab_len=s.get('ab', ''),
                bc_len=s.get('bc', ''),
                ac_len=s.get('ac', ''),
                is_right=s.get('is_right', False)
            )
            st.markdown(svg_html, unsafe_allow_html=True)

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

    # İleri / Geri Navigasyon Butonları
    nav_col1, nav_col2, nav_col3 = st.columns([1, 2, 1])
    with nav_col1:
        if st.session_state.current_page > 0:
            if st.button("⬅️ Önceki Soru"):
                st.session_state.current_page -= 1
                st.rerun()
                
    with nav_col3:
        if st.session_state.current_page < total_questions - 1:
            if st.button("Sonraki Soru ➡️"):
                st.session_state.current_page += 1
                st.rerun()

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
                st.markdown(f"**Soru {i + 1} ({q_item.get('subject', '')}):**\n\n{q_item['question']}")
                if 'shape' in q_item and q_item['shape'] and isinstance(q_item['shape'], dict):
                    s = q_item['shape']
                    if s.get('type') == 'triangle':
                        st.markdown(draw_triangle_svg(s.get('A', 'A'), s.get('B', 'B'), s.get('C', 'C'), s.get('ab', ''), s.get('bc', ''), s.get('ac', ''), s.get('is_right', False)), unsafe_allow_html=True)
                st.markdown(f"Seçiminiz: **{user_ans}** | Doğru Cevap: **{q_item['answer']}** {status}")
                st.markdown("---")
