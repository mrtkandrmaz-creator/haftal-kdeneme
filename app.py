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
    page_title="MEB Müfredatına Uygun Akıllı Deneme Sınavı Üretici",
    page_icon="📚",
    layout="wide"
)

# Özel CSS Tasarımları (Modern Butonlar, Tablolar, Kartlar ve Boyut Optimizasyonları)
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        font-weight: bold;
        height: 3.5em;
        background: linear-gradient(135deg, #4f46e5 0%, #3b82f6 100%);
        color: white;
        border: none;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #4338ca 0%, #2563eb 100%);
        box-shadow: 0 6px 8px rgba(0,0,0,0.15);
        transform: translateY(-1px);
    }
    .question-card {
        background-color: white;
        padding: 24px;
        border-radius: 14px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        border: 1px solid #e5e7eb;
    }
    .passage-box {
        background-color: #f3f4f6;
        border-left: 4px solid #4f46e5;
        padding: 14px 18px;
        border-radius: 0 8px 8px 0;
        margin-bottom: 15px;
        font-size: 15px;
        color: #1f2937;
        line-height: 1.6;
    }
    .modern-table {
        width: 100%;
        border-collapse: collapse;
        margin: 15px 0;
        font-size: 14px;
        background-color: white;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .modern-table th {
        background: linear-gradient(135deg, #4f46e5 0%, #3b82f6 100%);
        color: white;
        text-align: left;
        padding: 10px 14px;
        font-weight: 600;
    }
    .modern-table td {
        padding: 10px 14px;
        border-bottom: 1px solid #f3f4f6;
        color: #374151;
    }
    .modern-table tr:last-child td {
        border-bottom: none;
    }
    .modern-table tr:nth-child(even) {
        background-color: #f9fafb;
    }
    .solution-box {
        background-color: #ecfdf5;
        border: 1px solid #d1fae5;
        border-radius: 8px;
        padding: 12px 16px;
        margin-top: 12px;
        color: #065f46;
        font-size: 14px;
    }
    </style>
""", unsafe_allow_html=True)

# Oturum Durumu Tanımlamaları
if "exam_generated" not in st.session_state:
    st.session_state.exam_generated = False
if "questions" not in st.session_state:
    st.session_state.questions = []
if "user_answers" not in st.session_state:
    st.session_state.user_answers = {}
if "exam_submitted" not in st.session_state:
    st.session_state.exam_submitted = False

# Yan Menü (Sidebar) Yapılandırması
with st.sidebar:
    st.image("https://img.icons8.com/color/96/graduation-cap.png", width=70)
    st.title("Sınav Yapılandırma")
    st.markdown("MEB 2026-2027 Müfredatına Uygun Soru Havuzu")
    
    grade_level = st.selectbox("Sınıf Seviyesi", ["5. Sınıf", "6. Sınıf", "7. Sınıf", "8. Sınıf (LGS)"])
    exam_type = st.selectbox("Sınav Türü", ["Genel Deneme Sınavı (Tüm Dersler)", "Branş Denemesi", "Özel Konu Odaklı Deneme"])
    
    st.markdown("---")
    st.subheader("📝 Manuel Ünite/Konu Ekleme")
    custom_lesson_target = st.selectbox("Eklenecek Ders", ["Türkçe", "Matematik", "Fen Bilimleri", "Sosyal Bilgiler / T.C. İnkılap Tarihi", "Din Kültürü", "İngilizce"])
    custom_unit_topic = st.text_input("Özel Ünite veya Kazanım Adı", placeholder="Örn: Hücre ve Bölünmeler")
    
    if st.button("➕ Listeye Ekle"):
        if custom_unit_topic:
            if "custom_topics" not in st.session_state:
                st.session_state.custom_topics = []
            st.session_state.custom_topics.append({"lesson": custom_lesson_target, "topic": custom_unit_topic})
            st.success(f"'{custom_unit_topic}' konusu {custom_lesson_target} dersine başarıyla bağlandı!")
        else:
            st.warning("Lütfen bir konu adı giriniz.")
            
    if "custom_topics" in st.session_state and st.session_state.custom_topics:
        st.markdown("**Eklenen Özel Konular:**")
        for idx, item in enumerate(st.session_state.custom_topics):
            st.caption(f"{idx+1}. [{item['lesson']}] {item['topic']}")

    st.markdown("---")
    
    # Uzatılmış ve Büyük Tasarımlı "Soru Üret" Butonu
    generate_button = st.button("🎯 SORULARI ÜRET")

# Tablo Render Yardımcısı
def render_html_table(table_data):
    if not table_data or not isinstance(table_data, dict):
        return ""
    headers = table_data.get("headers", [])
    rows = table_data.get("rows", [])
    title = table_data.get("title", "")
    
    html = f"<div style='font-weight:600; margin-bottom:6px; color:#4f46e5;'>📊 {title}</div>"
    html += "<table class='modern-table'><thead><tr>"
    for h in headers:
        html += f"<th>{h}</th>"
    html += "</tr></thead><tbody>"
    for row in rows:
        html += "<tr>"
        for cell in row:
            html += f"<td>{cell}</td>"
        html += "</tr>"
    html += "</tbody></table>"
    return html

# Görsel / Grafik Çizim Yardımcısı (Kompakt ve Güvenli Boyutlar)
def draw_geometry_or_science_shape(q_data):
    fig, ax = plt.subplots(figsize=(4.2, 2.8), dpi=100)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')
    
    stype = q_data.get("shape_type", "")
    
    if stype == "circle":
        radius = q_data.get("radius", 5)
        circle = plt.Circle((0, 0), radius, color='#4f46e5', fill=False, linewidth=2.5)
        ax.add_patch(circle)
        ax.plot([0, 0], [0, radius], color='#ef4444', linestyle='--', linewidth=2, label=f"Yarıçap (r) = {radius} cm")
        ax.plot([0, 0], [0, 0], marker='o', color='black')
        ax.set_xlim(-radius-2, radius+2)
        ax.set_ylim(-radius-2, radius+2)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.legend(loc='upper right', fontsize=8)
        
    elif stype == "sun_earth_moon":
        # Fen Bilimleri için Dünya-Güneş-Ay Şeması
        sun = plt.Circle((-3, 0), 1.2, color='#f59e0b', alpha=0.9, label='Güneş')
        earth = plt.Circle((0, 0), 0.6, color='#3b82f6', alpha=0.9, label='Dünya')
        moon = plt.Circle((1.8, 0), 0.25, color='#94a3b8', alpha=0.9, label='Ay')
        ax.add_patch(sun)
        ax.add_patch(earth)
        ax.add_patch(moon)
        ax.plot([-3, 0, 1.8], [0, 0, 0], color='#cbd5e1', linestyle=':', linewidth=1.5)
        ax.text(-3, -1.6, 'Güneş', ha='center', fontsize=9, fontweight='bold', color='#b45309')
        ax.text(0, -0.9, 'Dünya', ha='center', fontsize=9, fontweight='bold', color='#1d4ed8')
        ax.text(1.8, -0.6, 'Ay', ha='center', fontsize=9, fontweight='bold', color='#475569')
        ax.set_xlim(-5, 3.5)
        ax.set_ylim(-2.2, 2.2)
        ax.axis('off')
        
    else:
        # Standart Geometrik Açı / Şekil
        ax.plot([0, 4, 2, 0], [0, 0, 3, 0], color='#4f46e5', linewidth=2.5, fillstyle='full')
        ax.text(2, 3.2, 'A', ha='center', fontsize=10, fontweight='bold')
        ax.text(-0.2, -0.3, 'B', ha='right', fontsize=10, fontweight='bold')
        ax.text(4.2, -0.3, 'C', ha='left', fontsize=10, fontweight='bold')
        ax.set_xlim(-1, 5)
        ax.set_ylim(-1, 4)
        ax.axis('off')

    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
    buf.seek(0)
    plt.close(fig)
    return buf

# Soru Üretme Mantığı
if generate_button:
    with st.spinner("⏳ MEB müfredatına uygun sorular hazırlanıyor, lütfen bekleyiniz..."):
        # Sol menüde yükleme animasyonları
        time.sleep(1.2)
        
        # Örnek Soru Havuzu (Türkçe, Matematik, Fen Bilimleri, Sosyal, Din, İngilizce - Dengeli Dağılım)
        generated_list = [
            {
                "lesson": "Türkçe",
                "unit": "Sözcükte Anlam ve Paragraf",
                "passage": "Teknolojinin hızla geliştiği günümüzde, bilgiye ulaşmak kadar bilgiyi doğru süzgeçten geçirmek de hayati bir önem kazanmıştır. Yüzeysel okumalar yerine derinlemesine analiz yapan bireyler, geleceğin dünyasında daha avantajlı konumda olacaktır.",
                "text": "Bu parçada asıl anlatılmak istenen düşünce aşağıdakilerden hangisidir?",
                "options": {
                    "A": "Teknolojik gelişmeleri yakından takip etmek gerekir.",
                    "B": "Bilgiye ulaşmak geçmişe göre çok daha kolaylaşmıştır.",
                    "C": "Bilgiyi eleştirel bir gözle değerlendirmek ve derinlemesine incelemek önemlidir.",
                    "D": "Gelecekte sadece teknolojiyle ilgilenenler başarılı olacaktır."
                },
                "correct": "C",
                "solution": "Paragrafta 'bilgiye ulaşmak kadar bilgiyi doğru süzgeçten geçirmek' ve 'derinlemesine analiz yapmak' vurgulanmıştır. Bu durum C seçeneğinde en net şekilde özetlenmiştir."
            },
            {
                "lesson": "Matematik",
                "unit": "Veri İşleme ve Tablolar",
                "passage": "",
                "text": "Aşağıdaki tablo, bir sınıftaki öğrencilerin okuma kitap sayısını göstermektedir. En çok kitap okuyan öğrenci kaç kitap okumuştur?",
                "table_data": {
                    "type": "table",
                    "title": "Kitap Okuma Tablosu",
                    "headers": ["Öğrenci", "Kitap Sayısı"],
                    "rows": [["Ali", "5"], ["Ayşe", "8"], ["Mehmet", "6"], ["Elif", "9"]]
                },
                "options": {
                    "A": "5",
                    "B": "8",
                    "C": "6",
                    "D": "9"
                },
                "correct": "D",
                "solution": "Tablodaki kitap sayıları incelendiğinde; Ali 5, Ayşe 8, Mehmet 6 ve Elif 9 kitap okumuştur. En yüksek değer 9 ile Elif'e aittir."
            },
            {
                "lesson": "Matematik",
                "unit": "Geometri ve Çember",
                "passage": "",
                "text": "Yandaki şekilde verilen çemberin yarıçapı 5 cm olduğuna göre, bu çemberin çapı kaç cm'dir?",
                "shape_type": "circle",
                "radius": 5,
                "options": {
                    "A": "5 cm",
                    "B": "10 cm",
                    "C": "15 cm",
                    "D": "25 cm"
                },
                "correct": "B",
                "solution": "Bir çemberin çapı, yarıçapının iki katına eşittir (Çap = 2 × r). Yarıçap 5 cm verildiğinden, çap 2 × 5 = 10 cm'dir."
            },
            {
                "lesson": "Fen Bilimleri",
                "unit": "Dünya, Güneş ve Ay",
                "passage": "Güneş, Dünya ve Ay'ın birbirine göre konumları onların evrelerini ve aralarındaki hareket ilişkisini belirler.",
                "text": "Yandaki Güneş-Dünya-Ay modeline göre Ay'ın hangi ana evresinde bu konum gerçekleşir?",
                "shape_type": "sun_earth_moon",
                "options": {
                    "A": "Yeni Ay",
                    "B": "İlk Dördün",
                    "C": "Dolunay",
                    "D": "Son Dördün"
                },
                "correct": "A",
                "solution": "Güneş ile Dünya arasında Ay'ın yer aldığı bu konumda, Ay'ın dünyaya bakan yüzü güneş ışığı alamaz ve bu evre 'Yeni Ay' olarak adlandırılır."
            },
            {
                "lesson": "Matematik",
                "unit": "Veri Analizi ve İstatistik",
                "passage": "",
                "text": "Aşağıdaki tablo, bir haftada satılan dondurma çeşitlerinin adedini göstermektedir. Toplam satılan dondurma adedini bulunuz.",
                "table_data": {
                    "type": "table",
                    "title": "Dondurma Satış Tablosu",
                    "headers": ["Gün", "Adet"],
                    "rows": [["Pazartesi", "12"], ["Salı", "15"], ["Çarşamba", "9"], ["Perşembe", "14"], ["Cuma", "11"], ["Cumartesi", "20"], ["Pazar", "18"]]
                },
                "options": {
                    "A": "95",
                    "B": "99",
                    "C": "105",
                    "D": "110"
                },
                "correct": "B",
                "solution": "Günlük satışlar toplandığında: 12 + 15 + 9 + 14 + 11 + 20 + 18 = 99 adet dondurma satıldığı görülür."
            }
        ]
        
        st.session_state.questions = generated_list
        st.session_state.exam_generated = True
        st.session_state.exam_submitted = False
        st.session_state.user_answers = {}

# Ana Ekran İçerik Yönetimi
if not st.session_state.exam_generated:
    st.markdown("""
        <div style='text-align: center; padding: 40px;'>
            <h2>🚀 MEB Müfredatlı Akıllı Sınav Sistemi</h2>
            <p style='color: #6b7280; font-size: 16px;'>Sol menüden sınıf seviyenizi seçin, dilerseniz özel konular ekleyin ve <b>🎯 SORULARI ÜRET</b> butonuna basarak tam donanımlı deneme sınavınızı oluşturun.</p>
        </div>
    """, unsafe_allow_html=True)
else:
    if not st.session_state.exam_submitted:
        st.markdown("### 📋 Hazırlanan Deneme Sınavı")
        st.info("Soruları yanıtladıktan sonra sayfanın altındaki **'Sınavı Bitir ve Karneni Gör'** butonuna tıklayabilirsiniz.")
        
        with st.form("exam_form"):
            for idx, q in enumerate(st.session_state.questions):
                st.markdown(f"<div class='question-card'>", unsafe_allow_html=True)
                st.markdown(f"**Soru {idx+1}** &nbsp;|&nbsp; <span style='color:#4f46e5; font-weight:600;'>{q['lesson']}</span> — *{q['unit']}*", unsafe_allow_html=True)
                
                # Metin öncülü varsa göster, yoksa gereksiz boşluk bırakma
                if q.get("passage"):
                    st.markdown(f"<div class='passage-box'>{q['passage']}</div>", unsafe_allow_html=True)
                
                st.markdown(f"<p style='font-size:16px; font-weight:500; color:#111827;'>{q['text']}</p>", unsafe_allow_html=True)
                
                # Tablo varsa çiz
                if "table_data" in q:
                    st.markdown(render_html_table(q["table_data"]), unsafe_allow_html=True)
                
                # Geometrik şekil / grafik veya fen şeması varsa çiz
                if "shape_type" in q:
                    img_buf = draw_geometry_or_science_shape(q)
                    st.image(img_buf, width=380)
                
                # Şıklar
                ans_choice = st.radio(
                    f"Cevabınız (Soru {idx+1}):",
                    options=list(q["options"].keys()),
                    format_func=lambda x: f"{x}) {q['options'][x]}",
                    key=f"q_{idx}"
                )
                st.session_state.user_answers[idx] = ans_choice
                st.markdown(f"</div>", unsafe_allow_html=True)
                
            submitted = st.form_submit_button("🏁 Sınavı Bitir ve Karneni Gör")
            if submitted:
                st.session_state.exam_submitted = True
                st.rerun()
                
    else:
        # Sonuç Karnesi ve Detaylı Çözümler
        st.markdown("## 📊 Sınav Sonuç Karnesi ve Detaylı Çözümler")
        
        correct_count = 0
        total_questions = len(st.session_state.questions)
        
        for idx, q in enumerate(st.session_state.questions):
            user_ans = st.session_state.user_answers.get(idx)
            is_correct = (user_ans == q["correct"])
            if is_correct:
                correct_count += 1
                
        score = (correct_count / total_questions) * 100
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Toplam Soru", total_questions)
        col2.metric("Doğru Sayısı", correct_count)
        col3.metric("Başarı Puanı", f"{score:.1f} Puan")
        
        st.markdown("---")
        st.subheader("🔍 Soru Bazlı Detaylı Çözüm Analizi")
        
        for idx, q in enumerate(st.session_state.questions):
            user_ans = st.session_state.user_answers.get(idx)
            is_correct = (user_ans == q["correct"])
            
            st.markdown(f"<div class='question-card'>", unsafe_allow_html=True)
            status_icon = "✅ Doğru" if is_correct else "❌ Yanlış"
            st.markdown(f"**Soru {idx+1}** ({q['lesson']} - {q['unit']}) &nbsp;|&nbsp; **Durum:** {status_icon}", unsafe_allow_html=True)
            st.markdown(f"<p style='font-weight:500;'>{q['text']}</p>", unsafe_allow_html=True)
            
            if "table_data" in q:
                st.markdown(render_html_table(q["table_data"]), unsafe_allow_html=True)
            if "shape_type" in q:
                img_buf = draw_geometry_or_science_shape(q)
                st.image(img_buf, width=340)
                
            st.markdown(f"**Senin Cevabın:** {user_ans} | **Doğru Cevap:** {q['correct']}")
            
            # Detaylı Gerekçeli Çözüm Açıklaması
            st.markdown(f"""
                <div class='solution-box'>
                    <b>💡 Neden Doğru? / Detaylı Çözüm:</b><br>
                    {q['solution']}
                </div>
            """, unsafe_allow_html=True)
            st.markdown(f"</div>", unsafe_allow_html=True)
            
        if st.button("🔄 Yeni Deneme Sınavı Oluştur"):
            st.session_state.exam_generated = False
            st.session_state.exam_submitted = False
            st.rerun()
