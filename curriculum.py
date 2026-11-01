"""MEB müfredat verisi, 36 haftalık plan ve OYSS senaryo üretici.

ÖNEMLİ: Ünite listeleri MEB/TTKB öğretim programı başlıklarına göre hazırlanmıştır.
Resmî tabloyla birebir eşleştirmek için UNITS ve OYSS_OVERRIDES sözlüklerini düzenleyebilirsin.
"""

TR, MAT, FEN, SOS, DIN, ING, ALM = (
    "Türkçe", "Matematik", "Fen Bilimleri", "Sosyal Bilgiler",
    "Din Kültürü ve Ahlak Bilgisi", "İngilizce", "Almanca",
)
INK = "T.C. İnkılap Tarihi ve Atatürkçülük"
CORE = [TR, MAT, FEN, SOS, DIN, ING]

GRADES = {
    "4": {"label": "4. Sınıf", "tag": "İlkokul", "icon": "🌱", "c": 0, "num": "4"},
    "5": {"label": "5. Sınıf", "tag": "Ortaokul · Maarif Modeli", "icon": "🚀", "c": 1, "num": "5"},
    "6": {"label": "6. Sınıf", "tag": "Ortaokul · Maarif Modeli", "icon": "🧭", "c": 2, "num": "6"},
    "7": {"label": "7. Sınıf", "tag": "Ortaokul · Maarif Modeli", "icon": "🔭", "c": 3, "num": "7"},
    "8": {"label": "8. Sınıf", "tag": "Ortaokul · Okul Müfredatı", "icon": "🎯", "c": 4, "num": "8"},
    "LGS": {"label": "LGS Hazırlık", "tag": "8. Sınıf · LGS Formatı", "icon": "🏆", "c": 5, "num": "8"},
}

DIFFICULTIES = [
    "🟢 1. Çok Kolay / Temel Kazanım Düzeyi",
    "🔵 2. Kolay / Bilgiyi Hatırlama ve Kavrama",
    "🟡 3. Orta / MEB Standart & Beceri Temelli (İdeal LGS)",
    "🟠 4. Güçlendirilmiş / Seçici ve Yorum Odaklı",
    "🔴 5. Üst Düzey Zor / LGS Seçici (Çok Aşamalı Muhakeme)",
    "⚡ 6. Çok Zor / Olimpiyat & Üst Düzey Beceri Odaklı",
]

