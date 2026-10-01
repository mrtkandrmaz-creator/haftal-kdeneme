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

# Modern UI ve Daha Büyük Turuncu Buton Tasarımı İçin Özel CSS
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
        white-space: pre-line;
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
st.markdown("<p style='text-align: center; color: #64748b; font-size: 1.1rem;'>MEB müfredatına tam uyumlu, kusursuz geometrik çizimli yeni nesil sorular.</p>", unsafe_allow_html=True)
st.markdown("---")

# Groq Çağrı Fonksiyonu
def call_groq_with_key(api_key, prompt_text):
    from groq import Groq
    client = Groq(api_key=api_key)
    completion = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": "Sen kıdemli bir MEB müfredat ve sınav hazırlama uzmanısın. Yalnızca eksiksiz ve geçerli JSON formatında yanıt ver. Asla HTML etiketi (örn: </p>) kullanma."},
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
        model="gemini-1.5-flash",
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
    with st.spinner(f"✨ Çoklu API havuzu taranıyor, {selected_grade} düzeyinde tam 60 adet kusursuz görsel üçgenli yeni nesil soru hazırlanıyor..."):
        prompt = f"""
        {selected_grade} {term} dönemi içinde yer alan '{selected_scope}' kazanımlarına uygun olarak, MEB müfredatındaki temel derslerden (Türkçe, Matematik, Fen Bilimleri, Sosyal Bilgiler/İnkılap Tarihi, Din Kültürü, İngilizce) toplamda KESİNLİKLE VE EKSİKSİZ olarak tam {question_count} adet yeni nesil beceri temelli soru hazırla.
        
        GEOMETRİ VE GÖRSEL ÇİZİM KURALLARI:
        1. Matematik sorularında dik üçgen, eşkenar üçgen, ikizkenar üçgen, açılar ve geometrik şekiller yer alırken, şekillerin köşeleri ve bütünlüğü kusursuz olsun diye ÜÇGENLERİ MUTLAKA MARKDOWN KOD BLOĞU İÇİNDE ```text ... ``` formatında, A, B, C köşe harfleri, diklik simgeleri ve kenar uzunlukları net şekilde çiz.
        2. ASLA bozuk karakter, eksik çizgi veya HTML etiketleri (`</p>`, `<div>` vb.) kullanma.
        3. "Şema", "grafik şeması" veya "görsel aşağıdadır" kelimelerini asla kullanma, doğrudan çizimi metne entegre et.
        
        Her sorunun 4 şıkkı (A, B, C, D) ve doğru cevabı ("A", "B", "C" veya "D") olmalıdır. 'subject' alanına ilgili dersin adını yaz.
        Çıktıyı KESİNLİKLE aşağıdaki JSON formatında ver, başka hiçbir açıklama metni ekleme:
        {{
            "questions": [
                {{
                    "id": 1,
                    "subject": "Matematik",
                    "question": "Soru metni ve içinde Markdown kod bloğuyla çizilmiş kusursuz şekil burada yer alacak...",
                    "options": {{
                        "A": "A şıkkı",
                        "B": "B şıkkı",
                        "C": "C şıkkı",
                        "D": "D şıkkı"
                    }},
                    "answer": "A"
                }}
            ]
        }}
        """
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
                st.markdown(f"Seçiminiz: **{user_ans}** | Doğru Cevap: **{q_item['answer']}** {status}")
                st.markdown("---")
