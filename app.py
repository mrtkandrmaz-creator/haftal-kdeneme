import io
import os
import re
import sys
import time
import google.generativeai as genai
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
import streamlit as st
import streamlit.components.v1 as components

# --- PyInstaller için SSL ve Dosya Yolu Sabitleme ---
if getattr(sys, "frozen", False):
    os.environ["SSL_CERT_FILE"] = os.path.join(
        sys._MEIPASS, "certifi", "cacert.pem"
    )

# Sayfa Yapılandırması ve Modern UI CSS Enjeksiyonu
st.set_page_config(
    page_title="Ortaokuldan LGS Deneme Sınavı Üretici",
    page_icon="🎯",
    layout="centered",
)

st.markdown(
    """
    <style>
    .main {
        background-color: #f8f9fa;
    }
    h1 {
        color: #1e3d59;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-weight: 700;
        text-align: center;
        margin-bottom: 5px;
    }
    .subtext {
        text-align: center;
        color: #6c757d;
        font-size: 1.1rem;
        margin-bottom: 30px;
    }
    .exam-card {
        background-color: #ffffff;
        padding: 30px;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        border: 1px solid #e1e4e8;
        margin-top: 20px;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# MEB 5, 6, 7, 8. Sınıf Müfredat ve Soru Dağılımı Veritabanı
SINIF_MUFREDATLARI = {
    "5. Sınıf": {
        "aciklama": (
            "5. Sınıf Normal Dönem Deneme Sınavı (Türkçe, Matematik, Fen,"
            " Sosyal, Din, İngilizce - 10'ar Soru)"
        ),
        "soru_dagilimi": {
            "Turkce": 10,
            "Matematik": 10,
            "Fen Bilimleri": 10,
            "Sosyal Bilgiler": 10,
            "Din Kültürü": 10,
            "İngilizce": 10,
        },
        "sure_dakika": 60,
    },
    "6. Sınıf": {
        "aciklama": (
            "6. Sınıf Normal Dönem Deneme Sınavı (Türkçe, Matematik, Fen,"
            " Sosyal, Din, İngilizce - 10'ar Soru)"
        ),
        "soru_dagilimi": {
            "Turkce": 10,
            "Matematik": 10,
            "Fen Bilimleri": 10,
            "Sosyal Bilgiler": 10,
            "Din Kültürü": 10,
            "İngilizce": 10,
        },
        "sure_dakika": 60,
    },
    "7. Sınıf": {
        "aciklama": (
            "7. Sınıf Normal Dönem Deneme Sınavı (Türkçe, Matematik, Fen,"
            " Sosyal, Din, İngilizce - 15'er Soru)"
        ),
        "soru_dagilimi": {
            "Turkce": 15,
            "Matematik": 15,
            "Fen Bilimleri": 15,
            "Sosyal Bilgiler": 15,
            "Din Kültürü": 15,
            "İngilizce": 15,
        },
        "sure_dakika": 90,
    },
    "8. Sınıf (LGS)": {
        "aciklama": (
            "Resmi LGS Soru Dağılımı (Türkçe:20, Matematik:20, Fen:20, İnkılap:10,"
            " Din:10, İngilizce:10 - Toplam 90 Soru)"
        ),
        "soru_dagilimi": {
            "Turkce": 20,
            "Matematik": 20,
            "Fen Bilimleri": 20,
            "T.C. İnkılap Tarihi": 10,
            "Din Kültürü": 10,
            "İngilizce": 10,
        },
        "sure_dakika": 155,
    },
}

# Haftalık Konu / Kazanım Veritabanı
HAFTALIK_ICERIKLER = {
    1: "1. Hafta Kazanımları: Temel kavramlara giriş, metin türleri, doğal sayılar/işlemler, güneşin yapısı ve özellikleri, birey ve toplum, ilahi kitaplar inancı, karşılama ve tanışma kalıpları.",
    2: "2. Hafta Kazanımları: Sözcükte anlam, kesirler, dünyamızın hareketi, sosyal rollerimiz, melekler ve ahiret inancı, günlük rutinler.",
    3: "3. Hafta Kazanımları: Cümlede anlam, ondalık gösterimler, canlılar ve yaşam, kültürel mirasımız, ibadet esasları, hava durumu ve doğa.",
    4: "🌟 4. HAFTA: AYLIK GENEL TARAMA VE DEĞERLENDİRME SINAVI (1., 2. ve 3. haftaların tüm kazanımlarını kapsayan kapsamlı genel tekrar sınavı).",
    5: "5. Hafta Kazanımları: Paragrafta anlam, oran-orantı, kuvvetin ölçülmesi, hak ve sorumluluklar, peygamberlik inancı, hobiler ve yetenekler.",
    6: "6. Hafta Kazanımları: Yazım kuralları, yüzdeler, madde ve ısı, afetler ve çevre, zekat ve sadaka ibadeti, sağlık ve rahatsızlıklar.",
    7: "7. Hafta Kazanımları: Noktalama işaretleri, cebirsel ifadeler, ışığın yayılması, üretim teknolojisi, Hz. Muhammed'in hayatı, yiyecekler ve içecekler.",
    8: "🌟 8. HAFTA: AYLIK GENEL TARAMA VE DEĞERLENDİRME SINAVI (5., 6. ve 7. haftaların tüm kazanımlarını kapsayan kapsamlı genel tekrar sınavı).",
    9: "9. Hafta Kazanımları: Metnin yapı taşları, üçgenler ve dörtgenler, ses özellikleri, Türk tarihi, Kur'an-ı Kerim ve özellikleri, seyahat ve ulaşım.",
    10: "10. Hafta Kazanımları: Anlatım bozuklukları, veri analizi, çözeltiler ve karışımlar, demokrasi tarihi, din ve ahlak ilişkisi, teknolojik aletler.",
    11: "11. Hafta Kazanımları: Sözel mantık becerileri, doğrusal denklemler, elektrik devreleri, uluslararası ilişkiler, İslam düşünce yorumları, çevre bilinci.",
    12: "🌟 12. HAFTA: AYLIK GENEL TARAMA VE DEĞERLENDİRME SINAVI (9., 10. ve 11. haftaların tüm kazanımlarını kapsayan kapsamlı genel tekrar sınavı).",
    13: "13. Hafta Kazanımları: İleri düzey okuma ve yorumlama, eşitsizlikler, basit makineler, küresel sorunlar, ahlaki erdemler, kariyer ve meslekler.",
    14: "14. Hafta Kazanımları: Görsel okuma ve grafik yorumlama, dönüşüm geometrisi, DNA ve genetik kod, ekonomi ve ticaret, inanç esasları derinlemesine, gelecek planları.",
    15: "15. Hafta Kazanımları: Mantıksal muhakeme, katı cisimler, iklim ve hava olayları, hukuk devleti bilinci, evrensel değerler, popüler kültür.",
    16: "🌟 16. HAFTA: AYLIK GENEL TARAMA VE DEĞERLENDİRME SINAVI (13., 14. ve 15. haftaların tüm kazanımlarını kapsayan kapsamlı genel tekrar sınavı).",
    17: "17. Hafta Kazanımları: LGS beceri temelli karma soru provası, genel deneme hazırlık ve eksik giderme çalışmaları.",
    18: "🌟 18. HAFTA: DÖNEM SONU GENEL KAPANIŞ VE GELİŞMİŞ TARAMA SINAVI (Tüm dönemin kazanımlarını kapsayan final düzeyinde deneme).",
}


# --- Otomatik Model Tarayan ve Uygun Olanı Seçen Akıllı Bağlantı ---
def ai_icerik_uret(prompt: str) -> str:
    gemini_key = st.secrets.get("GEMINI_API_KEY", "")
    if not gemini_key:
        raise RuntimeError("GEMINI_API_KEY anahtarı Streamlit Secrets içinde bulunamadı!")

    genai.configure(api_key=gemini_key)
    
    uygun_modeller = []
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                uygun_modeller.append(m.name)
    except Exception:
        pass

    yedek_liste = [
        "gemini-2.5-flash",
        "gemini-3.8-flash",
        "gemini-3.6-flash",
        "gemini-1.5-flash",
        "gemini-1.5-pro",
        "gemini-pro"
    ]
    
    tum_denenecekler = []
    for mod in uygun_modeller + yedek_liste:
        if mod not in tum_denenecekler:
            tum_denenecekler.append(mod)

    son_hata = None
    for model_adi in tum_denenecekler:
        try:
            model = genai.GenerativeModel(model_adi)
            response = model.generate_content(prompt)
            if response and response.text:
                return response.text
        except Exception as e:
            son_hata = e
            continue

    raise RuntimeError(f"Hesabınızın erişebileceği uygun Gemini modeli bulunamadı veya tüm denemeler başarısız oldu. Son Hata: {son_hata}")


# Soru Ayrıştırma Yardımcısı (Her sayfada 1 soru gösterebilmek için metni parçalar)
def soruları_ayristir(tam_metin):
    # Ders başlıklarını ve soruları regex ile ayıklama
    parcalar = []
    # Örnek soru formatı: "1. Soru metni..." veya "1-) ..."
    soru_bloklari = re.split(r'\n(?=\d+[\.\)]\s)', tam_metin)
    
    for blok in soru_bloklari:
        match = re.match(r'^(\d+)[\.\)]\s*(.*)', blok.strip(), re.DOTALL)
        if match:
            soru_no = int(match.group(1))
            soru_icerik = match.group(2)
            parcalar.append({"no": soru_no, "metin": soru_icerik})
    return parcalar


# Standart PDF Dönüştürücü
def create_pdf(text, sinif_adi):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )
    styles = getSampleStyleSheet()
    normal_style = styles["Normal"]
    normal_style.fontSize = 9
    normal_style.leading = 13

    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Heading1"],
        fontSize=13,
        leading=16,
        alignment=1,
        spaceAfter=15,
    )

    story = [
        Paragraph(
            f"<b>{sinif_adi.upper()} MERKEZİ SİSTEM DENEME SINAVI</b>",
            title_style,
        ),
        Spacer(1, 10),
    ]

    for line in text.split("\n"):
        if line.strip():
            safe_line = (
                line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            )
            story.append(Paragraph(safe_line, normal_style))
            story.append(Spacer(1, 3))
        else:
            story.append(Spacer(1, 6))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()


# Resmi Kitapçık Formatında PDF Üretici
def create_official_booklet_pdf(text, sinif_adi, donem, hafta_str):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=35,
        leftMargin=35,
        topMargin=35,
        bottomMargin=35,
    )
    styles = getSampleStyleSheet()

    cover_title_style = ParagraphStyle(
        "CoverTitle",
        parent=styles["Heading1"],
        fontSize=14,
        leading=18,
        alignment=1,
        spaceAfter=6,
        fontName="Helvetica-Bold",
    )
    cover_sub_style = ParagraphStyle(
        "CoverSub",
        parent=styles["Normal"],
        fontSize=10,
        leading=14,
        alignment=1,
        spaceAfter=20,
        fontName="Helvetica",
    )
    question_style = ParagraphStyle(
        "QuestionStyle",
        parent=styles["Normal"],
        fontSize=8.5,
        leading=12,
        spaceAfter=8,
        fontName="Helvetica",
    )

    story = [
        Paragraph(
            f"T.C. MİLLÎ EĞİTİM BAKANLIĞI<br/><b>{sinif_adi.upper()} DÜZEYİ ÖRNEK SORU KİTAPÇIĞI</b>",
            cover_title_style,
        ),
        Paragraph(
            f"<b>{donem} - {hafta_str}</b><br/>Bu kitapçık resmi sınav formatına uygun olarak hazırlanmıştır.",
            cover_sub_style,
        ),
        Spacer(1, 10),
    ]

    for line in text.split("\n"):
        if line.strip():
            safe_line = (
                line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            )
            story.append(Paragraph(safe_line, question_style))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()


# --- Streamlit Arayüzü ---
st.markdown(
    "<h1>🎯 Ortaokul ve LGS Deneme Sınavı Üretici</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p class='subtext'>MEB Müfredatına ve Kazanımlarına Uygun Sınav Sistemi.</p>",
    unsafe_allow_html=True,
)

# Sol Menü (Sidebar) Ayarları
st.sidebar.header("🗓️ Sınav Kriterleri")

sinif_secimi = st.sidebar.selectbox(
    "Sınıf Düzeyi Seçin", list(SINIF_MUFREDATLARI.keys())
)
donem_secimi = st.sidebar.selectbox("Dönem Seçin", ["1. Dönem", "2. Dönem"])

hafta_secenekleri = [f"{i}. Hafta" for i in range(1, 19)]
hafta_secimi_str = st.sidebar.selectbox(
    "Hafta / Tarama Seçin", hafta_secenekleri
)

secilen_hafta_num = int(hafta_secimi_str.split(".")[0])
ilgili_kazanimlar = HAFTALIK_ICERIKLER.get(
    secilen_hafta_num, "Standart müfredat kazanımları."
)

st.sidebar.markdown("---")
st.sidebar.markdown(f"### 📚 Seçilen Sınav Yapısı ({sinif_secimi})")
secilen_bilgi = SINIF_MUFREDATLARI[sinif_secimi]
st.sidebar.markdown(f"📌 **Format:** {secilen_bilgi['aciklama']}")
st.sidebar.markdown(f"📖 **Haftalık Kapsam:** {ilgili_kazanimlar}")
st.sidebar.markdown(f"⏱ **Süre:** {secilen_bilgi['sure_dakika']} Dakika")

st.sidebar.markdown("---")
toplam_soru = sum(secilen_bilgi["soru_dagilimi"].values())
st.sidebar.markdown(f"🎯 **Toplam Soru Sayısı:** {toplam_soru} Soru")

# Üretim Butonu
if st.sidebar.button(
    f"✨ {sinif_secimi} Sınavını Üret",
    type="primary",
    use_container_width=True,
):
    is_tarama = (
        secilen_hafta_num in [4, 8, 12, 16, 18]
        or "TARAMA" in ilgili_kazanimlar
    )
    sinav_tip_str = (
        "AYLIK GENEL TARAMA VE TEKRAR SINAVI"
        if is_tarama
        else f"HAFTALIK DENEME SINAVI ({hafta_secimi_str})"
    )

    dersler = secilen_bilgi["soru_dagilimi"]
    toplam_ders_sayisi = len(dersler)

    progress_bar = st.progress(0)
    status_text = st.empty()

    try:
        uretilen_metinler = [
            f"=== {sinif_secimi.upper()} - {donem_secimi} {hafta_secimi_str} ({sinav_tip_str}) ===\n"
        ]

        adim = 0
        for ders_adi, soru_adedi in dersler.items():
            adim += 1
            status_text.text(
                f"⚡ ({adim}/{toplam_ders_sayisi}) {ders_adi} dersi ({soru_adedi} soru) hazırlanıyor..."
            )

            prompt = f"""
            Sen uzman bir MEB müfredat rehber öğretmeni ve soru yazarısın. 
            {sinif_secimi} seviyesi, {donem_secimi} {hafta_secimi_str} kapsamı ve şu kazanımlar için:
            Kazanım/İçerik: {ilgili_kazanimlar}
            
            YALNIZCA VE SADECE **{ders_adi}** dersi için tam olarak **{soru_adedi}** adet özgün, MEB yeni nesil mantık-muhakeme çoktan seçmeli (A, B, C, D şıklı) soru hazırla.
            Soruların numaralandırmasını 1'den {soru_adedi}'ne kadar yap. Başka hiçbir dersin sorusunu ekleme.
            """

            ders_yaniti = ai_icerik_uret(prompt)

            uretilen_metinler.append(
                f"\n\n--- {ders_adi.upper()} ({soru_adedi} SORU) ---\n" + ders_yaniti
            )
            progress_bar.progress(adim / toplam_ders_sayisi)
            time.sleep(0.3)

        status_text.text(
            "📝 Tüm dersler tamamlandı, cevap anahtarı ve çözümler ekleniyor..."
        )
        cozum_prompt = f"""
        Yukarıda soruları hazırlanan {sinif_secimi} {hafta_secimi_str} ({donem_secimi}) deneme sınavı için;
        Tüm derslerin soru numaralarına karşılık gelen net bir **CEVAP ANAHTARI** ve kısa **ÇÖZÜM AÇIKLAMALARI** hazırla.
        """
        cozum_yaniti = ai_icerik_uret(cozum_prompt)
        uretilen_metinler.append(
            "\n\n--- CEVAP ANAHTARI VE ÇÖZÜMLER ---\n" + cozum_yaniti
        )

        progress_bar.progress(1.0)
        status_text.empty()

        st.session_state["sinav_metni"] = "\n".join(uretilen_metinler)
        st.session_state["aktif_sinif"] = sinif_secimi
        st.session_state["sinav_baslatildi"] = False
        st.session_state["aktif_soru_index"] = 0
        st.success(
            f"🎉 {sinif_secimi} - {hafta_secimi_str} Sınavı başarıyla oluşturuldu!"
        )

    except Exception as e:
        st.error(f"Sınav üretilirken bir hata oluştu: {e}")

# Sınav İçeriğini ve Başlatma Mantığını Yönetme
if "sinav_metni" in st.session_state:
    aktif_sinif = st.session_state.get("aktif_sinif", sinif_secimi)
    sure_dk = SINIF_MUFREDATLARI[aktif_sinif]["sure_dakika"]
    total_seconds = sure_dk * 60

    if not st.session_state.get("sinav_baslatildi", False):
        st.markdown("---")
        col_b1, col_b2, col_b3 = st.columns([1, 2, 1])
        with col_b2:
            if st.button(
                "🚀 Sınavı Başlat ve Süreyi Başlat",
                type="primary",
                use_container_width=True,
            ):
                st.session_state["sinav_baslatildi"] = True
                st.session_state["aktif_soru_index"] = 0
                st.rerun()

        st.info(
            "💡 Sınavınız hazır! Süreyi ve soruları her sayfada tek soru olacak şekilde görüntülemek için yukarıdaki **Sınavı Başlat** butonuna tıklayın."
        )

    if st.session_state.get("sinav_baslatildi", False):
        timer_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
        <style>
          .timer-container {{
              background: linear-gradient(135deg, #1e3d59 0%, #17b978 100%);
              color: white;
              padding: 22px;
              border-radius: 14px;
              text-align: center;
              font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
              box-shadow: 0 6px 20px rgba(0,0,0,0.08);
              margin-bottom: 25px;
          }}
          .timer-title {{
              font-size: 1.15rem;
              font-weight: 600;
              margin-bottom: 8px;
              letter-spacing: 0.5px;
              text-transform: uppercase;
          }}
          .timer-display {{
              font-size: 3.2rem;
              font-weight: 800;
              letter-spacing: 3px;
              font-variant-numeric: tabular-nums;
              text-shadow: 0 2px 5px rgba(0,0,0,0.2);
          }}
          .timer-controls {{
              margin-top: 15px;
          }}
          .btn {{
              background-color: white;
              color: #1e3d59;
              border: none;
              padding: 8px 18px;
              border-radius: 6px;
              font-weight: bold;
              cursor: pointer;
              margin: 0 6px;
              transition: 0.2s;
              font-size: 0.95rem;
          }}
          .btn:hover {{
              background-color: #f1f3f5;
              transform: translateY(-1px);
          }}
        </style>
        </head>
        <body>
          <div class="timer-container">
            <div class="timer-title">⏱️ Resmi Sınav Simülasyon Süresi ({sure_dk} Dakika)</div>
            <div class="timer-display" id="clock">00:00:00</div>
            <div class="timer-controls">
              <button class="btn" onclick="toggleTimer()" id="startBtn">Başlat / Durdur</button>
              <button class="btn" onclick="resetTimer()">Sıfırla</button>
            </div>
          </div>

          <script>
            let totalSeconds = {total_seconds};
            let timeLeft = totalSeconds;
            let timerId = null;
            let isRunning = false;

            function updateDisplay() {{
                let hours = Math.floor(timeLeft / 3600);
                let minutes = Math.floor((timeLeft % 3600) / 60);
                let secs = timeLeft % 60;
                document.getElementById('clock').innerText = 
                    String(hours).padStart(2, '0') + ':' + 
                    String(minutes).padStart(2, '0') + ':' + 
                    String(secs).padStart(2, '0');
            }}

            function startTimer() {{
                if (!isRunning) {{
                    isRunning = true;
                    timerId = setInterval(() => {{
                        if (timeLeft > 0) {{
                            timeLeft--;
                            updateDisplay();
                        }} else {{
                            clearInterval(timerId);
                            alert("Sınav Süresi Bitti!");
                            isRunning = false;
                        }}
                    }}, 1000);
                }}
            }}

            function toggleTimer() {{
                if (isRunning) {{
                    clearInterval(timerId);
                    isRunning = false;
                }} else {{
                    startTimer();
                }}
            }}

            function resetTimer() {{
                clearInterval(timerId);
                isRunning = false;
                timeLeft = totalSeconds;
                updateDisplay();
            }}

            updateDisplay();
            startTimer();
          </script>
        </body>
        </html>
        """

        components.html(timer_html, height=195)

        # Soruları ve Bölümleri Ayıkla
        metin = st.session_state["sinav_metni"]
        bulunan_sorular = soruları_ayristir(metin)

        if bulunan_sorular:
            if "aktif_soru_index" not in st.session_state:
                st.session_state["aktif_soru_index"] = 0

            toplam_bulunan = len(bulunan_sorular)
            
            # Güvenli index kontrolü
            if st.session_state["aktif_soru_index"] >= toplam_bulunan:
                st.session_state["aktif_soru_index"] = toplam_bulunan - 1

            current_idx = st.session_state["aktif_soru_index"]
            soru_obj = bulunan_sorular[current_idx]

            st.markdown("<div class='exam-card'>", unsafe_allow_html=True)
            st.subheader(f"📝 Soru {current_idx + 1} / {toplam_bulunan}")
            st.markdown(f"**Soru {soru_obj['no']}**")
            st.markdown(soru_obj['metin'])
            
            # Öğrencinin interaktif cevap verebilmesi için şık seçimi
            st.radio(
                "Cevabınız:", 
                ["Seçiniz...", "A", "B", "C", "D"], 
                key=f"cevap_{current_idx}",
                horizontal=True
            )
            st.markdown("</div>", unsafe_allow_html=True)

            # İlerleme Butonları
            col_nav1, col_nav2, col_nav3 = st.columns([1, 2, 1])
            with col_nav1:
                if current_idx > 0:
                    if st.button("⬅️ Önceki Soru", use_container_width=True):
                        st.session_state["aktif_soru_index"] -= 1
                        st.rerun()
            with col_nav3:
                if current_idx < toplam_bulunan - 1:
                    if st.button("Sonraki Soru ➡️", use_container_width=True):
                        st.session_state["aktif_soru_index"] += 1
                        st.rerun()
                else:
                    if st.button("🏁 Sınavı Bitir", type="primary", use_container_width=True):
                        st.success("Sınavı tamamladınız! Çözümleri ve cevap anahtarını aşağıdan kontrol edebilirsiniz.")
        else:
            # Yedek görünüm (Eğer ayrıştırılamazsa tüm metin gösterilir)
            st.markdown("<div class='exam-card'>", unsafe_allow_html=True)
            st.subheader(f"📝 Oluşturulan {aktif_sinif} Sınavı ({hafta_secimi_str})")
            st.markdown(st.session_state["sinav_metni"])
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("### 📥 Sınav Çıktı Seçenekleri")
        col1, col2 = st.columns(2)

        with col1:
            pdf_bytes = create_pdf(st.session_state["sinav_metni"], aktif_sinif)
            st.download_button(
                label="📄 Standart Sınav PDF İndir",
                data=pdf_bytes,
                file_name=f"{aktif_sinif.replace(' ', '_')}_Deneme_{donem_secimi}_{hafta_secimi_str.replace(' ', '_')}.pdf",
                mime="application/pdf",
                use_container_width=True,
            )

        with col2:
            booklet_bytes = create_official_booklet_pdf(
                st.session_state["sinav_metni"],
                aktif_sinif,
                donem_secimi,
                hafta_secimi_str,
            )
            st.download_button(
                label="📘 Resmi Sınav Kitapçığı PDF İndir",
                data=booklet_bytes,
                file_name=f"{aktif_sinif.replace(' ', '_')}_Resmi_Kitapcik_{donem_secimi}_{hafta_secimi_str.replace(' ', '_')}.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