# ---------------------------------------------------------------- ÜNİTELER
UNITS = {
    "4": {
        TR: ["Erdemler", "Millî Mücadele ve Atatürk", "Doğa ve Evren", "Bilim ve Teknoloji",
             "Birey ve Toplum", "Sanat", "Millî Kültürümüz", "Sağlık ve Spor"],
        MAT: ["Doğal Sayılar", "Toplama ve Çıkarma İşlemi", "Çarpma İşlemi", "Bölme İşlemi",
              "Kesirler", "Zaman Ölçme", "Uzunluk ve Çevre Ölçme", "Geometrik Cisimler ve Şekiller", "Veri Toplama ve Değerlendirme"],
        FEN: ["Yer Kabuğu ve Dünyamızın Hareketleri", "Besinlerimiz", "Kuvvetin Etkileri", "Maddenin Özellikleri",
              "Aydınlatma ve Ses Teknolojileri", "İnsan ve Çevre", "Basit Elektrik Devreleri"],
        SOS: ["Birey ve Toplum", "Kültür ve Miras", "İnsanlar, Yerler ve Çevreler", "Bilim, Teknoloji ve Toplum",
              "Üretim, Dağıtım ve Tüketim", "Etkin Vatandaşlık", "Küresel Bağlantılar"],
        DIN: ["Allah İnancı", "Temel İbadetler", "Hz. Muhammed'in Hayatı", "Ahlaki Değerler", "Dinimizde Güzel Davranışlar"],
        ING: ["Classroom Rules", "Nationality", "Cartoon Characters", "Free Time", "My Day", "Fun with Science", "Animals"],
        ALM: ["Hallo!", "Meine Familie", "Die Schule", "Zahlen und Farben", "Tiere"],
    },
    "5": {
        TR: ["Erdemler", "Millî Mücadele ve Atatürk", "Doğa ve Evren", "Bilim ve Teknoloji",
             "Birey ve Toplum", "Sanat", "Millî Kültürümüz", "Sağlık ve Spor"],
        MAT: ["Doğal Sayılarla İşlemler", "Çarpanlar ve Katlar", "Kesirler", "Ondalık Gösterim ve Yüzdeler",
              "Temel Geometrik Kavramlar ve Çizimler", "Çokgenler", "Uzunluk, Alan ve Zaman Ölçme", "Veri Toplama ve Değerlendirme"],
        FEN: ["Gezegenimizi Tanıyalım (Güneş, Dünya ve Ay)", "Beş Duyumuz", "Kuvvetin Etkileri", "Maddeyi Tanıyalım",
              "Işığın Yayılması", "Canlılarda Üreme, Büyüme ve Gelişme", "Elektrik Devre Elemanları"],
        SOS: ["Birey ve Toplum", "Kültür ve Miras", "İnsanlar, Yerler ve Çevreler", "Bilim, Teknoloji ve Toplum",
              "Üretim, Dağıtım ve Tüketim", "Etkin Vatandaşlık", "Küresel Bağlantılar"],
        DIN: ["Allah İnancı", "Namaz", "Ramazan ve Oruç", "Hz. Muhammed ve Aile Hayatı", "Dinimizin Temel Kaynakları"],
        ING: ["Hello!", "My Town", "Games and Hobbies", "My Daily Routine", "Health", "Movies", "Party Time", "Fitness", "The Animal Shelter", "Festivals"],
        ALM: ["Hallo!", "Meine Familie", "Meine Schule", "Essen und Trinken", "Freizeit"],
    },
    "6": {
        TR: ["Erdemler", "Millî Mücadele ve Atatürk", "Doğa ve Evren", "Bilim ve Teknoloji",
             "Birey ve Toplum", "Sanat", "Millî Kültürümüz", "Sağlık ve Spor"],
        MAT: ["Doğal Sayılarla İşlemler", "Çarpanlar ve Katlar", "Kümeler", "Tam Sayılar", "Kesirlerle İşlemler",
              "Ondalık Gösterim", "Oran ve Orantı", "Cebirsel İfadeler", "Veri Analizi", "Alan Ölçme ve Çember"],
        FEN: ["Güneş Sistemi ve Tutulmalar", "Vücudumuzdaki Sistemler", "Kuvvet ve Hareket", "Madde ve Isı",
              "Ses ve Özellikleri", "Vücudumuzdaki Sistemler ve Sağlığı", "Elektriğin İletimi"],
        SOS: ["Biz ve Değerlerimiz", "Tarihe Yolculuk", "Yeryüzünde Yaşam", "Bilim, Teknoloji ve Toplum",
              "Ekonomi ve Sosyal Hayat", "Yönetim ve Yurttaşlık", "Küresel Bağlantılar"],
        DIN: ["Peygamber ve İlahi Kitap İnancı", "Namaz ve Mescit", "Zekât, Sadaka ve Hac", "Ahlaki Değerler", "Kur'an-ı Kerim ve Güzel Ahlak"],
        ING: ["Life", "Yummy Breakfast", "Downtown", "Weather and Emotions", "At the Fair", "Occupations", "Holidays", "Bookworms", "Saving the Planet", "Democracy"],
        ALM: ["Hallo!", "Familie und Freunde", "Mein Tag", "Einkaufen", "Hobbys"],
    },
    "7": {
        TR: ["Erdemler", "Millî Mücadele ve Atatürk", "Doğa ve Evren", "Bilim ve Teknoloji",
             "Birey ve Toplum", "Sanat", "Millî Kültürümüz", "Sağlık ve Spor"],
        MAT: ["Tam Sayılarla İşlemler", "Rasyonel Sayılar", "Cebirsel İfadeler", "Eşitlik ve Denklem", "Oran ve Orantı",
              "Yüzdeler", "Doğrular ve Açılar", "Çokgenler ve Çember", "Veri Analizi", "Cisimlerin Hacmi"],
        FEN: ["Güneş Sistemi ve Ötesi", "Hücre ve Bölünmeler", "Kuvvet ve Enerji", "Saf Madde ve Karışımlar",
              "Işığın Madde ile Etkileşimi", "Canlılarda Üreme ve Kalıtım", "Elektrik Devreleri"],
        SOS: ["İletişim ve İnsan İlişkileri", "Türk Tarihinde Yolculuk", "Ülkemizin Nüfus ve Ekonomisi", "Zaman İçinde Bilim",
              "Ekonomi ve Sosyal Hayat", "Yaşayan Demokrasi", "Ülkeler Arası Köprüler"],
        DIN: ["Melek ve Ahiret İnancı", "Hac ve Kurban", "Ahlaki Tutum ve Davranışlar", "Hz. Muhammed'in Örnekliği", "Kur'an'da Temel Konular"],
        ING: ["Appearance and Personality", "Sports", "Biographies", "Wild Animals", "Television", "Celebrations", "Dreams", "Public Buildings", "Environment", "Planets"],
        ALM: ["Hallo!", "Mein Zuhause", "Gesundheit", "Reisen", "Kleidung"],
    },
    "8": {
        TR: ["Fiilimsiler", "Cümlenin Ögeleri", "Cümle Türleri", "Fiillerde Çatı", "Anlatım Bozuklukları",
             "Yazım Kuralları ve Noktalama", "Paragrafta Anlam", "Söz Sanatları", "Metin Türleri"],
        MAT: ["Çarpanlar ve Katlar", "Üslü İfadeler", "Kareköklü İfadeler", "Veri Analizi", "Basit Olayların Olasılığı",
              "Cebirsel İfadeler ve Özdeşlikler", "Doğrusal Denklemler", "Eşitsizlikler", "Üçgenler", "Eşlik ve Benzerlik",
              "Dönüşüm Geometrisi", "Geometrik Cisimler"],
        FEN: ["Mevsimler ve İklim", "DNA ve Genetik Kod", "Basınç", "Madde ve Endüstri", "Basit Makineler",
              "Enerji Dönüşümleri ve Çevre Bilimi", "Elektrik Yükleri ve Elektrik Enerjisi"],
        SOS: ["Bir Kahraman Doğuyor", "Millî Uyanış: Bağımsızlık Yolunda Atılan Adımlar", "Millî Bir Destan: Ya İstiklal Ya Ölüm",
              "Atatürkçülük ve Çağdaşlaşan Türkiye", "Demokratikleşme Çabaları", "Atatürk Dönemi Türk Dış Politikası",
              "Atatürk'ün Ölümü ve Sonrası"],
        DIN: ["Kader İnancı", "Zekât ve Sadaka", "Din ve Hayat", "Hz. Muhammed'in Örnekliği", "Kur'an-ı Kerim ve Yorumu"],
        ING: ["Friendship", "Teen Life", "In the Kitchen", "On the Phone", "The Internet", "Adventures", "Tourism", "Chores", "Science", "Natural Forces"],
        ALM: ["Hallo!", "Meine Stadt", "Reisen", "Medien", "Zukunft"],
    },
}
UNITS["8"][INK] = UNITS["8"].pop(SOS)
UNITS["LGS"] = UNITS["8"]


