import io
import os
import re
import sys
import time
import requests
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
import streamlit as st

# --- Groq API Anahtarınız ---
GROQ_API_KEY_DIRECT = "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"

# --- PyInstaller için SSL ve Dosya Yolu Sabitleme ---
if getattr(sys, "frozen", False):
    os.environ["SSL_CERT_FILE"] = os.path.join(
        sys._MEIPASS, "certifi", "cacert.pem"
    )

# Sayfa Yapılandırması ve Modern UI CSS Enjeksiyonu
st.set_page_config(
    page_title="Ortaokul dan LGS 60 Soruluk Deneme Sınavı Üretici",
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

# MEB Müfredatına Uygun 60 Soruluk Sınav Dağılımı Veritabanı
SINIF_MUFREDATLARI = {
    "5. Sınıf": {
        "aciklama": "60 Soruluk Kapsamlı Deneme Sınavı (Türkçe:10, Matematik:10, Fen:10, Sosyal:10, Din:10, İngilizce:10)",
        "soru_dagilimi": {
            "Türkçe": 10,
            "Matematik": 10,
            "Fen Bilimleri": 10,
            "Sosyal Bilgiler": 10,
            "Din Kültürü": 10,
            "İngilizce": 10,
        },
        "sure_dakika": 90,
    },
    "6. Sınıf": {
        "aciklama": "60 Soruluk Kapsamlı Deneme Sınavı (Türkçe:10, Matematik:10, Fen:10, Sosyal:10, Din:10, İngilizce:10)",
        "soru_dagilimi": {
            "Türkçe": 10,
            "Matematik": 10,
            "Fen Bilimleri": 10,
            "Sosyal Bilgiler": 10,
            "Din Kültürü": 10,
            "İngilizce": 10,
        },
        "sure_dakika": 90,
    },
    "7. Sınıf": {
        "aciklama": "60 Soruluk Kapsamlı Deneme Sınavı (Türkçe:10, Matematik:10, Fen:10, Sosyal:10, Din:10, İngilizce:10)",
        "soru_dagilimi": {
            "Türkçe": 10,
            "Matematik": 10,
            "Fen Bilimleri": 10,
            "Sosyal Bilgiler": 10,
            "Din Kültürü": 10,
            "İngilizce": 10,
        },
        "sure_dakika": 100,
    },
    "8. Sınıf (LGS)": {
        "aciklama": "60 Soruluk LGS Deneme Sınavı (Türkçe:10, Matematik:10, Fen:10, T.C. İnkılap:10, Din:10, İngilizce:10)",
        "soru_dagilimi": {
            "Türkçe": 10,
            "Matematik": 10,
            "Fen Bilimleri": 10,
            "T.C. İnkılap Tarihi": 10,
            "Din Kültürü": 10,
            "İngilizce": 10,
        },
        "sure_dakika": 100,
    },
}

HAFTALIK_ICERIKLER = {
    1: "1. Hafta Kazanımları: Temel kavramlara giriş, metin türleri, doğal sayılar/işlemler, güneşin yapısı ve özellikleri.",
    2: "2. Hafta Kazanımları: Sözcükte anlam, kesirler, dünyamızın hareketi, sosyal rollerimiz, melekler ve ahiret inancı.",
    3: "3. Hafta Kazanımları: Cümlede anlam, ondalık gösterimler, canlılar ve yaşam, ibadet esasları.",
    4: "🌟 4. HAFTA: AYLIK GENEL TARAMA VE DEĞERLENDİRME SINAVI.",
    5: "5. Hafta Kazanımları: Paragrafta anlam, oran-orantı, kuvvetin ölçülmesi, hak ve sorumluluklar.",
    6: "6. Hafta Kazanımları: Yazım kuralları, yüzdeler, madde ve ısı, afetler ve çevre.",
    7: "7. Hafta Kazanımları: Noktalama işaretleri, cebirsel ifadeler, ışığın yayılması, Hz. Muhammed'in hayatı.",
    8: "🌟 8. HAFTA: AYLIK GENEL TARAMA VE DEĞERLENDİRME SINAVI.",
    9: "9. Hafta Kazanımları: Üçgenler, dik açı, eşkenar üçgen, ikizkenar üçgen, açı ölçüleri, veri analizi ve grafik yorumlama.",
    10: "10. Hafta Kazanımları: Anlatım bozuklukları, veri analizi, çözeltiler ve karışımlar, demokrasi tarihi.",
    11: "11. Hafta Kazanımları: Sözel mantık, doğrusal denklemler, elektrik devreleri, uluslararası ilişkiler.",
    12: "🌟 12. HAFTA: AYLIK GENEL TARAMA VE DEĞERLENDİRME SINAVI.",
    13: "13. Hafta Kazanımları: Okuma yorumlama, eşitsizlikler, basit makineler, küresel sorunlar.",
    14: "14. Hafta Kazanımları: Görsel okuma, dönüşüm geometrisi, DNA ve genetik kod, ekonomi ve ticaret.",
    15: "15. Hafta Kazanımları: Mantıksal muhakeme, katı cisimler, iklim ve hava olayları, hukuk bilinci.",
    16: "🌟 16. HAFTA: AYLIK GENEL TARAMA VE DEĞERLENDİRME SINAVI.",
    17: "17. Hafta Kazanımları: LGS beceri temelli karma soru provası.",
    18: "🌟 18. HAFTA: DÖNEM SONU GENEL KAPANIŞ VE GELİŞMİŞ TARAMA SINAVI.",
}

# --- Güncellenmiş ve Temizlenmiş Akıllı API Fonksiyonu ---
def ai_icerik_uret(prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY_DIRECT}",
        "Content-Type": "application/json"
    }
    
    aktif_modeller = []
    try:
        models_res = requests.get("https://api.groq.com/openai/v1/models", headers=headers, timeout=10)
        if models_res.status_code == 200:
            data = models_res.json()
            for m in data.get("data", []):
                model_id = m["id"].lower()
                # Yalnızca güncel metin/sohbet modellerini al; guard, embed, whisper ve eski sürümleri hariç tut
                if any(k in model_id for k in ["llama-3", "mixtral", "gemma"]) and not any(x in model_id for x in ["guard", "embed", "whisper", "vision-preview", "8192"]):
                    aktif_modeller.append(m["id"])
    except Exception:
        pass
        
    # Dinamik çekilemezse veya filtrelendiyse yalnızca %100 güncel ve aktif yedek liste
    if not aktif_modeller:
        aktif_modeller = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"]

    chat_url = "https://api.groq.com/openai/v1/chat/completions"
    son_hata = ""
    
    for model_adi in aktif_modeller:
        payload = {
            "model": model_adi,
            "messages": [
                {"role": "system", "content": "Sen uzman bir MEB müfredat rehber öğretmeni ve LGS soru yazarısın."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 4000
        }

        try:
            response = requests.post(chat_url, json=payload, headers=headers, timeout=60)
            if response.status_code == 200:
                data = response.json()
                return data["choices"][0]["message"]["content"]
            else:
                son_hata = f"Model ({model_adi}) HTTP {response.status_code}: {response.text}"
        except Exception as e:
            son_hata = str(e)
            
    raise RuntimeError(f"Tüm geçerli Groq dil modelleri denendi ancak erişilemedi. Son hata: {son_hata}")

def soruları_ayristir(tam_metin):
    parcalar = []
    soru_bloklari = re.split(r'\n(?=\d+[\.\)]\s)', tam_metin)
    
    for blok in soru_bloklari:
        match = re.match(r'^(\d+)[\.\)]\s*(.*)', blok.strip(), re.DOTALL)
        if match:
            soru_no = int(match.group(1))
            soru_icerik = match.group(2)
            parcalar.append({"no": soru_no, "metin": soru_icerik})
    return parcalar

def build_exam_pdf(text, sinif_adi):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=25,
        leftMargin=25,
        topMargin=25,
        bottomMargin=25,
    )
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Heading1"],
        fontSize=12,
        leading=14,
        alignment=1,
        spaceAfter=10,
        fontName="Helvetica-Bold",
    )
    
    q_style = ParagraphStyle(
        "ExamQuestionStyle",
        parent=styles["Normal"],
        fontSize=8,
        leading=11,
        spaceAfter=2,
        fontName="Helvetica-Bold",
    )

    story = [
        Paragraph(f"<b>{sinif_adi.upper()} 60 SORULUK MERKEZİ SİSTEM DENEME SINAVI</b>", title_style),
        Spacer(1, 5),
    ]

    sorular = soruları_ayristir(text)
    if not sorular:
        for line in text.split("\n"):
            if line.strip():
                safe_line = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                story.append(Paragraph(safe_line, q_style))
                story.append(Spacer(1, 3))
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()

    chunk_size = 8
    total_chunks = (len(sorular) + chunk_size - 1) // chunk_size
    chunk_counter = 0

    for chunk_start in range(0, len(sorular), chunk_size):
        chunk_counter += 1
        chunk_sorular = sorular[chunk_start:chunk_start + chunk_size]
        row_data = []
        for i in range(0, len(chunk_sorular), 2):
            s1 = chunk_sorular[i]
            s1_text = f"<b>{s1['no']}.</b> {s1['metin']}"
            s1_text = re.sub(r'([A-D]\))', r'<br/>\1', s1_text)
            s1_text = s1_text.replace("\n", " ").replace("<br/><br/>", "<br/>")
            s1_text = s1_text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            s1_text = s1_text.replace("&lt;br/&gt;", "<br/>").replace("&lt;b&gt;", "<b>").replace("&lt;/b&gt;", "</b>")
            p1 = Paragraph(s1_text, q_style)

            p2 = ""
            if i + 1 < len(chunk_sorular):
                s2 = chunk_sorular[i + 1]
                s2_text = f"<b>{s2['no']}.</b> {s2['metin']}"
                s2_text = re.sub(r'([A-D]\))', r'<br/>\1', s2_text)
                s2_text = s2_text.replace("\n", " ").replace("<br/><br/>", "<br/>")
                s2_text = s2_text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                s2_text = s2_text.replace("&lt;br/&gt;", "<br/>").replace("&lt;b&gt;", "<b>").replace("&lt;/b&gt;", "</b>")
                p2 = Paragraph(s2_text, q_style)

            row_data.append([p1, p2])

        if row_data:
            t = Table(row_data, colWidths=[270, 270])
            t.setStyle(TableStyle([
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('LEFTPADDING', (0,0), (-1,-1), 4),
                ('RIGHTPADDING', (0,0), (-1,-1), 4),
                ('TOPPADDING', (0,0), (-1,-1), 2),
                ('BOTTOMPADDING', (0,0), (-1,-1), 4),
                ('LINEAFTER', (0,0), (-2,-1), 0.5, colors.lightgrey),
            ]))
            story.append(t)
            if chunk_counter < total_chunks:
                story.append(PageBreak())

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()


