import os
import re
import sys
import time
import requests
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
    page_title="Ortaokul ve LGS 80 Soruluk Deneme Sınavı Üretici",
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

# MEB Müfredatına Uygun 80 Soruluk Sınav Dağılımı Veritabanı (Her ders 10 soru x 8 ders = 80 Soru)
SINIF_MUFREDATLARI = {
    "5. Sınıf": {
        "aciklama": "80 Soruluk Kapsamlı Deneme Sınavı (8 Ders x 10 Soru)",
        "soru_dagilimi": {
            "Türkçe": 10,
            "Matematik": 10,
            "Fen Bilimleri": 10,
            "Sosyal Bilgiler": 10,
            "Din Kültürü ve Ahlak Bilgisi": 10,
            "İngilizce": 10,
            "Bilişim Teknolojileri": 10,
            "Görsel Sanatlar / Müzik Kültürü": 10,
        },
        "sure_dakika": 120,
    },
    "6. Sınıf": {
        "aciklama": "80 Soruluk Kapsamlı Deneme Sınavı (8 Ders x 10 Soru)",
        "soru_dagilimi": {
            "Türkçe": 10,
            "Matematik": 10,
            "Fen Bilimleri": 10,
            "Sosyal Bilgiler": 10,
            "Din Kültürü ve Ahlak Bilgisi": 10,
            "İngilizce": 10,
            "Bilişim Teknolojileri": 10,
            "Trafik Güvenliği": 10,
        },
        "sure_dakika": 120,
    },
    "7. Sınıf": {
        "aciklama": "80 Soruluk Kapsamlı Deneme Sınavı (8 Ders x 10 Soru)",
        "soru_dagilimi": {
            "Türkçe": 10,
            "Matematik": 10,
            "Fen Bilimleri": 10,
            "Sosyal Bilgiler": 10,
            "Din Kültürü ve Ahlak Bilgisi": 10,
            "İngilizce": 10,
            "Seçmeli Matematik ve Bilim Uygulamaları": 10,
            "Seçmeli Okuma Becerileri": 10,
        },
        "sure_dakika": 130,
    },
    "8. Sınıf (LGS)": {
        "aciklama": "80 Soruluk LGS Kapsamlı Deneme Sınavı (8 Ders x 10 Soru)",
        "soru_dagilimi": {
            "Türkçe": 10,
            "Matematik": 10,
            "Fen Bilimleri": 10,
            "T.C. İnkılap Tarihi ve Atatürkçülük": 10,
            "Din Kültürü ve Ahlak Bilgisi": 10,
            "İngilizce": 10,
            "LGS Beceri Temelli Mantık Muhakeme": 10,
            "LGS Sözel-Sayısal Karma Prova": 10,
        },
        "sure_dakika": 130,
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

# --- Kesin Çözümlü, Güncel Modelleri İçeren Akıllı API Fonksiyonu ---
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
                if not any(x in model_id for x in ["guard", "embed", "whisper", "vision-preview", "safeguard"]):
                    aktif_modeller.append(m["id"])
    except Exception:
        pass
        
    if not aktif_modeller:
        aktif_modeller = ["openai/gpt-oss-120b", "openai/gpt-oss-20b", "qwen/qwen3.8-27b"]

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
    # Metni satır satır veya soru kalıplarına göre ayırıp soru metni ile şıkları birbirinden ayıralım
    soru_bloklari = re.split(r'\n(?=\d+[\.\)]\s)', tam_metin)
    
    for blok in soru_bloklari:
        match = re.match(r'^(\d+)[\.\)]\s*(.*)', blok.strip(), re.DOTALL)
        if match:
            soru_no = int(match.group(1))
            icerik = match.group(2)
            
            # Soru metni içindeki A), B), C), D) şıklarını ayıklayalım ki metin içinde tekrarlanmasınlar
            # Şıkları bulmak için regex kalıbı
            siklar_pattern = re.compile(r'([A-D][\.\)]\s.*?)(?=[A-D][\.\)]\s|$)', re.DOTALL)
            bulunan_siklar = siklar_pattern.findall(icerik)
            
            # Asıl soru metnini şıklardan arındıralım
            temiz_soru_metni = re.sub(r'[A-D][\.\)]\s.*', '', icerik).strip()
            
            if not bulunan_siklar:
                # Alternatif şık bulma yöntemi
                parts = re.split(r'(?=[A-D]\))', icerik)
                if len(parts) > 1:
                    temiz_soru_metni = parts[0].strip()
                    bulunan_siklar = [p.strip() for p in parts[1:] if p.strip()]

            parcalar.append({
                "no": soru_no,
                "metin": temiz_soru_metni if temiz_soru_metni else icerik,
                "siklar": bulunan_siklar if bulunan_siklar else ["A) ...", "B) ...", "C) ...", "D) ..."]
            })
    return parcalar


# --- Streamlit Arayüzü ---
st.markdown(
    "<h1>🎯 Ortaokul ve LGS 80 Soruluk Deneme Sınavı Üretici</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p class='subtext'>Sıralı Ders Akışlı, İnteraktif Soru Çözüm Paneli (80 Soru).</p>",
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
    f"✨ {sinif_secimi} 80 Soruluk Sınavı Üret",
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
            f"=== {sinif_secimi.upper()} - 80 SORULUK DENEME ({donem_secimi} {hafta_secimi_str} - {sinav_tip_str}) ===\n"
        ]

        global_soru_sayaci = 1
        adim = 0
        for ders_adi, soru_adedi in dersler.items():
            adim += 1
            baslangic_no = global_soru_sayaci
            bitis_no = global_soru_sayaci + soru_adedi - 1
            
            status_text.text(
                f"⚡ ({adim}/{toplam_ders_sayisi}) Sıralı Ders: {ders_adi} için {baslangic_no} ile {bitis_no} arası sorular üretiliyor..."
            )

            prompt = f"""
            Sen uzman bir MEB müfredat rehber öğretmeni ve LGS soru yazarısın. 
            {sinif_secimi} seviyesi, {donem_secimi} {hafta_secimi_str} kapsamı ve şu kazanımlar için:
            Kazanım/İçerik: {ilgili_kazanimlar}
            
            YALNIZCA VE SADECE **{ders_adi}** dersi için KESİNLİKLE VE TAM OLARAK **{soru_adedi}** adet özgün soru hazırla.
            
            Çok Önemli Kurallar:
            1. Soru numaralarını KESİNLİKLE {baslangic_no}'den başlat ve sırayla tam {bitis_no}'e kadar git. Toplamda tam {soru_adedi} adet soru üretmelisin!
            2. HER BİR SORU mutlak surette A) ... B) ... C) ... D) ... şıklarının tamamını eksiksiz içermelidir.
            3. EĞER DERS MATEMATİK VEYA SAYISAL İSE; soruların içinde üçgenler, geometrik şekiller, grafikler ve tablolar ASCII sembolleri veya şekil açıklamalarıyla desteklenmelidir.
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
            "📝 Tüm sıralı dersler tamamlandı, detaylı cevap anahtarı ve çözüm açıklamaları ekleniyor..."
        )
        cozum_prompt = f"""
        Yukarıda hazırlanan {sinif_secimi} 80 soruluk {hafta_secimi_str} ({donem_secimi}) deneme sınavı için;
        1'den 80'e kadar tüm soru numaralarına karşılık gelen net bir **CEVAP ANAHTARI** ve adım adım kısa **ÇÖZÜM AÇIKLAMALARI** hazırla.
        """
        cozum_yaniti = ai_icerik_uret(cozum_prompt)
        uretilen_metinler.append(
            "\n\n--- CEVAP ANAHTARI VE ÇÖZÜMLER ---\n" + cozum_yaniti
        )

        progress_bar.progress(1.0)
        status_text.empty()

        st.session_state["sinav_metni"] = "\n".join(uretilen_metinler)
        st.session_state["aktif_sinif"] = sinif_secimi
        st.session_state["aktif_soru_index"] = 0
        st.success(
            f"🎉 {sinif_secimi} - 80 Soruluk Sıralı Deneme Sınavı başarıyla oluşturuldu!"
        )

    except Exception as e:
        st.error(f"Sınav üretilirken bir hata oluştu: {e}")

# --- İnteraktif Soru Çözüm Paneli (Her Sayfada Tek Soru ve Düzgün Şık İşaretleme) ---
if "sinav_metni" in st.session_state:
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

        st.markdown("---")
        st.markdown("### 📝 Soru Çözüm Paneli (Sıralı Ders Akışı - Her Sayfada Tek Soru)")

        # Soru Kartı
        st.markdown("<div class='exam-card'>", unsafe_allow_html=True)
        st.markdown(f"#### Soru {current_idx + 1} / {toplam_bulunan} (Soru No: {soru_obj['no']})")
        
        # Soru metni
        soru_icerik_metni = soru_obj['metin'].replace('\n', '<br>')
        st.markdown(f"<div style='font-size: 1.05rem; line-height: 1.6; margin-bottom: 20px;'>{soru_icerik_metni}</div>", unsafe_allow_html=True)
        
        # Şıkların metin halleri varsa gösterelim
        if soru_obj['siklar']:
            st.markdown("<div style='background-color: #f1f3f5; padding: 15px; border-radius: 8px; margin-bottom: 20px;'>", unsafe_allow_html=True)
            for sik in soru_obj['siklar']:
                st.markdown(f"<p style='margin: 5px 0; font-size: 1rem;'>{sik}</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # Şık İşaretleme Alanı (A, B, C, D Butonları)
        st.markdown("**Cevabınızı İşaretleyin:**")
        secim_kolonlari = st.columns(4)
        secilen_cevap_key = f"user_cevap_{current_idx}"
        
        if secilen_cevap_key not in st.session_state:
            st.session_state[secilen_cevap_key] = None

        for idx, harf in enumerate(["A", "B", "C", "D"]):
            with secim_kolonlari[idx]:
                is_selected = st.session_state[secilen_cevap_key] == harf
                btn_type = "primary" if is_selected else "secondary"
                if st.button(f"Şık {harf}", key=f"btn_{current_idx}_{harf}", type=btn_type, use_container_width=True):
                    st.session_state[secilen_cevap_key] = harf
                    st.rerun()

        if st.session_state[secilen_cevap_key]:
            st.info(f"✨ Bu soru için işaretlediğiniz şık: **{st.session_state[secilen_cevap_key]}**")

        st.markdown("</div>", unsafe_allow_html=True)

        # Navigasyon / İlerleme Butonları
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
                    st.success("Tebrikler! 80 soruluk sıralı deneme sınavını tamamladınız ve cevaplarınızı kaydettiniz.")