def subjects_for(grade: str, with_german=False):
    base = [TR, MAT, FEN, INK if grade in ("8", "LGS") else SOS, DIN, ING]
    return base + ([ALM] if with_german else [])


def social_name(grade: str):
    return INK if grade in ("8", "LGS") else SOS


def units_of(grade: str, subject: str):
    return UNITS.get(grade, UNITS["5"]).get(subject, [])


# ---------------------------------------------------------------- 36 HAFTA
def week_label(w: int) -> str:
    term = 1 if w <= 18 else 2
    tag = " · 📅 Aylık Tarama" if w % 4 == 0 else ""
    return f"Hafta {w} ({term}. Dönem){tag}"


def units_for_week(grade: str, subject: str, week: int):
    """Haftaya düşen üniteler. 4'ün katı haftalarda son 4 haftanın tamamı (aylık tarama)."""
    units = units_of(grade, subject)
    if not units:
        return []
    def idx(w):
        return min(len(units) - 1, int((w - 1) * len(units) / 36))
    weeks = range(week - 3, week + 1) if week % 4 == 0 else [week]
    seen = []
    for w in weeks:
        u = units[idx(max(1, w))]
        if u not in seen:
            seen.append(u)
    return seen


def units_for_term(grade: str, subject: str, term):
    units = units_of(grade, subject)
    if term == "all" or not units:
        return units
    half = (len(units) + 1) // 2
    return units[:half] if term == 1 else units[half:] or units


