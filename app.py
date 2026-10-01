import time
import streamlit as st
import json

# Sayfa Yapılandırması
st.set_page_config(
    page_title="MEB Müfredatı 80 Soruluk Çoklu API Deneme Paneli",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern UI ve Şık Tasarım İçin Özel CSS
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        font-weight: 700;
        padding: 0.85rem 1rem;
        background: linear-gradient(135deg, #4f46e5 0%, #3b82f6 100%);
        color: white;
        border: none;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 15px -3px rgba(79, 70, 229, 0.4);
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
if "quiz_started" not in st.session_state:
    st.session_state.quiz_started = False
if "questions" not in st.session_state:
    st.session_state.questions = []
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "selected_answers" not in st.session_state:
    st.session_state.selected_answers = {}

# Yan Menü - Kapsam ve Dönem Seçimi
st.sidebar.markdown("## ⚙️ Müfredat & Çoklu API Havuzu")
st.sidebar.markdown("---")

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
question_count = 80

st.sidebar.markdown("---")
st.sidebar.info(f"🔑 **Aktif API Havuzu:** {len(GROQ_KEYS)} Groq | {len(GEMINI_KEYS)} Gemini anahtarı yüklendi.")

# Ana Ekran Başlığı
st.markdown("<h1 style='text-align: center; color: #1e293b; font-weight: 900;'>🎯 5. Sınıf LGS Çoklu API Havuzlu Deneme Paneli</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748b; font-size: 1.1rem;'>Tanımlı çoklu Groq ve Gemini anahtarları arasında akıllı geçiş yapan 80 soruluk LGS sistemi.</p>", unsafe_allow_html=True)
st.markdown("---")

# Groq Çağrı Fonksiyonu (Güncel Model: llama-3.1-70b-versatile)
def call_groq_with_key(api_key, prompt_text):
    from groq import Groq
    client = Groq(api_key=api_key)
    completion = client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=[
            {"role": "system", "content": "Sen kıdemli bir 5. sınıf MEB müfredat ve LGS soru hazırlama uzmanısın. Yalnızca geçerli JSON formatında yanıt ver."},
            {"role": "user", "content": prompt_text}
        ],
        temperature=0.7,
        response_format={"type": "json_object"}
    )
    return completion.choices[0].message.content

# Gemini Çağrı Fonksiyonu (Güncel Model: gemini-3.8-flash)
def call_gemini_with_key(api_key, prompt_text):
    from google import genai
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt_text,
    )
    text = response.text
    if "```json" in text:
        text = text.split("```json")[1].split("```")[0].strip()
    elif "```" in text:
        text = text.split("```")[1].split("```")[0].strip()
    return text

# Çoklu Anahtar Havuzunu Yöneten Akıllı Dağıtıcı (Load Balancer & Fallback)
def multi_pool_generate(prompt_text):
    attempts = []
    for i, key in enumerate(GROQ_KEYS):
        if key.strip():
            attempts.append(("Groq", i+1, key, call_groq_with_key))
            
    for i, key in enumerate(GEMINI_KEYS):
        if key.strip():
            attempts.append(("Gemini", i+1, key, call_gemini_with_key))

    if not attempts:
        st.error("❌ Havuzda geçerli API anahtarı bulunamadı!")
        return None

    last_error = None
    for provider, index, key, func in attempts:
        try:
            st.info(f"🔄 Havuzdan **{provider} (#{index})** deneniyor...")
            result = func(key, prompt_text)
            if result:
                st.success(f"✅ Başarıyla **{provider} (#{index})** kullanılarak sorular oluşturuldu!")
                return result
        except Exception as e:
            last_error = e
            st.warning(f"⚠️ {provider} (#{index}) hata verdi: {e}. Havuzdaki sonraki anahtara geçiliyor...")
            continue

    st.error(f"❌ Tanımlı tüm API anahtarları havuzu denendi fakat yanıt alınamadı. Son Hata: {last_error}")
    return None

# Soru Üretim Butonu
col_b1, col_b2, col_b3 = st.columns([1, 2, 1])
with col_b2:
    generate_btn = st.button("🚀 Havuzdaki API'lerle 80 Soruluk Deneme Üret")