# --- Streamlit Arayüzü ---
st.markdown(
    "<h1>🎯 Ortaokul ve LGS 60 Soruluk Deneme Sınavı Üretici</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p class='subtext'>Akıllı Model Filtreli, Kesintisiz 60 Soru Üretim Sistemi.</p>",
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
    f"✨ {sinif_secimi} 60 Soruluk Sınavı Üret",
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
            f"=== {sinif_secimi.upper()} - 60 SORULUK DENEME ({donem_secimi} {hafta_secimi_str} - {sinav_tip_str}) ===\n"
        ]

        global_soru_sayaci = 1
        adim = 0
        for ders_adi, soru_adedi in dersler.items():
            adim += 1
            baslangic_no = global_soru_sayaci
            bitis_no = global_soru_sayaci + soru_adedi - 1
            
            status_text.text(
                f"⚡ ({adim}/{toplam_ders_sayisi}) {ders_adi} dersi için {baslangic_no} ile {bitis_no} arası sorular üretiliyor..."
            )

            prompt = f"""
            Sen uzman bir MEB müfredat rehber öğretmeni ve LGS soru yazarısın. 
            {sinif_secimi} seviyesi, {donem_secimi} {hafta_secimi_str} kapsamı ve şu kazanımlar için:
            Kazanım/İçerik: {ilgili_kazanimlar}
            
            YALNIZCA VE SADECE **{ders_adi}** dersi için KESİNLİKLE VE TAM OLARAK **{soru_adedi}** adet özgün soru hazırla.
            
            Çok Önemli Kurallar:
            1. Soru numaralarını KESİNLİKLE {baslangic_no}'den başlat ve sırayla tam {bitis_no}'e kadar git. Toplamda tam {soru_adedi} adet soru üretmelisin (Eksik soru asla kabul edilmez!).
            2. HER BİR SORU mutlak surette A) ... B) ... C) ... D) ... şıklarının tamamını eksiksiz içermelidir.
            3. EĞER DERS MATEMATİK İSE; soruların içinde üçgenler (eşkenar üçgen, ikizkenar üçgen, dik üçgen), dik açı, açı ölçüleri, grafikler ve tablolar gibi görsel/geometrik öğeler ASCII sembolleri, şekil açıklamaları veya koordinat şemalarıyla desteklenmelidir.
            4. Başka hiçbir dersin sorusunu bu bloğa karıştırma. Yalnızca {ders_adi} dersinin sorularını yaz.
            """

            ders_yaniti = ai_icerik_uret(prompt)

            uretilen_metinler.append(
                f"\n\n--- {ders_adi.upper()} ({baslangic_no}-{bitis_no}. SORULAR) ---\n" + ders_yaniti
            )
            global_soru_sayaci += soru_adedi
            progress_bar.progress(adim / toplam_ders_sayisi)
            time.sleep(0.2)

        status_text.text(
            "📝 Tüm dersler tamamlandı, detaylı cevap anahtarı ve çözüm açıklamaları ekleniyor..."
        )
        cozum_prompt = f"""
        Yukarıda hazırlanan {sinif_secimi} 60 soruluk {hafta_secimi_str} ({donem_secimi}) deneme sınavı için;
        1'den 60'a kadar tüm soru numaralarına karşılık gelen net bir **CEVAP ANAHTARI** ve adım adım kısa **ÇÖZÜM AÇIKLAMALARI** hazırla.
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
            f"🎉 {sinif_secimi} - 60 Soruluk {hafta_secimi_str} Sınavı başarıyla oluşturuldu!"
        )

    except Exception as e:
        st.error(f"Sınav üretilirken bir hata oluştu: {e}")

# Sınav İçeriğini ve Her Sayfada Tek Soru Gösteren Paneli Yönetme
if "sinav_metni" in st.session_state:
    aktif_sinif = st.session_state.get("aktif_sinif", sinif_secimi)
    sure_dk = SINIF_MUFREDATLARI[aktif_sinif]["sure_dakika"]
    total_seconds = sure_dk * 60

    if not st.session_state.get("sinav_baslatildi", False):
        st.markdown("---")
        col_b1, col_b2, col_b3 = st.columns([1, 2, 1])
        with col_b2:
            if st.button(
                "🚀 Sınavı Başlat ve Soruları Çöz",
                type="primary",
                use_container_width=True,
            ):
                st.session_state["sinav_baslatildi"] = True
                st.session_state["aktif_soru_index"] = 0
                st.rerun()

        st.info(
            "💡 60 soruluk sınavınız hazır! Soruları ekranda her sayfada tek soru olacak şekilde çözmek için yukarıdaki **Sınavı Başlat** butonuna tıklayın."
        )

    if st.session_state.get("sinav_baslatildi", False):
        metin = st.session_state["sinav_metni"]
        bulunan_sorular = soruları_ayristir(metin)

        if bulunan_sorular:
            if "aktif_soru_index" not in st.session_state:
                st.session_state["aktif_soru_index"] = 0

            toplam_bulunan = len(bulunan_sorular)
            
            if st.session_state["aktif_soru_index"] >= toplam_bulunan:
                st.session_state["aktif_soru_index"] = toplam_bulunan - 1

            current_idx = st.session_state["aktif_soru_index"]
            soru_obj = bulunan_sorular[current_idx]

            # Her sayfada tek soru görünümü
            st.markdown("<div class='exam-card'>", unsafe_allow_html=True)
            st.subheader(f"📝 Soru {current_idx + 1} / {toplam_bulunan}")
            st.markdown(f"**Soru {soru_obj['no']}**")
            st.markdown(soru_obj['metin'])
            
            # Doğrudan şıklardan işaretleme (A, B, C, D butonları)
            secim_kolar = st.columns(4)
            secilen_cevap_key = f"user_cevap_{current_idx}"
            
            if secilen_cevap_key not in st.session_state:
                st.session_state[secilen_cevap_key] = None

            for idx, harf in enumerate(["A", "B", "C", "D"]):
                with secim_kolar[idx]:
                    is_selected = st.session_state[secilen_cevap_key] == harf
                    btn_type = "primary" if is_selected else "secondary"
                    if st.button(f"{harf}", key=f"btn_{current_idx}_{harf}", type=btn_type, use_container_width=True):
                        st.session_state[secilen_cevap_key] = harf
                        st.rerun()

            st.markdown("</div>", unsafe_allow_html=True)

            # İlerleme / Navigasyon Butonları
            col_nav1, col_nav2, col_nav3 = st.columns([1, 2, 1])
            with col_nav1:
                if current_idx > 0:
                    if st.button("⬅ Önceki Soru", use_container_width=True):
                        st.session_state["aktif_soru_index"] -= 1
                        st.rerun()
            with col_nav3:
                if current_idx < toplam_bulunan - 1:
                    if st.button("Sonraki Soru ➡️", use_container_width=True):
                        st.session_state["aktif_soru_index"] += 1
                        st.rerun()
                else:
                    if st.button("🏁 Sınavı Tamamla", type="primary", use_container_width=True):
                        st.success("60 soruluk sınavı tamamladınız! Aşağıdan sınav kağıdını PDF olarak indirebilirsiniz.")
        else:
            st.markdown("<div class='exam-card'>", unsafe_allow_html=True)
            st.markdown(st.session_state["sinav_metni"])
            st.markdown("</div>", unsafe_allow_html=True)

        # Sınav Çıktı Seçenekleri
        st.markdown("---")
        st.markdown("### 📥 Sınav Çıktı Seçenekleri")
        col1, col2 = st.columns(2)

        with col1:
            pdf_bytes = build_exam_pdf(st.session_state["sinav_metni"], aktif_sinif)
            st.download_button(
                label="📄 Standart 60 Soru PDF İndir (İki Sütunlu Kitapçık)",
                data=pdf_bytes,
                file_name=f"{aktif_sinif.replace(' ', '_')}_60_Soruluk_Deneme_{donem_secimi}_{hafta_secimi_str.replace(' ', '_')}.pdf",
                mime="application/pdf",
                use_container_width=True,
            )

        with col2:
            booklet_bytes = build_exam_pdf(st.session_state["sinav_metni"], aktif_sinif)
            st.download_button(
                label="📘 Resmi 60 Soru Kitapçığı PDF İndir (İki Sütunlu Kitapçık)",
                data=booklet_bytes,
                file_name=f"{aktif_sinif.replace(' ', '_')}_60_Soruluk_Resmi_Kitapcik_{donem_secimi}_{hafta_secimi_str.replace(' ', '_')}.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