# ---------------------------------------------------------------- OYSS
OYSS_GRADES = ["5", "6", "7"]
# Not: MEB tablolarında Türkçe 6, Sosyal Bilgiler 5 senaryo; sorular 5-9 arası değişir.
_SCEN_COUNTS = {TR: [6, 6, 7, 7, 7, 8], SOS: [6, 6, 7, 7, 8]}
_DEFAULT_COUNTS = [6, 6, 7, 7, 8]
OYSS_OVERRIDES = {}   # {(grade, subject, term, exam_no, scenario_no): [(unit, soru_sayisi), ...]}


def oyss_subjects(grade: str):
    s = [TR, MAT, FEN, SOS, DIN]
    if grade in ("5", "6"):
        s.append(ING)  # 7. sınıf İngilizce OYSS dışındadır
    return s


def oyss_scenarios(grade, subject, term, exam_no):
    units = units_of(grade, subject)
    half = (len(units) + 1) // 2
    term_units = units[:half] if term == 1 else (units[half:] or units)
    mid = max(1, len(term_units) // 2)
    sl = (term_units[:mid] if exam_no == 1 else (term_units[mid:] or term_units)) or ["Genel kazanımlar"]
    counts = _SCEN_COUNTS.get(subject, _DEFAULT_COUNTS)
    out = []
    for k, n in enumerate(counts, start=1):
        key = (grade, subject, term, exam_no, k)
        if key in OYSS_OVERRIDES:
            dist = OYSS_OVERRIDES[key]
        else:
            dist = {}
            for i in range(n):
                u = sl[(i + k - 1) % len(sl)]
                dist[u] = dist.get(u, 0) + 1
            dist = list(dist.items())
        out.append({"no": k, "n": sum(c for _, c in dist), "dist": dist})
    return out


def oyss_points(n: int, difficulty_mix=None):
    """Toplam 100 puan; kolay 10-15, orta 15-20, zor 20-25 aralığında (yaklaşık)."""
    nk = max(1, round(n * 0.30)); nz = max(1, round(n * 0.25)); no = n - nk - nz
    levels = ["Kolay"] * nk + ["Orta"] * no + ["Zor"] * nz
    base = {"Kolay": 10, "Orta": 15, "Zor": 20}
    pts = [base[l] for l in levels]
    rest = 100 - sum(pts)
    order = sorted(range(len(pts)), key=lambda i: -base[levels[i]])  # fazla/eksik puanı önce zorlara dağıt
    step = 5 if rest > 0 else -5
    j = 0
    while rest != 0 and j < 500:
        i = order[j % len(order)]
        if pts[i] + step >= 5:
            pts[i] += step; rest -= step
        j += 1
    return list(zip(levels, pts))


LGS80 = [(TR, 15), (MAT, 15), (FEN, 15), (INK, 15), (DIN, 10), (ING, 10)]
LGS90 = [(TR, 20), (MAT, 20), (FEN, 20), (INK, 10), (DIN, 10), (ING, 10)]