if generate_btn:
    with st.spinner("✨ Çoklu API havuzu kullanılarak 80 soruluk MEB LGS denemesi hazırlanıyor..."):
        prompt = f"""
        5. sınıf {term} dönemi içinde yer alan '{selected_scope}' kriterine uygun olarak, MEB müfredatındaki tüm ana derslerin (Türkçe, Matematik, Fen Bilimleri, Sosyal Bilgiler vb.) o haftaya kadar işlenen kazanımlarını kapsayan tam {question_count} adet yeni nesil beceri temelli çoktan seçmeli soru hazırla.
        Her sorunun 4 şıkkı (A, B, C, D) ve doğru cevabı ("A", "B", "C" veya "D") olmalıdır.
        Çıktıyı KESİNLİKLE aşağıdaki JSON formatında ver, başka hiçbir açıklama metni ekleme:
        {{
            "questions": [
                {{
                    "id": 1,
                    "subject": "Ders Adı (Örn: Matematik)",
                    "question": "Soru metni burada yer alacak...",
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
        raw_json = multi_pool_generate(prompt)
        if raw_json:
            try:
                data = json.loads(raw_json)
                st.session_state.questions = data.get("questions", [])
                st.session_state.quiz_started = True
                st.session_state.start_time = time.time()
                experimental_rerun = getattr(st, "rerun", None) or getattr(st, "experimental_rerun", None)
                if experimental_rerun:
                    experimental_rerun()
            except json.JSONDecodeError:
                st.error("Yapay zeka yanıtı geçerli JSON formatına dönüştürülemedi.")
                st.code(raw_json)

# Sınav Ekranı ve Büyük Puntolu Arayüz
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
        st.markdown(f"### 📋 {term} - {selected_scope} Deneme Sınavı")
        st.markdown(f"<span class='badge'>Toplam Soru: {total_questions}</span> <span class='badge'>Soru Başı Süre: 80 Saniye</span>", unsafe_allow_html=True)
    with header_col2:
        st.markdown(f"<div class='timer-box'>⏳ {hours:02d}:{minutes:02d}:{seconds:02d}</div>", unsafe_allow_html=True)

    st.markdown("---")

    for idx, q in enumerate(st.session_state.questions):
        st.markdown(f"<div class='question-card'>", unsafe_allow_html=True)
        sub_badge = f"[{q.get('subject', 'Genel')}]" if 'subject' in q else ""
        st.markdown(f"<p class='question-title'>Soru {idx + 1} {sub_badge}: {q['question']}</p>", unsafe_allow_html=True)
        
        options = q['options']
        choice = st.radio(
            f"**Soru {idx + 1} Şıkları:**",
            options=list(options.keys()),
            format_func=lambda x: f"{x}) {options[x]}",
            key=f"q_{idx}"
        )
        st.session_state.selected_answers[idx] = choice
        st.markdown(f"</div>", unsafe_allow_html=True)

    if st.button("🏁 Deneme Sınavını Tamamla ve Sonuçları Gör"):
        correct_count, wrong_count = 0, 0
        for idx, q in enumerate(st.session_state.questions):
            if st.session_state.selected_answers.get(idx) == q['answer']:
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
            for idx, q in enumerate(st.session_state.questions):
                user_ans = st.session_state.selected_answers.get(idx)
                status = "✅" if user_ans == q['answer'] else "❌"
                st.markdown(f"**Soru {idx + 1} ({q.get('subject', '')}):** {q['question']}")
                st.markdown(f"Seçiminiz: **{user_ans}** | Doğru Cevap: **{q['answer']}** {status}")
                st.markdown("---")

    if remaining_time > 0:
        time.sleep(1)
        experimental_rerun = getattr(st, "rerun", None) or getattr(st, "experimental_rerun", None)
        if experimental_rerun:
            experimental_rerun()
    else:
        st.warning("⏰ Sınav süreniz doldu! Lütfen yanıtlarınızı kontrol edip sınavı tamamlayın.")
