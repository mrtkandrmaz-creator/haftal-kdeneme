# -*- coding: utf-8 -*-
"""Denemematik — TEK DOSYA sürümü (MEB Maarif Modeli yapay zekâ deneme platformu).
Çalıştırma: streamlit run app.py
Anahtarlar: Secrets -> [api_keys] groq_keys=[".."] gemini_keys=[".."]
Paketler: streamlit>=1.40 groq google-genai matplotlib numpy pandas altair reportlab requests pypdf
MODULES sözlüğündeki her kayıt bir modüldür (ör. core/curriculum = müfredat, core/meb_live = MEB'den çekme). İçinde üç tek tırnak yazmayın.
"""
import os
import sys
import types
import streamlit as st

APPDIR = os.path.dirname(os.path.abspath(__file__))

st.set_page_config(page_title="Denemematik • MEB Deneme Platformu", page_icon="🎓", layout="wide", initial_sidebar_state="expanded")

MODULES = {}
MODULES['core/curriculum'] = r'''# -*- coding: utf-8 -*-
"""MEB Türkiye Yüzyılı Maarif Modeli - 36 haftalık yıllık plan iskeleti.

NOT: Ünite/konu listeleri MEB öğretim programı ve ÖDSGM tablolarına göre hazırlanmış
bir iskelettir. Resmî tabloyla birebir eşleştirmek için sadece bu dosyadaki
listeleri düzenlemeniz yeterlidir; tüm ekranlar buradan beslenir.
"""

GRADE_LABELS = {"4": "4. Sınıf", "5": "5. Sınıf", "6": "6. Sınıf", "7": "7. Sınıf",
                "8": "8. Sınıf", "LGS": "LGS Hazırlık"}

DIFFICULTIES = [
    "🟢 1. Çok Kolay / Temel Kazanım Düzeyi",
    "🔵 2. Kolay / Bilgiyi Hatırlama ve Kavrama",
    "🟡 3. Orta / MEB Standart & Beceri Temelli (İdeal LGS)",
    "🟠 4. Güçlendirilmiş / Seçici ve Yorum Odaklı",
    "🔴 5. Üst Düzey Zor / LGS Seçici (Çok Aşamalı Muhakeme)",
    "⚡ 6. Çok Zor / Olimpiyat & Üst Düzey Beceri Odaklı",
]

TR, MAT, FEN, SOS, DIN, ING, ALM = ("Türkçe", "Matematik", "Fen Bilimleri", "Sosyal Bilgiler",
                                    "Din Kültürü ve Ahlak Bilgisi", "İngilizce", "Almanca")
INK = "T.C. İnkılap Tarihi ve Atatürkçülük"

SUBJECT_ICONS = {TR: "📖", MAT: "📐", FEN: "🔬", SOS: "🌍", INK: "🏛️", DIN: "🕌", ING: "🇬🇧", ALM: "🇩🇪"}
SUBJECT_COLORS = {TR: "#ef4444", MAT: "#0284c7", FEN: "#10b981", SOS: "#f59e0b", INK: "#f59e0b",
                  DIN: "#8b5cf6", ING: "#ec4899", ALM: "#64748b"}


def base_grade(g):
    return "8" if g == "LGS" else g


def subjects_for(g):
    b = base_grade(g)
    if b == "4":
        return [TR, MAT, FEN, SOS, DIN, ING]
    if b == "8":
        return [TR, MAT, FEN, INK, DIN, ING, ALM]
    return [TR, MAT, FEN, SOS, DIN, ING, ALM]


def _u(name, topics):
    return (name, [t.strip() for t in topics.split(";") if t.strip()])


C = {
 "4": {
  TR: [_u("Erdemler", "Okuma anlama; Ana fikir ve konu; Sözcükte anlam"), _u("Millî Mücadele ve Atatürk", "Metin türleri; Zıt ve eş anlam; Noktalama"),
      _u("Doğa ve Evren", "Bilgilendirici metin; Sebep-sonuç; Yazım kuralları"), _u("Millî Kültürümüz", "Deyim ve atasözü; Hikâye unsurları; Ses bilgisi"),
      _u("Bilim ve Teknoloji", "Grafik/tablo okuma; Başlık belirleme; Cümle türleri"), _u("Sanat ve Estetik", "Şiir; Söz sanatları temel; Anlatım biçimleri")],
  MAT: [_u("Doğal Sayılar", "Dört basamaklı sayılar; Basamak değeri; Yuvarlama"), _u("Toplama ve Çıkarma", "Zihinden işlem; Problem çözme"),
       _u("Çarpma ve Bölme", "Çarpma stratejileri; Bölme; Kalanlı bölme"), _u("Kesirler", "Birim kesir; Kesir karşılaştırma; Kesirle toplama"),
       _u("Geometri", "Açılar; Üçgen ve dörtgen; Simetri"), _u("Ölçme ve Veri", "Uzunluk; Zaman; Sıklık tablosu; Sütun grafiği")],
  FEN: [_u("Yer Kabuğu ve Dünya'mızın Hareketleri", "Yer kabuğu; Dünya'nın hareketleri"), _u("Besinlerimiz", "Besin içerikleri; Dengeli beslenme"),
       _u("Kuvvetin Etkileri", "İtme-çekme; Sürtünme"), _u("Maddenin Özellikleri", "Katı-sıvı-gaz; Isı etkisi"),
       _u("Aydınlatma ve Ses", "Işık kaynakları; Gölge; Ses yayılması"), _u("Elektrik", "Basit elektrik devresi; Elektrik güvenliği")],
  SOS: [_u("Birey ve Toplum", "Hak ve sorumluluklar; Rol ve statü"), _u("Kültür ve Miras", "Kültürel unsurlar; Yöresel kültür"),
       _u("İnsanlar, Yerler ve Çevreler", "Harita okuma; Yön bulma; Doğal afetler"), _u("Bilim, Teknoloji ve Toplum", "Teknoloji tarihi; Bilimsel buluşlar"),
       _u("Üretim, Dağıtım ve Tüketim", "Ekonomik faaliyetler; Tasarruf")],
  DIN: [_u("Allah İnancı", "Allah'ı tanıma; Güzel isimler"), _u("Temel İbadetler", "Namaz; Oruç; Dua"), _u("Hz. Muhammed'in Hayatı", "Çocukluk; Ahlakı"),
       _u("Değerlerimiz", "Dürüstlük; Yardımlaşma; Saygı"), _u("Kur'an-ı Kerim ve Dua", "Kur'an'ın tanıtımı; Kısa sureler")],
  ING: [_u("Hello!", "Greetings; Introducing"), _u("My Family", "Family members; Possessives"), _u("My Town", "Places; Directions"),
       _u("Daily Life", "Daily routines; Time"), _u("Food and Drinks", "Likes/dislikes; Ordering"), _u("Hobbies", "Free time; Can/can't")],
 },
 "5": {
  TR: [_u("Erdemler", "Okuma anlama; Ana fikir; Sözcükte anlam; Eş/zıt anlam"), _u("Millî Mücadele ve Atatürk", "Metin türleri; Anlatım biçimleri; Noktalama"),
      _u("Doğa ve Evren", "Bilgilendirici metin; Neden-sonuç; Cümlede anlam"), _u("Millî Kültürümüz", "Deyim ve atasözü; Hikâye unsurları; Ses bilgisi"),
      _u("Bilim ve Teknoloji", "Grafik/tablo yorumlama; Başlık; Yazım kuralları"), _u("Sanat ve Estetik", "Şiir; Söz sanatı; Paragraf yapısı"),
      _u("Birey ve Toplum", "Kelime türleri; Ad-sıfat; Cümle öğeleri giriş")],
  MAT: [_u("Temel Geometrik Çizimler ve İnşalar (MAT.5.3.1-2)", "Doğru, ışın, doğru parçası; Paralel ve dik doğrular; Geometrik çizimler"),
       _u("Açı Ölçme (MAT.5.3.3-4)", "Açı ölçme ve çizme; Açı türleri; Açıortay"),
       _u("Açı İlişkileri: Tümler, Bütünler, Komşu ve Ters Açılar (MAT.5.3.4)", "Tümler açılar (toplamı 90°); Bütünler açılar (toplamı 180°); Komşu açılar; Ters (karşıt) açılar; Kesişen iki doğrunun oluşturduğu açılar"),
       _u("Çokgenler ve Çember (MAT.5.3.5-7)", "Çokgenlerin elemanları; Çember ve daire elemanları; Çokgen çizimi"),
       _u("Basamak Değerlerini Çözümleme (MAT.5.1.1)", "Milyonlu sayılar; Basamak değeri; Sayı okuma-yazma"),
       _u("Doğal Sayılarla Dört İşlem (MAT.5.1.2)", "Dört işlem problemleri; Zihinden işlem; Tahmin"),
       _u("Dikdörtgenin Çevre ve Alanı (MAT.5.4.1-2)", "Çevre uzunluğu; Alan ölçme; Alan problemleri"),
       _u("Kesirler", "Kesir türleri; Kesir sıralama; Kesirlerle toplama-çıkarma"),
       _u("Ondalık Gösterim ve Yüzdeler", "Ondalık gösterim; Yüzde kavramı"),
       _u("Veri Toplama ve Değerlendirme", "Sütun grafiği; Veri yorumlama; Örüntüler")],
  FEN: [_u("Güneş, Dünya ve Ay", "Güneş'in yapısı; Dünya'nın hareketleri; Ay'ın evreleri; Tutulmalar"), _u("Canlıların Yapısı ve Hücre", "Hücre ve organeller; Canlı sınıflandırma"),
       _u("Kuvvetin Ölçülmesi ve Sürtünme", "Kuvvet ve dinamometre; Sürtünme kuvveti; Ağırlık-kütle"), _u("Madde ve Değişim", "Maddenin halleri; Isı ve sıcaklık; Erime-donma"),
       _u("Işığın Yayılması", "Işık kaynakları; Yansıma; Gölge"), _u("Elektrik Devreleri", "Devre elemanları; Seri-paralel bağlama; Elektrik güvenliği"),
       _u("Biyoçeşitlilik ve Çevre", "Ekosistem; Besin zinciri; Çevre sorunları")],
  SOS: [_u("Birlikte Yaşamak", "Birey-toplum; Haklar ve sorumluluklar; Roller"), _u("Evimiz Dünya", "Harita; Yer şekilleri; İklim; Doğal afetler"),
       _u("Ortak Mirasımız", "Kültürel miras; Anadolu medeniyetleri"), _u("Yaşayan Demokrasi", "Demokrasi; Seçim; Yönetim"),
       _u("Hayatımızdaki Ekonomi", "İhtiyaç-istek; Tasarruf; Meslekler"), _u("Teknoloji ve Sosyal Bilimler", "Bilim ve teknoloji tarihi; Bilişim güvenliği")],
  DIN: [_u("Allah İnancı", "Allah'ın varlığı; Güzel isimler"), _u("Namaz İbadeti", "Namazın önemi; Abdest; Namaz vakitleri"), _u("Hz. Muhammed'in Hayatı", "Peygamberliği; Örnek ahlakı"),
       _u("Kur'an-ı Kerim", "Kur'an'ın indirilişi; Temel konular"), _u("Değerlerimiz", "Dürüstlük; Adalet; Hoşgörü")],
  ING: [_u("Hello!", "Greetings; Introducing; Alphabet"), _u("My Town", "Places; Directions; Prepositions"), _u("Games and Hobbies", "Free time; Can/can't; Likes"),
       _u("My Daily Routine", "Daily routines; Time; Frequency"), _u("Health", "Body parts; Illnesses; Advice"), _u("Movies", "Genres; Opinions; Past simple basics"),
       _u("Party Time", "Invitations; Food; Dates"), _u("Fitness", "Sports; Healthy life")],
  ALM: [_u("Hallo!", "Begrüßung; Sich vorstellen; Alphabet"), _u("Meine Familie", "Familienmitglieder; Besitz"), _u("Zahlen und Farben", "Zahlen 1-100; Farben"),
       _u("Schule", "Schulfächer; Schulsachen"), _u("Essen und Trinken", "Lebensmittel; Vorlieben")],
 },
 "6": {
  TR: [_u("Erdemler", "Okuma anlama; Ana fikir; Deyim ve atasözü"), _u("Millî Mücadele ve Atatürk", "Metin türleri; Sözcükte anlam; Anlatım bozukluğu giriş"),
      _u("Doğa ve Evren", "Fiiller; Zarflar; Neden-sonuç"), _u("Millî Kültürümüz", "Söz sanatları; Söz grupları; Paragraf"),
      _u("Bilim ve Teknoloji", "Grafik okuma; Bilgilendirici metin; Noktalama"), _u("Sanat ve Estetik", "Şiir; Edat-bağlaç; Yazım kuralları"),
      _u("Birey ve Toplum", "Cümle türleri; Sözel mantık; Görsel okuma")],
  MAT: [_u("Doğal Sayılarla İşlemler", "Çarpanlar ve katlar; Asal sayılar; EBOB-EKOK giriş"), _u("Kesirlerle İşlemler", "Kesir işlemleri; Kesir problemleri"),
       _u("Ondalık Gösterim", "Ondalık sayılarla işlemler; Yüzde"), _u("Oran", "Oran kavramı; Orantı giriş"), _u("Tam Sayılar", "Tam sayılarla toplama-çıkarma; Mutlak değer"),
       _u("Cebirsel İfadeler", "Değişken; Cebirsel ifade; Eşitlik"), _u("Alan ve Çevre", "Üçgen, paralelkenar alanı; Çember uzunluğu"),
       _u("Veri Analizi", "Aritmetik ortalama; Çizgi ve daire grafiği")],
  FEN: [_u("Güneş Sistemi ve Tutulmalar", "Gezegenler; Ay-Güneş tutulması; Uzay araştırmaları"), _u("Vücudumuzdaki Sistemler", "Sindirim; Dolaşım; Solunum; Boşaltım"),
       _u("Kuvvet ve Hareket", "Sürat; Hareket grafikleri; Bileşke kuvvet"), _u("Madde ve Isı", "Saf madde-karışım; Isı alışverişi; Genleşme"),
       _u("Ses ve Işık", "Sesin özellikleri; Işığın yansıması; Mercekler"), _u("Elektrik", "Elektrik devreleri; Ohm yasası giriş; Güvenli kullanım"),
       _u("Canlılar Dünyası", "Hücre; Sınıflandırma; Ekosistem")],
  SOS: [_u("Birey ve Toplum", "Kimliğimiz; Sosyal rol; İletişim"), _u("Türklerde Devlet ve Kültür", "İlk Türk devletleri; Orta Asya"), _u("Bölgemizin Haritası", "Harita; Koordinat; Ölçek"),
       _u("Türkiye'nin Coğrafyası", "İklim; Nüfus; Doğal kaynaklar"), _u("Üretimden Tüketime", "Üretim; Kaynakların kullanımı; Girişimcilik"),
       _u("Yönetim ve Katılım", "Demokratik katılım; Kurumlar")],
  DIN: [_u("Peygamberlere İman", "Peygamberlerin özellikleri; İlahî kitaplar"), _u("İbadet", "Namaz; Zekât; Hac"), _u("Ahlak ve Değerler", "Sabır; Cömertlik; Adalet"),
       _u("Hz. Muhammed'in Örnekliği", "Hz. Muhammed'in ahlakı; Medine dönemi"), _u("Dinimizi Öğreniyoruz", "Kur'an; Hadis; Sünnet")],
  ING: [_u("Life", "Hobbies; Describing people; Present simple"), _u("Yummy Breakfast", "Food; Quantities; Some/any"), _u("Downtown", "Places; Prepositions; Directions"),
       _u("Weather", "Weather; Seasons; Present continuous"), _u("At the Fair", "Rides; Feelings; Invitations"), _u("Occupations", "Jobs; Future with will"),
       _u("Holidays", "Past simple; Travel; Plans"), _u("Bookworms", "Reading; Past experiences")],
  ALM: [_u("Hobbys", "Freizeit; Verbkonjugation"), _u("Mein Tag", "Uhrzeit; Tagesablauf"), _u("Meine Stadt", "Orte; Wegbeschreibung"), _u("Einkaufen", "Preise; Kleidung")],
 },
 "7": {
  TR: [_u("Erdemler", "Okuma anlama; Fiilimsiler giriş; Söz sanatları"), _u("Millî Mücadele ve Atatürk", "Metin türleri; Paragraf; Anlatım bozukluğu"),
      _u("Doğa ve Evren", "Cümle çeşitleri; Cümlenin ögeleri; Neden-sonuç"), _u("Millî Kültürümüz", "Deyim-atasözü; Sözcükte anlam; Yazım-noktalama"),
      _u("Bilim ve Teknoloji", "Grafik-tablo; Bilimsel metin; Ek fiil"), _u("Sanat ve Estetik", "Şiir; Edebî türler; Anlatım teknikleri"),
      _u("Birey ve Toplum", "Zarf; Edat-bağlaç-ünlem; Sözel mantık")],
  MAT: [_u("Tam Sayılar", "Tam sayılarla işlemler; Üslü ifadeler"), _u("Rasyonel Sayılar", "Rasyonel sayılarla işlemler; Sıralama"), _u("Cebirsel İfadeler", "Cebirsel ifadeler; Denklemler"),
       _u("Oran-Orantı ve Yüzdeler", "Doğru-ters orantı; Yüzde problemleri"), _u("Doğrular ve Açılar", "Açı ilişkileri; Paralel doğrular"),
       _u("Çokgenler ve Çember", "Çokgenler; Çember ve daire; Dönüşüm geometrisi"), _u("Veri Analizi", "Ortalama, ortanca, tepe değer; Grafikler"),
       _u("Geometrik Cisimler", "Prizmalar; Hacim ve yüzey alanı")],
  FEN: [_u("Güneş Sistemi ve Ötesi", "Uzay araştırmaları; Gök cisimleri"), _u("Hücre ve Bölünmeler", "Mitoz; Mayoz; Kalıtım giriş"), _u("Kuvvet ve Enerji", "İş-enerji; Enerji dönüşümü; Basit makineler"),
       _u("Saf Madde ve Karışımlar", "Element-bileşik; Karışımların ayrılması; Atom"), _u("Işığın Madde ile Etkileşimi", "Yansıma; Kırılma; Renkler"),
       _u("Elektrik Devreleri", "Akım-direnç-gerilim; Ohm yasası; Bağlantı"), _u("Canlılar ve Enerji İlişkileri", "Fotosentez; Besin zinciri; Madde döngüleri")],
  SOS: [_u("İletişim ve İnsan İlişkileri", "İletişim türleri; Etkili iletişim"), _u("Türklerin Anadolu'ya Yerleşmesi", "Malazgirt; Anadolu Selçuklu"), _u("Osmanlı Devleti'nin Kuruluşu", "Beylikten devlete; Fetihler"),
       _u("Ülkemizin Nüfusu ve Yerleşme", "Nüfus; Göç; Yerleşme"), _u("Ekonomi ve Sosyal Hayat", "Meslekler; Bütçe; Tüketici hakları"), _u("Zaman İçinde Bilim", "Bilim insanları; Buluşlar")],
  DIN: [_u("Melek ve Ahiret İnancı", "Melekler; Ahiret"), _u("Hac ve Kurban", "Hac; Kurban; Zekât"), _u("Ahlaki Davranışlar", "Hoşgörü; Dürüstlük; Çalışkanlık"),
       _u("Hz. Muhammed ve Örnek Hayatı", "Mekke ve Medine dönemi; Evrensel mesaj"), _u("İslam Düşüncesinde Yorumlar", "Mezhepler; Kültürel zenginlik")],
  ING: [_u("Appearance and Personality", "Describing; Comparatives"), _u("Sports", "Sports; Past simple; Likes"), _u("Biographies", "Past simple; Famous people"),
       _u("Wild Animals", "Animals; Comparatives; Habitats"), _u("Television", "Programs; Opinions; Preferences"), _u("Celebrations", "Festivals; Invitations"),
       _u("Dreams", "Future; Will/going to"), _u("Public Buildings", "Directions; Must/should")],
  ALM: [_u("Meine Schule", "Stundenplan; Fächer"), _u("Mein Zuhause", "Zimmer; Möbel; Präpositionen"), _u("Gesundheit", "Körperteile; Krankheiten"), _u("Reisen", "Verkehrsmittel; Reiseplan")],
 },
 "8": {
  TR: [_u("Fiilimsiler", "İsim-fiil; Sıfat-fiil; Zarf-fiil"), _u("Cümlenin Ögeleri", "Özne; Yüklem; Nesne; Tümleç"), _u("Cümle Türleri ve Anlam", "Cümle çeşitleri; Anlatım bozukluğu; Cümlede anlam"),
      _u("Paragraf ve Yeni Nesil Sorular", "Ana fikir; Yardımcı düşünce; Paragraf tamamlama; Görsel okuma"), _u("Söz Sanatları ve Edebî Türler", "Söz sanatları; Edebî türler; Metin türleri"),
      _u("Sözcükte Anlam", "Deyimler; Atasözleri; Söz grupları"), _u("Yazım ve Noktalama", "Yazım kuralları; Noktalama işaretleri")],
  MAT: [_u("Çarpanlar ve Katlar", "Asal çarpanlar; EBOB-EKOK; Problemler"), _u("Üslü İfadeler", "Üslü ifadeler; Bilimsel gösterim"), _u("Kareköklü İfadeler", "Kareköklü sayılar; Köklü işlemler"),
       _u("Veri Analizi", "Veri analizi; Grafik yorumlama"), _u("Basit Olayların Olma Olasılığı", "Olasılık; Örnek uzay"), _u("Cebirsel İfadeler ve Özdeşlikler", "Özdeşlikler; Çarpanlara ayırma"),
       _u("Doğrusal Denklemler", "Denklemler; Eğim; Doğru grafikleri"), _u("Eşitsizlikler", "Eşitsizlikler; Sayı doğrusu"), _u("Üçgenler", "Üçgen eşitsizliği; Pisagor; Benzerlik"),
       _u("Dönüşüm Geometrisi ve Geometrik Cisimler", "Yansıma-öteleme; Dik prizma; Silindir, koni")],
  FEN: [_u("Mevsimler ve İklim", "Mevsim oluşumu; İklim-hava durumu"), _u("DNA ve Genetik Kod", "DNA; Kalıtım; Mutasyon; Modifikasyon"), _u("Basınç", "Katı, sıvı, gaz basıncı; Atmosfer basıncı"),
       _u("Madde ve Endüstri", "Periyodik sistem; Kimyasal tepkimeler; Asit-baz"), _u("Basit Makineler", "Kaldıraç; Makara; Eğik düzlem"), _u("Enerji Dönüşümleri ve Çevre Bilimi", "Enerji dönüşümü; Yenilenebilir enerji; Geri dönüşüm"),
       _u("Elektrik Yükleri ve Elektrik Enerjisi", "Elektriklenme; Yükler; Elektrik enerjisi")],
  INK: [_u("Bir Kahraman Doğuyor", "Atatürk'ün gençliği; Mustafa Kemal'in kişiliği"), _u("Millî Uyanış: Bağımsızlık Yolunda Atılan Adımlar", "Mondros; Cemiyetler; Amasya; Kongreler"),
       _u("Millî Bir Destan: Ya İstiklal Ya Ölüm", "Sakarya; Kurtuluş Savaşı; Lozan"), _u("Atatürkçülük ve Çağdaşlaşan Türkiye", "İnkılaplar; İlkeler"),
       _u("Demokratikleşme Çabaları", "Çok partili hayat; Demokratik gelişmeler"), _u("Atatürk Dönemi Türk Dış Politikası", "Dış politika; Hatay"), _u("Atatürk'ün Ölümü ve Sonrası", "II. Dünya Savaşı; Atatürk'ün mirası")],
  DIN: [_u("Kader İnancı", "Kader ve kaza; İrade"), _u("Zekât ve Sadaka", "Zekât; Sadaka; Toplumsal dayanışma"), _u("Din ve Hayat", "Din-bilim; Din-ahlak"),
       _u("Hz. Muhammed'in Örnekliği", "Ahlakı; Hitabeler"), _u("Kur'an-ı Kerim ve Yorumu", "Kur'an'ın anlaşılması; Yorumlar")],
  ING: [_u("Friendship", "Invitations; Accepting/declining; Describing friends"), _u("Teen Life", "Daily life; Likes; Hobbies"), _u("In the Kitchen", "Recipes; Quantities; Imperatives"),
       _u("On the Phone", "Phone talk; Messages; Making plans"), _u("The Internet", "Online life; Opinions; Pros/cons"), _u("Adventures", "Travel; Past tense"),
       _u("Tourism", "Places; Recommendations"), _u("Chores", "Household; Obligations"), _u("Science", "Inventions; Passive voice basics"), _u("Natural Forces", "Disasters; Cause/effect")],
  ALM: [_u("Meine Freizeit", "Hobbys; Verabredungen"), _u("Reisen und Urlaub", "Reisepläne; Wetter"), _u("Gesund leben", "Ernährung; Sport"), _u("Medien", "Fernsehen; Internet")],
 },
}

import datetime as _dt

TOTAL_WEEKS = 36
# MEB 2026-2027 çalışma takvimi: 14 Eylül 2026 başlangıç, 22 Ocak 2027 dönem sonu, 8 Şubat 2027 2. dönem,
# ara tatiller 16-20 Kasım, 25 Ocak-5 Şubat (yarıyıl), 8-12 Mart; ders yılı sonu 25 Haziran 2027.
TERM1_START = _dt.date(2026, 9, 14)
TERM2_START = _dt.date(2027, 2, 8)
BREAKS = [(_dt.date(2026, 11, 16), _dt.date(2026, 11, 20)), (_dt.date(2027, 1, 25), _dt.date(2027, 2, 5)),
          (_dt.date(2027, 3, 8), _dt.date(2027, 3, 12))]
TR_MONTHS = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]


def _in_break(d):
    return any(a <= d <= b for a, b in BREAKS)


def _build_weeks():
    out = []
    for start, need in ((TERM1_START, 18), (TERM2_START, 18)):
        d, n = start, 0
        while n < need:
            if not _in_break(d):
                out.append(d)
                n += 1
            d += _dt.timedelta(days=7)
    return out


WEEK_STARTS = _build_weeks()  # hafta no (1..36) -> o haftanın pazartesisi


def _build_months():
    order, res = [], {}
    for w, d in enumerate(WEEK_STARTS, 1):
        k = (d.year, d.month)
        if k not in res:
            res[k] = {"year": d.year, "month": d.month, "name": TR_MONTHS[d.month - 1], "a": w, "b": w}
            order.append(k)
        res[k]["b"] = w
    out = []
    for i, k in enumerate(order, 1):
        m = res[k]
        m["m"] = i
        y, mo = (m["year"] + (m["month"] == 12), m["month"] % 12 + 1)
        d = _dt.date(y, mo, 1)
        while d.weekday() != 0:  # sonraki ayın ilk haftasının pazartesisi
            d += _dt.timedelta(days=1)
        m["solve"] = d if i < len(order) else None
        out.append(m)
    return out


MONTHS = _build_months()
NUM_MONTHS = len(MONTHS)


def fmt_date(d):
    return f"{d.day} {TR_MONTHS[d.month - 1]}"


def week_dates(w):
    a = WEEK_STARTS[w - 1]
    return f"{fmt_date(a)} – {fmt_date(a + _dt.timedelta(days=4))} {a.year}"


def current_week(today=None):
    today = today or _dt.date.today()
    for w, d in enumerate(WEEK_STARTS, 1):
        if d <= today <= d + _dt.timedelta(days=6):
            return w
    return None


def suggested_month(today=None):
    """Aylık deneme ayın ilk haftasında ÇÖZÜLÜR ve ÖNCEKİ ayın konularını ölçer."""
    today = today or _dt.date.today()
    prev = None
    for m in MONTHS:
        if (m["year"], m["month"]) < (today.year, today.month):
            prev = m["m"]
    return prev or 1


def month_scope(i):
    m = MONTHS[i - 1]
    return {"type": "month", "m": i, "a": m["a"], "b": m["b"], "name": m["name"]}


def month_note(i):
    m = MONTHS[i - 1]
    if m["solve"]:
        return f"{m['name']} ayı konularını ölçer • {TR_MONTHS[m['solve'].month - 1]} ayının ilk haftasında ({fmt_date(m['solve'])}) çözülür"
    return f"{m['name']} ayı konularını ölçer • ders yılı sonunda çözülür"


LIVE = {}  # core.meb_live tarafından MEB'den çekilen müfredat: "sınıf|ders" -> [(ünite, [kazanımlar])]


# MEB Öğretim Programları (tymm.meb.gov.tr) — Ortaokul Matematik, Türkiye Yüzyılı Maarif Modeli. Tema adları ve kazanım kodları resmî sayfadan alınmıştır.
MEB_MAT = {
    "5": [
        ("1. Tema: Sayılar ve Nicelikler (1)", [
            "MAT.5.1.1. Altı basamaklı sayıları okuma ve yazmayı çok basamaklı sayılara genelleyebilme",
            "MAT.5.1.2. Doğal sayılar ve işlemler içeren gerçek yaşam problemlerini çözebilme"]),
        ("1. Tema: Sayılar ve Nicelikler (2)", [
            "MAT.5.1.3. Gerçek yaşam durumlarına karşılık gelen kesirleri farklı biçimlerde temsil edebilme",
            "MAT.5.1.4. Farklı gösterimlerle ifade edilen kesirlerin karşılaştırılmasına yönelik çıkarım yapabilme"]),
        ("2. Tema: İşlemlerle Cebirsel Düşünme", [
            "MAT.5.2.1. Eşitliğin korunumuna ve işlem özelliklerine yönelik çıkarım yapabilme",
            "MAT.5.2.2. Karşılaştığı günlük hayat ya da matematiksel durumlarda işlem önceliğini yorumlayabilme",
            "MAT.5.2.3. Sayı ve şekil örüntülerinin kuralına ilişkin muhakeme yapabilme",
            "MAT.5.2.4. Temel aritmetik işlem içeren durumlardaki algoritmaları yorumlayabilme"]),
        ("3. Tema: Geometrik Şekiller", [
            "MAT.5.3.1. Temel geometrik inşalar için matematiksel araç ve teknolojiyi kullanabilme (nokta, doğru, doğru parçası, ışın, açı, çember, dik doğru)",
            "MAT.5.3.2. Temel geometrik inşa deneyimlerini yansıtabilme",
            "MAT.5.3.3. Açı ölçmede matematiksel araç ve teknolojiyi kullanabilme",
            "MAT.5.3.4. Düzlemde iki ya da üç doğrunun oluşturduğu açılara ilişkin çıkarım yapabilme",
            "MAT.5.3.5. Çokgenleri düzlemde ardışık kesişen doğruların oluşturduğu kapalı şekiller olarak yorumlayabilme",
            "MAT.5.3.6. Çokgenlerin kenar ve açı özelliklerine yönelik deneyimlerini yansıtabilme",
            "MAT.5.3.7. İki çemberin kesişimiyle oluşan üçgenlerin kenar özelliklerine ilişkin çıkarım yapabilme (eşkenar, ikizkenar, çeşitkenar)"]),
        ("4. Tema: Geometrik Nicelikler", [
            "MAT.5.4.1. Kenar uzunlukları doğal sayı olan bir dikdörtgenin çevre uzunluğu verildiğinde kenar uzunluklarını yorumlayabilme",
            "MAT.5.4.2. Birim karelerden yola çıkarak dikdörtgenin alanını değerlendirebilme",
            "MAT.5.4.3. Kenar uzunlukları doğal sayı olan bir dikdörtgenin alanı verildiğinde çevre uzunluğunu, çevresi verildiğinde alanını yorumlayabilme",
            "MAT.5.4.4. Dikdörtgenin çevre uzunluğu ve alanı ile ilgili problemleri çözebilme"]),
        ("5. Tema: İstatistiksel Araştırma Süreci", [
            "MAT.5.5.1. Kategorik veri ile çalışabilme ve veriye dayalı karar verebilme",
            "MAT.5.5.2. Başkaları tarafından oluşturulan kategorik veriye dayalı istatistiksel sonuç veya yorumları tartışabilme"]),
        ("6. Tema: Veriden Olasılığa", [
            "MAT.5.6.1. Herhangi bir olayın olasılığının 0 (imkânsız) ile 1 (kesin) arasında olduğunu (olasılık spektrumu) yorumlayabilme",
            "MAT.5.6.2. Olayları az ya da çok olasılıklı şeklinde yapılandırabilme"]),
    ],
    "6": [
        ("1. Tema: Sayılar ve Nicelikler (1)", [
            "MAT.6.1.1. Karşılaştığı problem durumlarında bir doğal sayının çarpan ve katlarına yönelik muhakeme yapabilme",
            "MAT.6.1.2. Bir doğal sayının 2, 3, 4, 5, 6, 9 ve 10 ile tam bölünebilme kriterlerine ilişkin çıkarım yapabilme",
            "MAT.6.1.3. Bir doğal sayının asal olma durumunu ve asal çarpanlarını çözümleyebilme",
            "MAT.6.1.4. Günlük hayat problemleri ya da matematiksel durumlar üzerinden ortak kat ve ortak böleni yorumlayabilme"]),
        ("1. Tema: Sayılar ve Nicelikler (2)", [
            "MAT.6.1.5. Gerçek yaşam durumlarında ondalık gösterimlerin basamak değerlerini kesirlerden yararlanarak yorumlayabilme",
            "MAT.6.1.6. Kesir ve bölme işlemi arasındaki ilişkiye yönelik tümevarımsal akıl yürütebilme",
            "MAT.6.1.7. Gerçek yaşam durumlarında karşılaşılan kesir, ondalık ve yüzde gösterimleri ile ilgili dört işlem gerektiren problemleri çözebilme",
            "MAT.6.1.8. Karşılaştığı günlük hayat ya da matematiksel durumlarda standart uzunluk ölçme birimlerini değerlendirebilme"]),
        ("2. Tema: İşlemlerle Cebirsel Düşünme ve Değişimler", [
            "MAT.6.2.1. Gerçek yaşam durumlarında bilinen niceliklerden bilinmeyen niceliklere ilişkin muhakeme yapabilme",
            "MAT.6.2.2. Sayı ve şekil örüntülerini yorumlayabilme",
            "MAT.6.2.3. Cebirsel ifadeler içeren durumlardaki algoritmaları yorumlayabilme"]),
        ("3. Tema: Geometrik Şekiller", [
            "MAT.6.3.1. İki paralel doğru ve bir kesenin oluşturduğu açıları belirleyip sınıflandırarak adlandırabilme",
            "MAT.6.3.2. İki paralel doğrunun iki kesenle oluşturduğu şekillerin özellikleri hakkında çıkarım yapabilme",
            "MAT.6.3.3. Birbirini ortalayan doğru parçalarını köşegen kabul eden dörtgenler hakkında çıkarım yapabilme",
            "MAT.6.3.4. Üçgen, yamuk, paralelkenar, eşkenar dörtgen, dikdörtgen ve karenin açılarıyla ilgili problemleri çözebilme"]),
        ("4. Tema: Geometrik Nicelikler", [
            "MAT.6.4.1. Uzunluk ve alan ölçme birimleri arasındaki ilişkilerle ilgili analojik akıl yürütebilme",
            "MAT.6.4.2. Dikdörtgenin alan bağıntısına yönelik deneyimlerini paralelkenar ve üçgenin alan bağıntılarına yansıtabilme",
            "MAT.6.4.3. Geometrik şekillerin alanları ile modellenen gerçek yaşam durumlarına yönelik problem çözebilme",
            "MAT.6.4.4. Çemberin uzunluğu ile çap uzunluğu arasındaki ilişkiye yönelik çıkarım yapabilme",
            "MAT.6.4.5. Çap veya yarıçap uzunluğu verilen bir çemberin uzunluğu ile ilgili problemleri çözebilme",
            "MAT.6.4.6. Çemberde merkez açının ölçüsü ile gördüğü yayın uzunluğu arasındaki ilişkiye dair tümevarımsal akıl yürütebilme"]),
        ("5. Tema: İstatistiksel Araştırma Süreci", [
            "MAT.6.5.1. Kategorik veya nicel (kesikli) veri ile çalışabilme ve veriye dayalı karar verebilme",
            "MAT.6.5.2. Başkaları tarafından oluşturulan kategorik veya nicel (kesikli) veriye dayalı istatistiksel sonuç veya yorumları tartışabilme"]),
        ("6. Tema: Veriden Olasılığa", [
            "MAT.6.6.1. Bir olayın olasılığını gözleme dayalı tahmin edebilme"]),
    ],
    "7": [
        ("1. Tema: Sayılar ve Nicelikler (1)", [
            "MAT.7.1.1. Gerçek yaşam ya da matematiksel durumlarda doğal sayı, tam sayı ve rasyonel sayıları yorumlayabilme",
            "MAT.7.1.2. Gerçek yaşam durumlarında rasyonel sayıların ondalık gösterimlerini yansıtabilme",
            "MAT.7.1.3. Rasyonel sayıların karşılaştırma ve sıralama ilişkilerini yorumlayabilme",
            "MAT.7.1.4. Rasyonel sayılar ve işlemler içeren gerçek yaşam problemlerini çözebilme"]),
        ("1. Tema: Sayılar ve Nicelikler (2)", [
            "MAT.7.1.5. Gerçek yaşam durumları üzerinden oran ilişkileri hakkında muhakeme yapabilme",
            "MAT.7.1.6. Gerçek yaşam durumları üzerinden orantılı durumları yorumlayabilme",
            "MAT.7.1.7. Gerçek yaşam durumları üzerinden doğru orantılı durumlara ilişkin problemleri çözebilme"]),
        ("2. Tema: İşlemlerle Cebirsel Düşünme ve Değişimler", [
            "MAT.7.2.1. Cebirsel ifadelerle toplama, çıkarma ve rasyonel sayıyla çarpma işlemlerini yorumlayabilme",
            "MAT.7.2.2. Birinci dereceden bir bilinmeyenli denklem ve eşitsizliklerle gerçek yaşam problemlerini çözebilme",
            "MAT.7.2.3. Sayılar ve özellikleriyle ilgili ispatlara dair matematiksel muhakeme yapabilme",
            "MAT.7.2.4. Aritmetik ve cebirsel işlem süreçlerini algoritma ifade yöntemleriyle yapılandırabilme"]),
        ("3. Tema: Dönüşüm", [
            "MAT.7.3.1. Şekillerin yansıma dönüşümü altındaki görüntülerinin oluşturulmasına dair çıkarım yapabilme",
            "MAT.7.3.2. Yansıma dönüşümündeki deneyimlerini orta dikme ve açıortay inşasına yansıtabilme"]),
        ("4. Tema: Geometrik Nicelikler (1)", [
            "MAT.7.4.1. Eş küplerle kurulan yapılar ile bu yapıların görünümleri arasındaki ilişkiyi çözümleyebilme",
            "MAT.7.4.2. Dikdörtgenler prizmasının yüzey alanını yorumlayabilme",
            "MAT.7.4.3. Dikdörtgenler prizmasının hacmini eş nesnelerle yorumlayabilme",
            "MAT.7.4.4. Dikdörtgenler prizmasının hacim bağıntısını değerlendirebilme",
            "MAT.7.4.5. Hacim ölçme birimleri arasındaki ilişkileri değerlendirebilme",
            "MAT.7.4.6. Günlük hayat durumlarında dikdörtgenler prizmalarıyla modellenen cisimlerin yüzey alanı ve hacmine ilişkin problem çözebilme"]),
        ("4. Tema: Geometrik Nicelikler (2)", [
            "MAT.7.4.7. Dikdörtgen ve paralelkenar alanı ile çember uzunluğuna ilişkin deneyimleri dairenin alan bağıntısına aktarabilme",
            "MAT.7.4.8. Merkez açı ile gördüğü yay uzunluğu arasındaki ilişkiden yola çıkarak daire ve daire dilimi alanları arasında analojik akıl yürütebilme",
            "MAT.7.4.9. Eşkenar dörtgen ve yamuğun alan bağıntıları hakkında çıkarım yapabilme",
            "MAT.7.4.10. Günlük hayat durumlarında daire, daire dilimi, eşkenar dörtgen ve yamuğun alanına ilişkin problem çözebilme"]),
        ("5. Tema: Geometrik Şekiller", [
            "MAT.7.5.1. Matematiksel araçlarla üçgenin kenarortay, açıortay ve yüksekliğini analiz edebilme",
            "MAT.7.5.2. Orta dikme inşası deneyimlerini üçgende kenarortay inşasına aktarabilme"]),
        ("6. Tema: İstatistiksel Araştırma Süreci", [
            "MAT.7.6.1. Kategorik veya nicel (sürekli) veriyle çalışarak veriye dayalı karar verebilme",
            "MAT.7.6.2. Başkaları tarafından oluşturulan kategorik veya nicel (sürekli) veriye dayalı istatistiksel sonuç ve yorumları tartışabilme"]),
        ("7. Tema: Veriden Olasılığa", [
            "MAT.7.7.1. Bir olayın ve tümleyeninin olasılıklarına ilişkin tümevarımsal akıl yürütebilme",
            "MAT.7.7.2. Aynı deneye ait olayların eşit olasılıklı olup olmadığını değerlendirebilme",
            "MAT.7.7.3. Olayları ayrık veya ayrık olmayan olarak sınıflandırabilme"]),
    ],
    "8": [
        ("1. Tema: Sayılar ve Nicelikler", [
            "MAT.8.1.1. Üslü ifadeler, özellikleri ve üslü ifadelerle işlemler hakkında çıkarım yapabilme",
            "MAT.8.1.2. Kareköklü ifadelerle ilgili problem durumlarında akıl yürütebilme",
            "MAT.8.1.3. Sayıların rasyonel mi irrasyonel mi olduğunu değerlendirebilme",
            "MAT.8.1.4. Gerçek sayıları ve sayı aralıklarını sayı doğrusunda yorumlayabilme"]),
        ("2. Tema: Cebirsel Düşünme ve Değişimler", [
            "MAT.8.2.1. Gerçek yaşam durumlarında dik koordinat sistemini inceleyebilme",
            "MAT.8.2.2. Gerçek yaşamdaki doğrusal ilişkileri doğrusal fonksiyonlarla gösterebilme",
            "MAT.8.2.3. Dik koordinat sisteminde iki doğrusal fonksiyonun konumu hakkında çıkarım yapabilme",
            "MAT.8.2.4. Doğrusal fonksiyon problemlerinin çözümünü algoritma yöntemleriyle düzenleyebilme"]),
        ("3. Tema: Geometrik Şekiller", [
            "MAT.8.3.1. Araç ve teknoloji yardımıyla üçgenin kenar ve açıları arasındaki ilişkiyi yorumlayabilme",
            "MAT.8.3.2. Araç ve teknoloji yardımıyla üçgenin kenar uzunlukları arasındaki ilişkiye dair çıkarım yapabilme",
            "MAT.8.3.3. Bir üçgene eş üçgen oluşturmak için hangi elemanların bilinmesinin yeterli olduğuna dair çıkarım yapabilme",
            "MAT.8.3.4. Bir üçgene benzer üçgen oluşturmak için hangi elemanların bilinmesinin yeterli olduğuna dair çıkarım yapabilme",
            "MAT.8.3.5. a²+b²=c² koşulunu sağlayan üçgenlerle dik üçgeni ve Pisagor bağıntısını yorumlayabilme",
            "MAT.8.3.6. Üçgende açı-kenar ilişkisi, üçgen eşitsizliği ve Pisagor bağıntısını içeren problemleri çözebilme"]),
        ("4. Tema: Geometrik Nicelikler", [
            "MAT.8.4.1. Dik prizmalar, dikdörtgen dik piramit, dik dairesel silindir ve dik dairesel koninin yüzey açınımlarını çözümleyebilme",
            "MAT.8.4.2. Dik dairesel silindirin yüzey açınımına ilişkin deneyimlerini dik dairesel silindirin yüzey alanına yansıtabilme",
            "MAT.8.4.3. Dairenin alan bağıntısının oluşturulma sürecinden hareketle dik dairesel silindirin hacim bağıntısına yönelik analojik akıl yürütebilme"]),
        ("5. Tema: Dönüşüm", [
            "MAT.8.5.1. Araç ve teknolojiyle öteleme dönüşümünü analiz edebilme",
            "MAT.8.5.2. Noktaların koordinatlarındaki değişimler hakkında öteleme ve eksen yansımasında çıkarım yapabilme",
            "MAT.8.5.3. Öteleme ve yansıma dönüşümü içeren problemleri çözebilme"]),
        ("6. Tema: İstatistiksel Araştırma Süreci", [
            "MAT.8.6.1. Kategorik veya nicel (kesikli-sürekli) veri ile çalışabilme ve veriye dayalı karar verebilme",
            "MAT.8.6.2. Başkaları tarafından oluşturulan kategorik veya nicel (kesikli-sürekli) veriye dayalı istatistiksel sonuç veya yorumları tartışabilme"]),
        ("7. Tema: Veriden Olasılığa", [
            "MAT.8.7.1. Gerçek yaşamdaki bir olayın olasılığı için öznel, deneysel veya teorik yaklaşımlardan uygun olanını seçerek karar verebilme"]),
    ],
}


def units(g, subject):
    b = base_grade(g)
    if subject == MAT and b in MEB_MAT:  # resmî MEB (tymm.meb.gov.tr) tema adları ve kazanımları kesin kaynaktır
        return MEB_MAT[b]
    lv = LIVE.get(f"{b}|{subject}")
    if lv:
        return lv
    return C[b].get(subject, [])


def _idx(w, n):
    return min(n - 1, int((w - 1) * n / TOTAL_WEEKS))


def week_unit_info(g, subject, w):
    """(unit_index, pozisyon, uzunluk) -> haftanın ünite içindeki yeri."""
    us = units(g, subject)
    n = len(us)
    if not n:
        return None
    u = _idx(w, n)
    weeks_of_u = [x for x in range(1, TOTAL_WEEKS + 1) if _idx(x, n) == u]
    return u, weeks_of_u.index(w), len(weeks_of_u)


def scope_range(scope):
    if scope["type"] == "month":
        return scope["a"], scope["b"]
    return scope["w"], scope["w"]


def scope_label(scope):
    if scope["type"] == "month":
        a, b = scope_range(scope)
        return f"AGİS • {scope['name']} Ayı (Hafta {a}-{b})"
    return f"{scope['w']}. Hafta ({week_dates(scope['w'])})"


def scope_units(g, subject, scope):
    """Kapsamdaki üniteler [(ad, konular, not)]"""
    us = units(g, subject)
    a, b = scope_range(scope)
    out, seen = [], set()
    for w in range(a, b + 1):
        info = week_unit_info(g, subject, w)
        if not info:
            continue
        u, p, k = info
        if u in seen:
            continue
        seen.add(u)
        note = f"(ünitenin {p + 1}/{k}. haftası)" if scope["type"] == "week" and k > 1 else ""
        out.append((us[u][0], us[u][1], note))
    return out


def scope_topic_text(g, subject, scope):
    parts = []
    for name, topics, note in scope_units(g, subject, scope):
        parts.append(f"{name} {note}: " + ", ".join(topics))
    return " | ".join(parts)


def scope_short(g, subject, scope):
    return "; ".join(n.split(" (MAT")[0] for n, _, _ in scope_units(g, subject, scope))


def all_topics(g, subject):
    out = []
    for name, topics in units(g, subject):
        for t in topics:
            out.append((name, t))
    return out


# ---- Sınav ön ayarları ----
def weekly_counts(g, monthly=False):
    if g == "LGS" and not monthly:
        return {TR: 15, MAT: 15, FEN: 15, INK: 15, DIN: 10, ING: 10}  # 80 soruluk mevcut format
    if g == "LGS" and monthly:
        return {TR: 15, MAT: 15, FEN: 15, INK: 15, DIN: 10, ING: 10}
    base = subjects_for(g)
    if monthly:
        d = {TR: 12, MAT: 12, FEN: 12, SOS: 12, INK: 12, DIN: 6, ING: 6}
    else:
        d = {TR: 8, MAT: 8, FEN: 8, SOS: 8, INK: 8, DIN: 4, ING: 4}
    out = {s: d.get(s, 0) for s in base}
    out[ALM] = 0 if ALM in out else 0
    if ALM not in base:
        out.pop(ALM, None)
    return out


LGS_OFFICIAL = {TR: 20, MAT: 20, FEN: 20, INK: 10, DIN: 10, ING: 10}  # resmî LGS 90 soru
'''
MODULES['core/oyss'] = r'''# -*- coding: utf-8 -*-
"""MEB Ortak Yazılı Sınav Sistemi (OYSS) - senaryo motoru.

Doğrulanan resmî bilgiler (MEB OYSS Uygulama Kılavuzu, ÖDSGM tabloları):
- Senaryo = konu-soru dağılım tablosundaki alternatif soru dağılım şablonu (S1..S5).
- Sınav açık uçlu ya da açık uçlu + kısa cevaplı sorulardan oluşur; 100 puan; en fazla 4 sayfa.
- Soru kolay/orta/zor etiketlidir. Resmî uygulama 5-6-7 (ortaokul) ve 9-10-11. sınıflardadır.
- 5. sınıf Matematik 1. dönem yazılıları tabloları ÖDSGM verisinden birebir aşağıdadır (40 dk).
Diğer ders/sınıf tabloları, aynı şablon mantığıyla müfredat konularından türetilir; ÖDSGM tablosunu
VERIFIED sözlüğüne ekleyerek birebir resmî hâle getirebilirsiniz.
"""
from . import curriculum as cur

SCENARIOS = [1, 2, 3, 4, 5]
OFFICIAL_GRADES = ("5", "6", "7")
DURATION_MIN = 40
TOTAL_POINTS = 100
MAX_PAGES = 4

# (sınıf, ders, dönem, yazılı) -> [(ünite, kod, [S1..S5])]
VERIFIED = {
    ("5", cur.MAT, 1, 1): [
        ("3. Tema: Geometrik Şekiller", "MAT.5.3.1", [1, 1, 1, 1, 1]),
        ("3. Tema: Geometrik Şekiller", "MAT.5.3.2", [1, 1, 0, 1, 1]),
        ("3. Tema: Geometrik Şekiller", "MAT.5.3.3", [1, 1, 2, 2, 2]),
        ("3. Tema: Geometrik Şekiller", "MAT.5.3.4", [1, 1, 2, 1, 2]),
        ("3. Tema: Geometrik Şekiller", "MAT.5.3.5", [1, 1, 1, 1, 1]),
        ("3. Tema: Geometrik Şekiller", "MAT.5.3.6", [1, 2, 1, 0, 0]),
        ("3. Tema: Geometrik Şekiller", "MAT.5.3.7", [1, 0, 0, 0, 0]),
    ],
    ("5", cur.MAT, 1, 2): [
        ("3. Tema: Geometrik Şekiller", "MAT.5.3.5", [0, 0, 1, 0, 1]),
        ("3. Tema: Geometrik Şekiller", "MAT.5.3.6", [0, 1, 0, 1, 1]),
        ("3. Tema: Geometrik Şekiller", "MAT.5.3.7", [2, 2, 1, 1, 1]),
        ("1. Tema: Sayılar ve Nicelikler (1)", "MAT.5.1.1", [2, 2, 2, 2, 1]),
        ("1. Tema: Sayılar ve Nicelikler (1)", "MAT.5.1.2", [2, 2, 2, 2, 2]),
        ("4. Tema: Geometrik Nicelikler", "MAT.5.4.1", [1, 1, 1, 0, 0]),
        ("4. Tema: Geometrik Nicelikler", "MAT.5.4.2", [1, 0, 0, 0, 0]),
    ],
}

_BASE_TOTALS = [7, 7, 7, 6, 7]
# senaryo karakteri (ağırlık profili): 1 dengeli, 2 başa, 3 ortaya, 4 bir konu hariç dengeli, 5 sona
_PROFILE_NAMES = {1: "Dengeli dağılım", 2: "Dönem başı kazanımlara ağırlık", 3: "Orta kazanımlara ağırlık",
                  4: "Bir kazanım hariç, dengeli dağılım", 5: "Dönem sonu kazanımlara ağırlık"}


def window_weeks(term, yazili):
    start = (term - 1) * 18 + (yazili - 1) * 9 + 1
    return start, start + 8


def _topics_for(g, subject, term, yazili):
    a, b = window_weeks(term, yazili)
    us = cur.units(g, subject)
    n = len(us)
    seen, out = [], []
    for w in range(a, b + 1):
        u = cur._idx(w, n)
        if u not in seen:
            seen.append(u)
    for u in seen:
        for t in us[u][1]:
            out.append((us[u][0], "", t))
    if len(out) > 5:
        step = len(out) / 5
        out = [out[int(i * step)] for i in range(5)]
    return out


def _distribute(n, total, scen):
    if scen == 1:
        w = [1.0] * n
        w[0] += .02
        w[-1] += .02
    elif scen == 2:
        w = [n - i + 1 for i in range(n)]
    elif scen == 3:
        mid = (n - 1) / 2
        w = [n - abs(i - mid) for i in range(n)]
    elif scen == 4:
        w = [1.0] * n
        w[n // 2] = 0
    else:
        w = [i + 2 for i in range(n)]
    nz = [i for i in range(n) if w[i] > 0]
    counts = [0] * n
    for i in nz:  # her kazanıma en az 1
        counts[i] = 1
    rest = total - sum(counts)
    while rest > 0:
        i = max(nz, key=lambda j: w[j] / (counts[j] + 0.6))
        counts[i] += 1
        rest -= 1
    while rest < 0:
        i = max((j for j in nz if counts[j] > 1), key=lambda j: counts[j] / w[j], default=None)
        if i is None:
            break
        counts[i] -= 1
        rest += 1
    return counts


def scenario_table(grade, subject, term, yazili, scen):
    """-> dict(rows=[{unit, code, topic, n}], total, verified)"""
    g = cur.base_grade(grade)
    key = (g, subject, term, yazili)
    if key in VERIFIED:
        kz = {k.split(". ", 1)[0]: k.split(". ", 1)[-1] for _, ks in cur.units(g, subject) for k in ks}
        rows = [{"unit": u, "code": c, "topic": kz.get(c, u), "n": cnt[scen - 1]}
                for u, c, cnt in VERIFIED[key] if cnt[scen - 1] > 0]
        return {"rows": rows, "total": sum(r["n"] for r in rows), "verified": True}
    topics = _topics_for(grade, subject, term, yazili)
    counts = _distribute(len(topics), _BASE_TOTALS[scen - 1], scen)
    rows = [{"unit": u, "code": f"K{i + 1}", "topic": t, "n": c}
            for i, ((u, _, t), c) in enumerate(zip(topics, counts)) if c > 0]
    return {"rows": rows, "total": sum(r["n"] for r in rows), "verified": False}


def point_split(total_q, total_points=TOTAL_POINTS):
    if total_q <= 0:
        return []
    base = total_points // total_q
    pts = [base] * total_q
    for i in range(total_points - base * total_q):
        pts[-(i + 1)] += 1
    return pts


def difficulty_labels(n):
    """MEB: kolay/orta/zor etiketli - yaklaşık 30/50/20 dağılım."""
    e = max(1, round(n * 0.3))
    h = max(1, round(n * 0.2))
    m = max(0, n - e - h)
    return ["Kolay"] * e + ["Orta"] * m + ["Zor"] * h


def profile_name(scen):
    return _PROFILE_NAMES[scen]
'''
MODULES['core/fenfig'] = r'''# -*- coding: utf-8 -*-
"""Fen Bilimleri / basit makineler çizimleri (Soru Fabrikası'ndan uyarlandı): sorudaki verilerle ölçekli, cevaba ipucu vermeyen şemalar."""
import itertools
import re
import textwrap
import numpy as np
from matplotlib.patches import Arc, FancyBboxPatch, Polygon, Rectangle, Wedge
import matplotlib.pyplot as plt


def _norm(s):
    s = str(s).replace("İ", "i").replace("I", "i").lower()
    for a, b in zip("çğıöşü", "cgiosu"):
        s = s.replace(a, b)
    return s.replace(" ", "_").replace("-", "_").replace("(", "").replace(")", "")



def _t(x):
    """Etiketi matplotlib için güvenli metne çevirir ($ / LaTeX kalıntılarını temizler)."""
    s = "" if x is None else str(x)
    s = s.replace("^\\circ", "°").replace("\\circ", "°").replace("$", "")
    s = re.sub(r'\\frac\{([^}]+)\}\{([^}]+)\}', r'\1/\2', s)
    s = s.replace("\\%", "%").replace("\\", "")
    return s.strip()


_OLCU_RE = re.compile(r'\s*(\d+(?:[.,]\d+)?)\s*(?:°|derece|cm|mm|km|m|N|kg|g|br|birim)?\s*', re.I)


def olcu_cek(deger):
    """'6 cm', '40°', 8 -> sayı. Sadece SAF ölçüler (x, 2x gibi cebirsel ifadeler -> None)."""
    if deger is None:
        return None
    if isinstance(deger, (int, float)):
        return float(deger)
    m = _OLCU_RE.fullmatch(str(deger))
    return float(m.group(1).replace(",", ".")) if m else None


def sayi_cek(deger, varsayilan=None):
    if deger is None:
        return varsayilan
    if isinstance(deger, (int, float)):
        return float(deger)
    m = re.search(r'-?\d+(?:[.,]\d+)?', str(deger))
    return float(m.group(0).replace(",", ".")) if m else varsayilan


def liste_cek(deger):
    if deger is None:
        return []
    if isinstance(deger, (list, tuple)):
        return list(deger)
    if isinstance(deger, str):
        ayirici = r'[;|]' if re.search(r'[;|]', deger) else r','
        return [x.strip() for x in re.split(ayirici, deger) if x.strip()]
    return [deger]




def _sar(metin, genislik=11):
    return textwrap.fill(_t(metin), genislik, break_long_words=False, break_on_hyphens=False)


def _guzel_adim(ust):
    for st_ in (0.1, 0.2, 0.5, 1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000):
        if ust / st_ <= 10:
            return st_
    return max(ust / 10, 1)



def _guzel_maks(v):
    for m in (5, 10, 20, 25, 50, 100, 200, 500):
        if v <= m:
            return m
    return float(np.ceil(v / 100) * 100)


def _dinamometre_tek(ax, cx, kuvvet, maks, ad="", yuk="", n=1, deger_yaz=False):
    w = 1.3 if n == 1 else 1.18
    ust, alt = 4.5, 1.9
    kuvvet = min(max(kuvvet, 0.0), maks)
    # asma halkası + gövde
    ax.add_patch(plt.Circle((cx, 4.78), 0.15, fill=False, ec='#475569', linewidth=2.4, zorder=2))
    ax.plot([cx, cx], [4.63, ust], color='#475569', linewidth=2.6, zorder=2)
    ax.add_patch(FancyBboxPatch((cx - w / 2, alt), w, ust - alt, boxstyle="round,pad=0,rounding_size=0.12",
                                fc='#e2e8f0', ec='#0f172a', linewidth=2.2, zorder=2))
    px0, px1 = cx - w / 2 + 0.09, cx + w / 2 - 0.09
    ax.add_patch(Rectangle((px0, alt + 0.1), px1 - px0, ust - alt - 0.2, fc='#ffffff', ec='#94a3b8', linewidth=1.2, zorder=3))
    s0, s1 = ust - 0.32, alt + 0.3

    def yv(v):
        return s0 - (v / maks) * (s0 - s1)
    adim = 1.0 if maks <= 10 else maks / 10.0
    for v in np.arange(0, maks + 1e-9, adim):
        ax.plot([px0, px0 + 0.16], [yv(v), yv(v)], color='#0f172a', linewidth=1.4, zorder=4)
        ax.text(px0 + 0.21, yv(v), f"{v:g}", fontsize=7.5, va='center', ha='left', color='#0f172a', zorder=4)
        if v + adim / 2 <= maks + 1e-9:
            ax.plot([px0, px0 + 0.08], [yv(v + adim / 2)] * 2, color='#0f172a', linewidth=0.9, zorder=4)
    ax.text(px1 - 0.03, ust - 0.2, "N", fontsize=9, fontweight='bold', color='#dc2626', ha='right', va='center', zorder=4)
    # kılavuz yuva
    ax.add_patch(Rectangle((cx - 0.045, yv(maks) - 0.06), 0.09, (yv(0) - yv(maks)) + 0.12, fc='#cbd5e1', ec='none', zorder=3))
    # ibre + çubuk + kanca
    yp = yv(kuvvet)
    ext = 0.1 + 0.3 * (kuvvet / maks)
    uc = alt - ext
    ax.plot([cx, cx], [yp, uc], color='#64748b', linewidth=3, zorder=4, solid_capstyle='butt')
    ax.plot([px0 + 0.02, cx - 0.09], [yp, yp], color='#dc2626', linewidth=1.2, zorder=3.5, alpha=0.9)
    ax.plot([cx - 0.09, px1 - 0.02], [yp, yp], color='#dc2626', linewidth=3.2, zorder=5, solid_capstyle='round')
    ax.add_patch(plt.Circle((cx, uc - 0.08), 0.08, fill=False, ec='#475569', linewidth=2, zorder=4))
    ip_ust = uc - 0.16
    bw, bh = (0.92, 0.6) if n == 1 else (0.8, 0.54)
    ax.plot([cx, cx], [ip_ust, ip_ust - 0.2], color='#475569', linewidth=2, zorder=4)
    wy = ip_ust - 0.2 - bh
    ax.add_patch(Rectangle((cx - bw / 2, wy), bw, bh, fc='#cbd5e1', ec='#0f172a', linewidth=2, zorder=4))
    ax.text(cx, wy + bh / 2, _t(yuk) or "Yük", fontsize=8.5 if n == 1 else 8, fontweight='bold', ha='center', va='center', color='#0f172a', zorder=5)
    if ad:
        ax.text(cx, max(wy - 0.22, 0.2), _t(ad), fontsize=12, fontweight='bold', ha='center', va='center', color='#0f172a')
    if deger_yaz:
        ax.text(cx + w / 2 + 0.1, yp, f"{kuvvet:g} N", fontsize=9, fontweight='bold', color='#dc2626', ha='left', va='center',
                bbox=dict(boxstyle='round,pad=0.2', fc='white', ec='#fca5a5', lw=1), zorder=6)


def _dinamometre_ciz(ax, et):
    ham = et.get("kuvvetler") if et.get("kuvvetler") is not None else et.get("kuvvet")
    ks = [sayi_cek(x, 0.0) for x in liste_cek(ham)][:3] or [4.0]
    maks = sayi_cek(et.get("maks"), None) or _guzel_maks(max(ks))
    maks = max(maks, max(ks))
    yukler = liste_cek(et.get("yukler") if et.get("yukler") is not None else et.get("yuk"))
    isimler = liste_cek(et.get("isimler"))
    deger_yaz = _norm(et.get("deger_yaz", "hayir")) in ("evet", "true", "1")
    n = len(ks)
    merkezler = {1: [3.0], 2: [1.9, 4.1], 3: [1.0, 3.0, 5.0]}[n]
    for i, (cx, kv) in enumerate(zip(merkezler, ks)):
        _dinamometre_tek(ax, cx, kv, maks, isimler[i] if i < len(isimler) else "",
                         yukler[i] if i < len(yukler) else "", n=n, deger_yaz=deger_yaz)


def _surtunme_ciz(ax, et):
    kv = sayi_cek(et.get("kuvvet") if et.get("kuvvet") is not None else et.get("kuvvetler"), 3.0)
    maks = max(sayi_cek(et.get("maks"), None) or _guzel_maks(kv), kv)
    zy = 1.4
    ax.plot([0.3, 5.7], [zy, zy], color='#0f172a', linewidth=2.5)
    for x in np.arange(0.4, 5.7, 0.22):
        ax.plot([x, x - 0.14], [zy, zy - 0.14], color='#94a3b8', linewidth=1)
    yuzey = _t(et.get("yuzey", ""))
    if yuzey:
        ax.text(3.0, 0.7, yuzey, fontsize=10, fontweight='bold', ha='center', color='#475569')
    ax.add_patch(Rectangle((0.9, zy), 1.4, 0.95, fc='#cbd5e1', ec='#0f172a', linewidth=2, zorder=3))
    ax.text(1.6, zy + 0.47, _t(et.get("yuk", "Cisim")), fontsize=10, fontweight='bold', ha='center', va='center', zorder=4)
    ay = zy + 0.47
    ax.plot([2.3, 2.75], [ay, ay], color='#475569', linewidth=2.5)
    bx0, bx1 = 2.75, 4.95
    ax.add_patch(Rectangle((bx0, ay - 0.22), bx1 - bx0, 0.44, fc='#f1f5f9', ec='#0f172a', linewidth=2, zorder=3))
    sx0, sx1 = bx0 + 0.18, bx1 - 0.18
    step = 1.0 if maks <= 10 else maks / 10
    for v in np.arange(0, maks + 1e-9, step):
        x = sx0 + (v / maks) * (sx1 - sx0)
        ax.plot([x, x], [ay + 0.22, ay + 0.08], color='#0f172a', linewidth=1.2, zorder=4)
        ax.text(x, ay + 0.3, f"{v:g}", fontsize=6.5, ha='center', va='bottom', zorder=4)
    xp = sx0 + (min(max(kv, 0), maks) / maks) * (sx1 - sx0)
    ax.plot([xp, xp], [ay - 0.2, ay + 0.2], color='#dc2626', linewidth=2.4, zorder=5)
    ax.text((bx0 + bx1) / 2, ay + 0.62, "Kuvvet (N)", fontsize=7.5, fontweight='bold', color='#dc2626', ha='center', va='bottom')
    ax.plot([bx1, bx1 + 0.2], [ay, ay], color='#475569', linewidth=2.5)
    ax.annotate("", xy=(5.75, ay), xytext=(5.15, ay), arrowprops=dict(arrowstyle='->', color='#16a34a', lw=2.2))
    ax.text(5.45, ay + 0.2, "Çekme", fontsize=8, fontweight='bold', color='#16a34a', ha='center')
    if _norm(et.get("surtunme_goster", "evet")) not in ("hayir", "false", "0"):
        ax.annotate("", xy=(0.45, zy + 0.12), xytext=(0.9, zy + 0.12), arrowprops=dict(arrowstyle='->', color='#dc2626', lw=2.2))
        ax.text(0.62, zy + 0.32, "Sürtünme", fontsize=7.5, fontweight='bold', color='#dc2626', ha='center')


# --- BASINÇ ---
def _basinc_kati(ax, et):
    durus = _norm(et.get("durus", "yatay"))
    w, h = (1.0, 2.4) if durus == "dikey" else (2.4, 1.0)
    zemin, cx = 1.3, 3.0
    ax.plot([0.5, 5.5], [zemin, zemin], color='#0f172a', linewidth=2.5)
    for x in np.arange(0.6, 5.5, 0.25):
        ax.plot([x, x - 0.15], [zemin, zemin - 0.15], color='#94a3b8', linewidth=1)
    ax.add_patch(Rectangle((cx - w / 2, zemin), w, h, fc='#cbd5e1', ec='#0f172a', linewidth=2, zorder=3))
    cisim = _t(et.get("cisim", ""))
    if cisim:
        ax.text(cx, zemin + h * 0.78, cisim, fontsize=10, fontweight='bold', ha='center', va='center', zorder=5)
    ax.annotate("", xy=(cx, zemin + 0.04), xytext=(cx, zemin + h * 0.5),
                arrowprops=dict(arrowstyle='->', color='#0f172a', lw=2), zorder=5)
    ax.text(cx + w / 2 + 0.12, zemin + h * 0.3, _t(et.get("G", "G")), fontsize=10, fontweight='bold', ha='left', va='center', zorder=5)
    ax.plot([cx + 0.04, cx + w / 2 + 0.08], [zemin + h * 0.3] * 2, color='#94a3b8', linewidth=0.9, linestyle=':', zorder=4)
    if et.get("F"):
        ax.annotate("", xy=(cx, zemin + h + 0.05), xytext=(cx, zemin + h + 0.95),
                    arrowprops=dict(arrowstyle='->', color='#dc2626', lw=2.4))
        ax.text(cx + 0.12, zemin + h + 0.5, _t(et["F"]), fontsize=10, fontweight='bold', color='#dc2626', ha='left', va='center')
    ax.annotate("", xy=(cx - w / 2, zemin - 0.4), xytext=(cx + w / 2, zemin - 0.4),
                arrowprops=dict(arrowstyle='<->', color='#475569', lw=1.6))
    s_et = _t(et.get("S", ""))
    ax.text(cx, zemin - 0.7, (f"S = {s_et}" if s_et and "=" not in s_et and s_et != "S" else (s_et or "S")),
            fontsize=9, fontweight='bold', ha='center', va='top', color='#475569')


def _basinc_sivi(ax, et):
    y0, yu = 0.9, 4.1
    seviye = 3.5
    noktalar = [_t(x) for x in liste_cek(et.get("noktalar"))]
    n = 1 if noktalar else max(1, min(int(sayi_cek(et.get("kap_sayisi"), 1)), 3))
    genislik = {1: [2.6 if noktalar else 1.8], 2: [1.4, 2.2], 3: [1.1, 1.8, 1.2]}[n]
    merkez = {1: [3.0], 2: [1.9, 4.2], 3: [1.2, 3.0, 4.8]}[n]
    sivi = _t(et.get("sivi_adi", "Su"))
    for cx, w in zip(merkez, genislik):
        ax.add_patch(Rectangle((cx - w / 2, y0), w, seviye - y0, fc='#bae6fd', ec='none', alpha=0.9, zorder=1))
        ax.plot([cx - w / 2, cx - w / 2, cx + w / 2, cx + w / 2], [yu, y0, y0, yu], color='#0f172a', linewidth=2.4, zorder=3)
        ax.plot([cx - w / 2 + 0.03, cx + w / 2 - 0.03], [seviye, seviye], color='#0284c7', linewidth=1.8, zorder=3)
    ax.text(merkez[-1], y0 - 0.3, sivi, fontsize=9, fontweight='bold', ha='center', va='top', color='#0369a1')
    if noktalar:
        der = [sayi_cek(x, i + 1.0) for i, x in enumerate(liste_cek(et.get("derinlikler")))]
        der += [float(i + 1) for i in range(len(der), len(noktalar))]
        dl = liste_cek(et.get("derinlikler"))
        mx = max(der)
        cx, w = merkez[0], genislik[0]
        for i, (ad, d) in enumerate(zip(noktalar, der)):
            y = seviye - (d / mx) * (seviye - y0 - 0.45)
            ax.plot([cx - w / 2, cx], [y, y], color='#475569', linewidth=0.9, linestyle=':', zorder=3)
            ax.plot(cx, y, 'ko', markersize=5, zorder=5)
            ax.text(cx + 0.15, y, ad, fontsize=10, fontweight='bold', va='center', zorder=5)
            if i < len(dl):
                ax.text(cx - w / 2 - 0.1, y, _t(dl[i]), fontsize=8, fontweight='bold', ha='right', va='center', color='#dc2626')
        return
    yp = seviye - 1.4
    for cx, w in zip(merkez, genislik):
        ax.plot(cx, yp, 'ko', markersize=5, zorder=5)
        ax.text(cx + 0.14, yp - 0.02, _t(et.get("P", "P")), fontsize=10, fontweight='bold', va='center', zorder=5)
        ax.annotate("", xy=(cx, yp + 0.05), xytext=(cx, seviye - 0.02), arrowprops=dict(arrowstyle='<->', color='#dc2626', lw=1.8), zorder=5)
        if et.get("h"):
            ax.text(cx - 0.1, (yp + seviye) / 2, _t(et["h"]), fontsize=9, fontweight='bold', color='#dc2626', ha='right', va='center', zorder=5)


# --- EK GÖRSEL TİPLERİ: MEVSİM, DNA, ÇAPRAZLAMA, DİRENÇ, BASİT MAKİNELER ---
def _mevsim_ciz(ax, et):
    gx, gy, a, b = 3.0, 2.5, 2.05, 1.4
    th = np.linspace(0, 2 * np.pi, 200)
    ax.plot(gx + a * np.cos(th), gy + b * np.sin(th), color='#94a3b8', linestyle='--', linewidth=1.2)
    ax.add_patch(plt.Circle((gx, gy), 0.42, color='#f59e0b', ec='#d97706', linewidth=2, zorder=2))
    ax.text(gx, gy, _t(et.get("G", "Güneş")), fontsize=6, fontweight='bold', color='#ffffff', ha='center', va='center', zorder=3)
    # (anahtar, yörünge açısı, tarih, kuzey yarımküre mevsimi) - Dünya saat yönünün tersine döner
    KON = [("haziran", 180, "21 Haziran", "Yaz"), ("eylul", 270, "23 Eylül", "Sonbahar"),
           ("aralik", 0, "21 Aralık", "Kış"), ("mart", 90, "21 Mart", "İlkbahar")]
    harf = {"haziran": "K", "eylul": "L", "aralik": "M", "mart": "N"}
    vurgu = _norm(et.get("vurgula", ""))
    tarih = _norm(et.get("tarih_goster", "hayir")) in ("evet", "true", "1")
    mevsim = _norm(et.get("mevsim_goster", "hayir")) in ("evet", "true", "1")
    tilt = np.radians(23.5)
    ux, uy = np.sin(tilt), np.cos(tilt)
    r = 0.3
    for key, ang, tr, mv in KON:
        t = np.radians(ang)
        ex, ey = gx + a * np.cos(t), gy + b * np.sin(t)
        ad = _t(et.get(key, harf[key]))
        if vurgu == key:
            ax.add_patch(plt.Circle((ex, ey), r + 0.13, fill=False, ec='#f97316', linewidth=2.4, zorder=3))
        ax.add_patch(plt.Circle((ex, ey), r, fc='#1e3a5f', ec='#0f172a', linewidth=1.4, zorder=4))
        gd = np.degrees(np.arctan2(gy - ey, gx - ex))
        ax.add_patch(Wedge((ex, ey), r, gd - 90, gd + 90, fc='#7dd3fc', ec='#0f172a', linewidth=1.0, zorder=5))
        ax.plot([ex - ux * (r + 0.2), ex + ux * (r + 0.2)], [ey - uy * (r + 0.2), ey + uy * (r + 0.2)],
                color='#dc2626', linewidth=1.8, zorder=6)
        ax.plot(ex + ux * (r + 0.2), ey + uy * (r + 0.2), 'o', color='#dc2626', ms=3.5, zorder=7)
        d = np.array([ex - gx, ey - gy])
        d = d / np.linalg.norm(d)
        lx, ly = ex + d[0] * (r + 0.55), ey + d[1] * (r + 0.5)
        metin = ad
        if tarih:
            metin += f"\n{tr}"
        if mevsim:
            metin += f"\n{mv}"
        ax.text(lx, ly, metin, fontsize=9 if metin == ad else 7, fontweight='bold', ha='center', va='center', color='#0f172a', zorder=8)
    ax.text(0.15, 0.2, "Kırmızı çubuk: Dünya'nın eksen eğikliği (kuzey ucu noktalı)", fontsize=5.5, color='#64748b', va='center')


def _dna_ciz(ax, et):
    dizi = re.sub(r'[^ATGC]', '', str(et.get("baz_dizisi", "ATGCCTAG")).upper())[:10] or "ATGCCTAG"
    n = len(dizi)
    comp = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}
    renk = {'A': '#ef4444', 'T': '#3b82f6', 'G': '#22c55e', 'C': '#f59e0b'}
    gizle = _norm(et.get("gizle", "")) in ("tamamlayici", "ikinci_zincir", "evet")
    xs = np.linspace(0.9, 5.1, n)
    xx = np.linspace(0.5, 5.5, 300)
    dalga = 0.14 * np.sin(2 * np.pi * (xx - 0.5) / 1.7)
    ax.plot(xx, 3.35 + dalga, color='#64748b', linewidth=3.5, solid_capstyle='round', zorder=2)
    ax.plot(xx, 1.65 - dalga, color='#64748b', linewidth=3.5, solid_capstyle='round', zorder=2)
    for x, b in zip(xs, dizi):
        yt = 3.35 + 0.14 * np.sin(2 * np.pi * (x - 0.5) / 1.7)
        yb = 1.65 - 0.14 * np.sin(2 * np.pi * (x - 0.5) / 1.7)
        ym = (yt + yb) / 2
        c2 = comp[b]
        ax.plot([x, x], [yt, ym], color=renk[b], linewidth=3.2, zorder=3)
        ax.plot([x, x], [ym, yb], color='#cbd5e1' if gizle else renk[c2], linewidth=3.2, zorder=3)
        ax.add_patch(plt.Circle((x, yt), 0.17, fc=renk[b], ec='#0f172a', linewidth=1.2, zorder=4))
        ax.text(x, yt, b, fontsize=8, fontweight='bold', color='#ffffff', ha='center', va='center', zorder=5)
        ax.add_patch(plt.Circle((x, yb), 0.17, fc='#e2e8f0' if gizle else renk[c2], ec='#0f172a', linewidth=1.2, zorder=4))
        ax.text(x, yb, "?" if gizle else c2, fontsize=8, fontweight='bold', color='#0f172a' if gizle else '#ffffff',
                ha='center', va='center', zorder=5)
    if et.get("baslik"):
        ax.text(3.0, 0.6, _t(et["baslik"]), fontsize=9, fontweight='bold', ha='center', color='#475569')


def _caprazlama_ciz(ax, et):
    e1 = re.sub(r'[^A-Za-z]', '', str(et.get("ebeveyn1", "Aa")))
    e2 = re.sub(r'[^A-Za-z]', '', str(et.get("ebeveyn2", "Aa")))
    if len(e1) < 2 or len(e1) % 2 or len(e1) != len(e2) or len(e1) > 4:
        e1, e2 = "Aa", "Aa"
    p1 = [e1[i:i + 2] for i in range(0, len(e1), 2)]
    p2 = [e2[i:i + 2] for i in range(0, len(e2), 2)]
    g1 = [''.join(c) for c in itertools.product(*p1)]
    g2 = [''.join(c) for c in itertools.product(*p2)]
    goster = _norm(et.get("hucreleri_goster", "hayir")) in ("evet", "true", "1")
    n1, n2 = len(g2), len(g1)
    cw = min(0.95, 3.6 / n1)
    ch = min(0.7, 2.8 / n2)
    x0, y0 = 1.6, 3.9 - ch
    ax.text(x0 - 0.12, y0 - (n2 * ch) / 2, _t(et.get("ad1", e1)), fontsize=10, fontweight='bold', ha='right', va='center', color='#4f46e5')
    ax.text(x0 + 0.5 + cw * n1 / 2, y0 + ch * 0.6 + 0.12, _t(et.get("ad2", e2)), fontsize=10, fontweight='bold', ha='center', va='bottom', color='#db2777')
    for j, g in enumerate(g2):
        ax.add_patch(Rectangle((x0 + 0.5 + j * cw, y0 + ch * 0.0 + 0.0), cw, ch * 0.6, fc='#fce7f3', ec='#0f172a', linewidth=1.2))
        ax.text(x0 + 0.5 + (j + 0.5) * cw, y0 + ch * 0.3, g, fontsize=8, fontweight='bold', ha='center', va='center')
    top = y0
    for i, g in enumerate(g1):
        yy = top - (i + 1) * ch
        ax.add_patch(Rectangle((x0, yy), 0.5, ch, fc='#e0e7ff', ec='#0f172a', linewidth=1.2))
        ax.text(x0 + 0.25, yy + ch / 2, g, fontsize=8, fontweight='bold', ha='center', va='center')
        for j, h in enumerate(g2):
            gen = []
            for k in range(len(p1)):
                ik = g[k] + h[k]
                gen.append(''.join(sorted(ik, key=lambda c: (c.islower(), c))))
            ax.add_patch(Rectangle((x0 + 0.5 + j * cw, yy), cw, ch, fc='#ffffff', ec='#0f172a', linewidth=1.2))
            ax.text(x0 + 0.5 + (j + 0.5) * cw, yy + ch / 2, ''.join(gen) if goster else "", fontsize=9, fontweight='bold',
                    ha='center', va='center', color='#0f172a')


def _direnc_ciz(ax, et):
    su = _norm(et.get("ortam", "hava")) == "su"
    isim = liste_cek(et.get("isimler")) or ["K", "L"]
    alan = liste_cek(et.get("alanlar")) or ["genis", "dar"]
    n = max(1, min(len(alan), 3))
    isim = (isim + ["K", "L", "M"])[:n]
    sozlu = {"genis": 1.5, "buyuk": 1.5, "orta": 1.0, "dar": 0.6, "kucuk": 0.6}
    ham = []
    for a in alan[:n]:
        v = olcu_cek(a)
        ham.append(v if v is not None else sozlu.get(_norm(a), 1.0))
    mx = max(ham)
    w = [max(0.45, 1.5 * h / mx) if all(olcu_cek(a) is not None for a in alan[:n]) else h for h, a in zip(ham, alan[:n])]
    parasut = _norm(et.get("sekil", "levha")) == "parasut"
    if su:
        ax.add_patch(Rectangle((0.2, 0.3), 5.6, 4.3, fc='#e0f2fe', ec='#38bdf8', linewidth=1.5, zorder=0))
        for y in (1.0, 2.0, 3.0, 4.0):
            xs = np.linspace(0.3, 5.7, 60)
            ax.plot(xs, y + 0.05 * np.sin(xs * 6), color='#7dd3fc', linewidth=1, zorder=0)
    merkez = {1: [3.0], 2: [1.8, 4.2], 3: [1.1, 3.0, 4.9]}[n]
    kg = _norm(et.get("kuvvet_goster", "hayir")) in ("evet", "true", "1")
    for cx, wi, ad in zip(merkez, w, isim):
        yc = 3.0
        if parasut:
            ax.add_patch(Wedge((cx, yc + 0.2), wi / 2 + 0.2, 0, 180, fc='#fbbf24', ec='#0f172a', linewidth=1.8, zorder=3))
            ax.plot([cx - wi / 2 - 0.2, cx], [yc + 0.2, yc - 0.45], color='#0f172a', linewidth=1, zorder=3)
            ax.plot([cx + wi / 2 + 0.2, cx], [yc + 0.2, yc - 0.45], color='#0f172a', linewidth=1, zorder=3)
            ax.add_patch(Rectangle((cx - 0.17, yc - 0.75), 0.34, 0.3, fc='#cbd5e1', ec='#0f172a', linewidth=1.5, zorder=4))
            ymid = yc - 0.3
        else:
            ax.add_patch(Rectangle((cx - wi / 2, yc), wi, 0.16, fc='#cbd5e1', ec='#0f172a', linewidth=1.8, zorder=3))
            ymid = yc + 0.08
        if kg:
            ax.annotate("", xy=(cx, ymid - 1.0), xytext=(cx, ymid), arrowprops=dict(arrowstyle='->', color='#0f172a', lw=2.2), zorder=6)
            ax.text(cx + 0.1, ymid - 0.75, "G", fontsize=9, fontweight='bold', va='center')
            rl = 0.35 + 0.65 * (wi / 1.5)
            ax.annotate("", xy=(cx, ymid + rl + (0.35 if parasut else 0.0)), xytext=(cx, ymid),
                        arrowprops=dict(arrowstyle='->', color='#dc2626', lw=2.2), zorder=6)
            ax.text(cx + 0.1, ymid + rl * 0.5 + (0.2 if parasut else 0.0), "R", fontsize=9, fontweight='bold', color='#dc2626', va='center')
        ax.text(cx, 1.05, ad, fontsize=11, fontweight='bold', ha='center', color='#0f172a', zorder=6)
    ax.text(5.7, 4.5, "Su" if su else "Hava", fontsize=8, fontweight='bold', ha='right', color='#0369a1' if su else '#64748b')


def _kaldirac_ciz(ax, et):
    tur = _norm(et.get("tur", "birinci"))
    ky, yy = olcu_cek(et.get("kuvvet_kolu")), olcu_cek(et.get("yuk_kolu"))
    ky_var, yy_var = ky is not None, yy is not None
    ky, yy = ky or 3.0, yy or 1.0
    if tur.startswith("ucuncu") and not (ky_var and yy_var):
        ky, yy = 2.0, 4.0
    L, x0, yb = 4.4, 0.8, 2.3
    if tur.startswith("ikinci"):
        yy = min(yy, ky * 0.9)
        xf, xl, xk = x0, x0 + L * yy / ky, x0 + L
        kuvvet_yon = "yukari"
    elif tur.startswith("ucuncu"):
        ky = min(ky, yy * 0.9)
        xf, xk, xl = x0, x0 + L * ky / yy, x0 + L
        kuvvet_yon = "yukari"
    else:
        xf, xl, xk = x0 + L * yy / (yy + ky), x0, x0 + L
        kuvvet_yon = "asagi"
    ax.add_patch(Rectangle((x0 - 0.1, yb), L + 0.2, 0.14, fc='#d6a65c', ec='#0f172a', linewidth=2, zorder=3))
    ax.add_patch(Polygon([[xf, yb], [xf - 0.3, yb - 0.6], [xf + 0.3, yb - 0.6]], fc='#94a3b8', ec='#0f172a', linewidth=2, zorder=2))
    ax.plot([xf - 0.7, xf + 0.7], [yb - 0.6, yb - 0.6], color='#0f172a', linewidth=2.5)
    ax.text(xf, yb - 0.85, "Destek", fontsize=7.5, fontweight='bold', ha='center', color='#475569')
    # yük: kirişten sarkan blok
    ax.plot([xl, xl], [yb, yb - 0.55], color='#475569', linewidth=2)
    ax.add_patch(Rectangle((xl - 0.28, yb - 1.15), 0.56, 0.6, fc='#cbd5e1', ec='#0f172a', linewidth=2, zorder=3))
    ax.text(xl, yb - 0.85, _t(et.get("yuk", "Yük")), fontsize=7.5, fontweight='bold', ha='center', va='center', zorder=4)
    kt = _t(et.get("kuvvet", "F"))
    if kuvvet_yon == "asagi":
        ax.annotate("", xy=(xk, yb + 0.14), xytext=(xk, yb + 1.0), arrowprops=dict(arrowstyle='<-', color='#dc2626', lw=2.4), zorder=6)
        ax.text(xk + 0.12, yb + 0.6, kt, fontsize=9, fontweight='bold', color='#dc2626', va='center')
    else:
        ax.annotate("", xy=(xk, yb + 0.16), xytext=(xk, yb - 0.85), arrowprops=dict(arrowstyle='<-', color='#dc2626', lw=2.4), zorder=6)
        ax.text(xk + 0.12, yb - 0.5, kt, fontsize=9, fontweight='bold', color='#dc2626', va='center')

    def kol(xa, xb, y, metin, renk):
        ax.annotate("", xy=(xb, y), xytext=(xa, y), arrowprops=dict(arrowstyle='<->', color=renk, lw=1.4))
        ax.text((xa + xb) / 2, y + 0.12, metin, fontsize=7.5, fontweight='bold', ha='center', color=renk)
    yk_m = _t(et.get("yuk_kolu")) if yy_var else "Yük kolu"
    kk_m = _t(et.get("kuvvet_kolu")) if ky_var else "Kuvvet kolu"
    kol(min(xf, xl), max(xf, xl), 3.5, yk_m, '#475569')
    kol(min(xf, xk), max(xf, xk), 4.0, kk_m, '#dc2626')


def _egik_duzlem_ciz(ax, et):
    uz, yk, tb = olcu_cek(et.get("uzunluk")), olcu_cek(et.get("yukseklik")), olcu_cek(et.get("taban"))
    if uz and yk and uz > yk:
        tb = (uz ** 2 - yk ** 2) ** 0.5
    elif yk and tb and not uz:
        uz = (yk ** 2 + tb ** 2) ** 0.5
    elif uz and tb and tb < uz:
        yk = (uz ** 2 - tb ** 2) ** 0.5
    if not (yk and tb):
        yk, tb = 2.0, 4.0
    s = min(4.2 / tb, 2.7 / yk)
    W, H = tb * s, yk * s
    A = np.array([0.8, 1.0])
    C = np.array([0.8 + W, 1.0])
    D = np.array([0.8 + W, 1.0 + H])
    ax.add_patch(Polygon([A, C, D], fc='#f1f5f9', ec='#0f172a', linewidth=2.2, zorder=2))
    ax.plot([C[0] - 0.25, C[0] - 0.25, C[0]], [C[1], C[1] + 0.25, C[1] + 0.25], color='#0f172a', linewidth=1.4)
    u = (D - A) / np.linalg.norm(D - A)
    nrm = np.array([-u[1], u[0]])
    p = A + u * np.linalg.norm(D - A) * 0.55
    bw, bh = 0.7, 0.45
    blok = [p - u * bw / 2, p + u * bw / 2, p + u * bw / 2 + nrm * bh, p - u * bw / 2 + nrm * bh]
    ax.add_patch(Polygon(blok, fc='#cbd5e1', ec='#0f172a', linewidth=2, zorder=4))
    bc = p + nrm * bh / 2
    ax.annotate("", xy=bc + u * 1.2, xytext=bc, arrowprops=dict(arrowstyle='->', color='#dc2626', lw=2.4), zorder=6)
    ft = bc + u * 1.3 + nrm * 0.15
    ax.text(ft[0], ft[1], _t(et.get("kuvvet", "F")), fontsize=10, fontweight='bold', color='#dc2626', zorder=6)
    ax.annotate("", xy=bc + np.array([0, -0.95]), xytext=bc, arrowprops=dict(arrowstyle='->', color='#0f172a', lw=2.2), zorder=6)
    ax.text(bc[0] + 0.1, bc[1] - 0.75, _t(et.get("yuk", "G")), fontsize=9, fontweight='bold', zorder=6)
    m = (A + D) / 2
    uzt = _t(et.get("uzunluk", ""))
    if uzt:
        m2 = A + u * np.linalg.norm(D - A) * 0.2
        q = m2 + np.array([-u[1], u[0]]) * 0.32
        ax.text(q[0], q[1], uzt, fontsize=9, fontweight='bold', color='#2563eb', ha='center', va='center', rotation=np.degrees(np.arctan2(u[1], u[0])))
    ykt = _t(et.get("yukseklik", ""))
    if ykt:
        ax.text(D[0] + 0.15, (C[1] + D[1]) / 2, ykt, fontsize=9, fontweight='bold', color='#16a34a', va='center')
    tbt = _t(et.get("taban", ""))
    if tbt:
        ax.text((A[0] + C[0]) / 2, A[1] - 0.25, tbt, fontsize=9, fontweight='bold', color='#475569', ha='center')


def _makara_ciz(ax, et):
    tur = _norm(et.get("tur", "sabit"))
    yuk, kt = _t(et.get("yuk", "Yük")), _t(et.get("kuvvet", "F"))
    ax.plot([1.6, 4.4], [4.6, 4.6], color='#0f172a', linewidth=3)
    for x in np.arange(1.7, 4.4, 0.2):
        ax.plot([x, x + 0.12], [4.6, 4.75], color='#94a3b8', linewidth=1)
    r = 0.45
    if tur.startswith("hareketli"):
        pc = (3.0, 2.9)
        ax.plot([2.55, 2.55], [4.6, pc[1]], color='#0f172a', linewidth=1.8)
        th = np.linspace(np.pi, 2 * np.pi, 40)
        ax.plot(pc[0] + r * np.cos(th), pc[1] + r * np.sin(th), color='#0f172a', linewidth=1.8)
        ax.plot([3.45, 3.45], [pc[1], 4.1], color='#0f172a', linewidth=1.8)
        ax.add_patch(plt.Circle(pc, r, fc='#e2e8f0', ec='#0f172a', linewidth=2, alpha=0.9, zorder=3))
        ax.plot(*pc, 'ko', ms=4, zorder=4)
        ax.plot([pc[0], pc[0]], [pc[1], 1.9], color='#475569', linewidth=2)
        ax.add_patch(Rectangle((2.65, 1.2), 0.7, 0.7, fc='#cbd5e1', ec='#0f172a', linewidth=2, zorder=3))
        ax.text(3.0, 1.55, yuk, fontsize=8, fontweight='bold', ha='center', va='center', zorder=4)
        ax.annotate("", xy=(3.45, 4.5), xytext=(3.45, 3.85), arrowprops=dict(arrowstyle='->', color='#dc2626', lw=2.4), zorder=6)
        ax.text(3.6, 4.15, kt, fontsize=10, fontweight='bold', color='#dc2626', va='center')
    else:
        pc = (3.0, 3.7)
        ax.plot([3.0, 3.0], [4.6, pc[1] + r], color='#0f172a', linewidth=2)
        ax.add_patch(plt.Circle(pc, r, fc='#e2e8f0', ec='#0f172a', linewidth=2, alpha=0.9, zorder=3))
        ax.plot(*pc, 'ko', ms=4, zorder=4)
        ax.plot([2.55, 2.55], [pc[1], 1.9], color='#0f172a', linewidth=1.8)
        ax.add_patch(Rectangle((2.2, 1.2), 0.7, 0.7, fc='#cbd5e1', ec='#0f172a', linewidth=2, zorder=3))
        ax.text(2.55, 1.55, yuk, fontsize=8, fontweight='bold', ha='center', va='center', zorder=4)
        ax.plot([3.45, 3.45], [pc[1], 2.5], color='#0f172a', linewidth=1.8)
        ax.annotate("", xy=(3.45, 1.7), xytext=(3.45, 2.5), arrowprops=dict(arrowstyle='->', color='#dc2626', lw=2.4), zorder=6)
        ax.text(3.6, 2.1, kt, fontsize=10, fontweight='bold', color='#dc2626', va='center')


def _disli_ciz(ax, et):
    sayilar = [max(6, min(int(sayi_cek(x, 20)), 60)) for x in liste_cek(et.get("dislerin_sayisi"))][:3] or [20, 40]
    isimler = (liste_cek(et.get("isimler")) + ["K", "L", "M"])[:len(sayilar)]
    yonler = liste_cek(et.get("yonler"))
    dis_goster = _norm(et.get("dis_goster", "evet")) not in ("hayir", "false", "0")
    s = min(0.06, 5.2 / (2 * sum(sayilar)))
    yaricap = [n * s for n in sayilar]
    cx = 0.45 + yaricap[0]
    cy = 2.5
    phi_onceki, n_onceki = None, None
    for i, (n, r, ad) in enumerate(zip(sayilar, yaricap, isimler)):
        adim = 2 * np.pi / n
        if i == 0:
            phi = 0.0
        else:
            frac = ((0 - phi_onceki) / n_onceki) % 1
            tooth = frac < 0.25 or frac > 0.75
            phi = np.pi + adim / 2 if tooth else np.pi
        pts = []
        for k in range(n):
            a0 = phi + k * adim
            for da, rr in ((-0.32, 0.88), (-0.2, 1.1), (0.2, 1.1), (0.32, 0.88)):
                a = a0 + da * adim
                pts.append((cx + r * rr * np.cos(a), cy + r * rr * np.sin(a)))
        renk = ['#93c5fd', '#fdba74', '#86efac'][i % 3]
        ax.add_patch(Polygon(pts, fc=renk, ec='#0f172a', linewidth=1.6, zorder=3))
        ax.add_patch(plt.Circle((cx, cy), r * 0.13, fc='#ffffff', ec='#0f172a', linewidth=1.2, zorder=4))
        fs_ad = 9 if r < 0.7 else 11
        ax.text(cx, cy + r * 0.62, _t(ad), fontsize=fs_ad, fontweight='bold', ha='center', va='center', zorder=5)
        if dis_goster:
            ax.text(cx, cy - r * 0.62, f"{n} diş", fontsize=7 if r < 0.7 else 8, fontweight='bold', ha='center', va='center', zorder=5)
        yon = _norm(yonler[i]) if i < len(yonler) else ("saat" if i == 0 else "")
        if yon in ("saat", "ters"):
            ra = min(0.3, r * 0.3)
            t = np.radians(np.linspace(50, 300, 30)) if yon == "ters" else np.radians(np.linspace(300, 50, 30))
            px, py = cx + ra * np.cos(t), cy + ra * np.sin(t)
            ax.plot(px[:-1], py[:-1], color='#dc2626', linewidth=1.8, zorder=6)
            ax.annotate("", xy=(px[-1], py[-1]), xytext=(px[-3], py[-3]), arrowprops=dict(arrowstyle='->', color='#dc2626', lw=1.8), zorder=6)
        phi_onceki, n_onceki = phi, n
        if i + 1 < len(sayilar):
            cx += r + yaricap[i + 1]


# --- ANA ÇİZİCİ ---


KINDS = {"surtunme": _surtunme_ciz, "basinc_kati": _basinc_kati, "basinc_sivi": _basinc_sivi, "mevsim": _mevsim_ciz, "dna": _dna_ciz,
         "caprazlama": _caprazlama_ciz, "direnc": _direnc_ciz, "kaldirac": _kaldirac_ciz, "egik_duzlem": _egik_duzlem_ciz,
         "makara": _makara_ciz, "disli": _disli_ciz}
_HINT_KEYS = ("surtunme_goster", "kuvvet_goster", "hucreleri_goster", "tarih_goster", "mevsim_goster", "etiket_goster", "deger_goster", "deger_yaz", "gorunum_goster")


def kind_of(d):
    k = _norm(d.get("sub_type", ""))
    return k if k in KINDS else ""


def draw(ax, d):
    """Cevaba ipucu veren seçenekler, soru açıkça istemedikçe KAPALI çizilir."""
    et = dict(d)
    for k in _HINT_KEYS:
        et.setdefault(k, "hayir")
    KINDS[kind_of(d)](ax, et)
    ax.set_xlim(-0.1, 6.1)
    ax.set_ylim(0, 5.0)
'''
MODULES['core/visuals'] = r'''# -*- coding: utf-8 -*-
"""Soruya uyumlu görsel motoru. Saf matplotlib; Streamlit ve PDF aynı PNG'yi kullanır.
Kural: Görseller cevabı/ipucunu ASLA yazmaz (yalnızca veri gösterir)."""
import io
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon, Rectangle, Wedge, Ellipse, FancyArrowPatch

plt.rcParams["font.sans-serif"] = ["DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

INK, BLUE, ORANGE, GREEN, SLATE, GOLD = "#1e293b", "#0284c7", "#ea580c", "#10b981", "#94a3b8", "#f59e0b"
PALETTE = ["#0284c7", "#ea580c", "#10b981", "#8b5cf6", "#f59e0b", "#ec4899", "#14b8a6", "#64748b"]


def _f(v, d=0.0):
    try:
        return float(str(v).replace(",", ".").strip())
    except Exception:
        return d


def _title(ax, d, default=""):
    t = str(d.get("title", default) or "")
    if t:
        ax.set_title(t, fontsize=11, fontweight="bold", color=INK, pad=14)


def _clean_axes(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(INK)
    ax.tick_params(colors=INK, labelsize=9)


# ------------------------------------------------------------------ geometri
def _triangle(ax, d):
    sub = str(d.get("sub_type", "scalene")).lower()
    A, B, C = (str(d.get(k, k)) for k in "ABC")
    if sub == "right":
        pts = np.array([[0, 0], [4, 0], [0, 3]])
        ax.plot([0, .35, .35, 0], [0, 0, .35, .35], color=INK, lw=1.2)
    elif sub == "equilateral":
        pts = np.array([[0, 0], [4, 0], [2, np.sqrt(3) / 2 * 4]])
    else:
        pts = np.array([[0, 0], [5, 0], [2, 4.2]])
    ax.add_patch(Polygon(pts, closed=True, fc="#f8fafc", ec=INK, lw=2))
    offs, labs = [[-.5, -.5], [.4, -.5], [0, .35]], [B, C, A]
    for i, p in enumerate(pts):
        ax.text(p[0] + offs[i][0], p[1] + offs[i][1], labs[i], fontsize=10, fontweight="bold", color=INK)
    if d.get("side_ab"):
        ax.text(-.8, 1.5, f"AB: {d['side_ab']}", fontsize=8.5, color=BLUE, fontweight="bold", ha="right")
    if d.get("side_bc"):
        ax.text(2.5, -.7, f"BC: {d['side_bc']}", fontsize=8.5, color=BLUE, fontweight="bold", ha="center")
    if d.get("side_ac"):
        ax.text(2.8, 2.3, f"AC: {d['side_ac']}", fontsize=8.5, color=BLUE, fontweight="bold")
    if d.get("angle_a"):
        ax.text(2.0, 3.8, f"Â={d['angle_a']}", fontsize=8.5, color=ORANGE, fontweight="bold", ha="center")
    ax.set_xlim(-3.5, 7.5)
    ax.set_ylim(-2.5, 5.8)


def _circle(ax, d):
    ax.add_patch(Circle((0, 0), 2.2, fc="#f8fafc", ec=INK, lw=2))
    ax.plot(0, 0, "o", color=ORANGE, ms=5)
    ax.text(.18, -.38, str(d.get("center", "O")), fontsize=10, fontweight="bold", color=ORANGE)
    r = str(d.get("radius", "r"))
    if d.get("show_diameter"):
        ax.plot([-2.2, 2.2], [0, 0], ls="--", color=SLATE, lw=1.4)
        ax.text(0, .25, f"Çap: {r}", fontsize=8.5, fontweight="bold", color=BLUE, ha="center")
    else:
        ax.plot([0, 2.2], [0, 0], color=BLUE, lw=1.8)
        ax.text(1.1, .2, f"r = {r}", fontsize=8.5, fontweight="bold", color=BLUE)
    if d.get("chord"):
        ax.plot([-1.8, 1.8], [-1.3, -1.3], color=GREEN, lw=1.8)
        ax.text(0, -1.75, f"Kiriş: {d['chord']}", fontsize=8.5, fontweight="bold", color=GREEN, ha="center")
    ax.set_xlim(-3.2, 3.2)
    ax.set_ylim(-3.2, 3.2)


def _rectangle(ax, d):
    w, h = _f(d.get("width", 6), 6), _f(d.get("height", 4), 4)
    k = 5.0 / max(w, h)
    W, H = w * k, h * k
    ax.add_patch(Rectangle((0, 0), W, H, fc="#e0f2fe", ec=INK, lw=2))
    ax.text(W / 2, -.5, str(d.get("width_label", f"{w:g} cm")), ha="center", fontsize=9.5, fontweight="bold", color=BLUE)
    ax.text(-.25, H / 2, str(d.get("height_label", f"{h:g} cm")), ha="right", va="center", fontsize=9.5, fontweight="bold", color=BLUE)
    ax.set_xlim(-2.2, W + 1)
    ax.set_ylim(-1.3, H + 1)


# ------------------------------------------------------------------ grafikler
def _bar(ax, d):
    ax.axis("on")
    ax.set_aspect("auto")
    vals = [_f(v) for v in d.get("values", [10, 25, 15, 30])]
    labels = d.get("labels") or [f"Öğe {i + 1}" for i in range(len(vals))]
    labels = [str(x) for x in labels][:len(vals)]
    bars = ax.bar(labels, vals[:len(labels)], color=BLUE, width=.5, ec=INK, lw=1, alpha=.92)
    _title(ax, d, "Veri ve Grafik Analizi")
    _clean_axes(ax)
    ax.tick_params(axis="x", rotation=15)
    mx = max(vals) if vals else 10
    for b in bars:
        ax.text(b.get_x() + b.get_width() / 2, b.get_height() + mx * .03, f"{b.get_height():g}", ha="center",
                fontsize=9, fontweight="bold", color=INK)
    ax.set_ylim(0, mx * 1.3 if mx else 1)
    if d.get("ylabel"):
        ax.set_ylabel(str(d["ylabel"]), fontsize=9, color=INK)


def _line(ax, d):
    ax.axis("on")
    ax.set_aspect("auto")
    vals = [_f(v) for v in d.get("values", [12, 18, 15, 22, 30])]
    labels = [str(x) for x in (d.get("labels") or [f"Ay {i + 1}" for i in range(len(vals))])][:len(vals)]
    xs = range(len(labels))
    ax.plot(xs, vals[:len(labels)], marker="o", color=ORANGE, lw=2.5, ms=7, mfc=BLUE, mec="white")
    ax.set_xticks(list(xs))
    ax.set_xticklabels(labels, fontsize=9, fontweight="bold", color=INK, rotation=15)
    _title(ax, d, "Değişim Grafiği")
    _clean_axes(ax)
    ax.grid(axis="y", alpha=.25)
    mx = max(vals) if vals else 10
    for x, y in zip(xs, vals):
        ax.text(x, y + mx * .04, f"{y:g}", ha="center", fontsize=9, fontweight="bold", color=INK)
    ax.set_ylim(0, mx * 1.35 if mx else 1)
    ax.set_xlim(-.5, len(labels) - .5)
    if d.get("ylabel"):
        ax.set_ylabel(str(d["ylabel"]), fontsize=9, color=INK)


def _pie(ax, d):
    vals = [max(0.0, _f(v)) for v in d.get("values", [40, 30, 20, 10])]
    labels = [str(x) for x in (d.get("labels") or [f"Dilim {i + 1}" for i in range(len(vals))])][:len(vals)]
    tot = sum(vals) or 1
    ax.pie(vals[:len(labels)], labels=labels, colors=PALETTE[:len(labels)], startangle=90, counterclock=False,
           wedgeprops=dict(ec="white", lw=2), textprops=dict(fontsize=9, fontweight="bold", color=INK),
           autopct=(lambda p: f"{p:.0f}%") if d.get("show_percent", True) else None, pctdistance=.7)
    ax.set_aspect("equal")
    _title(ax, d, "Daire Grafiği")


# ------------------------------------------------------------------ fen
def _moon(ax, cx, cy, r, phase, dark="#1f2937", lit="#f8fafc"):
    """phase 0..7: 0 yeni ay, 2 ilk dördün, 4 dolunay, 6 son dördün."""
    ax.add_patch(Circle((cx, cy), r, fc=dark, ec="#475569", lw=1.2))
    a = np.deg2rad((phase % 8) * 45.0)
    if phase % 8 == 0:
        return
    th = np.linspace(np.pi / 2, -np.pi / 2, 70)
    outer = np.c_[r * np.cos(th), r * np.sin(th)]
    th2 = np.linspace(-np.pi / 2, np.pi / 2, 70)
    term = np.c_[r * np.cos(a) * np.cos(th2), r * np.sin(th2)]
    pts = np.vstack([outer, term])
    if (phase % 8) > 4:  # azalan: sol taraf aydınlık
        pts[:, 0] *= -1
    pts[:, 0] += cx
    pts[:, 1] += cy
    ax.add_patch(Polygon(pts, closed=True, fc=lit, ec="none"))
    ax.add_patch(Circle((cx, cy), r, fc="none", ec="#475569", lw=1.2))


def _space(ax, d):
    sub = str(d.get("sub_type", "orbit")).lower()
    _title_txt = d.get("title", "")
    if sub in ("moon_single", "single_moon", "moon_phase"):
        ph = int(_f(d.get("phase", 0))) % 8
        _moon(ax, 0, 0, 1.55, ph)
        lab = str(d.get("label") or "").strip()
        if lab:
            ax.text(0, -2.15, lab, ha="center", fontsize=12, fontweight="bold", color=INK)
        ax.set_xlim(-2.4, 2.4)
        ax.set_ylim(-2.6, 2.0)
        ax.set_facecolor("#e2e8f0")
        return
    if sub in ("moon_phases", "moon_sequence", "phases"):
        phases = d.get("phases") or list(range(8))
        phases = [int(_f(p)) % 8 for p in phases][:8]
        labels = d.get("labels") or [chr(65 + i) for i in range(len(phases))]
        show_names = bool(d.get("show_names", False))
        names = ["Yeni Ay", "Hilal (büyüyen)", "İlk Dördün", "Şişkin Ay (büyüyen)", "Dolunay", "Şişkin Ay (küçülen)", "Son Dördün", "Hilal (küçülen)"]
        n = len(phases)
        cols = min(n, 4)
        rows = int(np.ceil(n / cols))
        for i, p in enumerate(phases):
            cx, cy = (i % cols) * 2.4, -(i // cols) * 2.9
            _moon(ax, cx, cy, .9, p)
            ax.text(cx, cy - 1.35, names[p] if show_names else str(labels[i]), ha="center", fontsize=9.5,
                    fontweight="bold", color=INK)
        ax.set_xlim(-1.4, (cols - 1) * 2.4 + 1.4)
        ax.set_ylim(-(rows - 1) * 2.9 - 1.9, 1.3)
        ax.set_facecolor("#e2e8f0")
        return
    if sub in ("moon_orbit", "moon_positions"):
        ax.add_patch(Circle((-4.6, 0), .75, fc=GOLD, ec="#d97706", lw=1.5))
        for a in np.linspace(0, 2 * np.pi, 12, endpoint=False):
            ax.plot([-4.6 + .85 * np.cos(a), -4.6 + 1.1 * np.cos(a)], [.85 * np.sin(a), 1.1 * np.sin(a)], color=GOLD, lw=1.5)
        ax.text(-4.6, -1.5, "Güneş", ha="center", fontsize=8.5, fontweight="bold", color="#d97706")
        for y in (-1.0, 0, 1.0):
            ax.annotate("", xy=(-1.9, y), xytext=(-3.1, y), arrowprops=dict(arrowstyle="->", color=GOLD, lw=1.4))
        ax.add_patch(Circle((0, 0), .55, fc=BLUE, ec="#0369a1", lw=1.5))
        ax.text(0, 0, "Dünya", ha="center", va="center", fontsize=7.5, fontweight="bold", color="white")
        ax.add_patch(Circle((0, 0), 2.0, fill=False, ec=SLATE, ls="--", lw=1))
        labels = d.get("labels") or [str(i + 1) for i in range(8)]
        for k in range(8):
            ang = np.deg2rad(90 + 45 * k)  # 0: üst
            mx, my = 2.0 * np.cos(ang), 2.0 * np.sin(ang)
            ax.add_patch(Circle((mx, my), .27, fc="#1f2937", ec="#475569", lw=1))
            ax.add_patch(Wedge((mx, my), .27, 90, 270, fc="#f8fafc", ec="none"))  # güneşe bakan yarı
            ox, oy = 2.55 * np.cos(ang), 2.55 * np.sin(ang)
            ax.text(ox, oy, str(labels[k]), ha="center", va="center", fontsize=10, fontweight="bold", color=ORANGE)
        ax.set_xlim(-5.8, 3.4)
        ax.set_ylim(-3.2, 3.2)
        return
    if sub == "solar_eclipse":
        ax.add_patch(Polygon([[-.45, .25], [-.45, -.25], [1.35, -.2], [1.35, .2]], fc="#cbd5e1", alpha=.55, ec="none"))
        ax.add_patch(Circle((-2.6, 0), .8, fc=GOLD, ec="#d97706", lw=1.5))
        ax.add_patch(Circle((-.7, 0), .25, fc="#cbd5e1", ec="#64748b"))
        ax.add_patch(Circle((1.5, 0), .55, fc=BLUE, ec="#0369a1", lw=1.5))
        for x, t, c in ((-2.6, "Güneş", "#d97706"), (-.7, "Ay", "#64748b"), (1.5, "Dünya", BLUE)):
            ax.text(x, -1.0 if x < -2 else -.7, t, ha="center", fontsize=8.5, fontweight="bold", color=c)
        ax.set_xlim(-3.9, 3.0)
        ax.set_ylim(-2, 2)
        return
    if sub == "lunar_eclipse":
        ax.add_patch(Polygon([[-.5, .55], [-.5, -.55], [1.2, -.3], [1.2, .3]], fc="#94a3b8", alpha=.45, ec="none"))
        ax.add_patch(Circle((-2.6, 0), .8, fc=GOLD, ec="#d97706", lw=1.5))
        ax.add_patch(Circle((-.5, 0), .55, fc=BLUE, ec="#0369a1", lw=1.5))
        ax.add_patch(Circle((1.5, 0), .25, fc="#cbd5e1", ec="#64748b"))
        for x, t, c in ((-2.6, "Güneş", "#d97706"), (-.5, "Dünya", BLUE), (1.5, "Ay", "#64748b")):
            ax.text(x, -1.0 if x < -2 else -.8, t, ha="center", fontsize=8.5, fontweight="bold", color=c)
        ax.set_xlim(-3.9, 3.0)
        ax.set_ylim(-2, 2)
        return
    # yörünge
    ax.add_patch(Circle((-2.0, 0), .8, fc=GOLD, ec="#d97706", lw=1.5))
    ax.text(-2.0, -1.2, "Güneş", fontsize=8.5, fontweight="bold", color="#d97706", ha="center")
    ax.add_patch(Circle((0, 0), 2.1, fill=False, ec=SLATE, ls="--", lw=1.2))
    ax.add_patch(Circle((2.1, 0), .4, fc=BLUE, ec="#0369a1", lw=1.2))
    ax.text(2.1, -.75, "Dünya", fontsize=8.5, fontweight="bold", color=BLUE, ha="center")
    ax.set_xlim(-3.8, 3.5)
    ax.set_ylim(-2.5, 2.5)


def _dynamometer(ax, d):
    mx = max(1.0, _f(d.get("max_value", 10), 10))
    val = min(mx, max(0.0, _f(d.get("value", 4), 4)))
    unit = str(d.get("unit", "N"))
    step = _f(d.get("step", 1 if mx <= 12 else mx / 10), 1)
    top, bot = 7.0, 0.8
    y = lambda v: top - (top - bot) * v / mx
    ax.plot([0, 0], [8.6, 8.0], color=INK, lw=2)
    ax.add_patch(Circle((0, 8.9), .3, fill=False, ec=INK, lw=2))
    ax.add_patch(Rectangle((-.55, .2), 1.1, 7.8, fc="#f1f5f9", ec=INK, lw=2))
    for i in range(int(round(mx / step)) + 1):
        v = i * step
        long = (i % 5 == 0) or step * 5 > mx
        ax.plot([.55, .55 + (.35 if long else .2)], [y(v), y(v)], color=INK, lw=1.2)
        if long or mx <= 12:
            ax.text(.98, y(v), f"{v:g}", va="center", fontsize=8, color=INK)
    ax.text(1.0, 8.0, unit, fontsize=9, fontweight="bold", color=BLUE)
    ax.add_patch(Polygon([[-.55, y(val)], [-1.0, y(val) + .17], [-1.0, y(val) - .17]], fc="#dc2626", ec="none"))
    ax.plot([-.55, .55], [y(val), y(val)], color="#dc2626", lw=1.6)
    ax.plot([0, 0], [.2, -.5], color=INK, lw=2)
    ax.add_patch(Rectangle((-.6, -1.9), 1.2, 1.4, fc="#cbd5e1", ec=INK, lw=1.8))
    if d.get("mass_label"):
        ax.text(0, -1.2, str(d["mass_label"]), ha="center", va="center", fontsize=9, fontweight="bold", color=INK)
    ax.set_xlim(-2.2, 2.6)
    ax.set_ylim(-2.4, 9.4)


def _thermometer(ax, d):
    lo, hi = _f(d.get("min", -10), -10), _f(d.get("max", 50), 50)
    val = min(hi, max(lo, _f(d.get("value", 20), 20)))
    step = _f(d.get("step", 10), 10)
    unit = str(d.get("unit", "°C"))
    y0, y1 = 1.0, 8.0
    y = lambda v: y0 + (y1 - y0) * (v - lo) / (hi - lo)
    ax.add_patch(Rectangle((-.22, y0 - .2), .44, y1 - y0 + .6, fc="white", ec=INK, lw=2, zorder=1))
    ax.add_patch(Circle((0, y0 - .55), .5, fc="#dc2626", ec=INK, lw=2, zorder=2))
    ax.add_patch(Rectangle((-.12, y0 - .3), .24, y(val) - y0 + .3, fc="#dc2626", ec="none", zorder=3))
    v = lo
    while v <= hi + 1e-9:
        ax.plot([.22, .45], [y(v), y(v)], color=INK, lw=1.2)
        ax.text(.6, y(v), f"{v:g}", va="center", fontsize=8.5, color=INK)
        v += step
    ax.text(.3, y1 + .6, unit, fontsize=9, fontweight="bold", color=BLUE)
    ax.set_xlim(-1.6, 1.8)
    ax.set_ylim(-.8, y1 + 1.2)


def _numberline(ax, d):
    lo, hi = _f(d.get("min", 0)), _f(d.get("max", 10), 10)
    step = _f(d.get("step", 1), 1)
    ax.axis("on")
    ax.set_aspect("auto")
    ax.spines[["left", "right", "top"]].set_visible(False)
    ax.set_yticks([])
    ax.spines["bottom"].set_position(("data", 0))
    ax.spines["bottom"].set_color(INK)
    ax.spines["bottom"].set_linewidth(2)
    ticks = np.arange(lo, hi + step / 2, step)
    ax.set_xticks(ticks)
    ax.set_xticklabels([f"{t:g}" for t in ticks], fontsize=8.5, color=INK)
    ax.set_xlim(lo - step * .6, hi + step * .6)
    ax.set_ylim(-1, 1.6)
    for m in d.get("marks", []):
        if isinstance(m, dict):
            v, lab = _f(m.get("value")), str(m.get("label", ""))
            ax.plot(v, 0, "o", color=ORANGE, ms=9, zorder=5)
            ax.text(v, .35, lab, ha="center", fontsize=11, fontweight="bold", color=ORANGE)
    _title(ax, d)


def _forces(ax, d):
    left = [_f(x) for x in d.get("left", [])]
    right = [_f(x) for x in d.get("right", [])]
    unit = str(d.get("unit", "N"))
    ax.add_patch(Rectangle((-1, -.8), 2, 1.6, fc="#cbd5e1", ec=INK, lw=2))
    if d.get("object_label"):
        ax.text(0, 0, str(d["object_label"]), ha="center", va="center", fontsize=10, fontweight="bold", color=INK)
    def arrows(vals, sign, col):
        mx = max(left + right + [1.0])
        for i, v in enumerate(vals):
            ln = 1.0 + 2.6 * v / mx
            x0, y = sign * 1.0, .45 - i * .8 if len(vals) > 1 else 0.0
            ax.add_patch(FancyArrowPatch((x0, y), (x0 + sign * ln, y), arrowstyle="-|>", mutation_scale=18, color=col, lw=2.6))
            ax.text(x0 + sign * ln / 2, y + .25, f"{v:g} {unit}", ha="center", fontsize=9.5, fontweight="bold", color=col)
    arrows(left, -1, ORANGE)
    arrows(right, 1, BLUE)
    ax.set_xlim(-4.4, 4.4)
    ax.set_ylim(-1.8, 1.8)
    _title(ax, d)


def _cylinder(ax, d):
    mx = _f(d.get("max", 100), 100)
    lv = min(mx, max(0.0, _f(d.get("level", 50), 50)))
    step = _f(d.get("step", mx / 10), mx / 10)
    unit = str(d.get("unit", "mL"))
    y = lambda v: .6 + 7.2 * v / mx
    ax.add_patch(Rectangle((-.6, y(0)), 1.2, y(lv) - y(0), fc="#7dd3fc", ec="none", alpha=.85))
    ax.plot([-.6, -.6, .6, .6], [8.2, y(0), y(0), 8.2], color=INK, lw=2.2)
    ax.plot([-.85, -.6], [8.2, 8.2], color=INK, lw=2)
    ax.plot([.6, .85], [8.2, 8.2], color=INK, lw=2)
    ax.plot([-.9, .9], [.6, .6], color=INK, lw=3)
    v = 0.0
    while v <= mx + 1e-9:
        ax.plot([.6, .85], [y(v), y(v)], color=INK, lw=1.1)
        ax.text(1.0, y(v), f"{v:g}", va="center", fontsize=8, color=INK)
        v += step
    ax.text(.9, 8.7, unit, fontsize=9, fontweight="bold", color=BLUE)
    ax.set_xlim(-1.8, 2.2)
    ax.set_ylim(0, 9.4)


# ------------------------------------------------------------------ kesin ölçülü geometri (geo)
def _dot(ax, p, lab="", off=(0, -.38), color=INK, fs=11):
    ax.plot(*p, "o", color=color, ms=5, zorder=5)
    if lab:
        ax.text(p[0] + off[0], p[1] + off[1], lab, fontsize=fs, fontweight="bold", color=color, ha="center", va="center", zorder=6)


def _arrow(ax, a, b, both=False, color=INK, lw=2):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="<|-|>" if both else "-|>", mutation_scale=16, color=color, lw=lw, shrinkA=0, shrinkB=0, zorder=3))


def _rot(v, deg):
    t = np.radians(deg)
    return np.array([v[0] * np.cos(t) - v[1] * np.sin(t), v[0] * np.sin(t) + v[1] * np.cos(t)])


def _right_mark(ax, o, u, v, s=.32):
    u, v = np.array(u, float), np.array(v, float)
    u, v = u / np.linalg.norm(u), v / np.linalg.norm(v)
    ax.plot([o[0] + s * u[0], o[0] + s * (u[0] + v[0]), o[0] + s * v[0]], [o[1] + s * u[1], o[1] + s * (u[1] + v[1]), o[1] + s * v[1]], color=INK, lw=1.4, zorder=4)


def _arc_mark(ax, o, a0, a1, r=.7, color=ORANGE, label=None):
    th = np.radians(np.linspace(a0, a1, 40))
    ax.plot(o[0] + r * np.cos(th), o[1] + r * np.sin(th), color=color, lw=2, zorder=4)
    if label:
        m = np.radians((a0 + a1) / 2)
        ax.text(o[0] + (r + .42) * np.cos(m), o[1] + (r + .42) * np.sin(m), label, fontsize=10, fontweight="bold", color=color, ha="center", va="center", zorder=6)


def _regular(n, R=2.0, rot=90):
    return np.array([[R * np.cos(np.radians(rot + 360 * i / n)), R * np.sin(np.radians(rot + 360 * i / n))] for i in range(n)])


def _poly(ax, pts, labels=None, fc="#e0f2fe", ticks=False, diagonals=False, label_off=.38):
    pts = np.array(pts, float)
    n = len(pts)
    c = pts.mean(axis=0)
    ax.add_patch(Polygon(pts, closed=True, fc=fc, ec=INK, lw=2.2, joinstyle="round", zorder=2))
    if diagonals:
        for i in range(n):
            for j in range(i + 2, n):
                if not (i == 0 and j == n - 1):
                    ax.plot(*zip(pts[i], pts[j]), color=SLATE, lw=1.2, ls="--", zorder=2)
    if ticks:
        for i in range(n):
            a, b = pts[i], pts[(i + 1) % n]
            m, v = (a + b) / 2, b - a
            nrm = np.array([-v[1], v[0]]) / np.linalg.norm(v)
            for k in (-1, 1) if False else (0,):
                ax.plot(*zip(m - .12 * nrm, m + .12 * nrm), color=ORANGE, lw=2, zorder=4)
    for i, p in enumerate(pts):
        ax.plot(*p, "o", color=INK, ms=4, zorder=5)
        if labels:
            d = (p - c) / (np.linalg.norm(p - c) or 1)
            q = p + d * label_off
            ax.text(q[0], q[1], labels[i], fontsize=11, fontweight="bold", color=INK, ha="center", va="center", zorder=6)


_POLY_N = {"üçgen": 3, "dörtgen": 4, "beşgen": 5, "altıgen": 6, "yedigen": 7, "sekizgen": 8}


def _geo(ax, d):
    sub = str(d.get("sub_type", "polygon")).lower()
    L = [str(x) for x in (d.get("labels") or [])]
    ax.set_aspect("equal")
    if sub in ("line", "ray", "segment"):
        a, b = np.array([-3., 0]), np.array([3., 0])
        la, lb = (L + ["A", "B"])[:2]
        if sub == "line":
            _arrow(ax, a - [.5, 0], b + [.5, 0], both=True)
            _dot(ax, a + [1, 0], la); _dot(ax, b - [1, 0], lb)
        elif sub == "ray":
            _arrow(ax, a, b + [.6, 0]); _dot(ax, a, la); _dot(ax, b - [1.5, 0], lb)
        else:
            ax.plot(*zip(a, b), color=INK, lw=2.4, zorder=3); _dot(ax, a, la); _dot(ax, b, lb)
        ax.set_xlim(-4.3, 4.3); ax.set_ylim(-1.5, 1.5)
    elif sub == "lines_set":  # I, II, III: doğru / ışın / doğru parçası karışık (kimin ne olduğunu sorusu sorar)
        kinds = [str(k).lower() for k in (d.get("kinds") or ["segment", "ray", "line"])][:4]
        for i, k in enumerate(kinds):
            y = -i * 1.5
            a, b = np.array([-3., y]), np.array([3., y])
            if k == "line":
                _arrow(ax, a - [.5, 0], b + [.5, 0], both=True)
            elif k == "ray":
                _arrow(ax, a, b + [.6, 0]); ax.plot(*a, "o", color=INK, ms=5, zorder=5)
            else:
                ax.plot(*zip(a, b), color=INK, lw=2.4, zorder=3); ax.plot(*a, "o", color=INK, ms=5); ax.plot(*b, "o", color=INK, ms=5)
            ax.text(-4.3, y, ["I", "II", "III", "IV"][i], fontsize=12, fontweight="bold", color=BLUE, va="center", ha="center")
        ax.set_xlim(-5, 4.6); ax.set_ylim(-1.5 * len(kinds) + .5, 1)
    elif sub == "perpendicular":  # kesin 90°
        tilt = _f(d.get("tilt", 20), 20)
        o = np.array([0., 0])
        u, v = _rot([1, 0], tilt), _rot([1, 0], tilt + 90)
        _arrow(ax, o - 3 * u, o + 3 * u, both=True); _arrow(ax, o - 2.6 * v, o + 2.6 * v, both=True)
        _right_mark(ax, o, u, v)
        names = (L + ["d₁", "d₂", "A"])[:3]
        ax.text(*(o + 3.35 * u), names[0], fontsize=11, fontweight="bold", color=BLUE, ha="center", va="center")
        ax.text(*(o + 2.95 * v), names[1], fontsize=11, fontweight="bold", color=GREEN, ha="center", va="center")
        _dot(ax, o, names[2], off=(.5, -.5)); ax.set_xlim(-4, 4); ax.set_ylim(-3.4, 3.4)
    elif sub == "parallel":  # paralel iki doğru (+ isteğe bağlı kesen)
        tilt = _f(d.get("tilt", 0), 0)
        u = _rot([1, 0], tilt); n = _rot([0, 1], tilt)
        for k, nm in ((0, "d₁"), (1, "d₂")):
            o = n * (-.9 + 1.8 * k)
            _arrow(ax, o - 3.4 * u, o + 3.4 * u, both=True)
            ax.text(*(o + 3.9 * u), (L + ["d₁", "d₂"])[k], fontsize=11, fontweight="bold", color=BLUE, ha="center", va="center")
        if d.get("transversal"):
            w = _rot([1, 0], _f(d.get("angle", 60), 60) + tilt)
            _arrow(ax, -2.6 * w + n * -.9 - n * .0, 2.6 * w + n * 0.9 + n * 0, both=True, color=GREEN) if False else None
            # kesen: iki doğruyu kesecek şekilde
            c = n * 0
            _arrow(ax, c - 2.4 * w, c + 2.4 * w, both=True, color=GREEN)
            ax.text(*(c + 2.8 * w), (L + ["d₁", "d₂", "k"])[2], fontsize=11, fontweight="bold", color=GREEN, ha="center", va="center")
        ax.set_xlim(-4.6, 4.6); ax.set_ylim(-3.6, 3.6)
    elif sub == "angle":  # kesin ölçülü açı
        deg = _f(d.get("degree", 50), 50)
        base = _f(d.get("rotation", 0), 0)
        o = np.array([0., 0])
        p = o + 3.2 * _rot([1, 0], base); q = o + 3.2 * _rot([1, 0], base + deg)
        _arrow(ax, o, p); _arrow(ax, o, q)
        _arc_mark(ax, o, base, base + deg, r=.9, label=str(d.get("angle_label", "")) or None)
        ln = (L + ["A", "B", "C"])[:3]  # köşe=ln[0]
        _dot(ax, o, ln[0], off=_rot([1, 0], base + deg / 2) * -.45)
        ax.text(*(p + .4 * _rot([1, 0], base)), ln[1], fontsize=11, fontweight="bold", ha="center", va="center", color=INK)
        ax.text(*(q + .4 * _rot([1, 0], base + deg)), ln[2], fontsize=11, fontweight="bold", ha="center", va="center", color=INK)
        ax.set_xlim(-2.5, 4.2); ax.set_ylim(-2, 4.2)
    elif sub == "angles_two_lines":  # kesişen iki doğru: ölçüsü verilen bir açı, diğeri sorulur
        deg = _f(d.get("degree", 60), 60)
        o = np.array([0., 0]); u, v = _rot([1, 0], 0), _rot([1, 0], deg)
        _arrow(ax, o - 3 * u, o + 3 * u, both=True); _arrow(ax, o - 3 * v, o + 3 * v, both=True)
        _arc_mark(ax, o, 0, deg, r=.9, label=str(d.get("given", f"{deg:g}°")))
        _arc_mark(ax, o, deg, 180, r=1.3, color=BLUE, label=str(d.get("ask", "x")))
        _dot(ax, o, "O", off=(.1, -.42)); ax.set_xlim(-3.8, 3.8); ax.set_ylim(-3.2, 3.2)
    elif sub == "polygon_set":  # K, L, M, N: farklı çokgenler (adı yazmaz)
        ks = [str(k).lower() for k in (d.get("kinds") or ["üçgen", "dörtgen", "beşgen", "altıgen"])][:4]
        names = (L + ["K", "L", "M", "N"])[:len(ks)]
        for i, k in enumerate(ks):
            n = _POLY_N.get(k, 5)
            pts = _regular(n, 1.0, 90 if n % 2 else 90 + 180 / n) * (1.0 if n != 4 else .9) + [i * 2.8, 0]
            if n == 4:
                pts = np.array([[0, 0], [1.7, 0], [1.7, 1.7], [0, 1.7]]) - [.85, .85] + [i * 2.8, 0]
            _poly(ax, pts, fc=PALETTE[i % 3] + "22")
            ax.text(i * 2.8, -1.7, names[i], fontsize=12, fontweight="bold", color=BLUE, ha="center")
        ax.set_xlim(-1.6, 2.8 * len(ks) - 1.2); ax.set_ylim(-2.3, 1.7)
    else:  # polygon: düzgün/düzgün olmayan çokgen, köşe harfli
        n = int(_f(d.get("sides", _POLY_N.get(str(d.get("kind", "")).lower(), 5)), 5))
        n = max(3, min(n, 8))
        pts = _regular(n, 2.0, 90 if n % 2 else 90 + 180 / n)
        if d.get("irregular"):
            rng = np.random.RandomState(int(_f(d.get("seed", 7), 7)))
            pts = np.array([p * (.75 + .5 * rng.rand()) for p in pts])
        labs = (L + list("ABCDEFGH"))[:n]
        _poly(ax, pts, labels=labs, ticks=bool(d.get("equal_ticks")) and not d.get("irregular"), diagonals=bool(d.get("diagonals")))
        ax.set_xlim(-3.2, 3.2); ax.set_ylim(-3.2, 3.2)


# ---- üçgen / dörtgen / çember: kesin koordinatlı çizimler
def _tri_pts(kind, scale=1.0):
    k = str(kind).lower()
    if k in ("right", "dik"):
        P = [[0, 0], [4, 0], [0, 3]]            # 3-4-5, dik açı B'de değil A'da (ilk köşe)
    elif k in ("equilateral", "eşkenar"):
        P = [[0, 0], [4, 0], [2, 4 * np.sqrt(3) / 2]]
    elif k in ("isosceles", "ikizkenar"):
        P = [[0, 0], [4, 0], [2, 3.6]]          # |AC| = |BC|
    elif k in ("obtuse", "geniş"):
        P = [[0, 0], [5, 0], [-1.2, 2.2]]
    elif k in ("acute", "dar"):
        P = [[0, 0], [4.6, 0], [2.7, 3.4]]
    else:                                        # çeşitkenar
        P = [[0, 0], [5, 0], [1.4, 3.3]]
    return np.array(P, float) * scale


def _tick(ax, a, b, n=1, color=ORANGE):
    a, b = np.array(a, float), np.array(b, float)
    m, v = (a + b) / 2, b - a
    u = v / np.linalg.norm(v); nrm = np.array([-u[1], u[0]])
    for i in range(n):
        c = m + (i - (n - 1) / 2) * .16 * u
        ax.plot(*zip(c - .13 * nrm, c + .13 * nrm), color=color, lw=2, zorder=4)


def _tri_apex_pts(ai):
    """İkizkenar üçgen: eşit kenarların ortak köşesi (tepe) ai. 0=A (üstte), 1=B (üstte), 2=C (üstte)."""
    T = np.array([[0, 0], [4, 0], [2, 3.6]], float)
    return {0: np.array([T[2], T[0], T[1]]), 1: np.array([T[0], T[2], T[1]]), 2: T}[ai]


def _vertex_arc(ax, P, i, text, color=ORANGE, r=.75, lab=None):
    """P[i] köşesinde iç açıyı yayla gösterir ve ölçüyü (3x+5°, ? ...) yayın yanına yazar."""
    o = P[i]
    nP = len(P)
    a, b = P[(i + 1) % nP] - o, P[(i - 1) % nP] - o
    t1 = np.degrees(np.arctan2(a[1], a[0])); t2 = np.degrees(np.arctan2(b[1], b[0]))
    d = (t2 - t1) % 360
    if d > 180:
        t1, d = t2, 360 - d
    th = np.radians(np.linspace(t1, t1 + d, 40))
    ax.plot(o[0] + r * np.cos(th), o[1] + r * np.sin(th), color=color, lw=2, zorder=4)
    m = np.radians(t1 + d / 2)
    rl = r + (lab if lab else (.7 if d >= 45 else 1.0))
    ax.text(o[0] + rl * np.cos(m), o[1] + rl * np.sin(m), str(text), fontsize=9.5, fontweight="bold", color=color, ha="center", va="center", zorder=6,
            bbox=dict(boxstyle="round,pad=0.14", fc="white", ec="none", alpha=.9))


def _num(v):
    import re
    m = re.search(r"\d+(?:[.,]\d+)?", str(v))
    return float(m.group(0).replace(",", ".")) if m else None


def _right_tri_pts(ri, sides):
    """Dik açı ri köşesinde; dik kenarlar yatay/düşey. Verilen uzunluklar varsa oranlar ona göre."""
    a, b = (ri + 1) % 3, (ri + 2) % 3
    sk = lambda i, j: "".join(sorted("ABC"[i] + "ABC"[j]))
    l1, l2, h = _num(sides.get(sk(ri, a))), _num(sides.get(sk(ri, b))), _num(sides.get(sk(a, b)))
    if l1 is None and l2 and h and h > l2:
        l1 = (h * h - l2 * l2) ** .5
    if l2 is None and l1 and h and h > l1:
        l2 = (h * h - l1 * l1) ** .5
    if not (l1 and l2):
        l1, l2 = 4.0, 3.0
    k = 4.6 / max(l1, l2)
    w, hh = max(l1 * k, 2.0), max(l2 * k, 2.0)
    P = np.zeros((3, 2))
    P[ri], P[a], P[b] = [0, 0], [w, 0], [0, hh]
    return P


def _triangle_geo(ax, d, pts=None):
    kind = str(d.get("kind", "scalene")).lower()
    apex = str(d.get("apex", "")).upper()
    ai = 2  # ikizkenarda varsayılan tepe C
    ri = "ABC".index(str(d.get("right_at", "A")).upper()[:1]) if str(d.get("right_at", "A")).upper()[:1] in ("A", "B", "C") else 0
    if pts is None and kind in ("right", "dik"):
        P = _right_tri_pts(ri, {"".join(sorted(str(k).upper())): v for k, v in (d.get("sides") or {}).items()})
    elif pts is None and kind in ("isosceles", "ikizkenar") and apex in ("A", "B", "C"):
        ai = "ABC".index(apex)
        P = _tri_apex_pts(ai)
    else:
        P = _tri_pts(kind) if pts is None else pts
    L = (list(map(str, d.get("labels") or [])) + ["A", "B", "C"])[:3]
    c = P.mean(axis=0)
    ax.add_patch(Polygon(P, closed=True, fc="#e0f2fe", ec=INK, lw=2.2, joinstyle="round", zorder=2))
    for i, p in enumerate(P):
        ax.plot(*p, "o", color=INK, ms=4, zorder=5)
        dd = (p - c) / np.linalg.norm(p - c)
        ax.text(*(p + dd * .45), L[i], fontsize=11, fontweight="bold", ha="center", va="center", color=INK, zorder=6)
    side = lambda i, j: (P[i], P[j])
    if d.get("ticks", True):
        if kind in ("equilateral", "eşkenar"):
            for i, j in ((0, 1), (1, 2), (2, 0)):
                _tick(ax, *side(i, j), n=1)
        elif kind in ("isosceles", "ikizkenar"):
            for j in range(3):
                if j != ai:
                    _tick(ax, *side(ai, j))  # eşit kenarlar tepe köşesinden çıkan iki kenar
    right_at = None
    if kind in ("right", "dik"):
        _right_mark(ax, P[ri], P[(ri + 1) % 3] - P[ri], P[(ri + 2) % 3] - P[ri], s=.35)
        right_at = ri
    if d.get("height"):  # C'den AB'ye yükseklik
        foot = np.array([P[2][0], 0.0])
        ax.plot(*zip(P[2], foot), color=GREEN, lw=1.6, ls="--", zorder=3)
        _right_mark(ax, foot, [-1, 0] if P[2][0] > 0 else [1, 0], [0, 1], s=.28)
    skey = lambda k: "".join(sorted(str(k).upper()))
    sides = {skey(k): v for k, v in (d.get("sides") or {}).items()}
    for key, (i, j) in (("AB", (0, 1)), ("BC", (1, 2)), ("AC", (0, 2))):
        if key in sides:
            m = (P[i] + P[j]) / 2; e_ = P[j] - P[i]; out = np.array([-e_[1], e_[0]]) / np.linalg.norm(e_)
            if np.dot(out, m - c) < 0:
                out = -out  # kenara dik, üçgenin dışına bakan birim vektör
            ha = "right" if out[0] < -.3 else "left" if out[0] > .3 else "center"
            va = "top" if out[1] < -.3 else "bottom" if out[1] > .3 else "center"
            ax.text(*(m + out * .14), str(sides[key]), fontsize=9.5, fontweight="bold", color=BLUE, ha=ha, va=va, zorder=6)
    angs = {str(k).upper(): v for k, v in (d.get("angles") or {}).items()}
    for key, i in (("A", 0), ("B", 1), ("C", 2)):
        if key in angs and not (right_at == i and str(angs[key]).strip().startswith("90")):
            _vertex_arc(ax, P, i, angs[key], color="#7c3aed" if str(angs[key]).strip() in ("?", "x") else ORANGE)
    lo, hi = P.min(axis=0) - 1.5, P.max(axis=0) + 1.5
    ax.set_xlim(lo[0], hi[0]); ax.set_ylim(lo[1], hi[1])


def _quad_pts(kind):
    k = str(kind).lower()
    if k in ("square", "kare"):
        return np.array([[0, 0], [3, 0], [3, 3], [0, 3]], float)
    if k in ("rectangle", "dikdörtgen"):
        return np.array([[0, 0], [4.4, 0], [4.4, 2.6], [0, 2.6]], float)
    if k in ("parallelogram", "paralelkenar"):
        return np.array([[0, 0], [4, 0], [5.2, 2.4], [1.2, 2.4]], float)
    if k in ("rhombus", "eşkenar dörtgen", "eskenar dortgen"):
        return np.array([[0, 1.6], [2.2, 0], [4.4, 1.6], [2.2, 3.2]], float)
    if k in ("trapezoid", "yamuk"):
        return np.array([[0, 0], [5, 0], [3.8, 2.4], [1.0, 2.4]], float)
    if k in ("isosceles_trapezoid", "ikizkenar yamuk", "ikizkenar_yamuk"):
        return np.array([[0, 0], [5, 0], [4, 2.4], [1, 2.4]], float)  # bacaklar eşit
    if k in ("general", "genel", "quad"):
        return np.array([[0, 0], [5, 0.3], [4.1, 2.7], [0.7, 2.2]], float)  # özel olmayan dörtgen
    return np.array([[0, 1.5], [1.6, 0], [4.6, 1.5], [1.6, 3.2]], float)  # deltoid


def _quad_geo(ax, d, pts=None, labels=None):
    kind = str(d.get("kind", "rectangle")).lower()
    isos = kind in ("isosceles_trapezoid", "ikizkenar yamuk", "ikizkenar_yamuk")
    P = _quad_pts("isosceles_trapezoid" if isos else kind) if pts is None else pts
    L = labels or (list(map(str, d.get("labels") or [])) + list("ABCD"))[:4]
    c = P.mean(axis=0)
    ax.add_patch(Polygon(P, closed=True, fc="#e0f2fe", ec=INK, lw=2.2, joinstyle="round", zorder=2))
    for i, p in enumerate(P):
        ax.plot(*p, "o", color=INK, ms=4, zorder=5)
        dd = (p - c) / np.linalg.norm(p - c)
        ax.text(*(p + dd * .45), L[i], fontsize=11, fontweight="bold", ha="center", va="center", color=INK, zorder=6)
    E = {"AB": (0, 1), "BC": (1, 2), "CD": (2, 3), "AD": (3, 0)}
    groups = d.get("equal_groups")
    if d.get("ticks", True):
        e = lambda i: (P[i], P[(i + 1) % 4])
        if groups:  # metinde eşit denen kenarlar: her eşit grup ayrı sayıda çentikle işaretlenir
            for gi, g in enumerate(groups):
                for k in g:
                    key = "".join(sorted(str(k).upper()))
                    if key in E:
                        _tick(ax, P[E[key][0]], P[E[key][1]], n=gi + 1)
        elif kind in ("square", "kare", "rhombus", "eşkenar dörtgen", "eskenar dortgen"):
            for i in range(4):
                _tick(ax, *e(i))
        elif kind in ("rectangle", "dikdörtgen", "parallelogram", "paralelkenar"):
            _tick(ax, *e(0)); _tick(ax, *e(2)); _tick(ax, *e(1), n=2); _tick(ax, *e(3), n=2)
        elif isos:  # ikizkenar yamuk: eşit olan BACAKLAR
            _tick(ax, *e(1)); _tick(ax, *e(3))
        elif kind not in ("trapezoid", "yamuk", "general", "genel", "quad"):  # deltoid
            _tick(ax, *e(0)); _tick(ax, *e(3)); _tick(ax, *e(1), n=2); _tick(ax, *e(2), n=2)
    right_kinds = ("square", "kare", "rectangle", "dikdörtgen")
    if kind in right_kinds:
        for i in range(4):
            _right_mark(ax, P[i], P[(i + 1) % 4] - P[i], P[(i - 1) % 4] - P[i], s=.26)
    if d.get("diagonals"):
        ax.plot(*zip(P[0], P[2]), color=SLATE, lw=1.3, ls="--", zorder=2); ax.plot(*zip(P[1], P[3]), color=SLATE, lw=1.3, ls="--", zorder=2)
    qs_ = {"".join(sorted(str(k).upper())): v for k, v in (d.get("sides") or {}).items()}
    for key, (i, j) in E.items():  # metinde verilen uzunluklar şekilde de görünsün
        if key in qs_:
            m = (P[i] + P[j]) / 2; out = m - c; out = out / np.linalg.norm(out)
            ax.text(*(m + out * (.55 + .4 * abs(out[0]))), str(qs_[key]), fontsize=9.5, fontweight="bold", color=BLUE, ha="center", va="center", zorder=6)
    angs = {str(k).upper(): v for k, v in (d.get("angles") or {}).items()}
    for key, i in (("A", 0), ("B", 1), ("C", 2), ("D", 3)):  # verilen/sorulan açılar köşelerinde yayla
        if key in angs and not (kind in right_kinds and str(angs[key]).strip().startswith("90")):
            _vertex_arc(ax, P, i, angs[key], color="#7c3aed" if str(angs[key]).strip() in ("?", "x") else ORANGE, r=.55, lab=.5)
    lo, hi = P.min(axis=0) - np.array([1.9, 1.5]), P.max(axis=0) + np.array([1.9, 1.5])
    ax.set_xlim(lo[0], hi[0]); ax.set_ylim(lo[1], hi[1])


def _circle_parts(ax, d):
    parts = [str(x).lower() for x in (d.get("parts") or ["radius"])]
    R = 2.4
    ax.add_patch(Circle((0, 0), R, fc="#f0f9ff", ec=INK, lw=2.2, zorder=2))
    _dot(ax, (0, 0), str(d.get("center", "O")), off=(.1, -.38), color=ORANGE)
    pt = lambda deg: np.array([R * np.cos(np.radians(deg)), R * np.sin(np.radians(deg))])
    def lab(p, t, k=1.18):
        ax.plot(*p, "o", color=INK, ms=5, zorder=5); ax.text(*(p * k), t, fontsize=11, fontweight="bold", ha="center", va="center", zorder=6)
    L = (list(map(str, d.get("labels") or [])) + ["A", "B", "C", "D", "E"])
    if "radius" in parts:
        p = pt(35); ax.plot(*zip([0, 0], p), color=BLUE, lw=2.2, zorder=3); lab(p, L[0])
    if "diameter" in parts:
        p, q = pt(160), pt(340); ax.plot(*zip(p, q), color=GREEN, lw=2.2, zorder=3); lab(p, L[1]); lab(q, L[2])
    if "chord" in parts:
        p, q = pt(250), pt(300) if False else pt(295); ax.plot(*zip(p, q), color=ORANGE, lw=2.2, zorder=3); lab(p, L[3]); lab(q, L[4])
    if "arc" in parts:
        th = np.radians(np.linspace(40, 110, 40)); ax.plot(R * np.cos(th), R * np.sin(th), color="#8b5cf6", lw=5, zorder=4, solid_capstyle="round")
    if "tangent" in parts:
        p = pt(0); ax.plot([p[0], p[0]], [-2.2, 2.2], color="#ec4899", lw=2.2, zorder=3); ax.plot(*p, "o", color=INK, ms=5, zorder=5)
    if "sector" in parts:
        ax.add_patch(Wedge((0, 0), R, 20, 100, fc="#fde68a", ec=INK, lw=1.8, zorder=3))
    ax.set_xlim(-3.6, 3.6); ax.set_ylim(-3.3, 3.3)


def _shape_set(ax, d, kind_fn, default):
    ks = [str(k).lower() for k in (d.get("kinds") or default)][:4]
    names = (list(map(str, d.get("labels") or [])) + ["K", "L", "M", "N"])[:len(ks)]
    off = 0.0
    for i, k in enumerate(ks):
        P = kind_fn(k)
        P = P / max(np.ptp(P[:, 0]), np.ptp(P[:, 1])) * 2.0
        P = P - [P[:, 0].min(), P[:, 1].min()] + [off, 0]
        ax.add_patch(Polygon(P, closed=True, fc=PALETTE[i % 3] + "22", ec=INK, lw=2.2, joinstyle="round", zorder=2))
        for p in P: ax.plot(*p, "o", color=INK, ms=3.5, zorder=5)
        ax.text(P[:, 0].mean(), -.55, names[i], fontsize=12, fontweight="bold", color=BLUE, ha="center")
        off += np.ptp(P[:, 0]) + 1.0
    ax.set_xlim(-.6, off); ax.set_ylim(-1.1, 2.6)


_geo_basic = _geo


def _geo(ax, d):
    sub = str(d.get("sub_type", "polygon")).lower()
    ax.set_aspect("equal")
    if sub in ("triangle", "triangle_kind"):
        return _triangle_geo(ax, d)
    if sub in ("triangle_set",):
        return _shape_set(ax, d, _tri_pts, ["right", "equilateral", "isosceles", "scalene"])
    if sub in ("quad", "quadrilateral"):
        return _quad_geo(ax, d)
    if sub in ("quad_set",):
        return _shape_set(ax, d, _quad_pts, ["square", "rectangle", "parallelogram", "rhombus"])
    if sub in ("circle_parts", "circle"):
        return _circle_parts(ax, d)
    return _geo_basic(ax, d)


def _fen(ax, d):
    from . import fenfig
    fenfig.draw(ax, d)


_DISPATCH = {
    "fen": _fen, "triangle": _triangle, "circle": _circle, "rectangle": _rectangle,
    "bar_chart": _bar, "science_chart": _bar, "line_chart": _line, "pie_chart": _pie,
    "science_space": _space, "space_orbit": _space, "eclipse": _space, "moon_phases": _space,
    "dynamometer": _dynamometer, "thermometer": _thermometer, "number_line": _numberline,
    "forces": _forces, "cylinder": _cylinder, "geo": _geo,
}
_CHARTS = {"bar_chart", "science_chart", "line_chart", "number_line"}


def shape_type(shape):
    if not isinstance(shape, dict):
        return ""
    return str(shape.get("type", "")).strip().lower()


def normalize_shape(shape):
    """AI'dan gelen şemayı güvenli hâle getirir; çizilemeyecekse None. Cevabı sızdıran alanları kapatır."""
    if not isinstance(shape, dict):
        return None
    t = shape_type(shape)
    if not t:
        return None
    sh = dict(shape)
    sh["type"] = t
    if t == "table":
        hs, rows = sh.get("headers"), sh.get("rows")
        if not isinstance(hs, (list, tuple)) or not isinstance(rows, (list, tuple)) or not hs:
            return None
        sh["headers"] = [str(x) for x in hs]
        sh["rows"] = [[str(c) for c in r] if isinstance(r, (list, tuple)) else [str(r)] for r in rows if r is not None]
        sh["title"] = str(sh.get("title") or "")
        return sh if sh["rows"] else None
    if t not in _DISPATCH:
        return None
    if t == "fen":
        from . import fenfig
        k = fenfig.kind_of(sh)
        if not k:
            return None
        sh["sub_type"] = k
    sh["show_names"] = False  # evre/konum adlarını yazmak cevabı verir
    return sh


def is_table(shape):
    return shape_type(shape) == "table"


def render_shape(shape, dpi=170):
    """-> PNG bytes ya da None (tablo ya da çizilemeyen şema)."""
    t = shape_type(shape)
    if not t or t == "table" or t not in _DISPATCH:
        return None
    shape = dict(shape)
    if t == "moon_phases" and "sub_type" not in shape:
        shape["sub_type"] = "moon_phases"
    fig, ax = plt.subplots(figsize=(6.2, 3.8))
    try:
        ax.axis("off")
        ax.set_aspect("equal")
        _DISPATCH[t](ax, shape)
        if t in ("science_space", "space_orbit", "eclipse", "moon_phases"):
            _title(ax, shape)
        if t in _CHARTS:
            fig.subplots_adjust(bottom=.3, left=.14, right=.96, top=.85)
        buf = io.BytesIO()
        fig.savefig(buf, format="png", bbox_inches="tight", dpi=dpi, facecolor="white", pad_inches=.12)
        return buf.getvalue()
    except Exception:
        return None
    finally:
        plt.close(fig)


def table_html(shape):
    headers = shape.get("headers", ["Veri", "Değer"]) or []
    rows = shape.get("rows", []) or []
    title = str(shape.get("title", "Veri Tablosu"))
    h = f"<p style='font-weight:700;color:#1e293b;margin-bottom:.4rem'>📊 {title}</p>"
    h += "<div class='custom-table-container'><table class='custom-table'><thead><tr>"
    h += "".join(f"<th>{x}</th>" for x in headers) + "</tr></thead><tbody>"
    for r in rows:
        h += "<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>"
    return h + "</tbody></table></div>"


def draw_geometry_shape(shape_data):
    """Streamlit tarafı (eski fonksiyon adı korunur). Hata verirse sayfayı bozmaz."""
    import streamlit as st
    try:
        sh = normalize_shape(shape_data)
        if not sh:
            return
        if is_table(sh):
            st.markdown(table_html(sh), unsafe_allow_html=True)
            return
        png = render_shape(sh)
        if png:
            st.image(png, width=420)
    except Exception:
        st.caption("📊 (Bu sorunun görseli yüklenemedi)")
'''
MODULES['core/pdf_export'] = r'''# -*- coding: utf-8 -*-
"""Soru bankası tarzı PDF: sayfa ortadan ikiye bölünmüş, iki sütunda yan yana sorular,
sonda cevap anahtarı. DejaVu fontu (matplotlib ile gelir) Türkçe/Almanca karakterleri tam destekler;
fontta olmayan karakterler otomatik temizlenir -> PDF'te bozuk karakter oluşmaz."""
import io
import os
import re
import html
import datetime
import matplotlib
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle,
                                Image, KeepTogether, NextPageTemplate, PageBreak)
from . import visuals

_FD = os.path.join(matplotlib.get_data_path(), "fonts", "ttf")
for _n, _f in (("DV", "DejaVuSans.ttf"), ("DV-B", "DejaVuSans-Bold.ttf"),
               ("DV-I", "DejaVuSans-Oblique.ttf"), ("DV-BI", "DejaVuSans-BoldOblique.ttf")):
    try:
        pdfmetrics.getFont(_n)
    except KeyError:
        pdfmetrics.registerFont(TTFont(_n, os.path.join(_FD, _f)))
pdfmetrics.registerFontFamily("DV", normal="DV", bold="DV-B", italic="DV-I", boldItalic="DV-BI")
_CMAP = pdfmetrics.getFont("DV").face.charToGlyph

NAVY, BLUE, ORANGE = colors.HexColor("#0f172a"), colors.HexColor("#0284c7"), colors.HexColor("#ea580c")
LIGHT, LINE = colors.HexColor("#f1f5f9"), colors.HexColor("#cbd5e1")
SUP = str.maketrans("0123456789+-n", "⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻ⁿ")
LATEX = [(r"\\times", "×"), (r"\\div", "÷"), (r"\\cdot", "·"), (r"\\sqrt", "√"), (r"\\pi", "π"), (r"\\leq?", "≤"),
         (r"\\geq?", "≥"), (r"\\neq", "≠"), (r"\\%", "%"), (r"\\circ", "°"), (r"\\left|\\right", ""), (r"\\\(|\\\)|\\\[|\\\]", "")]


def clean(t):
    """PDF'te sorun çıkarabilecek her şeyi temizler."""
    t = "" if t is None else str(t)
    for pat, rep in LATEX:
        t = re.sub(pat, rep, t)
    t = re.sub(r"\^\{?([0-9+\-n]+)\}?", lambda m: m.group(1).translate(SUP), t)
    t = re.sub(r"\*\*(.+?)\*\*", r"\1", t)
    t = t.replace(" ", " ").replace("\t", " ")
    t = re.sub(r"[​-‏⁠︎️‪-‮]", "", t)
    t = re.sub(r"[\U00010000-\U0010FFFF]", "", t)
    t = "".join(ch if (ch in "\n" or ord(ch) in _CMAP) else ("" if ord(ch) > 0x2E80 or ord(ch) < 32 else "?") for ch in t)
    return t.strip()


def esc(t):
    return html.escape(clean(t), quote=False).replace("\n", "<br/>")


def _styles(fs=8.3):
    d = dict(fontName="DV", fontSize=fs, leading=fs * 1.32, textColor=NAVY)
    return {
        "q": ParagraphStyle("q", **d), "opt": ParagraphStyle("opt", leftIndent=11, firstLineIndent=-11, spaceBefore=1.2, **d),
        "pas": ParagraphStyle("pas", **{**d, "fontSize": fs - .3, "leading": (fs - .3) * 1.35}),
        "num": ParagraphStyle("num", **{**d, "fontName": "DV-B", "fontSize": fs + 2.2, "textColor": BLUE, "leading": fs + 5}),
        "hdr": ParagraphStyle("hdr", **{**d, "fontName": "DV-B", "fontSize": fs + 1, "textColor": colors.white, "leading": fs + 4}),
        "cell": ParagraphStyle("cell", **{**d, "fontSize": 6.9, "leading": 8.4}),
        "cellh": ParagraphStyle("cellh", **{**d, "fontName": "DV-B", "fontSize": 6.9, "leading": 8.4, "textColor": colors.white}),
        "sol": ParagraphStyle("sol", **{**d, "fontSize": 7.4, "leading": 9.6}),
        "title": ParagraphStyle("title", **{**d, "fontName": "DV-B", "fontSize": 14, "leading": 18}),
        "h2": ParagraphStyle("h2", **{**d, "fontName": "DV-B", "fontSize": 10.5, "leading": 14, "textColor": BLUE, "spaceBefore": 8, "spaceAfter": 3}),
    }


def _img(png, max_w, max_h):
    iw, ih = ImageReader(io.BytesIO(png)).getSize()
    k = min(max_w / iw, max_h / ih)
    return Image(io.BytesIO(png), width=iw * k, height=ih * k)


def _shape_flowables(shape, width, S, max_h=3.7 * cm):
    try:
        return _shape_flowables_raw(visuals.normalize_shape(shape), width, S, max_h)
    except Exception:
        return []


def _shape_flowables_raw(shape, width, S, max_h):
    if not isinstance(shape, dict) or not visuals.shape_type(shape):
        return []
    if visuals.is_table(shape):
        hs = [Paragraph(esc(h), S["cellh"]) for h in shape.get("headers", [])]
        rows = [[Paragraph(esc(c), S["cell"]) for c in r] for r in shape.get("rows", [])]
        if not hs or not rows:
            return []
        n = len(hs)
        rows = [r + [Paragraph("", S["cell"])] * (n - len(r)) if len(r) < n else r[:n] for r in rows]
        t = Table([hs] + rows, colWidths=[width / n] * n, repeatRows=1)
        t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), BLUE), ("GRID", (0, 0), (-1, -1), .4, LINE),
                               ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT]), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                               ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                               ("LEFTPADDING", (0, 0), (-1, -1), 3), ("RIGHTPADDING", (0, 0), (-1, -1), 3)]))
        out = []
        if shape.get("title"):
            out.append(Paragraph(f"<b>{esc(shape['title'])}</b>", S["cell"]))
        return out + [t, Spacer(1, 3)]
    png = visuals.render_shape(shape, dpi=200)
    if not png:
        return []
    return [_img(png, width * .94, max_h), Spacer(1, 2)]


def _options(q, width, S):
    opts = q.get("options") or {}
    keys = list(opts.keys())
    if not keys:
        return []
    short = max(len(clean(opts[k])) for k in keys) <= 9 and len(keys) == 4
    if short:
        cells = [Paragraph(f"<b>{k})</b> {esc(opts[k])}", S["q"]) for k in keys]
        t = Table([cells], colWidths=[width / 4] * 4)
        t.setStyle(TableStyle([("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                               ("TOPPADDING", (0, 0), (-1, -1), 1), ("BOTTOMPADDING", (0, 0), (-1, -1), 1)]))
        return [t]
    return [Paragraph(f"<b>{k})</b> {esc(opts[k])}", S["opt"]) for k in keys]


def _q_table(q, num, colw, S, answer_lines=0):
    cw = colw - 0.85 * cm
    body = []
    pas = clean(q.get("passage", ""))
    if pas and pas.lower() != "null":
        pt = Table([[Paragraph(esc(pas), S["pas"])]], colWidths=[cw])
        pt.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), LIGHT), ("LINEBEFORE", (0, 0), (0, -1), 2, BLUE),
                                ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                                ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
        body += [pt, Spacer(1, 3)]
    body += _shape_flowables(q.get("shape"), cw, S)
    body.append(Paragraph(esc(q.get("question", "")), S["q"]))
    body.append(Spacer(1, 2))
    body += _options(q, cw, S)
    if answer_lines:
        body.append(Spacer(1, 4))
        lt = Table([[""]] * answer_lines, colWidths=[cw], rowHeights=[.7 * cm] * answer_lines)
        lt.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, -1), .4, LINE)]))
        body.append(lt)
    t = Table([[Paragraph(f"{num}.", S["num"]), body]], colWidths=[.85 * cm, cw])
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0),
                           ("RIGHTPADDING", (0, 0), (-1, -1), 0), ("TOPPADDING", (0, 0), (-1, -1), 0),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 9)]))
    return t


def _subject_bar(text, colw, S, color):
    t = Table([[Paragraph(esc(text), S["hdr"])]], colWidths=[colw])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), color), ("LEFTPADDING", (0, 0), (-1, -1), 6),
                           ("TOPPADDING", (0, 0), (-1, -1), 2.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5)]))
    return t


# ----------------------------------------------------------------- belge
class _Doc(BaseDocTemplate):
    pass


def build_pdf(questions, meta, include_solutions=True, include_key=True):
    """questions: soru listesi. meta: {title, subtitle, grade_label, scope, difficulty, duration_min, kind('mc'|'open'),
    info:[(etiket,deger)]}. -> PDF bytes"""
    buf = io.BytesIO()
    W, H = A4
    M, GUT = 1.25 * cm, .9 * cm
    colw = (W - 2 * M - GUT) / 2
    kind = meta.get("kind", "mc")
    S = _styles(8.3 if kind == "mc" else 9.2)
    first_top = H - M - 3.5 * cm
    bottom = 1.5 * cm
    title = clean(meta.get("title", "Denemematik"))

    def frames(top, pid):
        h = top - bottom
        return [Frame(M, bottom, colw, h, 0, 0, 0, 0, id=f"{pid}L"),
                Frame(M + colw + GUT, bottom, colw, h, 0, 0, 0, 0, id=f"{pid}R")], h

    def sep(c, top):
        if kind == "open":
            return
        c.setStrokeColor(LINE)
        c.setLineWidth(.7)
        c.line(W / 2, bottom, W / 2, top)

    def footer(c, d):
        c.setFont("DV", 7)
        c.setFillColor(colors.HexColor("#64748b"))
        c.drawString(M, .8 * cm, clean(f"Denemematik • {title}"))
        c.drawRightString(W - M, .8 * cm, f"Sayfa {d.page}")

    def on_first(c, d):
        c.saveState()
        c.setFillColor(NAVY)
        c.roundRect(M, H - M - 2.2 * cm, W - 2 * M, 2.2 * cm, 8, fill=1, stroke=0)
        c.setFillColor(colors.white)
        c.setFont("DV-B", 14)
        c.drawString(M + .5 * cm, H - M - .95 * cm, title)
        c.setFont("DV", 8)
        c.drawString(M + .5 * cm, H - M - 1.55 * cm, clean(meta.get("subtitle", "")))
        c.setFillColor(ORANGE)
        c.roundRect(W - M - 3.6 * cm, H - M - 1.7 * cm, 3.2 * cm, .9 * cm, 5, fill=1, stroke=0)
        c.setFillColor(colors.white)
        c.setFont("DV-B", 8.5)
        c.drawCentredString(W - M - 2.0 * cm, H - M - 1.35 * cm, clean(meta.get("grade_label", "")))
        c.setFillColor(NAVY)
        c.setFont("DV", 8)
        y = H - M - 2.95 * cm
        c.drawString(M, y, "Ad Soyad: ______________________   Sınıf/No: ________   Tarih: ____________")
        c.drawRightString(W - M, y, clean(meta.get("info_line", "")))
        sep(c, first_top)
        footer(c, d)
        c.restoreState()

    def on_later(c, d):
        c.saveState()
        c.setFont("DV-B", 7.5)
        c.setFillColor(BLUE)
        c.drawString(M, H - M + .1 * cm, title)
        c.setStrokeColor(LINE)
        c.line(M, H - M - .1 * cm, W - M, H - M - .1 * cm)
        sep(c, H - M - .4 * cm)
        footer(c, d)
        c.restoreState()

    def on_key(c, d):
        c.saveState()
        footer(c, d)
        c.restoreState()

    doc = _Doc(buf, pagesize=A4, title=title, author="Denemematik", leftMargin=M, rightMargin=M,
               topMargin=M, bottomMargin=bottom)
    f1, h1 = frames(first_top, "a")
    f2, h2 = frames(H - M - .5 * cm, "b")
    single = [Frame(M, bottom, W - 2 * M, H - M - bottom, id="s")]
    if kind == "open":
        f1 = [Frame(M, bottom, W - 2 * M, first_top - bottom, id="a")]
        f2 = [Frame(M, bottom, W - 2 * M, H - M - .5 * cm - bottom, id="b")]
        h1, h2 = first_top - bottom, H - M - .5 * cm - bottom
        colw = W - 2 * M
    doc.addPageTemplates([PageTemplate("first", f1, onPage=on_first), PageTemplate("later", f2, onPage=on_later),
                          PageTemplate("key", single, onPage=on_key)])

    story = [NextPageTemplate("later")]
    last_subj = None
    n_sub = {}
    from .curriculum import SUBJECT_COLORS
    for i, q in enumerate(questions, 1):
        subj = q.get("subject", "")
        lines = 0
        if kind == "open":
            lines = 5 if "çık" in str(q.get("type", "")).lower() else 2
        qt = _q_table(q, i, colw, S, lines)
        mx = (h1 if len(story) < 3 else h2) - 4
        parts = []
        if subj != last_subj:
            col = colors.HexColor(SUBJECT_COLORS.get(subj, "#0284c7"))
            parts += [_subject_bar(subj, colw, S, col), Spacer(1, 5)]
            last_subj = subj
        if kind == "open":
            pts = q.get("points")
            tag = f"({pts} puan • {q.get('difficulty', '')} • {q.get('type', '')})" if pts else ""
            parts.append(Paragraph(f"<font color='#64748b' size='7.5'>{esc(tag)}</font>", S["q"]))
        parts.append(qt)
        story.append(KeepTogether(parts))
    if include_key and questions:
        story += [NextPageTemplate("key"), PageBreak()]
        story += _answer_key(questions, meta, S, include_solutions, W - 2 * M)
    doc.build(story)
    return buf.getvalue()


def _answer_key(questions, meta, S, include_solutions, width):
    out = [Paragraph("CEVAP ANAHTARI", S["title"]), Paragraph(esc(meta.get("title", "")), S["q"]), Spacer(1, 6)]
    kind = meta.get("kind", "mc")
    if kind == "mc":
        by = {}
        for i, q in enumerate(questions, 1):
            by.setdefault(q.get("subject", "Genel"), []).append((i, q.get("answer", "-")))
        for subj, items in by.items():
            out.append(Paragraph(esc(subj), S["h2"]))
            per = 10
            rows = []
            for k in range(0, len(items), per):
                chunk = items[k:k + per]
                row = [Paragraph(f"<b>{n}.</b> {esc(a)}", S["q"]) for n, a in chunk]
                row += [""] * (per - len(row))
                rows.append(row)
            t = Table(rows, colWidths=[width / per] * per)
            t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), .4, LINE), ("BACKGROUND", (0, 0), (-1, -1), LIGHT),
                                   ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
            out.append(t)
        if include_solutions and any(q.get("explanation") for q in questions):
            out.append(Paragraph("ÇÖZÜM AÇIKLAMALARI", S["h2"]))
            for i, q in enumerate(questions, 1):
                ex = clean(q.get("explanation", ""))
                if ex:
                    out.append(Paragraph(f"<b>{i}. ({esc(q.get('answer', ''))})</b> {esc(ex)}", S["sol"]))
                    out.append(Spacer(1, 2.5))
    else:
        for i, q in enumerate(questions, 1):
            out.append(Paragraph(f"<b>Soru {i}</b> — {esc(q.get('kazanim', ''))} • {q.get('points', '')} puan • {esc(q.get('difficulty', ''))}", S["h2"]))
            out.append(Paragraph(f"<b>Beklenen cevap:</b> {esc(q.get('answer', ''))}", S["sol"]))
            rub = q.get("rubric") or []
            if rub:
                rows = [[Paragraph("Puanlama adımı", S["cellh"]), Paragraph("Puan", S["cellh"])]]
                rows += [[Paragraph(esc(r.get("step", "")), S["cell"]), Paragraph(esc(r.get("points", "")), S["cell"])] for r in rub]
                t = Table(rows, colWidths=[width - 2 * cm, 2 * cm])
                t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), BLUE), ("GRID", (0, 0), (-1, -1), .4, LINE)]))
                out += [Spacer(1, 2), t]
    return out


# ----------------------------------------------------------------- sertifika
def certificate_pdf(name, subject, grade_label, pct, topic=""):
    buf = io.BytesIO()
    W, H = landscape(A4)
    c = rl_canvas.Canvas(buf, pagesize=landscape(A4))
    c.setFillColor(colors.HexColor("#fff7ed"))
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setStrokeColor(ORANGE)
    c.setLineWidth(6)
    c.rect(1 * cm, 1 * cm, W - 2 * cm, H - 2 * cm)
    c.setStrokeColor(BLUE)
    c.setLineWidth(1.5)
    c.rect(1.5 * cm, 1.5 * cm, W - 3 * cm, H - 3 * cm)
    c.setFillColor(NAVY)
    c.setFont("DV-B", 34)
    c.drawCentredString(W / 2, H - 5 * cm, "BAŞARI SERTİFİKASI")
    c.setFont("DV", 14)
    c.drawCentredString(W / 2, H - 7 * cm, "Bu belge, aşağıda adı yazılı öğrencinin")
    c.setFillColor(ORANGE)
    c.setFont("DV-B", 28)
    c.drawCentredString(W / 2, H - 9.2 * cm, clean(name) or "Öğrenci")
    c.setFillColor(NAVY)
    c.setFont("DV", 14)
    c.drawCentredString(W / 2, H - 11 * cm, clean(f"{grade_label} • {subject} dersinde"))
    if topic:
        c.drawCentredString(W / 2, H - 12 * cm, clean(f"“{topic}” kazanımında"))
    c.setFont("DV-B", 16)
    c.drawCentredString(W / 2, H - 13.6 * cm, f"%{pct:.0f} başarı göstererek üstün başarı elde ettiğini belgeler.")
    c.setFont("DV", 10)
    c.setFillColor(colors.HexColor("#64748b"))
    c.drawCentredString(W / 2, 2.6 * cm, datetime.date.today().strftime("%d.%m.%Y") + "  •  Denemematik")
    c.save()
    return buf.getvalue()


def report_pdf(name, grade_label, hist, stats, weak, streak_n, level, comment=""):
    """Veli / öğretmen için tek sayfalık gelişim raporu."""
    from reportlab.platypus import SimpleDocTemplate
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, leftMargin=1.6 * cm, rightMargin=1.6 * cm, topMargin=1.4 * cm, bottomMargin=1.4 * cm)
    H1 = ParagraphStyle("h1", fontName="DV-B", fontSize=19, leading=24, textColor=NAVY, spaceAfter=4)
    H2 = ParagraphStyle("h2", fontName="DV-B", fontSize=12, textColor=BLUE, spaceBefore=9, spaceAfter=4)
    P = ParagraphStyle("p", fontName="DV", fontSize=9.2, leading=13, textColor=colors.HexColor("#1e293b"))
    sm = ParagraphStyle("sm", fontName="DV", fontSize=8, textColor=colors.HexColor("#64748b"))
    el = [Paragraph("Denemematik • Öğrenci Gelişim Raporu", H1),
          Paragraph(clean(f"{name or 'Öğrenci'} • {grade_label} • {datetime.date.today().strftime('%d.%m.%Y')}"), sm), Spacer(1, 6)]
    pcts = [h["pct"] for h in hist]
    last5 = pcts[-5:]
    avg = sum(pcts) / len(pcts) if pcts else 0
    trend = (sum(last5[-2:]) / len(last5[-2:]) - sum(last5[:2]) / len(last5[:2])) if len(last5) >= 3 else 0
    kp = [["Çözülen sınav", "Ortalama başarı", "Son 5 sınav trendi", "Çalışma serisi", "Seviye"],
          [str(len(hist)), f"%{avg:.0f}", ("▲ " if trend > 0 else "▼ " if trend < 0 else "■ ") + f"{abs(trend):.0f} puan", f"{streak_n} gün", clean(f"{level['level']} • {level['title']}")]]
    t = Table(kp, colWidths=[3.4 * cm] * 5)
    t.setStyle(TableStyle([("FONT", (0, 0), (-1, 0), "DV", 7.5), ("FONT", (0, 1), (-1, 1), "DV-B", 12), ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#64748b")),
                           ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f5f3ff")), ("BOX", (0, 0), (-1, -1), .8, colors.HexColor("#c4b5fd")),
                           ("ALIGN", (0, 0), (-1, -1), "CENTER"), ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    el += [t, Paragraph("Ders bazında durum", H2)]
    rows = [["Ders", "Ort. başarı", "Soru başı süre", "Değerlendirme"]]
    for s_, v in sorted(stats.items(), key=lambda x: x[1]["pct"]):
        rows.append([clean(s_), f"%{v['pct']:.0f}", f"{v['sec']:.0f} sn" if v.get("sec") else "-",
                     "Güçlü" if v["pct"] >= 75 else "Gelişiyor" if v["pct"] >= 50 else "Destek gerekli"])
    t2 = Table(rows, colWidths=[6 * cm, 3 * cm, 3.4 * cm, 4.2 * cm], repeatRows=1)
    t2.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "DV", 8.8), ("FONT", (0, 0), (-1, 0), "DV-B", 8.8), ("BACKGROUND", (0, 0), (-1, 0), BLUE), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]), ("GRID", (0, 0), (-1, -1), .4, colors.HexColor("#e2e8f0")),
                            ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
    el.append(t2)
    weak = [w for w in weak if w[2] < 70]
    if weak:
        el.append(Paragraph("Öncelikli çalışılacak kazanımlar", H2))
        for s_, tp, p_, _ in weak[:6]:
            el.append(Paragraph(clean(f"• {s_} — {tp} (başarı %{p_:.0f})"), P))
    el.append(Paragraph("Öğretmen değerlendirmesi ve tavsiye", H2))
    el.append(Paragraph(clean(comment or "Düzenli çalışmaya devam edilmesi, zayıf kazanımların günlük tekrarla pekiştirilmesi önerilir."), P))
    el += [Spacer(1, 10), Paragraph("Bu rapor Denemematik tarafından öğrencinin çözdüğü denemelerden otomatik üretilmiştir.", sm)]
    doc.build(el)
    return buf.getvalue()
'''
MODULES['core/store'] = r'''# -*- coding: utf-8 -*-
"""Yerel kayıt: sınav geçmişi, yanlış soru arşivi, son sorular (tekrarsızlık). JSON dosyaları ./data altında.
Streamlit Cloud geçicidir: Performans ekranındaki 'Yedekle / Geri yükle' düğmelerini kullanın."""
import json
import os
import time
import uuid

DATA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
os.makedirs(DATA, exist_ok=True)


def _p(name):
    return os.path.join(DATA, name)


def _load(name, default):
    try:
        with open(_p(name), encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def _save(name, obj):
    tmp = _p(name) + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False)
    os.replace(tmp, _p(name))


# ---- geçmiş
def history():
    return _load("history.json", [])


def _today():
    import datetime as _d
    try:
        from zoneinfo import ZoneInfo
        return _d.datetime.now(ZoneInfo("Europe/Istanbul")).date()
    except Exception:
        return _d.date.today()


def count_generated(n):
    """Takvim gününe göre üretilen/sunulan soru sayısını günlük sayaca ekler."""
    try:
        n = int(n)
        if n <= 0:
            return
        d = _load("gen_stats.json", {})
        if not isinstance(d, dict):
            d = {}
        k = _today().isoformat()
        d[k] = int(d.get(k, 0)) + n
        _save("gen_stats.json", d)
    except Exception:
        pass


def gen_totals():
    """(bugün, bu hafta [Pazartesi-başlangıçlı], bu ay) — takvim gününe göre."""
    import datetime as _d
    d = _load("gen_stats.json", {})
    t = _today()
    wk0 = t - _d.timedelta(days=t.weekday())
    day = wk = mo = 0
    for k, v in (d.items() if isinstance(d, dict) else []):
        try:
            dt = _d.date.fromisoformat(k); v = int(v)
        except Exception:
            continue
        if dt == t:
            day += v
        if wk0 <= dt <= t:
            wk += v
        if dt.year == t.year and dt.month == t.month and dt <= t:
            mo += v
    return day, wk, mo


def add_attempt(rec):
    h = history()
    rec = {**rec, "id": uuid.uuid4().hex[:10], "ts": int(time.time())}
    h.append(rec)
    _save("history.json", h)
    return rec


def replace_history(h):
    _save("history.json", h)


# ---- yanlışlar
def wrong():
    return _load("wrong.json", [])


def add_wrong(items):
    w = wrong()
    have = {x.get("key") for x in w}
    for it in items:
        if it["key"] not in have:
            w.append(it)
            have.add(it["key"])
    _save("wrong.json", w)


def remove_wrong(key):
    _save("wrong.json", [x for x in wrong() if x.get("key") != key])


def replace_wrong(w):
    _save("wrong.json", w)


# ---- tekrarsızlık için son soru gövdeleri
def recent_stems():
    return _load("stems.json", {})


def add_stems(questions):
    d = recent_stems()
    for q in questions:
        import re
        s = re.sub(r"\W+", " ", str(q.get("question", "")).lower())[:70].strip()
        d.setdefault(q.get("subject", "Genel"), []).append(s)
    for k in d:
        d[k] = d[k][-300:]
    _save("stems.json", d)


# ---- hatalı bildirilen sorular: bankadan ve yanlış arşivinden çıkar, bir daha üretilirse elenir
def bad_stems():
    return set(_load("bad.json", []))


def report_bad(q):
    import re as _re
    stem = _re.sub(r"\W+", " ", str(q.get("question", "")).lower())[:70].strip()
    if not stem:
        return False
    bad = _load("bad.json", [])
    if stem not in bad:
        bad.append(stem)
    _save("bad.json", bad[-1000:])
    try:  # bankadaki aynı soru
        with _BANK_LOCK:
            b = _bank()
            for k in list(b):
                b[k]["qs"] = [x for x in b[k]["qs"] if _bstem(x) != stem]
                if not b[k]["qs"]:
                    b.pop(k)
            _save("bank.json", b)
    except Exception:
        pass
    try:  # yanlış arşivinden de çıkar (hatalı soruyu çalıştırmasın)
        _save("wrong.json", [x for x in wrong() if _re.sub(r"\W+", " ", str((x.get("q") or {}).get("question", "")).lower())[:70].strip() != stem])
    except Exception:
        pass
    return True


def update_wrong(key, **fields):
    w = wrong()
    for x in w:
        if x.get("key") == key:
            x.update(fields)
    _save("wrong.json", w)


# ---- ayarlar (öğrenci adı, günlük hedef, günlük tekrar sayacı)
def settings():
    d = _load("settings.json", {})
    d.setdefault("name", "")
    d.setdefault("goal", 20)
    d.setdefault("reviews", {})
    return d


def save_settings(**kw):
    d = settings()
    d.update(kw)
    _save("settings.json", d)


# ---- SORU BANKASI: kapsam başına önceden üretilmiş, doğrulanmış sorular (tek kullanımlık, tüketilir)
import hashlib
import re
import threading

_BANK_LOCK = threading.Lock()
BANK_VER = "v3"  # soru kalitesi/zorluk kuralları değişince artırılır: eski bankadaki sorular kullanılmaz
BANK_PER_KEY = 80
BANK_TOTAL = 2500


def bank_key(grade_label, subject, difficulty, topics):
    return hashlib.sha1(f"{BANK_VER}|{grade_label}|{subject}|{difficulty}|{topics}".encode("utf-8")).hexdigest()[:16]


def _bstem(q):
    return re.sub(r"\W+", " ", str(q.get("question", "")).lower())[:70].strip()


def _bank():
    return _load("bank.json", {})


def bank_count(key):
    e = _bank().get(key)
    return len(e["qs"]) if e else 0


def bank_peek(key, limit=20):
    with _BANK_LOCK:
        e = _bank().get(key)
        return [dict(q) for q in e["qs"][:limit]] if e else []


def bank_remove(key, stems):
    stems = set(stems)
    if not stems:
        return
    with _BANK_LOCK:
        b = _bank()
        e = b.get(key)
        if not e:
            return
        e["qs"] = [q for q in e["qs"] if _bstem(q) not in stems]
        if e["qs"]:
            e["ts"] = int(time.time())
        else:
            b.pop(key)
        _save("bank.json", b)


def bank_put(key, meta, qs):
    clean = [{k: v for k, v in q.items() if k != "id"} for q in qs]
    clean = [c for c in clean if _bstem(c)]
    if not clean:
        return 0
    with _BANK_LOCK:
        b = _bank()
        e = b.setdefault(key, {"meta": meta, "qs": [], "ts": 0})
        have = {_bstem(q) for q in e["qs"]}
        added = 0
        for c in clean:
            st_ = _bstem(c)
            if st_ in have:
                continue
            e["qs"].append(c)
            have.add(st_)
            added += 1
        e["qs"] = e["qs"][-BANK_PER_KEY:]
        e["ts"] = int(time.time())
        total = sum(len(x["qs"]) for x in b.values())
        if total > BANK_TOTAL:  # en eski kullanılmayan kapsamlar önce silinir
            for k in sorted((k for k in b if k != key), key=lambda k: b[k].get("ts", 0)):
                total -= len(b[k]["qs"])
                b.pop(k)
                if total <= BANK_TOTAL:
                    break
        _save("bank.json", b)
        return added


def bank_all():
    return _bank()


def replace_bank(b):
    with _BANK_LOCK:
        _save("bank.json", b if isinstance(b, dict) else {})


def replace_stems(d):
    _save("stems.json", d if isinstance(d, dict) else {})


def bank_stats():
    per = {}
    for e in _bank().values():
        sj = (e.get("meta") or {}).get("subject", "?")
        per[sj] = per.get(sj, 0) + len(e["qs"])
    return {"total": sum(per.values()), "per": per}
'''
MODULES['core/meb_live'] = r'''# -*- coding: utf-8 -*-
"""MEB Öğretim Programları (mufredat.meb.gov.tr) sitesinden program PDF'lerini çeker, kazanım kodlarını ayrıştırır
ve curriculum.LIVE içine yükler. Site yapısı değişirse ya da ders için kazanım kodu bulunamazsa yerleşik müfredat
kullanılmaya devam eder (uygulama asla bozulmaz).

Program sayfaları: https://mufredat.meb.gov.tr/ProgramDetay.aspx?PID=<no>  (indirme bağlantısı /Dosyalar/....pdf)
PID numaraları MEB sitesinin listesinden alınmıştır (2026 programları; İngilizce/Almanca 2025, İnkılap 8. sınıf 2024).
Yeni sürüm çıkınca PROGRAMS listesindeki numarayı güncelleyin."""
import io
import json
import os
import re
import time
from . import curriculum as cur
from . import store

BASE = "https://mufredat.meb.gov.tr"
UA = {"User-Agent": "Mozilla/5.0 (Denemematik; +müfredat okuyucu)"}
G = ["4", "5", "6", "7", "8"]
PROGRAMS = [
    (cur.TR, ["4"], 2351), (cur.TR, ["5", "6", "7", "8"], 2352),
    (cur.MAT, ["4"], 2339), (cur.MAT, ["5", "6", "7", "8"], 2340),
    (cur.FEN, G, 2334), (cur.SOS, ["4", "5", "6", "7"], 2347), (cur.DIN, G, 2150),
    (cur.ING, G, 1903), (cur.ALM, ["5", "6", "7", "8"], 2023), (cur.INK, ["8"], 1974),
]
CODE = re.compile(r"(?<![A-Za-z0-9ÇĞİÖŞÜçğıöşü])([A-ZÇĞİÖŞÜ]{1,6})\.(\d)\.(\d{1,2})\.(\d{1,2})(?:\.(\d{1,2}))?\.?(?=\s)")
CUT = re.compile(r"(Açıklama|Süreç Bileşenleri|Öğrenme Çıktıları|Eğitim Öğretim Durumları|Değerlendirme)")
CACHE = "meb_curriculum.json"


def _get(url, binary=False, timeout=60):
    import requests
    r = requests.get(url, headers=UA, timeout=timeout)
    r.raise_for_status()
    return r.content if binary else r.text


def find_pdf(pid):
    html = _get(f"{BASE}/ProgramDetay.aspx?PID={pid}")
    m = re.search(r'href="([^"]*Dosyalar/[^"]+?\.pdf)"', html, re.I)
    if not m:
        raise RuntimeError(f"PID {pid}: PDF bağlantısı bulunamadı")
    u = m.group(1).replace(" ", "%20")
    return u if u.startswith("http") else BASE + "/" + u.lstrip("/")


def pdf_text(data):
    from pypdf import PdfReader
    rd = PdfReader(io.BytesIO(data))
    return "\n".join((p.extract_text() or "") for p in rd.pages)


def parse(text, grade):
    """Metinden o sınıfa ait kazanımları ayıklar -> [(ünite_adı, [ 'KOD metin', ...])]"""
    t = re.sub(r"\s+", " ", text)
    ms = list(CODE.finditer(t))
    best = {}
    for i, m in enumerate(ms):
        if m.group(2) != str(grade):
            continue
        end = ms[i + 1].start() if i + 1 < len(ms) else len(t)
        body = CUT.split(t[m.end():end])[0].strip(" .-–")[:230]
        if len(body) < 12:
            continue
        code = m.group(0).rstrip(".")
        if code not in best or len(body) > len(best[code][1]):
            best[code] = (int(m.group(3)), body)
    units = {}
    for code, (u, body) in best.items():
        units.setdefault(u, []).append(f"{code}. {body}")
    out = [(f"{u}. Ünite/Tema", sorted(v)) for u, v in sorted(units.items())]
    return out if sum(len(v) for _, v in out) >= 6 else []


def refresh(progress=None, deadline=75):
    """Tüm programları PARALEL indirir; süre dolarsa elde olanla yetinir. -> (kayıt_sayısı, hatalar)"""
    from concurrent.futures import ThreadPoolExecutor, wait
    say = progress or (lambda m: None)
    t0 = time.time()
    data, errs = {}, []
    pids = {}
    for subj, grades, pid in PROGRAMS:
        pids.setdefault(pid, []).append((subj, grades))

    def work(pid):
        return pdf_text(_get(find_pdf(pid), binary=True, timeout=40))

    ex = ThreadPoolExecutor(max_workers=6)
    futs = {ex.submit(work, pid): pid for pid in pids}
    done, pending = wait(list(futs), timeout=deadline)
    for f in pending:
        f.cancel()
        errs.append("zaman aşımı: bazı programlar indirilemedi (yerleşik müfredat kullanılacak)")
    ex.shutdown(wait=False, cancel_futures=True)
    for f in done:
        pid = futs[f]
        try:
            txt = f.result()
        except Exception as e:
            errs.append(f"{type(e).__name__}: {str(e)[:100]}")
            continue
        for subj, grades in pids[pid]:
            for g in grades:
                try:
                    u = parse(txt, g)
                except Exception:
                    u = []
                if u and sane(subj, u):
                    data[f"{g}|{subj}"] = u
    _mark_attempt()
    if data:
        try:
            with open(os.path.join(store.DATA, CACHE), "w", encoding="utf-8") as f:
                json.dump({"ts": int(time.time()), "data": data}, f, ensure_ascii=False)
        except Exception:
            pass
        apply(data)
    return len(data), errs


ATTEMPT = "meb_attempt.txt"


def _mark_attempt():
    try:
        os.makedirs(store.DATA, exist_ok=True)
        with open(os.path.join(store.DATA, ATTEMPT), "w") as f:
            f.write(str(int(time.time())))
    except Exception:
        pass


def needs_refresh(max_age_days=14, retry_hours=6):
    """Önbellek yoksa/eskiyse ve son deneme yakın zamanda yapılmadıysa True."""
    now = time.time()
    try:
        with open(os.path.join(store.DATA, ATTEMPT)) as f:
            if now - int(f.read().strip() or 0) < retry_hours * 3600:
                return False
    except Exception:
        pass
    try:
        with open(os.path.join(store.DATA, CACHE), encoding="utf-8") as f:
            ts = json.load(f)["ts"]
        return now - ts > max_age_days * 86400
    except Exception:
        return True


KEYS = {
    cur.DIN: ["allah", "peygamber", "ibadet", "namaz", "kur", "ahlak", "din", "islam", "iman", "hz.", "hac", "oruç", "zekât", "dua", "hadis", "sabır", "değer", "kader", "melek", "ayet", "cami", "bayram"],
    cur.MAT: ["sayı", "işlem", "üçgen", "açı", "kesir", "geometri", "ölç", "denklem", "oran", "veri", "çarp", "böl", "toplam", "alan", "çevre", "problem", "olasılık", "cebir", "doğru", "çember", "yüzde", "grafik", "örüntü"],
    cur.FEN: ["canlı", "madde", "kuvvet", "enerji", "hücre", "ışık", "ses", "elektrik", "dünya", "güneş", "ay", "deney", "gözlem", "çevre", "isı", "maddenin", "bitki", "hayvan", "ekosistem", "mıknatıs", "asit", "gen"],
    cur.TR: ["metin", "okuma", "yazma", "dinleme", "konuşma", "sözcük", "cümle", "paragraf", "anlam", "şiir", "hikâye", "hikaye", "noktalama", "yazım", "kelime", "anlat", "deyim", "atasöz", "fiil", "isim"],
    cur.SOS: ["toplum", "tarih", "harita", "coğrafya", "kültür", "vatandaş", "ekonomi", "göç", "birey", "türk", "devlet", "bölge", "nüfus", "kaynak", "miras", "demokrasi", "üretim", "tüketim", "yaşam"],
    cur.INK: ["atatürk", "inkılap", "cumhuriyet", "savaş", "kurtuluş", "osmanlı", "milli", "mondros", "lozan", "tbmm", "kongre", "devrim", "antlaşma"],
    cur.ING: ["english", "listen", "speak", "read", "write", "student", "school", "friend", "family", "daily", "teen", "sentence", "dialog", "yabancı dil", "konuş", "dinle", "okuma", "yazma", "tanıt", "anlat", "iletişim"],
    cur.ALM: ["deutsch", "almanca", "hören", "sprechen", "lesen", "schreiben", "dinle", "konuş", "okuma", "yazma", "tanıt", "anlat", "iletişim"],
}


def sane(subject, units):
    """Çekilen programın o derse ait olup olmadığını anahtar kelimelerle doğrular (yanlış PDF = yerleşik müfredata dön)."""
    kz = [str(k).lower() for _, ks in units for k in ks]
    keys = KEYS.get(subject) if subject in (cur.DIN, cur.MAT, cur.FEN, cur.TR) else None  # dil dersleri/Sosyal: kontrol yok
    if not kz or not keys:
        return bool(kz)
    hit = sum(any(w in k for w in keys) for k in kz)
    return hit / len(kz) >= 0.2


def apply(data):
    cur.LIVE.clear()
    for k, v in data.items():
        subj = k.split("|", 1)[-1]
        if sane(subj, v):
            cur.LIVE[k] = [(n, list(t)) for n, t in v]


def load_cache():
    """Önceden çekilmiş MEB müfredatını yükler -> zaman damgası ya da None"""
    try:
        with open(os.path.join(store.DATA, CACHE), encoding="utf-8") as f:
            d = json.load(f)
        apply(d["data"])
        return d["ts"]
    except Exception:
        return None


def status():
    return {"count": len(cur.LIVE)}
'''
MODULES['core/ai_engine'] = r'''# -*- coding: utf-8 -*-
"""Soru üretim motoru. DÜZEN KORUNDU: önce tüm Groq anahtarları, sonra Gemini anahtarları denenir.
Model adları eski kodla aynıdır. Yenilikler: ders ders paralel üretim, tekrarsızlık (nonce + son sorular listesi),
JSON onarımı, doğrulama, seçenek karıştırma, çözüm açıklaması."""
import json
import os
import random
import re
import time
import uuid
from concurrent.futures import ThreadPoolExecutor

GROQ_MODEL = "openai/gpt-oss-120b"
GEMINI_MODEL = "gemini-3.6-flash"
# ORTAK HAVUZ: sıra önemlidir (en iyi model önce). Secrets'ta [api_keys] groq_models / gemini_models ile ezilebilir.
GROQ_MODELS = ["openai/gpt-oss-120b", "openai/gpt-oss-20b", "moonshotai/kimi-k2-instruct", "qwen/qwen3-32b",
               "llama-3.3-70b-versatile", "meta-llama/llama-4-scout-17b-16e-instruct", "llama-3.1-8b-instant"]
GEMINI_MODELS = ["gemini-3.6-flash", "gemini-2.5-flash", "gemini-2.5-flash-lite", "gemini-2.0-flash"]
POOL_MAX_WAIT = 45      # hepsi soğumadaysa en çok bu kadar sn bekleyip yeniden dene
HEDGE_AFTER = 9        # sn; bir model bu sürede yanıt vermezse BEKLEMEDEN sıradaki model de başlatılır (ilk gelen kazanır)
POOL_DEADLINE = 90      # tek istek için toplam üst süre (sn)
SYSTEM = ("Sen MEB Türkiye Yüzyılı Maarif Modeli soru hazırlama uzmanısın. Bağlam temelli, görsel ve veri yoğun, "
          "yorum ve mantık yürütmeye dayalı yeni nesil sorular yazarsın. Paragraf, metin, tablo ve şema sorularında "
          "asla kesinti yapmaz, eksiksiz üretirsin. Yalnızca geçerli JSON döndürürsün.")
CHUNK = 5          # istek sayısı azalır (kota + bekleme); parça başına ~7 soru istenir (5 + EXTRA_FIRST)
WORKERS = 16
EXTRA_FIRST = 2    # ilk turda fazladan istenen soru (elenenler için yedek; tamamlama turlarını çoğunlukla gereksiz kılar)
CALL_TIMEOUT = 25  # sn; takılan çağrı bütün üretimi bekletmesin, havuz sıradaki modele geçsin
GROQ_REASONING = "low"  # gpt-oss modellerinde düşünme süresini kısaltır
# İKİNCİ MODEL KONTROLÜ: üretilen soru, ayrı (hızlı) bir modele cevabı gösterilmeden çözdürülür; tutmayanlar elenir.
VERIFY_SUBJECTS = ("Matematik", "Fen Bilimleri")  # sayısal muhakeme dersleri doğrulanır; diğerleri doğrulama beklemeden hızlı akar
GEN_REASONING = {"Matematik": "low", "Fen Bilimleri": "low"}  # hesap gerektiren derslerde daha derin düşünme
VERIFY_GROQ_MODELS = ["openai/gpt-oss-120b", "openai/gpt-oss-20b", "llama-3.3-70b-versatile"]
VERIFY_GEMINI_MODELS = ["gemini-2.5-flash", "gemini-2.5-flash-lite"]
VERIFY_DEADLINE = 25  # sn; doğrulayıcı yanıt vermezse sorular doğrulanmadan korunur
GEN_BUDGET = 120      # sn; bu süreden sonra yeni tamamlama turu başlatılmaz
MAX_ROUNDS = 5        # istenen sayıya ulaşmak için en çok tur
OYSS_CHUNK = 5        # yazılı sınavda tek istekteki soru sayısı


def _split_keys(v):
    """Liste ya da 'a, b\nc' biçiminde yazılmış anahtarları temiz, tekrarsız listeye çevirir."""
    if v is None:
        return []
    items = re.split(r"[,\s;]+", v) if isinstance(v, str) else [str(x) for x in v]
    out = []
    for k in items:
        k = str(k).strip().strip("\"'")
        if len(k) >= 8 and k not in out and "..." not in k:
            out.append(k)
    return out


def _env_keys(*names):
    out = []
    for nm in names:
        out += _split_keys(os.environ.get(nm))
    i = 1
    while i < 60:  # GROQ_API_KEY_1, _2 …
        v = os.environ.get(f"{names[0].rstrip('S')}_{i}")
        if v:
            out += _split_keys(v)
        i += 1
    return out


def _secret_keys(name):
    import streamlit as st
    try:
        return _split_keys(st.secrets["api_keys"].get(name, []))
    except Exception:
        return []


def load_keys():
    """Groq ve Gemini anahtarları: secrets ([api_keys] groq_keys / gemini_keys) + ortam değişkenleri (GROQ_API_KEYS, GEMINI_API_KEYS…).
    Sınırsız sayıda anahtar eklenebilir; hepsi tek havuzda kullanılır."""
    g = _split_keys(_secret_keys("groq_keys") + _env_keys("GROQ_API_KEYS", "GROQ_API_KEY"))
    m = _split_keys(_secret_keys("gemini_keys") + _env_keys("GEMINI_API_KEYS", "GEMINI_API_KEY", "GOOGLE_API_KEY"))
    return g, m


# Havuza katılabilen ek (OpenAI uyumlu) sağlayıcılar: anahtarı varsa otomatik devreye girer -> çok daha büyük kota.
EXTRA_PROVIDERS = {
    "cerebras": ("https://api.cerebras.ai/v1", ["gpt-oss-120b", "llama-3.3-70b", "qwen-3-235b-a22b-instruct-2507", "llama3.1-8b"]),
    "openrouter": ("https://openrouter.ai/api/v1", ["openai/gpt-oss-120b:free", "meta-llama/llama-3.3-70b-instruct:free", "qwen/qwen3-235b-a22b:free", "deepseek/deepseek-chat-v3.1:free"]),
    "mistral": ("https://api.mistral.ai/v1", ["mistral-large-latest", "mistral-small-latest", "open-mistral-nemo"]),
    "sambanova": ("https://api.sambanova.ai/v1", ["gpt-oss-120b", "Meta-Llama-3.3-70B-Instruct", "DeepSeek-V3.1"]),
    "nvidia": ("https://integrate.api.nvidia.com/v1", ["openai/gpt-oss-120b", "meta/llama-3.3-70b-instruct", "nvidia/llama-3.3-nemotron-super-49b-v1"]),
    "github": ("https://models.github.ai/inference", ["openai/gpt-4.1", "openai/gpt-4.1-mini", "meta/Llama-3.3-70B-Instruct"]),
}


def extra_keys():
    """{sağlayıcı: [anahtarlar]} — secrets'ta '<ad>_keys' (cerebras_keys, openrouter_keys, mistral_keys, sambanova_keys, nvidia_keys, github_keys) ya da ortam değişkeni."""
    out = {}
    for nm in EXTRA_PROVIDERS:
        ks = _split_keys(_secret_keys(nm + "_keys") + _env_keys(nm.upper() + "_API_KEYS", nm.upper() + "_API_KEY"))
        if ks:
            out[nm] = ks
    return out


def has_any_keys():
    g, m = load_keys()
    return bool(g or m or extra_keys())


def demo_mode():
    return os.environ.get("DENEMEMATIK_DEMO") == "1"


# ---------------------------------------------------------------- ORTAK HAVUZ (kota dostu)
import itertools
import threading
import functools

_UID = itertools.count()
_INFL = {}              # (sağlayıcı, anahtar_no, model) -> o an uçuştaki istek sayısı
INFLIGHT_CAP = 2        # aynı anahtar+model'e aynı anda en çok bu kadar istek: yük modellere/anahtarlara yayılır, ani 429'lar azalır
_POOL_LOCK = threading.Lock()
_COOL = {}   # (sağlayıcı, anahtar_no, model) -> bu zamana kadar bekle
_DEAD = {}   # ("model", sağlayıcı, model) / ("key", sağlayıcı, anahtar_no) -> bu zamana kadar kullanma


_PREF_CACHE = {}


def _pref_models():
    """Tercih sırası: secrets ([api_keys] groq_models / gemini_models) varsa o, yoksa koddaki liste. auto_models=false -> keşif kapalı."""
    import streamlit as st
    g, m, auto = list(GROQ_MODELS), list(GEMINI_MODELS), True
    try:
        ak = st.secrets["api_keys"]
        g = list(ak.get("groq_models", g)) or g
        m = list(ak.get("gemini_models", m)) or m
        auto = bool(ak.get("auto_models", True))
        _PREF_CACHE["v"] = (g, m, auto)
    except Exception:
        if "v" in _PREF_CACHE:
            return _PREF_CACHE["v"]
    return g, m, auto


# ---------------------------------------------------------------- MODEL KEŞFİ: mevcut + gelecekte çıkacak modeller
_DISC = {}  # sağlayıcı -> {"ts": zaman, "ids": [modeller]}
_DISC_LOCK = threading.Lock()
DISC_TTL = 6 * 3600     # başarılı keşif önbelleği
DISC_FAIL_TTL = 300     # başarısız keşif tekrar deneme aralığı
MAX_EXTRA = 6           # listede olmayan, yeni keşfedilen en çok bu kadar model eklenir
_GROQ_BAD = re.compile(r"whisper|tts|guard|safeguard|orpheus|playai|embed|compound|moderation|transcri|speech", re.I)
_GEM_BAD = re.compile(r"embed|imagen|veo|aqa|tts|image|live|audio|robotics|computer-use|learnlm|gemma|latest|transcri|native|dialog", re.I)


def _list_groq(key):
    from groq import Groq
    c = Groq(api_key=key, timeout=10, max_retries=0)
    out = []
    for m in c.models.list().data:
        mid = str(getattr(m, "id", "") or "")
        cw = getattr(m, "context_window", None)
        if not mid or getattr(m, "active", True) is False or (isinstance(cw, int) and cw < 8192) or _GROQ_BAD.search(mid):
            continue
        out.append(mid)
    return out


def _list_gemini(key):
    from google import genai
    from google.genai import types
    c = genai.Client(api_key=key, http_options=types.HttpOptions(timeout=10000))
    out = []
    for m in c.models.list():
        name = str(getattr(m, "name", "") or "").replace("models/", "")
        acts = getattr(m, "supported_actions", None)
        if acts is not None and "generateContent" not in acts:
            continue
        if name.startswith("gemini") and not _GEM_BAD.search(name):
            out.append(name)
    return out


def _discover(provider, keys):
    now = time.time()
    with _DISC_LOCK:
        e = _DISC.get(provider)
        if e and now - e["ts"] < (DISC_TTL if e["ids"] else DISC_FAIL_TTL):
            return e["ids"]
        fn = _list_groq if provider == "groq" else _list_gemini
        ids = []
        for k in list(keys)[:3]:
            try:
                ids = fn(k)
                if ids:
                    break
            except Exception:
                continue
        _DISC[provider] = {"ts": now, "ids": ids}
        return ids


def _rank_groq(mid):
    low = mid.lower()
    m = re.search(r"(\d+(?:\.\d+)?)b", low)
    size = float(m.group(1)) if m else 40.0
    return -(size - (5 if "preview" in low else 0))


def _rank_gemini(mid):
    low = mid.lower()
    v = re.search(r"gemini-(\d+(?:\.\d+)?)", low)
    ver = float(v.group(1)) if v else 0.0
    tier = 3 if ("flash" in low and "lite" not in low) else 2 if "lite" in low else 1 if "pro" in low else 0
    return (-tier, 1 if ("preview" in low or "exp" in low) else 0, -ver)


def resolve_models(pref_g, pref_m, gkeys, mkeys, extras=True):
    """Tercih listesini API'nin GERÇEK model listesiyle süzer (kalkan modeller düşer), yeni çıkan modelleri sona ekler.
    Keşif başarısızsa tercih listesi olduğu gibi kullanılır."""
    out = []
    for prov, pref, keys, rank in (("groq", pref_g, gkeys, _rank_groq), ("gemini", pref_m, mkeys, _rank_gemini)):
        keys = [k for k in keys if str(k).strip()]
        avail = _discover(prov, keys) if keys else []
        if not avail:
            out.append(list(pref))
            continue
        lst = [m for m in pref if m in set(avail)]
        if extras:
            lst += sorted((m for m in avail if m not in set(lst)), key=rank)[:MAX_EXTRA]
        elif not lst:
            lst = sorted(avail, key=rank)[:2]
        out.append(lst or list(pref))
    return tuple(out)


def load_models(gkeys=None, mkeys=None):
    g, m, auto = _pref_models()
    if auto and (gkeys or mkeys):
        try:
            return resolve_models(g, m, gkeys or [], mkeys or [])
        except Exception:
            pass
    return g, m


def model_summary():
    with _DISC_LOCK:
        return {k: len(v["ids"]) for k, v in _DISC.items()}


class _HttpErr(Exception):
    def __init__(self, msg, code):
        super().__init__(msg)
        self.status_code = code


_XM_CACHE = {}  # sağlayıcı -> (zaman, [model kimlikleri])
_NOT_CHAT = re.compile(r"embed|vision|guard|whisper|tts|image|rerank|moderation|ocr|audio|safety|speech|clip|stable|flux", re.I)


def _extra_models(name, base, key):
    """Tercih listesi (secrets'ta '<ad>_models' ile değiştirilebilir) + varsa /models ile keşfedilen en iyi yeni modeller."""
    import streamlit as st
    pref = list(EXTRA_PROVIDERS[name][1])
    try:
        pref = list(st.secrets["api_keys"].get(name + "_models", pref)) or pref
    except Exception:
        pass
    ts, ids = _XM_CACHE.get(name, (0, None))
    if ids is None or time.time() - ts > 3600:
        ids = []
        try:
            import urllib.request
            rq = urllib.request.Request(base.rstrip("/") + "/models", headers={"Authorization": "Bearer " + key, "User-Agent": "denemematik"})
            with urllib.request.urlopen(rq, timeout=6) as r:
                d = json.loads(r.read().decode("utf-8", "replace"))
            ids = [str(x.get("id")) for x in (d.get("data") if isinstance(d, dict) else d) if isinstance(x, dict) and x.get("id")]
        except Exception:
            ids = []
        _XM_CACHE[name] = (time.time(), ids)
    if not ids:
        return pref
    have = [m for m in pref if m in ids]
    if name == "openrouter":
        free = [m for m in ids if m.endswith(":free") and not _NOT_CHAT.search(m)]
        score = lambda m: -(int(re.search(r"(\d+)b", m).group(1)) if re.search(r"(\d+)b", m) else 0)
        extra = sorted([m for m in free if m not in have], key=score)[:3]
    else:
        score = lambda m: -(int(re.search(r"(\d+)[bB]", m).group(1)) if re.search(r"(\d+)[bB]", m) else 0)
        extra = sorted([m for m in ids if m not in have and not _NOT_CHAT.search(m) and re.search(r"gpt-oss|llama|qwen|mistral|deepseek|gemma|nemotron", m, re.I)], key=score)[:2]
    return (have + extra) or pref


def _compat_call(name, base, key, prompt_text, system=None, temperature=0.85, model=None, reasoning=None):
    """OpenAI uyumlu /chat/completions çağrısı (stdlib ile; ek paket gerekmez)."""
    import urllib.request
    import urllib.error
    system = SYSTEM if system is None else system
    drop = _CAPS.setdefault((name, model), set())
    for _ in range(4):
        body = {"model": model, "max_tokens": 8000,
                "messages": [{"role": "system", "content": system}, {"role": "user", "content": prompt_text}]}
        if "temperature" not in drop:
            body["temperature"] = temperature
        if "response_format" not in drop:
            body["response_format"] = {"type": "json_object"}
        rq = urllib.request.Request(base.rstrip("/") + "/chat/completions", data=json.dumps(body).encode("utf-8"),
                                    headers={"Authorization": "Bearer " + key, "Content-Type": "application/json", "User-Agent": "denemematik"})
        try:
            with urllib.request.urlopen(rq, timeout=CALL_TIMEOUT) as r:
                data = json.loads(r.read().decode("utf-8", "replace"))
        except urllib.error.HTTPError as e:
            txt = e.read().decode("utf-8", "replace")[:600]
            low = txt.lower()
            if e.code in (400, 422):
                hit = next((t for t in ("response_format", "temperature") if t in low and t not in drop), None)
                if hit:
                    drop.add(hit)
                    continue
                if "json" in low and "response_format" not in drop:
                    drop.add("response_format")
                    continue
            ra = e.headers.get("retry-after") if e.headers else None
            raise _HttpErr(f"HTTP {e.code}: {txt}" + (f" Please try again in {ra}s" if ra and str(ra).replace('.', '').isdigit() else ""), e.code)
        ch = (data.get("choices") or [{}])[0]
        if ch.get("finish_reason") == "length":
            raise ValueError("truncated: finish_reason=length")
        txt = (ch.get("message") or {}).get("content") or ""
        if not txt.strip():
            raise ValueError("boş yanıt")
        return _strip_think(txt)
    raise RuntimeError(f"{name}: uyumlu istek parametreleri bulunamadı")


def _retry_after(msg):
    """Hata metninden 'try again in 7m12.5s' / 'retry in 34s' / retryDelay: '34s' süresini saniye olarak çıkarır."""
    m = re.search(r"(?:try again in|retry in|retrydelay['\"]?\s*:\s*['\"]?)\s*([0-9hmsµ\.]+)", msg, re.I)
    if not m:
        return None
    tot = 0.0
    for num, unit in re.findall(r"(\d+(?:\.\d+)?)(ms|h|m|s)", m.group(1)):
        tot += float(num) * {"ms": .001, "s": 1, "m": 60, "h": 3600}[unit]
    return tot or None


def _classify(e):
    """-> (tür, saniye): 'rate' (kota/hız), 'model' (model yok/kalktı), 'key' (anahtar geçersiz), 'other'"""
    msg = f"{type(e).__name__}: {e}"
    low = msg.lower()
    code = getattr(e, "status_code", None) or getattr(e, "code", None)
    try:
        code = int(code)
    except Exception:
        code = None
    if "limit: 0" in low:  # bu modelin bu anahtarda ücretsiz kotası yok
        return "rate", 3600
    if (code in (400, 403, 404) and "model" in low and ("terms" in low or "not support" in low or "not a valid model" in low or "invalid model" in low
                                                         or "no access" in low or "does not have access" in low or "not available" in low)) \
            or code == 404 or "model_not_found" in low or "decommissioned" in low or "does not exist" in low or "not found" in low and "model" in low:
        return "model", 6 * 3600
    if code in (401, 403) or "invalid api key" in low or "api key not valid" in low or "api key expired" in low or "api_key_invalid" in low or "permission_denied" in low:
        return "key", 6 * 3600
    if code in (429, 413) or "rate limit" in low or "rate_limit" in low or "quota" in low or "resource_exhausted" in low or "too many requests" in low:
        ra = _retry_after(msg)
        if ra is None:
            ra = 3600 if re.search(r"per day|perday|daily|tokens per day|requests per day", low) else 60
        return "rate", min(max(ra, 2), 6 * 3600)
    if code in (500, 502, 503, 504) or "overloaded" in low or "unavailable" in low or "timeout" in low:
        return "other", 8
    return "other", 5


def _mark(provider, kidx, model, kind, secs):
    now = time.time()
    with _POOL_LOCK:
        if kind == "key":
            _DEAD[("key", provider, kidx)] = now + secs
        elif kind == "model":
            _DEAD[("model", provider, model)] = now + secs
        else:
            _COOL[(provider, kidx, model)] = now + secs


def _wait_for(provider, kidx, model, now):
    """Bu üçlü şimdi kullanılabilir mi? 0 = evet, aksi hâlde kalan bekleme (sn)."""
    w = 0.0
    for d, k in ((_DEAD, ("key", provider, kidx)), (_DEAD, ("model", provider, model)), (_COOL, (provider, kidx, model))):
        w = max(w, d.get(k, 0) - now)
    return max(w, 0.0)


def _penalize(provider, model, secs=30):
    """Yanıtı kullanılamaz çıkan (bozuk JSON / geçersiz soru) modeli kısa süre sona iter."""
    with _POOL_LOCK:
        _DEAD[("model", provider, model)] = max(_DEAD.get(("model", provider, model), 0), time.time() + secs)


def pool_status():
    now = time.time()
    with _POOL_LOCK:
        cool = sum(1 for v in _COOL.values() if v > now)
        dead = sum(1 for v in _DEAD.values() if v > now)
        badk = sum(1 for k, v in _DEAD.items() if k[0] == "key" and v > now)
    return {"cooling": cool, "disabled": dead, "bad_keys": badk}


# ---------------------------------------------------------------- API çağrıları
_CAPS = {}  # (sağlayıcı, model) -> o modelin desteklemediği, hata mesajından ÖĞRENİLEN seçenekler


def _strip_think(t):
    """Düşünme bloklarını (<think>…</think>) temizler; yeni modeller içeriğe düşünceyi katarsa JSON bozulmasın."""
    t = t or ""
    t = re.sub(r"<think>.*?</think>", "", t, flags=re.S | re.I)
    if "</think>" in t:
        t = t.split("</think>")[-1]
    if "<think>" in t:
        t = t.split("<think>")[0]
    return t.strip()


def call_groq_with_key(api_key, prompt_text, system=SYSTEM, temperature=0.85, model=None, reasoning=None):
    from groq import Groq
    model = model or GROQ_MODEL
    client = Groq(api_key=api_key, timeout=CALL_TIMEOUT, max_retries=0)  # yeniden denemeyi havuz yönetir
    drop = _CAPS.setdefault(("groq", model), set())  # kalıcı: model bu seçeneği desteklemiyor
    tmp = set()                                      # geçici: yalnızca bu çağrı
    for _ in range(6):
        off = drop | tmp
        kw = dict(model=model, messages=[{"role": "system", "content": system}, {"role": "user", "content": prompt_text}])
        kw["max_tokens" if "use_max_tokens" in off else "max_completion_tokens"] = 8000
        if "temperature" not in off:
            kw["temperature"] = temperature
        if "response_format" not in off:
            kw["response_format"] = {"type": "json_object"}
        if "reasoning_effort" not in off and (reasoning or GROQ_REASONING) and model.startswith("openai/gpt-oss"):
            kw["reasoning_effort"] = reasoning or GROQ_REASONING
        try:
            comp = client.chat.completions.create(**kw)
        except Exception as e:
            low = str(e).lower()
            if getattr(e, "status_code", None) in (400, 422):
                if "json_validate_failed" in low or "failed to generate json" in low:
                    if "response_format" not in tmp:
                        tmp.add("response_format")  # model bu sefer geçerli JSON üretemedi: serbest metin iste, ayrıştırırız
                        continue
                else:
                    hit = next((t for t in ("response_format", "reasoning_effort", "temperature") if t in low and t not in drop), None)
                    if hit:
                        drop.add(hit)
                        continue
                    if "max_completion_tokens" in low and "use_max_tokens" not in drop:
                        drop.add("use_max_tokens")
                        continue
                    if "json" in low and "response_format" not in drop:
                        drop.add("response_format")
                        continue
            raise
        ch = comp.choices[0]
        if getattr(ch, "finish_reason", None) == "length":
            raise ValueError("truncated: finish_reason=length")  # yarım JSON: sıradaki modele geç
        return _strip_think(ch.message.content)
    raise RuntimeError("groq: uyumlu istek parametreleri bulunamadı")


def call_gemini_with_key(api_key, prompt_text, system=SYSTEM, temperature=None, model=None, reasoning=None):
    from google import genai
    from google.genai import types
    model = model or GEMINI_MODEL
    try:
        ho = types.HttpOptions(timeout=CALL_TIMEOUT * 1000, retry_options=types.HttpRetryOptions(attempts=1))  # yeniden denemeyi havuz yönetir
    except Exception:
        ho = types.HttpOptions(timeout=CALL_TIMEOUT * 1000)
    client = genai.Client(api_key=api_key, http_options=ho)
    drop = _CAPS.setdefault(("gemini", model), set())
    response = None
    for _ in range(3):
        cfg = None if "json" in drop else types.GenerateContentConfig(response_mime_type="application/json")
        try:
            response = client.models.generate_content(model=model, contents=system + "\n\n" + prompt_text, config=cfg)
        except Exception as e:
            low = str(e).lower()
            if cfg is not None and str(getattr(e, "code", "") or getattr(e, "status_code", "")) == "400" and ("mime" in low or "json" in low or "response_schema" in low):
                drop.add("json")  # bu model JSON modunu desteklemiyor: düz metin iste
                continue
            raise
        break
    try:
        text = response.text or ""
    except Exception:  # engellenen / boş yanıt
        text = ""
    text = _strip_think(text)
    if "```json" in text:
        text = text.split("```json")[1].split("```")[0].strip()
    elif "```" in text:
        text = text.split("```")[1].split("```")[0].strip()
    return text


from concurrent.futures import ThreadPoolExecutor as _TPE, wait as _cf_wait, FIRST_COMPLETED as _cf_first
_HEDGE_EX = _TPE(max_workers=96)


_LAT = {}  # (sağlayıcı, model) -> ortalama başarılı yanıt süresi (sn); en hızlı sağlıklı model öne alınır
LAT_DEFAULT = 5.0


def _lat_update(prov, model, secs, ok):
    with _POOL_LOCK:
        old = _LAT.get((prov, model), LAT_DEFAULT)
        _LAT[(prov, model)] = .6 * old + .4 * (secs if ok else max(30.0, secs))


def _timed(prov, model, fn, key, prompt_text, kw):
    t = time.time()
    try:
        r = fn(key, prompt_text, **kw)
    except Exception:
        _lat_update(prov, model, time.time() - t, False)
        raise
    _lat_update(prov, model, time.time() - t, bool(r))
    return r


def _infl_done(bk):
    with _POOL_LOCK:
        _INFL[bk] = max(0, _INFL.get(bk, 0) - 1)


def multi_pool_generate(prompt_text, groq_keys, gemini_keys, offset=0, temperature=None, models=None, system=None, reasoning=None, deadline=None, max_wait=None, exclude=None, meta=None):
    """Ortak havuz: önce Groq'un TÜM modelleri (her model için tüm anahtarlar), sonra Gemini'nin tüm modelleri.
    Kota/hız sınırına takılan (anahtar, model) çifti süreli 'soğumaya' alınır ve atlanır; tüm iş parçacıkları
    bu durumu paylaşır, böylece aynı kotaya tekrar tekrar çarpılmaz."""
    gk = [(i, k) for i, k in enumerate(groq_keys) if str(k).strip()]
    mk = [(i, k) for i, k in enumerate(gemini_keys) if str(k).strip()]
    xk = extra_keys()
    if not gk and not mk and not xk:
        return None, "Geçerli API anahtarı bulunamadı!"
    gmodels, mmodels = models if models else load_models([k for _, k in gk], [k for _, k in mk])
    deadline = POOL_DEADLINE if deadline is None else deadline
    max_wait = POOL_MAX_WAIT if max_wait is None else max_wait
    plan = []
    for prov, keys, models, fn in (("groq", gk, gmodels, call_groq_with_key), ("gemini", mk, mmodels, call_gemini_with_key)):
        if not keys:
            continue
        r = offset % len(keys)
        rot = keys[r:] + keys[:r]  # paralel işlerde yükü dağıt
        for model in models:
            if exclude and model in exclude:
                continue
            for kidx, key in rot:
                plan.append((prov, kidx, key, model, fn))
    for nm, ks in xk.items():  # ek sağlayıcılar: Groq ve Gemini'den sonra
        try:
            base = EXTRA_PROVIDERS[nm][0]
            mods = _extra_models(nm, base, ks[0])
        except Exception:
            continue
        rotx = [(i, k) for i, k in enumerate(ks)]
        r0 = offset % len(rotx)
        rotx = rotx[r0:] + rotx[:r0]
        fnx = functools.partial(_compat_call, nm, base)
        for model in mods:
            if exclude and model in exclude:
                continue
            for kidx, key in rotx:
                plan.append((nm, kidx, key, model, fnx))
    plan.sort(key=lambda e: _LAT.get((e[0], e[3]), LAT_DEFAULT))  # kararlı sıralama: en hızlı sağlıklı model önce, anahtar sırası korunur
    t0 = time.time()
    last = None
    tried = set()
    pend = {}  # uçuştaki çağrılar: future -> (sağlayıcı, anahtar, model)

    def collect(wait_s):
        nonlocal last
        if not pend:
            return None
        done, _ = _cf_wait(list(pend), timeout=wait_s, return_when=_cf_first)
        for f in done:
            prov_, kidx_, model_ = pend.pop(f)
            try:
                r_ = f.result()
                if r_:
                    if meta is not None:
                        meta.update(provider=prov_, model=model_)
                    return r_
                _mark(prov_, kidx_, model_, "other", 5)  # boş yanıt
            except Exception as e:
                last = e
                kind, secs = _classify(e)
                _mark(prov_, kidx_, model_, kind, secs)
        return None

    while time.time() - t0 < deadline:
        now = time.time()
        soonest = None
        progressed = False
        for prov, kidx, key, model, fn in plan:
            if (prov, kidx, model) in tried:
                continue
            w = _wait_for(prov, kidx, model, now)
            if w <= 0 and _INFL.get((prov, kidx, model), 0) >= INFLIGHT_CAP:
                w = 1.0  # bu anahtar+model şu an meşgul: sıradakine geç
            if w > 0:
                soonest = w if soonest is None else min(soonest, w)
                continue
            tried.add((prov, kidx, model))
            progressed = True
            kw = {"model": model}
            if temperature is not None:
                kw["temperature"] = temperature
            if system is not None:
                kw["system"] = system
            if reasoning is not None:
                kw["reasoning"] = reasoning
            _bk = (prov, kidx, model)
            with _POOL_LOCK:
                _INFL[_bk] = _INFL.get(_bk, 0) + 1
            _f = _HEDGE_EX.submit(_timed, prov, model, fn, key, prompt_text, kw)
            _f.add_done_callback(lambda _x, _bk=_bk: _infl_done(_bk))
            pend[_f] = (prov, kidx, model)
            r = collect(HEDGE_AFTER)  # yavaşsa beklemeden sıradaki modeli de başlat
            if r:
                return r, None
            if time.time() - t0 >= deadline:
                break
        # bir tur bitti: her şey denendiyse ya da soğumadaysa
        remaining = [p for p in plan if (p[0], p[1], p[3]) not in tried]
        if pend:  # uçuştaki çağrıları bekle
            r = collect(2 if (remaining and progressed) else 3)
            if r:
                return r, None
            if not (remaining and progressed):
                continue
        if remaining and progressed:
            continue
        # denenmemiş ve şu an uygun olan kalmadı: soğuma bitenler için tekrar dene
        tried.clear()
        with_wait = [(_wait_for(p[0], p[1], p[3], time.time()), p) for p in plan]
        avail = [w for w, _ in with_wait if w <= 0]
        if avail and progressed:
            continue
        nxt = min((w for w, _ in with_wait), default=None)
        if nxt is None or nxt > max_wait or time.time() - t0 + nxt > deadline:
            break
        time.sleep(min(nxt, max_wait) + .3)
    st_ = pool_status()
    return None, f"Tüm modeller/anahtarlar şu an dolu (soğumada: {st_['cooling']}, devre dışı: {st_['disabled']}). Son hata: {str(last)[:160] if last else '-'}"


def parse_json(raw):
    if not raw:
        return None
    t = raw.strip()
    t = re.sub(r"^```(?:json)?|```$", "", t, flags=re.M).strip()
    for cand in (t, t[t.find("{"):t.rfind("}") + 1] if "{" in t else ""):
        if not cand:
            continue
        for c in (cand, re.sub(r",\s*([}\]])", r"\1", cand)):
            try:
                return json.loads(c)
            except Exception:
                pass
    return None


def _salvage_objects(raw):
    """Yarım kalmış JSON'dan, TAMAMLANMIŞ soru nesnelerini kurtarır."""
    if not raw:
        return []
    i = raw.find('"questions"')
    i = raw.find("[", i if i >= 0 else 0)
    if i < 0:
        return []
    out, depth, start, in_str, esc = [], 0, None, False, False
    for j in range(i + 1, len(raw)):
        ch = raw[j]
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
            continue
        if ch == '"':
            in_str = True
        elif ch == "{":
            if depth == 0:
                start = j
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0 and start is not None:
                try:
                    out.append(json.loads(raw[start:j + 1]))
                except Exception:
                    pass
                start = None
            elif depth < 0:
                break
        elif ch == "]" and depth == 0:
            break
    return [o for o in out if isinstance(o, dict)]


def _extract_questions(raw):
    data = parse_json(raw)
    if isinstance(data, dict):
        q = data.get("questions")
        if isinstance(q, list):
            return [x for x in q if isinstance(x, dict)]
        for v in data.values():  # model anahtarı farklı adlandırdıysa
            if isinstance(v, list) and v and all(isinstance(x, dict) for x in v):
                return v
    if isinstance(data, list):
        return [x for x in data if isinstance(x, dict)]
    return _salvage_objects(raw)


def _ask_questions(prompt, gk, mk, offset, validate, tries=3, reasoning=None):
    """Havuzdan soru ister. Yanıt kullanılamazsa (bozuk JSON / hiç geçerli soru yok) AYNI modeli tekrarlamaz, sıradakine geçer.
    -> (geçerli_sorular, hata)"""
    exclude, last = set(), None
    for t in range(tries):
        meta = {}
        raw, err = multi_pool_generate(prompt, gk, mk, offset=offset + t, exclude=exclude, meta=meta, reasoning=reasoning)
        if not raw:
            return [], err  # havuz tükendi: aynı şeyi tekrar denemek boşuna
        good = validate(_extract_questions(raw))
        if good:
            return good, None
        last = "geçersiz yanıt"
        if meta.get("model"):
            exclude.add(meta["model"])
            _penalize(meta.get("provider", ""), meta["model"], 30)
    return [], last


# ---------------------------------------------------------------- ikinci model kontrolü
VERIFY_SYSTEM = "Sen titiz bir MEB soru doğrulayıcısısın. Soruları bağımsız çözer, yalnızca geçerli JSON döndürürsün."
VERIFY_STATS = {"checked": 0, "rejected": 0, "unverified": 0}


def verify_stats():
    with _POOL_LOCK:
        return dict(VERIFY_STATS)


def _vq_text(i, q):
    sh = q.get("shape")
    sh_txt = json.dumps(sh, ensure_ascii=False)[:1500] if sh else "yok"
    opts = " | ".join(f"{k}) {v}" for k, v in q["options"].items())
    return f"[{i}] METİN: {q.get('passage') or '-'}\n    GÖRSEL VERİSİ: {sh_txt}\n    SORU: {q['question']}\n    ŞIKLAR: {opts}"


def _verify_models(gk, mk):
    try:
        return resolve_models(VERIFY_GROQ_MODELS, VERIFY_GEMINI_MODELS, gk, mk, extras=False)
    except Exception:
        return (VERIFY_GROQ_MODELS, VERIFY_GEMINI_MODELS)


def verify_questions(qs, gk, mk, offset=0):
    """Soruları cevap gösterilmeden çözdürür; doğru şıkkı tutmayan (ya da hatalı bulunan) soruları eler.
    Doğrulayıcıya ulaşılamazsa sorular doğrulanmadan korunur."""
    if not qs:
        return qs
    prompt = ("Aşağıdaki çoktan seçmeli soruları SEN çöz. Her soru için doğru şıkkı bağımsız olarak hesapla/doğrula ve harfini ver (A, B, C veya D). "
              "Soru hatalıysa (doğru şık yok, birden çok şık doğru, cevap için veri eksik, soru ile görsel verisi ya da kendi içindeki sayılar/ifadeler tutarsız, bilgi yanlış) 'X' ver.\n\n"
              + "\n\n".join(_vq_text(i, q) for i, q in enumerate(qs, 1))
              + '\n\nÇIKTI SADECE şu JSON: {"results":[{"i":1,"answer":"A"}]}')
    raw, err = multi_pool_generate(prompt, gk, mk, offset=offset, temperature=0, models=_verify_models(gk, mk),
                                   system=VERIFY_SYSTEM, reasoning="medium", deadline=VERIFY_DEADLINE, max_wait=0)
    data = parse_json(raw)
    res = data.get("results") if isinstance(data, dict) else None
    if not isinstance(res, list):  # ulaşılamadı / bozuk yanıt: farklı model/anahtarla bir kez daha dene
        raw, err = multi_pool_generate(prompt, gk, mk, offset=offset + 3, temperature=0, models=_verify_models(gk, mk),
                                       system=VERIFY_SYSTEM, reasoning="medium", deadline=VERIFY_DEADLINE, max_wait=0)
        data = parse_json(raw)
        res = data.get("results") if isinstance(data, dict) else None
    if not isinstance(res, list):
        with _POOL_LOCK:
            VERIFY_STATS["unverified"] += len(qs)
        return qs
    got = {}
    for r in res:
        try:
            got[int(r.get("i"))] = str(r.get("answer", "")).strip().upper()[:1]
        except Exception:
            pass
    keep, rej, unv = [], 0, 0
    for i, q in enumerate(qs, 1):
        a = got.get(i)
        if a is None:
            unv += 1
            keep.append(q)
        elif a == q["answer"]:
            keep.append(q)
        else:
            rej += 1
    with _POOL_LOCK:
        VERIFY_STATS["checked"] += len(qs) - unv
        VERIFY_STATS["rejected"] += rej
        VERIFY_STATS["unverified"] += unv
    return keep


# ---------------------------------------------------------------- prompt
_SR_HEAD = (
    "🚨 GÖRSEL KURALLARI (`shape` nesnesi). Matematik, fen ve veri okuma sorularında konuya UYGUN şemayı mutlaka ekle:\n"
)

_SR_BASIC = (
    '- Üçgen: {"type":"triangle","sub_type":"right|scalene|equilateral","A":"A","B":"B","C":"C","side_ab":"3 cm","side_bc":"4 cm","angle_a":"60°"}\n'
    '- Çember: {"type":"circle","center":"O","radius":"5 cm","show_diameter":true}\n'
    '- Dikdörtgen: {"type":"rectangle","width":8,"height":5,"width_label":"8 cm","height_label":"5 cm"}\n'
)

_SR_GEO = (
    '- 📐 KESİN ÖLÇÜLÜ GEOMETRİ (doğru/ışın/doğru parçası, dik-paralel doğrular, açılar, çokgenler; GEOMETRİ konularında TERCİH ET, `labels` köşe/nokta harfleridir):\n'
    '   {"type":"geo","sub_type":"line|ray|segment","labels":["A","B"]}  |  {"type":"geo","sub_type":"lines_set","kinds":["segment","ray","line"]} (I,II,III numaralı karışık çizim; soruda "hangisi ışındır?" gibi)\n'
    '   {"type":"geo","sub_type":"perpendicular","labels":["d1","d2","A"],"tilt":25} (tam 90°)  |  {"type":"geo","sub_type":"parallel","labels":["d1","d2","k"],"transversal":true,"angle":60}\n'
    '   {"type":"geo","sub_type":"angle","degree":50,"rotation":0,"labels":["A","B","C"],"angle_label":"?"} (açı TAM `degree` derece çizilir; ölçüyü soru metni verir ya da öğrenci açıyı türünden sınıflar)\n'
    '   {"type":"geo","sub_type":"angles_two_lines","degree":60,"given":"60°","ask":"x"} (kesişen iki doğru)\n'
    '   {"type":"geo","sub_type":"polygon","sides":6,"labels":["A","B","C","D","E","F"],"equal_ticks":true,"diagonals":false,"irregular":false}  (3-8 kenar)\n'
    '   {"type":"geo","sub_type":"polygon_set","kinds":["üçgen","dörtgen","beşgen","altıgen"],"labels":["K","L","M","N"]} (adı yazmaz; "hangisi beşgendir?")\n'
    '   {"type":"geo","sub_type":"triangle","kind":"right|equilateral|isosceles|scalene|obtuse|acute","labels":["A","B","C"],"ticks":true,"height":false,"apex":"A","right_at":"A","sides":{"AB":"4 cm","AC":"3 cm"},"angles":{"B":"3x+5°","C":"2x+15°","A":"?"}} (kind=right: dik açı right_at köşesinde, dik üçgen gibi çizilir; kind=isosceles: apex = eşit kenarların ortak köşesi, ör. AB=AC ise "A"; ticks=true eş kenarları işaretler; angles/sides: soruda verilen ölçüler AYNEN, sorulan açı "?"; "hangi üçgen?" sorularında ticks:false yap)\n'
    '   {"type":"geo","sub_type":"triangle_set","kinds":["right","equilateral","isosceles","scalene"],"labels":["K","L","M","N"]}\n'
    '   {"type":"geo","sub_type":"quad","kind":"square|rectangle|parallelogram|rhombus|trapezoid|isosceles_trapezoid|kite","labels":["A","B","C","D"],"ticks":true,"diagonals":false,"angles":{"B":"2x+10°","D":"?"},"sides":{"AB":"8 cm"}}  |  {"type":"geo","sub_type":"quad_set","kinds":["square","rectangle","parallelogram","rhombus"]}\n'
    '   {"type":"geo","sub_type":"circle_parts","center":"O","parts":["radius","diameter","chord","arc","tangent","sector"],"labels":["A","B","C","D","E"]} (yarıçap OA, çap BC, kiriş DE; seçilen parçalar çizilir)\n'
    '   ⚠ Soru metni çizilenle BİREBİR aynı olsun: köşe sayısı, harfler, açı ölçüsü, çizim türü çelişmesin; şekil türünün adını (ışın, altıgen…) görselde ipucu olarak yazma.\n'
)

_SR_CHART = (
    '- Çubuk: {"type":"bar_chart","labels":[...],"values":[...],"title":"..."}   Çizgi: {"type":"line_chart","labels":[...],"values":[...],"title":"..."}\n'
    '- Daire grafiği: {"type":"pie_chart","labels":[...],"values":[...],"title":"..."}\n'
    '- Tablo: {"type":"table","title":"...","headers":[...],"rows":[[...],[...]]}\n'
)

_SR_NUMLINE = (
    '- Sayı doğrusu: {"type":"number_line","min":0,"max":10,"step":1,"marks":[{"label":"A","value":2.5}]}\n'
)

_SR_SCI = (
    '- Dinamometre (kuvvet ölçme): {"type":"dynamometer","value":6.5,"max_value":10,"unit":"N","mass_label":"m"}\n'
    '- Termometre: {"type":"thermometer","value":23,"min":-10,"max":50,"step":10,"unit":"°C"}\n'
    '- Dereceli silindir: {"type":"cylinder","max":100,"level":62,"step":10,"unit":"mL"}\n'
    '- Kuvvetler: {"type":"forces","left":[20],"right":[35],"unit":"N","object_label":"Kutu"}\n'
    '- Ay evreleri (8 evre, harf etiketli, adı yazmaz): {"type":"science_space","sub_type":"moon_phases","phases":[0,1,2,3,4,5,6,7],"labels":["A","B","C","D","E","F","G","H"],"title":"..."}  (phases: 0 yeni ay,2 ilk dördün,4 dolunay,6 son dördün)\n'
    '- TEK Ay evresi (büyük, adı yazmaz): {"type":"science_space","sub_type":"moon_single","phase":2,"label":"K"}  (phase: 0 yeni ay,1 büyüyen hilal,2 ilk dördün,3 büyüyen şişkin ay,4 dolunay,5 küçülen şişkin ay,6 son dördün,7 küçülen hilal)\n'
    '- Ay'"'"'ın Dünya çevresindeki 8 konumu (numaralı): {"type":"science_space","sub_type":"moon_orbit","title":"..."}\n'
    '- Güneş/Ay tutulması: {"type":"science_space","sub_type":"solar_eclipse|lunar_eclipse","title":"..."}; Yörünge: {"type":"science_space","sub_type":"orbit"}\n'
)

_SR_FEN = (
    '- 🔧 FEN ŞEMALARI {"type":"fen","sub_type":"..."} (sorudaki TÜM sayı/harfler şemada AYNEN olsun; sorulan değeri şemaya YAZMA, bilinmeyeni "x" ya da "?" yaz; ipucu veren "*_goster" anahtarlarını yazma):\n'
    '   surtunme {"kuvvet":3,"maks":10,"yuk":"2 kg","yuzey":"Pürüzlü yüzey"}  |  basinc_kati {"cisim":"5 kg","G":"50 N","F":"20 N","S":"100 cm²","durus":"yatay|dikey"}  |  '
    'basinc_sivi {"sivi_adi":"Su","noktalar":["K","L","M"],"derinlikler":["10 cm","20 cm","30 cm"]} ya da {"sivi_adi":"Su","kap_sayisi":2,"h":"20 cm"}\n'
    '   mevsim {"K":"K","L":"L","M":"M","N":"N","vurgula":"haziran|eylul|aralik|mart"} (K=21 Haziran, L=23 Eylül, M=21 Aralık, N=21 Mart; tarih/mevsim adını yazma)  |  '
    'dna {"baz_dizisi":"ATGCCTAG","gizle":"tamamlayici"} (en çok 10 baz)  |  caprazlama {"ebeveyn1":"Aa","ebeveyn2":"Aa"} (iki özellik: "AaBb")\n'
    '   direnc {"ortam":"hava|su","isimler":["K","L"],"alanlar":["genis","dar"],"sekil":"levha|parasut"}  |  kaldirac {"tur":"birinci|ikinci|ucuncu","yuk":"60 N","kuvvet":"F","yuk_kolu":"1 m","kuvvet_kolu":"3 m"}  |  '
    'egik_duzlem {"uzunluk":"5 m","yukseklik":"3 m","yuk":"100 N","kuvvet":"F"}  |  makara {"tur":"sabit|hareketli","yuk":"40 N","kuvvet":"F"}  |  disli {"dislerin_sayisi":[20,40],"isimler":["K","L"],"yonler":["saat"]}\n'
)

_SR_FOOT = (
    "⛔ Şemanın başlığı, etiketleri ve değerleri sorunun CEVABINI veya İPUCUNU ASLA içermesin; yalnızca ham veriyi göstersin.\n"
    "Görsel gerektirmeyen sorularda 'shape' değerini null yap. Her seferinde konuya uygun FARKLI görsel türü seç.\n"
    "Metinlerde LaTeX KULLANMA; üs için x², kök için √, çarpma için ×, bölme için ÷ gibi Unicode karakterleri kullan.\n"
)

# Tam metin (geriye dönük uyumluluk)
SHAPE_RULES = _SR_HEAD + _SR_BASIC + _SR_GEO + _SR_CHART + _SR_NUMLINE + _SR_SCI + _SR_FOOT


def shape_rules(subject, geo_on=False):
    """Prompt kısaltma: yalnızca dersin ve konunun gerektirdiği görsel kuralları gönderilir."""
    if subject not in VISUAL_SUBJECTS:
        return ""
    if subject == "Matematik":
        return _SR_HEAD + _SR_BASIC + (_SR_GEO if geo_on else "") + _SR_CHART + _SR_NUMLINE + _SR_FOOT
    if subject == "Fen Bilimleri":
        return _SR_HEAD + _SR_CHART + _SR_SCI + _SR_FEN + _SR_FOOT
    return _SR_HEAD + _SR_CHART + _SR_NUMLINE + _SR_FOOT

SUBJECT_HINT = {
    "Türkçe": "LGS Türkçe tarzı: gerçek bir metin parçası gibi eksiksiz paragraf (ana fikir, yardımcı düşünce, çıkarım, anlatım teknikleri, metnin yapısı), sözel mantık, "
              "deyim/atasözü-metin ilişkisi, yazım-noktalama, anlatım bozukluğu, fiilimsi-ek fiil-cümle türleri, söz sanatları, tablo/grafik/görsel okuma. Metinleri ASLA KISALTMA, eksiksiz yaz.",
    "Matematik": "LGS Matematik tarzı: günlük hayat bağlamında ÇOK ADIMLI problem (cebirsel ifadeler, denklemler, üslü/köklü sayılar, oran-orantı, yüzde, olasılık, veri analizi), "
                 "sayısal mantık ve örüntü, grafik/tablo yorumlama. İşlem sonucu tek ve kesin olsun; tek işlemle çıkan sorular YOK.",
    "Fen Bilimleri": "LGS Fen tarzı: deney düzeneği/hipotez/değişkenler (bağımlı-bağımsız-kontrol), tablo-grafik yorumlama, günlük olayın bilimsel açıklaması, çıkarım, "
                     "kavramları birleştiren çok adımlı muhakeme, gerekiyorsa basit hesaplama. Ay-Güneş-Dünya konularında konuya özel şema seç; kuvvet ölçmede dinamometre kullan.",
    "Sosyal Bilgiler": "LGS Sosyal tarzı: kaynak/belge, harita, tablo, kronoloji yorumlama; neden-sonuç, karşılaştırma ve çıkarım; I-II-III yargı değerlendirme.",
    "T.C. İnkılap Tarihi ve Atatürkçülük": "LGS İnkılap tarzı: kaynak/belge/bildiri yorumlama, neden-sonuç, kronolojik sıralama, olaylar arası ilişki, karşılaştırma; I-II-III yargı değerlendirme; doğru tarih ve olay bilgisi.",
    "Din Kültürü ve Ahlak Bilgisi": "LGS Din Kültürü tarzı: ayet/hadis meali ve vaka/durum yorumlama, değer ve davranış çıkarımı, kavramları ilişkilendirme. Saygılı ve doğru bilgi.",
    "İngilizce": "Sorular İNGİLİZCE yazılır (yönerge dahil). LGS İngilizce tarzı: diyalog tamamlama, okuma parçasından çıkarım, tablo/kart/ilan bilgisi, cümle tamamlama, kelime-bağlam ilişkisi.",
    "Almanca": "Sorular ALMANCA yazılır. A1 düzeyi: diyalog, okuma, kelime, dilbilgisi.",
}


_GEO = {"triangle", "circle", "rectangle", "cylinder", "number_line", "geo"}
_SCI = {"fen", "science_space", "space_orbit", "eclipse", "moon_phases", "dynamometer", "thermometer", "forces", "science_chart", "cylinder"}
_CH = {"bar_chart", "line_chart", "pie_chart", "table"}
ALLOWED_SHAPES = {  # her ders yalnızca kendi alanına uygun görsel türlerini kullanabilir
    "Matematik": _GEO | _CH,
    "Fen Bilimleri": (_SCI | _CH) - {"cylinder"},
    "Sosyal Bilgiler": {"table", "bar_chart", "line_chart", "pie_chart", "number_line"},
    "T.C. İnkılap Tarihi ve Atatürkçülük": {"table", "bar_chart", "line_chart", "number_line"},
}
VISUAL_HINT = {
    "Matematik": "Şekil/grafik/tablo: geometri (üçgen, çember, dikdörtgen), sayı doğrusu, sütun/çizgi/daire grafiği, veri tablosu.",
    "Fen Bilimleri": "Görsel: deney düzeneği verileri, dinamometre, termometre, kuvvet, sürtünme, basınç, mevsimler, DNA, çaprazlama, basit makineler (kaldıraç, eğik düzlem, makara, dişli), Ay evreleri/Güneş-Dünya, tablo ve grafikler. Geometri şekli (üçgen/çember) KULLANMA.",
    "Sosyal Bilgiler": "Görsel yalnızca tablo, sütun/çizgi/daire grafiği ya da zaman çizelgesi (sayı doğrusu) olabilir; geometri ve fen şemaları YOK.",
    "T.C. İnkılap Tarihi ve Atatürkçülük": "Görsel yalnızca kronoloji tablosu/şeridi ya da basit grafik olabilir; geometri ve fen şemaları YOK.",
}
VISUAL_SUBJECTS = ("Matematik", "Fen Bilimleri", "Sosyal Bilgiler", "T.C. İnkılap Tarihi ve Atatürkçülük")
FOREIGN = {  # ders -> o derste olmaması gereken ifadeler (başka dersin sorusu sızarsa elenir)
    "Din Kültürü ve Ahlak Bilgisi": re.compile(r"\b(cm|m²|km|üçgen|dörtgen|çember|denklem|hesapla|kesir|yüzde|ondalık|alanı|çevresi|hacim|formül|newton|joule|hücre|atom)\b", re.I),
    "Türkçe": re.compile(r"\b(üçgen|denklem|kesir|hacim|newton|joule|hücre|atom|alanı kaç)\b", re.I),
    "Sosyal Bilgiler": re.compile(r"\b(üçgen|denklem|kesir|newton|joule|atom)\b", re.I),
    "İngilizce": re.compile(r"\b(üçgen|denklem|kesir|hacim|newton|joule)\b", re.I),
}


# ---------------------------------------------------------------- konu-görsel tutarlılığı (katı)
_MOON = re.compile(r"\bevre|hilal|dolunay|yeni ay|dördün|tutulma|gelgit|\bay['’]?ın\b|dünya.{0,25}\bay\b|\bay\b.{0,25}dünya|güneş.{0,25}\bay\b", re.I)
_FEN_REQ = {
    "surtunme": r"sürtünme|pürüz|dinamometre|kuvvet|yüzey|çekme",
    "basinc_kati": r"basınç|kuvvet|yüzey alan|ağırlık|taban",
    "basinc_sivi": r"basınç|sıvı|derinlik|kap\b|su\b",
    "mevsim": r"mevsim|yörünge|eksen|iklim|haziran|aralık|eylül|mart|güneş ışın",
    "dna": r"dna|baz|nükleotid|genetik|tamamlayıcı|gen\b",
    "caprazlama": r"çaprazlama|genotip|fenotip|kalıtım|allel|punnett|baskın|çekinik|gen\b|bireyler",
    "direnc": r"direnç|hava|su\b|paraşüt|yüzey alan|sürtünme",
    "kaldirac": r"kaldıraç|kuvvet kolu|yük kolu|destek|basit makine",
    "egik_duzlem": r"eğik düzlem|basit makine|yük|kuvvet|rampa",
    "makara": r"makara|basit makine|yük|kuvvet",
    "disli": r"dişli|basit makine|dönüş|devir|diş",
}
_FEN_KINDS = set(_FEN_REQ)

_MOON_KINDS = {"moon_single", "moon_phases", "moon_sequence", "phases", "moon_orbit", "moon_positions", "solar_eclipse", "lunar_eclipse", "eclipse", "orbit", "space_orbit"}
_TOPIC_RULES = [  # (ad, konu regex, izinli görsel türleri)
    ("ay", _MOON, _MOON_KINDS | {"mevsim"}),
    ("kuvvet", re.compile(r"dinamometre|kuvvet|sürtünme|newton|ağırlık|dengelen", re.I), {"dynamometer", "forces", "line_chart", "bar_chart", "table"} | _FEN_KINDS),
    ("ısı", re.compile(r"sıcaklık|termometre|ısı|erime|donma|kaynama|buharlaş", re.I), {"thermometer", "line_chart", "bar_chart", "table", "cylinder"}),
]
_REQUIRE = {  # özel görsel -> metinde bulunması gereken anahtarlar
    "dynamometer": r"kuvvet|dinamometre|ağırlık|newton|yay|kütle",
    "thermometer": r"sıcaklık|termometre|ısı|°|derece",
    "triangle": r"üçgen|açı|kenar|çevre|alan|dik|yükseklik",
    "circle": r"çember|daire|yarıçap|çap|merkez|yay|alan|çevre",
    "rectangle": r"dikdörtgen|kare|dörtgen|alan|çevre|bahçe|zemin|tarla|kenar|uzunluk|genişlik|oda",
    "cylinder": r"hacim|silindir|ml|litre|sıvı|ölç|kap|taşır",
    "forces": r"kuvvet|\bnet\b|hareket|sürtünme|dengelen|itme|çekme",
    "geo": r"doğru|ışın|parça|dik|paralel|açı|çokgen|üçgen|dörtgen|beşgen|altıgen|köşegen|kenar|köşe|şekil|kesen|eş",
    "number_line": r"sayı|doğru|konum|yıl|zaman|kronolo|kesir|ondalık|negatif|tam sayı|eksi|işaret|mutlak|sıra",
}
_REQUIRE.update(_FEN_REQ)
for _k in _MOON_KINDS:
    _REQUIRE[_k] = r"\bay\b|ay['’]?ın|evre|tutulma|uzay|gezegen|yörünge|dünya|güneş|gökcis|uydu|hilal|dolunay"
_FIG = re.compile(r"\b(şekil|şekle|şekilde|şekildeki|grafik|grafiğe|grafikte|grafikteki|tablo|tabloya|tabloda|tablodaki|görsel|görselde|resim|resimde|çizim|çizimde|diyagram)\w*", re.I)


def _kind(shape):
    t = shape.get("type")
    if t == "fen":
        return str(shape.get("sub_type") or "").lower()
    return str(shape.get("sub_type") or t).lower() if t == "science_space" else t


def coherent_shape(shape, text):
    """Görsel, konu/soru metniyle birebir uyumlu mu? -> (şema ya da None, uyumsuz_mu)"""
    if not shape:
        return None, False
    k = _kind(shape)
    for _n, rx, allowed in _TOPIC_RULES:
        if rx.search(text):
            if k not in allowed:
                return None, True
            if k not in _FEN_KINDS:
                return shape, False
            break  # fen şemaları ayrıca kendi konu anahtarını da taşımalı
    req = _REQUIRE.get(k)
    if req and not re.search(req, text, re.I):
        return None, True
    return shape, False


def topic_visual_rules(topics_text):
    """Planın konularına göre prompta eklenecek katı görsel kuralları."""
    out = ""
    if _MOON.search(topics_text or ""):
        out += ("🌙 AY/GÜNEŞ/DÜNYA KONUSU KATI KURAL: Bu konudaki sorularda görsel YALNIZCA Ay evreleri (`moon_phases`), Ay'ın Dünya çevresindeki konumları (`moon_orbit`), "
                "tutulma (`solar_eclipse`/`lunar_eclipse`) ya da yörünge (`orbit`) şeması olabilir. TABLO, ÇUBUK/ÇİZGİ/DAİRE GRAFİĞİ, DİNAMOMETRE, TERMOMETRE, KUVVET şeması KESİNLİKLE YASAK. "
                "Soru metni görseldeki harf/numaralara atıf yapsın (örn. 'Şekildeki K evresi…'); görselde evre adı yazmaz.\n"
                "🌙 AY EVRELERİ SORU ÇEŞİTLERİ (hepsinde görsel ZORUNLU, bol ve çeşitli kullan): (1) `moon_single` ile tek evre göster, 'Şekildeki Ay evresi hangisidir?' (şıklar: Yeni Ay, Hilal, İlk Dördün, Şişkin Ay, Dolunay, Son Dördün); "
                "(2) `moon_phases` ile 3-8 evreyi KARIŞIK sırada (örn. phases [4,0,6,2,7,3,5,1], labels A,B,C…) ver, 'Hangi harf İlk Dördün/Son Dördün/Dolunay/Yeni Ay/Şişkin Ay evresidir?'; "
                "(3) evre sıralaması: 3-4 evreyi karışık ver, 'Ay'ın evre sırasına göre dizilişi hangisidir?'; (4) `moon_orbit` numaralı konumlarda 'Dolunay/Yeni Ay hangi konumda?'; "
                "(5) tutulma şemasıyla Güneş-Dünya-Ay dizilişi; (6) 'Şekildeki evreden … gün sonra Ay hangi evrede olur?' (7 günde bir çeyrek ilerler). "
                "Doğru şık görseldeki evrelerle KESİNLİKLE tutarlı olsun: ilk dördün = sağ yarısı aydınlık (phase 2), son dördün = sol yarısı aydınlık (phase 6), dolunay = phase 4, yeni ay = phase 0, şişkin ay = phase 3 veya 5. "
                "Her soruda FARKLI evre/harf düzeni kullan; aynı görseli tekrar etme.\n")
    if re.search(r"dinamometre|kuvvet|sürtünme", topics_text or "", re.I) and not _MOON.search(topics_text or ""):
        out += "💪 KUVVET konusunda görsel dinamometre ya da kuvvet şeması olsun; sorudaki sayılar görseldekiyle birebir aynı olsun.\n"
    out += ("🎯 SORU–GÖRSEL BİREBİR UYUM: Görsel varsa soru ona doğrudan dayansın ve görseldeki her veri soruyla tutarlı olsun. Konuyla ilgisiz görsel (ör. Ay evresi sorusuna tablo, "
            "Din/Türkçe sorusuna grafik) ASLA koyma; uygun görsel yoksa shape null yap ve metne 'şekil/grafik/tablo' deme.\n")
    return out


def _subject_lock(subject, topics=""):
    base = (f"\n🔒 DERS KİLİDİ: Bu sorular YALNIZCA {subject} dersine aittir. Başka bir dersin (özellikle Matematik/Fen) sorusu, işlem ya da "
            f"geometri problemi SORMA. Her soru verilen ünite/kazanımlardan birine dayansın; kazanımları sırayla gez, her soruda FARKLI bir kazanım ve farklı bağlam kullan.\n")
    if subject not in VISUAL_SUBJECTS:
        base += "Bu derste şekil/grafik ÇİZDİRME: `shape` alanı null olsun (gerekirse yalnızca konuyla ilgili basit bir tablo; matematik/fen şeması ASLA).\n"
    else:
        base += f"GÖRSEL KISITI: {VISUAL_HINT.get(subject, '')} Görsel soruyla birebir ilgili olsun.\n"
    return base + topic_visual_rules(topics)


MATH_NOTATION = (
    "GEOMETRİ GÖSTERİMİ (MEB): açı ölçüsü m(ABC) = 40° biçiminde (tepe harfi ORTADA), kenar uzunluğu |AB| = 5 cm, eş kenarlar |AB| = |AC| biçiminde yazılır. "
    "'∠B = 40°', 'AB = AC', 'm(A)' gibi yazma. Metinde verilen HER eşitlik, ölçü ve uzunluk ŞEKİLDE DE gösterilsin: üçgen şemasında 'kind' (ikizkenarsa 'apex': eşit kenarların ortak köşesi), "
    "'angles' (ör. {\"B\":\"3x+5°\",\"C\":\"2x+15°\"}, sorulan açı için \"?\") ve 'sides' alanlarını soruyla BİREBİR doldur. Şekilde olmayan veri metinde, metinde olmayan veri şekilde olmasın (sorulan değer hariç). "
    "Dörtgenlerde köşeleri sırayla A, B, C, D adlandır ve metinde 'ABCD dörtgeninde' diye belirt (şekil aynı harfleri taşır); dörtgen türünü (dikdörtgen, paralelkenar, ikizkenar yamuk…) soruda yaz, "
    "'quad' şemasında 'kind' ve 'angles'/'sides' alanlarını doldur. İkizkenar üçgen/yamukta eşit kenarları metinde AÇIKÇA yaz (|AB| = |AC|); şekilde bu kenarlar işaretlenir. "
    "Yamukta paralel kenarları metinde yaz (AB ∥ DC); şekil aynı kenarları paralel çizer. Metinde adı geçmeyen özel tür (ikizkenar, dik, eşkenar, dikdörtgen…) şekilde GÖSTERİLMEZ. "
    "Eşkenar üçgende her açı 60° olduğundan cebirsel açı ifadesi (ör. m(BAC) = 3x − 15°) 60°'ye eşitlenince x TAM SAYI çıksın; verilen ifade şekilde ilgili köşede görünür. Dik üçgende dik açının köşesini metinde belirt (m(ABC) = 90° ya da AB ⊥ BC); şekil dik üçgen olarak çizilir. ÇEVRE sorulurken gereken TÜM uzunluklar verilsin: üçgende üç kenar, ya da eşitlik bilgisi (|AB| = |AC| gibi) / eşkenar / dik üçgende iki kenar (Pisagor); iki kenar verip üçüncüsünü bilgisiz bırakma. Metindeki her açı ve uzunluk şekilde de yazılsın; şekilde gösterilemeyen alt açı (ör. m(BAD)) kullanma.\n")

GEO_STYLE = (
    "\n📐 GEOMETRİ SORU TARZI (KATI KURAL; yukarıdaki 'günlük hayat bağlamı / senaryo / metin' yönergesi geometri soruları için GEÇERSİZDİR):\n"
    "- MEB/LGS yeni nesil geometri tarzı: soru kökü KISA (en çok 2-3 cümle, ~45 kelime) ve ŞEKLE dayalı; 'passage' HER ZAMAN null. Ama çözüm TEK ADIMLI OLMASIN: en az İKİ-ÜÇ adımlı muhakeme gerektirsin.\n"
    "- 🚫 YASAK BASİT KALIPLAR: iki açısı verilen üçgende üçüncü açıyı sorma; tek adımlı bütünler/tümler/doğru açı hesabı; tek formüle sayı koyup çevre/alan bulma; "
    "'hangisi üçgendir/ışındır/çaptır' gibi yalnızca tanıma-adlandırma soruları.\n"
    "- BUNUN YERİNE şunlardan BİRİNİ ya da BİRKAÇINI birleştir: bilinmeyenleri cebirsel ifadelerle ver (m(ABC) = 2x + 10°, m(ACB) = 3x − 20°) ve denklem kurdur; paralel doğrular + ikizkenar/eşkenar üçgen + iç-dış açı ilişkisi; "
    "açıortay/yükseklik/kenarortay özelliği; Pisagor + çevre/alan; çokgenin iç/dış açı toplamı + eşitlik; çemberde yarıçap-çap-kiriş ilişkisi + çevre; bileşik şekilde alan/çevre; "
    "şekle bakarak I, II, III yargılarından hangilerinin doğru olduğunu değerlendirtme.\n"
    "- Hikâye, senaryo, tarih, kültür bağlamı YOK. Osmanlı/padişah/savaş/kale/müze/arkeoloji gibi tarihî ya da kültürel konular ve "
    "Güneş/Ay/Dünya/gezegen/uzay gibi gök cismi konuları KESİNLİKLE YASAK. Yalnızca nokta, harf, doğru, açı, kenar, çokgen, çember dili kullan.\n"
    "- HER geometri sorusunda `shape` ZORUNLU (null YASAK). Sorudaki tüm veriler (harfler, ölçüler, x) çizimdekiyle BİREBİR aynı ve kendi içinde TUTARLI olsun (açı toplamları, kenar ilişkileri). "
    "Soru kökü 'Şekilde…', 'Yukarıdaki şekle göre…' diye şekle atıf yapsın; şekildeki verileri uzun metinle yeniden anlatma.\n"
    "- Örnek kök TARZI (kopyalama, kendi verilerini kur): 'Şekilde d₁ ∥ d₂ ve |AB| = |AC| olduğuna göre x kaç derecedir?' | "
    "'Şekildeki ABC üçgeninde |AB| = |AC|, m(ABC) = 2x + 10°, m(ACB) = 3x − 20° ise m(BAC) kaç derecedir?' | "
    "'Yukarıdaki şekle göre I, II ve III yargılarından hangileri doğrudur?' | 'Şekildeki bileşik şeklin çevresi kaç cm'dir?'\n"
    "- Şıklar kısa olsun (sayı, derece, cm, harf ya da numara).\n" + MATH_NOTATION)
_GEO_BASIC_RX = re.compile(r"ışın|doğru parçası|doğrusal|\bnokta", re.I)
_GEO_PLAN_RX = re.compile(r"geometri|açı|ışın|çokgen|üçgen|dörtgen|çember|\bdaire\b|dik |paralel|inşa|prizma|silindir|doğru parçası|köşegen|eşkenar|ikizkenar|\bkare\b", re.I)
_GEO_STRICT = re.compile(r"geometri|açı|ışın|çokgen|üçgen|dörtgen|çember|paralel|\bdik\b|\bkare\b|eşkenar|ikizkenar|köşegen|doğru parçası|inşa|prizma|koni|simetri|dönüşüm", re.I)
_GEO_DRAW = {"geo", "triangle", "circle", "rectangle"}
_GEO_BAN = re.compile(r"osmanl|padişah|sultan|fetih|savaş|tarih|imparator|devlet|medeniyet|kale\b|saray|cami|müze|arkeolo|kazı|gezegen|uzay|yörünge|güneş|\bay\b|ay['’]ın|dünya|\bevre|ilkçağ|masal|hikâye|hikaye", re.I)
_GEO_SKILLS = ["paralel doğruları ve üçgen özelliklerini birleştirerek bilinmeyen açıyı cebirsel ifadeyle bulma", "ikizkenar/eşkenar üçgen özelliği + iç-dış açı ilişkisi",
               "açıortay, yükseklik ya da kenarortay özelliğini kullanarak açı/uzunluk bulma", "Pisagor bağıntısıyla kenar bulup çevre ya da alan hesaplama",
               "bileşik şekilde çevre ya da alan hesaplama", "çokgenin iç/dış açı toplamıyla bilinmeyeni bulma", "çemberde yarıçap-çap-kiriş ilişkisiyle uzunluk hesabı",
               "şekle bakarak I, II, III yargılarını değerlendirme"]


def _is_geo_q(q, shape, subject):
    if subject != "Matematik":
        return False
    if isinstance(shape, dict) and shape.get("type") in _GEO_DRAW:
        return True
    tp = str(q.get("topic") or "")
    return bool(_GEO_STRICT.search(tp)) and not re.search(r"grafik|veri|tablo|olasılık|ortalama", tp, re.I)


_THEMES = ["spor müsabakası", "market alışverişi", "okul kantini", "doğa yürüyüşü", "müze gezisi", "çiftlik", "toplu taşıma", "robotik atölyesi", "resim sergisi",
           "sağlık kontrolü", "hayvanat bahçesi", "mutfak tarifi", "yaz tatili", "kütüphane", "geri dönüşüm", "şehir planı", "bilim insanı", "kültür festivali",
           "bahçe düzenleme", "su tasarrufu", "bisiklet turu", "kamp", "pazar yeri", "fotoğrafçılık", "inşaat", "uzay merkezi", "balıkçılık", "gıda üretimi",
           "okul bahçesi", "tarihî yapı", "kitap fuarı", "hava durumu", "enerji tasarrufu", "kodlama kulübü", "pastane", "arkeoloji kazısı", "akvaryum", "ormancılık"]
_SKILLS = ["kavramı günlük hayattaki bir olaya uygulama", "verilen veriden çıkarım yapma", "iki durumu karşılaştırma", "neden-sonuç ilişkisi kurma", "verilen çözümdeki hatayı bulma",
           "eksik bilgiyi tamamlama", "modelden/şekilden yorum yapma", "çok adımlı muhakeme", "sınıflandırma/eşleştirme", "tahmin ve doğrulama", "örnek/karşı örnek bulma", "sonucu yorumlayıp karar verme"]


def _visual_candidates(subject, topics):
    kinds = []
    for k in sorted(ALLOWED_SHAPES.get(subject, set())):
        if k in ("science_chart", "eclipse", "space_orbit", "moon_phases"):
            continue  # komutta kullanılmayan eş adlar
        if k == "science_space":
            kinds += [("science_space", sub) for sub in ("moon_phases", "moon_single", "moon_orbit", "solar_eclipse", "lunar_eclipse", "orbit")]
        elif k == "fen":
            kinds += [("fen", "fen:" + sub) for sub in sorted(_FEN_KINDS)]
        else:
            kinds.append((k, None))
    ok = []
    for k, sub in kinds:
        sh = {"type": k}
        if sub:
            sh["sub_type"] = sub[4:] if sub.startswith("fen:") else sub
        shp, _bad = coherent_shape(sh, topics or "")
        if shp:
            ok.append(sub or k)
    return sorted(set(ok))


def _variety_plan(subject, n, topics):
    """Her soruya FARKLI bağlam, beceri ve görsel türü atar -> sorular birbirine benzemesin."""
    th = random.sample(_THEMES, min(n, len(_THEMES))) + [random.choice(_THEMES) for _ in range(max(0, n - len(_THEMES)))]
    sk = []
    while len(sk) < n:
        sk += random.sample(_SKILLS, len(_SKILLS))
    vis = _visual_candidates(subject, topics) if subject in VISUAL_SUBJECTS else []
    moon = subject != "Matematik" and bool(_MOON.search(topics or ""))
    if moon:  # Ay evreleri: bolca ve çeşitli Ay görseli, görselsiz soru yok
        vis = ["moon_phases", "moon_single", "moon_phases", "moon_single", "moon_orbit", "moon_phases", "moon_single", "solar_eclipse", "lunar_eclipse"]
    geom = subject == "Matematik" and bool(_GEO_PLAN_RX.search(topics or ""))
    if geom:  # geometri ünitesi: kesin ölçülü geo görselleri ağırlıklı
        geo_k = ["geo:line", "geo:ray", "geo:segment", "geo:lines_set", "geo:perpendicular", "geo:parallel", "geo:angle", "geo:angles_two_lines", "geo:polygon", "geo:polygon_set", "geo:triangle", "geo:triangle", "geo:triangle_set", "geo:quad", "geo:quad_set", "geo:circle_parts", "geo:circle_parts"]
        if not _GEO_BASIC_RX.search(topics or ""):  # temel tanıma görselleri (doğru/ışın/doğru parçası) yalnızca konusu geçiyorsa
            geo_k = [k for k in geo_k if k not in ("geo:line", "geo:ray", "geo:segment", "geo:lines_set")]
        vis = geo_k * 2  # yalnızca kesin ölçülü geometri çizimleri (Ay/tablo/grafik karışmaz)
        sk = []
        while len(sk) < n:
            sk += random.sample(_GEO_SKILLS, len(_GEO_SKILLS))
    else:
        vis = [v for v in vis if v != "geo"]
    random.shuffle(vis)
    lines = []
    for i in range(n):
        if vis and (moon or geom or random.random() > 0.22):  # geometride görsel HER soruda zorunlu
            v = vis[i % len(vis)]
            vtxt = (f"görsel = {{\"type\":\"geo\",\"sub_type\":\"{v[4:]}\"}} (geo şeması)" if v.startswith("geo:") else
                    f"görsel = {{\"type\":\"fen\",\"sub_type\":\"{v[4:]}\"}} (fen şeması)" if v.startswith("fen:") else f"görsel türü = {v}")
        else:
            vtxt = "görselsiz (shape null) ya da metin/tablo ağırlıklı"
        ctx = "YOK (hikâyesiz, kısa, doğrudan şekil sorusu)" if geom else th[i]
        lines.append(f"  Soru {i + 1}: bağlam = {ctx}; beceri = {sk[i]}; {vtxt}")
    return ("\nSORU PLANI (HER SORU AYNI NUMARADAKİ SATIRA UYSUN; sorular ve görseller BİRBİRİNE BENZEMESİN, farklı sayılar/veriler/şekil ölçüleri kullan, "
            "aynı kazanımın farklı yönlerini ölç):\n" + "\n".join(lines) + "\nPlandaki görsel türü konuya uymuyorsa o soruyu görselsiz yaz; ama iki soruda aynı görsel/veri tekrar etmesin.\n")


PLAIN_RULE = ("🚫 GÖRSEL YOK: 'shape' alanını null yap. Soru metni 'şekilde', 'grafikte', 'tabloda' gibi bir görsele atıf yapmasın; gerekirse veriyi metin ya da paragraf içinde ver. "
              "Sorular yalnızca metinle çözülebilsin.\nMetinlerde LaTeX KULLANMA; üs için x², kök için √, çarpma için ×, bölme için ÷ kullan.\n")


DIFF_SPEC = {
    1: "Temel kazanım düzeyi: bilgiyi bağlam içinde kullandır (doğrudan tanım sorma).",
    2: "Kavrama: 1-2 adımlı, bilgiyi yeni bir durumda yorumlatma.",
    3: "Uygulama/yorum: 2-3 adımlı; veriyi okuyup ilişki kurma. LGS'nin orta sorularına denk.",
    4: "LGS orta-zor: 3 ve üzeri adımlı muhakeme; en az İKİ bilgi/kazanımı birleştirme; verilerden çıkarım; çeldiriciler tipik kavram yanılgılarından ve işlem hatalarından türesin.",
    5: "LGS seçici (son sorular): çok aşamalı muhakeme, birden fazla kazanım ya da veri kaynağını birleştirme, özgün durum, tuzak çeldiriciler; kestirme çözümü olmasın.",
    6: "Olimpiyat/üst düzey: LGS'nin en zor sorularından da zor, özgün, çok aşamalı, koşul analizi gerektiren; yine de sınıf düzeyindeki kazanımlarla çözülebilsin.",
}


def bump_difficulty(difficulty):
    """Seçilen kademeyi BİR kademe artırır (en üst kademede kalır). -> (metin, kademe_no)"""
    try:
        from . import curriculum as cur
        L = list(cur.DIFFICULTIES)
        if difficulty in L:
            i = min(L.index(difficulty) + 1, len(L) - 1)
            return L[i], i + 1
        m = re.search(r"(\d)\.", str(difficulty))
        if m:
            i = min(int(m.group(1)), len(L) - 1)
            return L[i], i + 1
    except Exception:
        pass
    return difficulty, 4


LGS_STYLE = (
    "LGS / MEB YENİ NESİL SORU TARZI (KATI):\n"
    "- Soru, bir BAĞLAM ya da VERİ (kısa senaryo, deney, metin, tablo, grafik) sunar; sonra ölçtüğü beceriye yönelik TEK net soru sorar: 'Buna göre … hangisidir?', "
    "'Bu verilere göre aşağıdakilerden hangisi söylenemez?', 'I, II ve III yargılarından hangileri doğrudur?'.\n"
    "- Soru kökü çeşitli olsun: yargı değerlendirme (I-II-III), olumsuz kök (yanlış/söylenemez), sıralama, eşleştirme, çıkarım, karşılaştırma, hata bulma. Tüm sorular aynı kalıpta olmasın.\n"
    "- 🚫 Doğrudan tanım/ezber ('… nedir?', tek bilgiyi hatırlama) ve TEK İŞLEMLİ/TEK ADIMLI sorular YASAK; her soru en az iki adımlı muhakeme (veriyi oku → ilişki kur → sonuca var) gerektirsin.\n"
    "- Çeldiriciler rastgele olmasın: öğrencilerin yapabileceği tipik yanılgılardan ve işlem hatalarından türesin; şıklar benzer uzunlukta olsun, doğru şık uzunluğuyla ya da ifadesiyle ele vermesin.\n")

LOGIC_RULES = (
    "MANTIK KONTROLÜ (ZORUNLU): Her soruyu yazdıktan sonra KENDİN baştan çöz ve şunları doğrula: "
    "(1) Doğru şık TEK ve gerçekten doğru; diğer üç şık KESİNLİKLE yanlış (hiçbiri savunulabilir olmasın). "
    "(2) Soru ve görseldeki tüm sayılar/ifadeler birbiriyle TUTARLI (açı toplamları, yüzde/oran toplamları, tablo-toplam uyumu, birimler). "
    "(3) Cevap için gereken TÜM veri verilmiş; eksik, fazla ya da çelişen veri yok. "
    "(4) Olumsuz kökte (yanlış/söylenemez/değildir) doğru cevabın 'yanlış olan' şık olduğunu karıştırma. "
    "(5) Bilimsel ve tarihsel bilgiler doğru; gerçek kişi/olay/tarih uydurma. Gerçek hayat büyüklükleri mantıklı (süre, uzunluk, kütle, fiyat). "
    "(6) Şıklar birbirinden farklı olsun, aynı anlama gelen iki şık YOK.\n"
    "GERÇEKÇİLİK: Sayılar gerçek hayatta makul olsun (yaş, boy, fiyat, hız, süre, kütle, sıcaklık); birimler tutarlı; adlar ve yerler Türkçe ve doğal (Ayşe, Mehmet, İzmir…); "
    "işlem sonuçları 'düzgün' çıksın (tam sayı ya da yalın kesir/ondalık); senaryo gerçekten yaşanabilir olsun; dil MEB/LGS yeni nesil soru kökü gibi akıcı ve kısa; "
    "çeldiriciler öğrencinin gerçek hata türlerinden (işlem hatası, birim karıştırma, kavram yanılgısı, yönü/işareti karıştırma) türesin; sayısal şıkları küçükten büyüğe sırala. "
    "Önce 'explanation' alanında çözümü ADIM ADIM ama ÖZ yap (en çok 4 kısa adım), doğru sonucu bulduktan sonra 'answer' yaz. Çözümün SON adımı işaretlediğin şıkkın değeriyle BİREBİR aynı sonucu versin (çözüm ile cevap çelişmesin). 'explanation' şık HARFİ (A, B…) yazmasın, şıkkın DEĞERİNİ yazsın.\n")


def mc_prompt(grade_label, subject, n, topics, difficulty, scope_label, avoid, focus="", start_id=1, plain=False):
    nonce = uuid.uuid4().hex[:8]
    av = ("\nAŞAĞIDAKİ SORULARI/KONULARI TEKRARLAMA (farklı bağlam ve veri kullan):\n- " + "\n- ".join(avoid[-18:])) if avoid else ""
    geo_on = subject == "Matematik" and bool(_GEO_PLAN_RX.search(topics or ""))
    plain = plain and not geo_on  # geometri şekilsiz olmaz
    eff, lvl = bump_difficulty(difficulty)
    fc = f"\nODAK KONU: '{focus}' (soruların yaklaşık 1/3'ünde bu konuya odaklan, kalanı diğer kazanımlardan)." if focus.strip() else ""
    return (
        f"Türkiye Cumhuriyeti MEB {grade_label} {subject} dersi resmî öğretim programı (Türkiye Yüzyılı Maarif Modeli) kazanımlarına "
        f"tam uygun, TAM {n} adet ÇOKTAN SEÇMELİ (A,B,C,D) yeni nesil soru hazırla.\n"
        f"KAPSAM: {scope_label}\nKONULAR/KAZANIMLAR: {topics}{fc}\n"
        f"ZORLUK KADEMESİ: '{eff}'. Bu kademeye kesin uy → {DIFF_SPEC.get(lvl, '')}\n"
        f"DERS YÖNERGESİ: {SUBJECT_HINT.get(subject, '')}\n"
        + ("MEB/LGS geometri soru anlayışı: kısa, şekle dayalı, hikâyesiz ama ÇOK ADIMLI muhakeme gerektiren sorular.\n" if geo_on else LGS_STYLE) +
        "Sınıf düzeyinin dışına (üst sınıf konusuna) taşma; kazanım kapsamında kal.\n" + (MATH_NOTATION if (subject == "Matematik" and not geo_on) else "") + LOGIC_RULES +
        f"Çeşitlilik tohumu: {nonce}. Her soru birbirinden bağımsız ve farklı olsun.{'' if plain else _variety_plan(subject, n, topics)}"
        f"{av}\n{_subject_lock(subject, topics)}\n{PLAIN_RULE if plain else shape_rules(subject, geo_on) + (GEO_STYLE if geo_on else '')}\n"
        "Her soruda: kısa 'topic' (kazanım adı), gerekirse 'passage', 'question', 4 şık, adım adım 'explanation' (çözüm) ve çözümden SONRA 'answer' (A/B/C/D) olsun.\n"
        'ÇIKTI SADECE şu JSON: {"questions":[{"id":%d,"subject":"%s","topic":"...","passage":"... veya null","question":"...",'
        '"shape":null,"options":{"A":"..","B":"..","C":"..","D":".."},"explanation":"..","answer":"A"}]}' % (start_id, subject))


def oyss_prompt(grade_label, subject, items, difficulty, avoid):
    """items: [{kazanim, n, difficulty_labels:[..]}]"""
    nonce = uuid.uuid4().hex[:8]
    lines = []
    for it in items:
        lines.append(f"- Kazanım: {it['kazanim']} → {it['n']} soru (zorluk etiketleri: {', '.join(it['labels'])})")
    av = ("\nTekrar etme:\n- " + "\n- ".join(avoid[-12:])) if avoid else ""
    geo_on = subject == "Matematik" and bool(_GEO_PLAN_RX.search(" ".join(str(it.get("kazanim", "")) for it in items)))
    eff, lvl = bump_difficulty(difficulty)
    return (
        f"MEB Ortak Yazılı Sınav Sistemi (OYSS) için {grade_label} {subject} dersi yazılı sınavı soruları hazırla. "
        "Sorular AÇIK UÇLU ve KISA CEVAPLI olacak (çoktan seçmeli DEĞİL); yaklaşık 1/3'ü kısa cevaplı, kalanı açık uçlu. "
        "Her soru tek bir kazanımı ölçsün, beceri temelli ve bağlamlı olsun; öğrencinin yazarak cevaplayacağı şekilde kurgulansın.\n"
        f"DAĞILIM (kazanım başına tam soru sayısı):\n" + "\n".join(lines) + "\n"
        f"KALİTE KADEMESİ: '{eff}'. Etiket (Kolay/Orta/Zor) ile birlikte bu kademeye uy → {DIFF_SPEC.get(lvl, '')}\n"
        "Yazılı soru tarzı: bağlamlı/veri içeren, en az iki adımlı muhakeme ya da yorum gerektiren; doğrudan tanım ve tek işlemli sorular YOK. "
        "Soru ve verilen veriler kendi içinde TUTARLI, beklenen cevap gerçekten doğru ve rubric adımlarıyla uyumlu olsun (kendin çözerek doğrula).\n"
        f"DERS YÖNERGESİ: {SUBJECT_HINT.get(subject, '')}\nÇeşitlilik tohumu: {nonce}.{av}\n{_subject_lock(subject, ' '.join(str(it.get('kazanim', '')) for it in items))}\n{shape_rules(subject, geo_on)}{GEO_STYLE if geo_on else ''}\n"
        "Her soru için: beklenen 'answer', ve puanlama anahtarı 'rubric' (adımlar ve göreli puanlar; toplam 10 olsun).\n"
        'ÇIKTI SADECE şu JSON: {"questions":[{"kazanim":"..","type":"Açık uçlu|Kısa cevaplı","difficulty":"Kolay|Orta|Zor",'
        '"passage":"... veya null","question":"..","shape":null,"answer":"..","rubric":[{"step":"..","points":5},{"step":"..","points":5}]}]}')


# ---------------------------------------------------------------- doğrulama
_NOSHUF = re.compile(r"hepsi|yukarıdakilerin|yalnız|yalnızca|ve [IV]+|[IV]+ ve|I, II|hiçbiri|all of|none of|beide|alle", re.I)


_ANG1 = re.compile(r"∠\s*([A-ZÇĞİÖŞÜ]{1,3})(?=\s*(?:=|<|>|≠|kaç))")
_MPAR = re.compile(r"m\s*\(\s*(?:∠\s*)?([A-ZÇĞİÖŞÜ]{1,3})\s*\)")
_SIDE_EQ = re.compile(r"(?<![\w|(\[])([A-Z]{2})\s*=\s*([A-Z]{2})(?![\w|)\]])")
_SIDE_LEN = re.compile(r"(?<![\w|(\[])([A-Z]{2})\s*=\s*(?=\d)")


def _angle3(v, L):
    """Köşe harfi -> 3 harfli açı adı (tepe ortada): A->BAC, B->ABC, C->ACB."""
    if L and len(L) == 3 and v in L:
        n = [x for x in L if x != v]
        return f"{n[0]}{v}{n[1]}"
    if L and len(L) == 4 and v in L:  # dörtgen: komşu köşeler (D-A-B, A-B-C, B-C-D, C-D-A)
        i = L.index(v)
        return f"{L[(i - 1) % 4]}{v}{L[(i + 1) % 4]}"
    return None


def _fix_geo_notation(t, L=None):
    """MEB gösterimi: m(ABC) = 40°, |AB| = |AC|, |AB| = 5 cm  ('∠B =', 'AB = AC', 'm(A)' yerine)."""
    if not t:
        return t
    t = str(t)

    def ang(m):
        v = m.group(1)
        if len(v) == 3:
            return f"m({v})"
        a3 = _angle3(v, L)
        return f"m({a3})" if a3 else f"m(∠{v})"
    t = _MPAR.sub(lambda m: ang(m) if len(m.group(1)) < 3 else f"m({m.group(1)})", t)
    t = _ANG1.sub(ang, t)
    t = _SIDE_EQ.sub(lambda m: f"|{m.group(1)}| = |{m.group(2)}|", t)
    t = _SIDE_LEN.sub(lambda m: f"|{m.group(1)}| = ", t)
    return t


_NAME_RX = re.compile(r"\b([A-ZÇĞİÖŞÜ]{3,8})\s+(?:üçgen|dörtgen|beşgen|altıgen|yedigen|sekizgen|çokgen|yamuk|paralelkenar|dikdörtgen|kare|eşkenar\s+dörtgen|deltoid)")
_QUAD_KW = [(r"ikizkenar\s+yamuk", "isosceles_trapezoid"), (r"eşkenar\s+dörtgen", "rhombus"), (r"dikdörtgen", "rectangle"),
            (r"paralelkenar", "parallelogram"), (r"deltoid", "kite"), (r"yamuk", "trapezoid"),
            (r"\bkare\b|\bkaresi\w*|\bkarenin\b|[A-Z]{4}\s+kare", "square")]
_PAR_RX = re.compile(r"[\[|]?([A-Z]{2})[\]|]?\s*(?:∥|//)\s*[\[|]?([A-Z]{2})[\]|]?")


def _geo_kind_fix(sh, text, n, has_eq):
    """Şekil, metinde ADI/KANITI olmayan özel tür (ikizkenar, eşkenar, dik, dikdörtgen…) göstermesin."""
    k = str(sh.get("kind", "")).lower()
    if n == 3:
        ev_iso = bool(re.search(r"ikizkenar", text, re.I)) or has_eq
        ev_eq = bool(re.search(r"eşkenar", text, re.I))
        ev_r = bool(re.search(r"dik\s+üçgen|⊥|=\s*90\s*°|köşesinde\s+dik|açısı\s+dik", text, re.I))
        if (k in ("isosceles", "ikizkenar") and not ev_iso) or (k in ("equilateral", "eşkenar") and not ev_eq) or (k in ("right", "dik") and not ev_r):
            sh["kind"], sh["ticks"] = "scalene", False
            sh.pop("apex", None)
            sh.pop("right_at", None)
        if str(sh.get("kind", "")).lower() in ("isosceles", "ikizkenar") and not sh.get("apex"):
            sh["ticks"] = False  # hangi kenarların eşit olduğu metinde yok -> işaretleme
    else:
        if not any(re.search(rx, text, re.I) for rx, _ in _QUAD_KW) and not has_eq:
            sh["kind"] = "general"
            sh["ticks"] = False
    return sh


def _geo_labels(shape, text=""):
    """Üçgen/dörtgen köşe harfleri: önce metindeki ad ('ABCD dörtgeninde'), sonra şemadaki etiketler, sonra A, B, C…"""
    sub = str(shape.get("sub_type", "")).lower() if isinstance(shape, dict) and shape.get("type") == "geo" else ""
    n = 3 if sub == "triangle" else 4 if sub == "quad" else 0
    if not n:
        if re.search(r"üçgen", text, re.I):
            n = 3
        elif re.search(r"dörtgen|\bkare|yamuk|paralelkenar|deltoid", text, re.I):
            n = 4
    if not n:
        return None
    nm = _NAME_RX.search(text)
    if nm and len(nm.group(1)) == n:
        return list(nm.group(1))
    L = [str(x) for x in ((shape or {}).get("labels") or [])][:n] if sub else []
    return (L + list("ABCD")[len(L):])[:n]


_VAL = r"([0-9xy+\-−–()\s.]+°)"


def _sync_geo_shape(shape, text):
    """Metinde verilen ad, tür, eşit kenar, açı ve uzunlukları ŞEKİLDE de gösterir (şema metinle BİREBİR uyumlu olsun)."""
    if not isinstance(shape, dict) or shape.get("type") != "geo":
        return shape
    sub = str(shape.get("sub_type", "")).lower()
    if sub not in ("triangle", "quad", "polygon"):
        return shape
    sh = dict(shape)
    nm = _NAME_RX.search(text)
    if sub == "polygon":
        try:
            ns = int(sh.get("sides") or 0)
        except Exception:
            ns = 0
        if nm and len(nm.group(1)) == ns:
            sh["labels"] = list(nm.group(1))
        return sh
    n = 3 if sub == "triangle" else 4
    if nm and len(nm.group(1)) == n:
        sh["labels"] = list(nm.group(1))
    if sub == "triangle" and re.search(r"eşkenar\s+üçgen", text, re.I):
        sh["kind"], sh["ticks"] = "equilateral", True  # üç kenar da eşit işaretlenir
    if sub == "quad":
        if nm and nm.group(1) and re.search(re.escape(nm.group(1)) + r"\s+kare", text):
            sh["kind"] = "square"
        else:
            for rx, k in _QUAD_KW:
                if re.search(rx, text, re.I):
                    sh["kind"] = k
                    break
    default = list("ABCD")[:n]
    L = [str(x) for x in (sh.get("labels") or [])][:n]
    L = (L + default[len(L):])[:n]
    if sub == "quad" and str(sh.get("kind", "")).lower() in ("trapezoid", "yamuk", "isosceles_trapezoid"):
        pr_ = _PAR_RX.findall(text)
        if pr_:
            a_, b_ = pr_[0]
            if all(x in L for x in a_ + b_):
                ia = sorted(L.index(x) for x in a_)
                if ia in ([1, 2], [0, 3]):
                    L = L[1:] + L[:1]  # paralel kenarlar şekilde alt/üst (AB, DC) olacak biçimde köşe sırasını döndür
    eq = re.findall(r"\|([A-Z]{2})\|\s*=\s*\|([A-Z]{2})\|", text)
    lens = re.findall(r"\|([A-Z]{2})\|\s*=\s*(\d[\d.,]*\s*(?:cm|mm|m|birim)?)", text)
    angs = re.findall(r"m\(([A-Z]{3})\)\s*=\s*" + _VAL, text)
    ask = re.findall(r"m\(([A-Z]{3})\)\s*(?:kaç|=\s*\?)", text)
    lens_any = re.findall(r"\|([A-Z]{2})\|\s*=\s*(?!\|)(?=[0-9xy(+\-−])", text)
    used = set("".join(x for pr in eq for x in pr) + "".join(a for a, _ in lens) + "".join(a for a, _ in angs) + "".join(ask) + "".join(lens_any))
    perim = re.search(r"çevre\w*\s+(?:uzunluğ\w*\s+)?(?:kaç|nedir|hesapla|bul)", text, re.I)
    if not used:
        sh["labels"] = L
        if perim and sub in ("triangle", "quad"):
            sh["_bad"] = True  # çevre soruluyor ama hiç kenar verisi yok
        return _geo_kind_fix(sh, text, n, False)
    if not used <= set(L):
        if used <= set(default):
            L = default
        elif len(used) == n:
            L = sorted(used)
        else:
            return sh
    sh["labels"] = L
    pos = {ch: i for i, ch in enumerate(L)}
    P = "ABCD"
    pk = lambda pair: "".join(sorted(P[pos[x]] for x in pair))

    def nb_ok(abc):  # m(XYZ): X ve Z, Y köşesinin komşusu olmalı (yoksa alt açıdır, şekilde gösterilemez)
        if abc[1] not in pos:
            return False
        i = pos[abc[1]]
        return {abc[0], abc[2]} == {L[(i - 1) % n], L[(i + 1) % n]}
    if lens:
        sh["sides"] = {pk(pr): v.strip() for pr, v in lens if all(x in pos for x in pr)}
        if any(not all(x in pos for x in pr) for pr, _ in lens):
            sh["_bad"] = True  # metinde verilen uzunluk şekildeki köşelere ait değil
    rv = None
    if angs or ask:
        d = {}
        for abc, v in angs:
            if nb_ok(abc):
                d[P[pos[abc[1]]]] = v.strip()
                if n == 3 and re.fullmatch(r"\s*90\s*°", v):
                    rv = abc[1]
            # alt açı / başka noktaya ait açı: şekilde gösterilemez; soruyu eleme, yalnızca şemaya işleme
        for abc in ask:
            if nb_ok(abc):
                d.setdefault(P[pos[abc[1]]], "?")
        sh["angles"] = d
    if n == 3:
        for a_, b_ in re.findall(r"\|?([A-Z]{2})\|?\s*⊥\s*\|?([A-Z]{2})\|?", text):
            cm = set(a_) & set(b_)
            if len(cm) == 1 and list(cm)[0] in pos:
                rv = list(cm)[0]
        for m_ in re.finditer(r"\b([A-Z])\s+(?:köşesinde|açısı)\s+dik", text):
            if m_.group(1) in pos:
                rv = m_.group(1)
        if rv in pos:
            sh["kind"], sh["right_at"] = "right", P[pos[rv]]
        elif re.search(r"dik\s+üçgen", text, re.I):
            sh["kind"] = "right"
            sh["right_at"] = str(sh.get("right_at") or "A").upper()[:1] if str(sh.get("right_at") or "A").upper()[:1] in "ABC" else "A"
            sh["_rnote"] = L["ABC".index(sh["right_at"])]  # dik açının köşesi metinde yok -> metne eklenecek
    if perim and sub in ("triangle", "quad"):  # çevre için GEREKLİ tüm uzunluklar verilmiş mi?
        sides_ = ["AB", "BC", "AC"] if n == 3 else ["AB", "BC", "CD", "AD"]
        par = {x: x for x in sides_}

        def fd(x):
            while par[x] != x:
                x = par[x]
            return x

        def un(*xs):
            for x in xs[1:]:
                par[fd(x)] = fd(xs[0])
        k_ = str(sh.get("kind", "")).lower()
        if n == 3 and k_ in ("equilateral", "eşkenar"):
            un("AB", "BC", "AC")
        elif n == 4:
            if k_ in ("square", "kare", "rhombus", "eşkenar dörtgen"):
                un("AB", "BC", "CD", "AD")
            elif k_ in ("rectangle", "dikdörtgen", "parallelogram", "paralelkenar"):
                un("AB", "CD"); un("BC", "AD")
            elif k_ in ("isosceles_trapezoid", "ikizkenar yamuk"):
                un("BC", "AD")
            elif k_ in ("kite", "deltoid"):
                un("AB", "AD"); un("BC", "CD")
        for pr in eq:
            if all(x in pos for x in pr[0] + pr[1]) and pk(pr[0]) in par and pk(pr[1]) in par:
                un(pk(pr[0]), pk(pr[1]))
        given = {fd(pk(a)) for a in lens_any if all(x in pos for x in a) and pk(a) in par}
        classes = {fd(x) for x in sides_}
        need = len(classes) - (1 if (n == 3 and k_ in ("right", "dik")) else 0)  # dik üçgende Pisagor ile üçüncü kenar bulunur
        if len(given & classes) < need:
            sh["_bad"] = True
    if eq and str(sh.get("kind", "")).lower() not in ("right", "dik"):
        if n == 3:
            E = {pk(x) for pr in eq for x in (pr[0], pr[1])}
            if len(E) >= 3:
                sh["kind"], sh["ticks"] = "equilateral", True
            elif len(E) == 2:
                (a_, b_) = list(E)
                common = set(a_) & set(b_)
                if common:
                    sh["kind"], sh["apex"], sh["ticks"] = "isosceles", common.pop(), True  # eşit kenarların ortak köşesi
        else:
            groups = []
            for pr in eq:
                g = {pk(pr[0]), pk(pr[1])}
                for old in [x for x in groups if x & g]:
                    g |= old
                    groups.remove(old)
                groups.append(g)
            sh["equal_groups"], sh["ticks"] = [sorted(g) for g in groups], True
    return _geo_kind_fix(sh, text, n, bool(eq))


def _nums(t):
    return [float(x.replace(",", ".")) for x in re.findall(r"\d+(?:[.,]\d+)?", str(t).replace("−", "-").replace("–", "-"))]


def _expl_consistent(expl, opts, ans):
    """Çözüm metni, işaretli doğru şıkla çelişiyor mu? (çözümde başka bir şık harfi ya da başka bir şıkkın değeri sonuç olarak çıkıyorsa elenir)"""
    if not expl or ans not in opts:
        return True
    m = re.search(r"doğru\s+(?:cevap|yanıt|şık)\w*\s*[:\-]?\s*\(?\b([A-D])\b\)?", expl, re.I)
    if m and m.group(1).upper() != ans:
        return False
    m = re.search(r"\b([A-D])\)?\s+şıkkı\s+doğru", expl)
    if m and m.group(1) != ans:
        return False
    corr = _optnum(opts[ans])
    ns = _nums(expl)
    if corr is None or not ns or corr != int(corr):
        return True
    if abs(corr) not in [abs(x) for x in ns]:
        return False  # çözümde işaretlenen sonuca hiç ulaşılmıyor
    tail = ns[-2:]
    if abs(corr) not in [abs(x) for x in tail]:
        others = {abs(_optnum(v)) for k, v in opts.items() if k != ans and _optnum(v) is not None}
        if abs(ns[-1]) in others:
            return False  # çözüm başka bir şıkkın değeriyle bitiyor
    return True


_BAD_C = {"t": 0, "v": frozenset()}


def _is_bad(stem):
    if time.time() - _BAD_C["t"] > 5:
        try:
            from . import store
            _BAD_C["v"] = frozenset(store.bad_stems())
        except Exception:
            pass
        _BAD_C["t"] = time.time()
    return stem in _BAD_C["v"]


def _circle_ok(shape, text):
    """Daire şeması: metindeki yarıçap/çap değeri şekildeki yarıçapla çelişmesin."""
    if not isinstance(shape, dict) or shape.get("type") != "circle":
        return True
    r = _num_len(shape.get("radius", ""))
    if r is None:
        return True
    for m in re.finditer(r"yarıçap\w*[^.\d]{0,30}?(\d+(?:[.,]\d+)?)\s*(?:cm|birim)", text, re.I):
        if abs(float(m.group(1).replace(",", ".")) - r) > 1e-6:
            return False
    for m in re.finditer(r"çap\w*[^.\d]{0,30}?(\d+(?:[.,]\d+)?)\s*(?:cm|birim)", text, re.I):
        if abs(float(m.group(1).replace(",", ".")) / 2 - r) > 1e-6 and "yarıçap" not in text[max(0, m.start() - 4):m.end()].lower():
            return False
    return True


def _quota_like(e):
    return bool(e) and bool(re.search(r"429|rate.?limit|quota|kota|resource_exhausted|too many|tokens per|try again in|limit", str(e), re.I))


def _optnum(t):
    t = re.sub(r"cm²|cm2|cm|birim²|birim|br|°|\s|\^2", "", str(t)).replace(",", ".")
    return float(t) if re.fullmatch(r"-?\d+(?:\.\d+)?", t) else None


def _lin(v):
    """'3x + 5°' -> (3, 5);  '70°' -> (0, 70);  '?' / karmaşık -> None"""
    from fractions import Fraction
    t = str(v).replace("°", "").replace("−", "-").replace("–", "-").replace(" ", "").replace(",", ".")
    if not t or t == "?":
        return None
    toks = re.findall(r"[+-]?\d*\.?\d*x|[+-]?\d+\.?\d*", t)
    if "".join(toks) != t.lstrip("+") and "".join(toks) != t:
        return None
    a = b = Fraction(0)
    for k in toks:
        if k.endswith("x"):
            c = k[:-1]
            a += Fraction(-1 if c == "-" else 1 if c in ("", "+") else c)
        else:
            b += Fraction(k)
    return a, b


def _geo_consistent(shape, text, opts, ans):
    """Üçgen/dörtgen: açı ve uzunluk verileri kendi içinde TUTARLI mı, sorulan değer işaretli doğru şıkla uyuşuyor mu?
    Yanlış cevap anahtarlı ya da imkânsız (örn. iç açılar toplamı tutmayan) soruları eler."""
    from fractions import Fraction
    if not isinstance(shape, dict) or shape.get("type") != "geo" or shape.get("sub_type") not in ("triangle", "quad"):
        return True
    n = 3 if shape["sub_type"] == "triangle" else 4
    kind = str(shape.get("kind", "")).lower()
    names = "ABCD"[:n]
    ang = {str(k).upper(): v for k, v in (shape.get("angles") or {}).items() if str(k).upper() in names}
    V = {}
    for k, v in ang.items():
        if str(v).strip() == "?":
            V[k] = (Fraction(0), Fraction(1), Fraction(0))  # sorulan açı: y
        else:
            ab = _lin(v)
            if ab is None:
                return True  # çözemediğimiz ifade: kontrol dışı bırak
            V[k] = (ab[0], Fraction(0), ab[1])
    nxt = lambda c: names[(names.index(c) + 1) % n]
    prv = lambda c: names[(names.index(c) - 1) % n]
    cons = []
    sub = lambda a, b: (a[0] - b[0], a[1] - b[1], a[2] - b[2])
    add = lambda *xs: tuple(sum(x[i] for x in xs) for i in range(3))
    const = lambda c: (Fraction(0), Fraction(0), Fraction(c))
    same = lambda a, b: V.__setitem__(b, V[a]) if (a in V and b not in V) else (V.__setitem__(a, V[b]) if (b in V and a not in V) else (cons.append(sub(V[a], V[b])) if (a in V and b in V) else None))
    sumc = lambda a, b, tot: cons.append(sub(add(V[a], V[b]), const(tot))) if (a in V and b in V) else None
    if n == 3:
        if kind in ("equilateral", "eşkenar"):
            for c in names:
                if c in V:
                    cons.append(sub(V[c], const(60)))
                else:
                    V[c] = const(60)
        elif kind in ("right", "dik"):
            r = str(shape.get("right_at", "A")).upper()[:1]
            if r in V:
                cons.append(sub(V[r], const(90)))
            else:
                V[r] = const(90)
        elif kind in ("isosceles", "ikizkenar") and str(shape.get("apex", "")).upper() in names:
            ap = str(shape.get("apex")).upper()
            same(nxt(ap), prv(ap))
        if all(c in V for c in names):
            cons.append(sub(add(*[V[c] for c in names]), const(180)))
    else:
        if kind in ("square", "kare", "rectangle", "dikdörtgen"):
            for c in names:
                if c in V:
                    cons.append(sub(V[c], const(90)))
                else:
                    V[c] = const(90)
        elif kind in ("parallelogram", "paralelkenar", "rhombus", "eşkenar dörtgen"):
            same("A", "C"); same("B", "D"); sumc("A", "B", 180)
        elif kind in ("isosceles_trapezoid", "ikizkenar yamuk"):
            same("A", "B"); same("C", "D"); sumc("A", "D", 180); sumc("B", "C", 180)
        elif kind in ("trapezoid", "yamuk"):
            sumc("A", "D", 180); sumc("B", "C", 180)
        elif kind in ("kite", "deltoid"):
            same("B", "D")
        if all(c in V for c in names):
            cons.append(sub(add(*[V[c] for c in names]), const(360)))
    # ---- x, y için doğrusal sistem
    sol = {}
    eqs = [e for e in cons if e[0] != 0 or e[1] != 0 or e[2] != 0]
    for e in eqs:
        if e[0] == 0 and e[1] == 0:
            return False  # sabit eşitlik tutmuyor (örn. açılar toplamı ≠ 180°)
    pure_x = [e for e in eqs if e[1] == 0 and e[0] != 0]
    if pure_x:
        x = -pure_x[0][2] / pure_x[0][0]
        if any(e[0] * x + e[2] != 0 for e in pure_x):
            return False
        sol["x"] = x
    mixed = [e for e in eqs if e[1] != 0]
    if "x" not in sol and len(mixed) >= 2:
        e1, e2 = mixed[0], mixed[1]
        det = e1[0] * e2[1] - e2[0] * e1[1]
        if det != 0:
            sol["x"] = (-e1[2] * e2[1] + e2[2] * e1[1]) / det
    if "x" in sol:
        for e in mixed:
            yv = -(e[0] * sol["x"] + e[2]) / e[1]
            if "y" in sol and sol["y"] != yv:
                return False
            sol["y"] = yv
    elif mixed and all(e[0] == 0 for e in mixed):
        ys = {-e[2] / e[1] for e in mixed}
        if len(ys) > 1:
            return False
        sol["y"] = ys.pop()
    xv, yv = sol.get("x"), sol.get("y")
    if xv is not None and xv <= 0:
        return False
    for c, (ax, ay, cc) in V.items():
        if (ay != 0 and yv is None) or (ax != 0 and xv is None):
            continue
        val = ax * (xv or 0) + ay * (yv or 0) + cc
        if val <= 0 or val >= 180:
            return False
    # ---- sorulan değer, işaretli şıkla uyuşuyor mu?
    cv = _optnum(opts.get(ans, ""))
    qt = str(text)
    if cv is not None:
        if yv is not None and re.search(r"m\([A-Z]{3}\)\s*(?:kaç|=\s*\?)", qt) and sum(1 for v in ang.values() if str(v).strip() == "?") == 1 \
                and not re.search(r"çevre|alan|toplam|fark|oran|çarp", qt, re.I):
            if abs(float(yv) - cv) > 1e-6:
                return False
        if xv is not None and re.search(r"\bx(?:'in)?\s+(?:değeri\s+)?kaç|x\s+değeri|x\s+kaçtır", qt) and not re.search(r"çevre|alan|toplam|fark|oran|çarp", qt, re.I):
            if abs(float(xv) - cv) > 1e-6:
                return False
    # ---- uzunluklar
    S = {"".join(sorted(str(k).upper())): _num_len(v) for k, v in (shape.get("sides") or {}).items()}
    S = {k: v for k, v in S.items() if v is not None}
    names_s = ["AB", "BC", "AC"] if n == 3 else ["AB", "BC", "CD", "AD"]
    par = {x: x for x in names_s}

    def fd(x):
        while par[x] != x:
            x = par[x]
        return x

    def un(*xs):
        for x in xs[1:]:
            par[fd(x)] = fd(xs[0])
    if n == 3:
        if kind in ("equilateral", "eşkenar"):
            un("AB", "BC", "AC")
        elif kind in ("isosceles", "ikizkenar") and str(shape.get("apex", "")).upper() in names:
            ap = str(shape.get("apex")).upper()
            un(*["".join(sorted(ap + o)) for o in names if o != ap])
    else:
        if kind in ("square", "kare", "rhombus", "eşkenar dörtgen"):
            un("AB", "BC", "CD", "AD")
        elif kind in ("rectangle", "dikdörtgen", "parallelogram", "paralelkenar"):
            un("AB", "CD"); un("BC", "AD")
        elif kind in ("isosceles_trapezoid", "ikizkenar yamuk"):
            un("BC", "AD")
        elif kind in ("kite", "deltoid"):
            un("AB", "AD"); un("BC", "CD")
        for g in shape.get("equal_groups") or []:
            ks = ["".join(sorted(str(x).upper())) for x in g]
            ks = [k for k in ks if k in par]
            if len(ks) > 1:
                un(*ks)
    val = {}
    for k, v in S.items():
        if k in par:
            r = fd(k)
            if r in val and abs(val[r] - v) > 1e-6:
                return False  # eşit olduğu söylenen kenarlara farklı uzunluk verilmiş
            val[r] = v
    full = {k: val.get(fd(k)) for k in names_s}
    if n == 3:
        if kind in ("right", "dik"):
            r = str(shape.get("right_at", "A")).upper()[:1]
            hyp = "".join(sorted(c for c in names if c != r))
            legs = [k for k in names_s if k != hyp]
            if full[hyp] is None and all(full[l] is not None for l in legs):
                full[hyp] = (full[legs[0]] ** 2 + full[legs[1]] ** 2) ** .5
            elif full[hyp] is not None:
                for i, l in enumerate(legs):
                    o = legs[1 - i]
                    if full[l] is None and full[o] is not None:
                        if full[hyp] <= full[o]:
                            return False
                        full[l] = (full[hyp] ** 2 - full[o] ** 2) ** .5
            if all(full[k] is not None for k in names_s) and abs(full[legs[0]] ** 2 + full[legs[1]] ** 2 - full[hyp] ** 2) > 1e-6 * max(1, full[hyp] ** 2):
                return False
        if all(full[k] is not None for k in names_s):
            a_, b_, c_ = sorted(full.values())
            if a_ + b_ <= c_ + 1e-9:
                return False  # üçgen eşitsizliği sağlanmıyor
    if cv is not None and all(full[k] is not None for k in names_s):
        tot = sum(full.values())
        if re.search(r"çevre\w*\s+(?:uzunluğ\w*\s+)?(?:kaç|nedir|hesapla|bul)", qt, re.I) and abs(tot - cv) > 1e-6:
            return False
        if kind in ("rectangle", "dikdörtgen") and re.search(r"alan\w*\s+(?:kaç|nedir|hesapla|bul)", qt, re.I) and abs(full["AB"] * full["BC"] - cv) > 1e-6:
            return False
        if kind in ("square", "kare") and re.search(r"alan\w*\s+(?:kaç|nedir|hesapla|bul)", qt, re.I) and abs(full["AB"] ** 2 - cv) > 1e-6:
            return False
    if cv is not None and n == 3 and kind in ("right", "dik") and all(full[k] is not None for k in names_s) and re.search(r"alan\w*\s+(?:kaç|nedir|hesapla|bul)", qt, re.I):
        r = str(shape.get("right_at", "A")).upper()[:1]
        hyp = "".join(sorted(c for c in names if c != r))
        l1, l2 = [full[k] for k in names_s if k != hyp]
        if abs(l1 * l2 / 2 - cv) > 1e-6:
            return False
    return True


def _num_len(v):
    m = re.match(r"\s*(\d+(?:[.,]\d+)?)\s*(?:cm|mm|m|birim|br)?\s*$", str(v))
    return float(m.group(1).replace(",", ".")) if m else None


_ANGLE_ASSIGN = re.compile(r"m\s*\(\s*[A-ZÇĞİÖŞÜ∠^\s]{1,5}\s*\)\s*=\s*\d+\s*°?")
_GEO_COMPLEX = re.compile(r"(?<![A-Za-zÇĞİÖŞÜçğıöşü])[xy](?![A-Za-zÇĞİÖŞÜçğıöşü])|[∥⊥]|ikizkenar|eşkenar|dış açı|dik üçgen|açıortay|yükseklik|kenarortay|çevre|\balan|pisagor|benzer|\|[A-Z]{2}\||paralel|çember|yamuk|paralelkenar|yargı", re.I)
_GEO_ROMAN = re.compile(r"\bI{1,3}\b")


def _trivial_geo(text):
    """İki açısı verilip üçüncüsü sorulan türden, tek adımlı basit üçgen sorusu."""
    t = str(text)
    if "üçgen" in t.lower() and len(_ANGLE_ASSIGN.findall(t)) >= 2 and not _GEO_COMPLEX.search(re.sub(_ANGLE_ASSIGN, "", t)) and not _GEO_ROMAN.search(t):
        return True
    return bool(re.search(r"(iki|2)\s+açısı.*(üçüncü|diğer)\s+açı", t, re.I))


def _norm_q(q, subject):
    if not isinstance(q, dict):
        return None
    opts = q.get("options")
    if isinstance(opts, list) and len(opts) == 4:
        opts = dict(zip("ABCD", opts))
    if not isinstance(opts, dict) or len(opts) < 4 or not str(q.get("question", "")).strip():
        return None
    opts = {k.strip().upper()[:1]: str(v) for k, v in opts.items()}
    if sorted(opts) != ["A", "B", "C", "D"]:
        return None
    ans = str(q.get("answer", "")).strip().upper()[:1]
    if ans not in opts:
        return None
    if len({_alnum(v) for v in opts.values()}) < 4:
        return None  # aynı şık iki kez geçiyor -> birden çok doğru olabilir
    _nv = [_optnum(v) for v in opts.values()]
    if all(x is not None for x in _nv) and len(set(_nv)) == 4:  # sayısal şıklar LGS'deki gibi küçükten büyüğe sıralı
        _correct = opts[ans]
        opts = dict(zip("ABCD", [v for _k, v in sorted(opts.items(), key=lambda kv: _optnum(kv[1]))]))
        ans = [k for k, v in opts.items() if v == _correct][0]
    elif not any(_NOSHUF.search(v) for v in opts.values()):  # şık konumu dengesi: doğru cevap dağılımı
        vals = list(opts.values())
        correct = opts[ans]
        random.shuffle(vals)
        opts = dict(zip("ABCD", vals))
        ans = [k for k, v in opts.items() if v == correct][0]
    from . import visuals
    shape = visuals.normalize_shape(q.get("shape"))
    if shape and shape.get("type") not in ALLOWED_SHAPES.get(subject, {"table"}):
        shape = None
    shape, bad = coherent_shape(shape, f"{q.get('topic', '')} {q.get('question', '')} {q.get('passage', '')}")
    if not shape and re.search(_FIG, str(q.get("question", ""))) and not str(q.get("passage") or "").count("|"):
        return None  # görsele atıf var ama uygun görsel yok -> soruyu ele
    fr = FOREIGN.get(subject)
    if fr and fr.search(str(q.get("question", "")) + " " + str(q.get("passage", ""))):
        return None
    pas = q.get("passage") if str(q.get("passage")).lower() not in ("none", "null", "") else ""
    qtext, expl = str(q["question"]).strip(), str(q.get("explanation") or "")
    if subject == "Matematik" and (_is_geo_q(q, shape, subject) or (isinstance(shape, dict) and shape.get("type") == "geo") or "∠" in qtext):
        L3 = _geo_labels(shape, f"{qtext} {pas}")
        qtext, pas, expl = _fix_geo_notation(qtext, L3), _fix_geo_notation(pas, L3), _fix_geo_notation(expl, L3)
        opts = {k: _fix_geo_notation(v, L3) for k, v in opts.items()}
        shape = _sync_geo_shape(shape, f"{qtext} {pas}")
        if isinstance(shape, dict) and shape.get("_bad"):
            return None  # çevre için eksik veri ya da metindeki veri şekle işlenemiyor -> soruyu ele
        try:
            if not _geo_consistent(shape, f"{qtext} {pas}", opts, ans):
                return None  # veriler kendi içinde çelişiyor / işaretli cevap hesapla uyuşmuyor
        except Exception:
            pass
        if isinstance(shape, dict) and shape.get("_rnote"):
            shape = dict(shape)
            pas = (f"{pas} Dik açı {shape.pop('_rnote')} köşesindedir.").strip()
        if isinstance(shape, dict) and shape.get("type") == "geo":  # şekildeki ölçü doğru şıkkı ele vermesin
            corr = re.sub(r"[\s°]|cm|birim", "", opts[ans]).lower()
            for dct in (shape.get("angles"), shape.get("sides")):
                for v in (dct or {}).values():
                    if corr and str(v) != "?" and re.sub(r"[\s°]|cm|birim", "", str(v)).lower() == corr:
                        return None
    if subject in ("Matematik", "Fen Bilimleri") and not _expl_consistent(expl, opts, ans):
        return None  # çözüm ile işaretli cevap tutmuyor
    if not _circle_ok(shape, f"{qtext} {pas}"):
        return None  # metindeki yarıçap/çap şekille çelişiyor
    if _is_bad(re.sub(r"\W+", " ", qtext.lower())[:70].strip()):
        return None  # kullanıcı bu soruyu hatalı diye bildirmişti
    if _is_geo_q(q, shape, subject):  # geometri: şekil ZORUNLU, metin KISA, hikâye/tarih/gök cismi bağlamı YOK
        if not shape:
            return None
        if len(str(q.get("question", "")).split()) > 60 or len(str(pas or "").split()) > 20:
            return None
        if _trivial_geo(f"{qtext} {pas}"):
            return None
        if _GEO_BAN.search(f"{q.get('question', '')} {pas} {' '.join(opts.values())}"):
            return None
    out = {"subject": subject, "topic": str(q.get("topic") or ""), "passage": pas,
           "question": qtext, "shape": shape, "options": opts, "answer": ans, "explanation": expl}
    return None if leaks_answer(out) else out


def _alnum(t):
    return re.sub(r"[\W_]+", " ", str(t).lower()).strip()


def _strings(o):
    if isinstance(o, dict):
        for k, v in o.items():
            if k not in ("type", "sub_type"):
                yield from _strings(v)
    elif isinstance(o, (list, tuple)):
        for v in o:
            yield from _strings(v)
    elif isinstance(o, str):
        yield o


def leaks_answer(q):
    """Doğru şıkkın metni görselde ya da soru/metin içinde aynen geçiyorsa True (cevap/ipucu sızıntısı)."""
    ans = _alnum(q["options"][q["answer"]])
    if len(ans) < 5:
        return False
    if q.get("shape"):
        hay = " | ".join(_alnum(x) for x in _strings(q["shape"]))
        if ans in hay:
            return True
    return len(ans) >= 9 and ans in _alnum(str(q.get("passage", "")) + " " + str(q.get("question", "")))


def _stem(q):
    return re.sub(r"\W+", " ", str(q.get("question", "")).lower())[:70].strip()


def _qwords(q):
    t = str(q.get("question", "")) + " " + str(q.get("passage", "")) + " " + " ".join(str(v) for v in (q.get("options") or {}).values())
    return {w for w in re.sub(r"[^\w\s]", " ", t.lower()).split() if len(w) > 2}


def _vsig(q):
    sh = q.get("shape")
    if not isinstance(sh, dict):
        return None
    d = {k: v for k, v in sh.items() if k not in ("title",)}
    return json.dumps(d, sort_keys=True, ensure_ascii=False)


def _vkind(q):
    sh = q.get("shape")
    return _kind(sh) if isinstance(sh, dict) else None


def accept_diverse(q, kept, n):
    """Aynı sette benzer soru/aynı görsel/aynı görsel türü yığılması varsa reddeder."""
    if demo_mode():
        return True
    w = _qwords(q)
    for k in kept:
        wk = _qwords(k)
        if w and wk and len(w & wk) / len(w | wk) > 0.75:
            return False
    sig, kind = _vsig(q), _vkind(q)
    if sig:
        if any(_vsig(k) == sig for k in kept):
            return False
        cap = max(3, -(-n * 3 // 5))  # tek tür en çok ~%60
        if sum(1 for k in kept if _vkind(k) == kind) >= cap:
            return False
    return True


# ---------------------------------------------------------------- demo (çevrimdışı test)
def _demo_mc(subject, n, topics):
    shapes = [None, {"type": "bar_chart", "labels": ["A", "B", "C"], "values": [random.randint(5, 30) for _ in range(3)], "title": "Veri"},
              {"type": "dynamometer", "value": random.randint(1, 9), "max_value": 10, "unit": "N"}, None,
              {"type": "science_space", "sub_type": "moon_phases", "title": "Ay'ın Evreleri"}]
    out = []
    for i in range(n):
        out.append({"subject": subject, "topic": topics.split(":")[0][:40], "passage": "Örnek bağlam metni %d." % random.randint(1, 999) if i % 2 == 0 else "",
                    "question": f"[{subject}] Örnek soru {uuid.uuid4().hex[:5]}: Hangisi doğrudur?", "shape": random.choice(shapes),
                    "options": {"A": "Seçenek 1", "B": "Seçenek 2", "C": "Seçenek 3", "D": "Seçenek 4"},
                    "answer": random.choice("ABCD"), "explanation": "Demo açıklama."})
    return out


# ---------------------------------------------------------------- üst düzey API
def bank_key_for(p, grade_label, difficulty):
    from . import store
    return store.bank_key(grade_label, p["subject"], difficulty, p.get("topics", ""))


def _bank_meta(p, grade_label, difficulty):
    return {"grade_label": grade_label, "subject": p["subject"], "difficulty": difficulty, "topics": str(p.get("topics", ""))[:120]}


def bank_counts(plan, grade_label, difficulty):
    """Plandaki her ders için bankada hazır soru sayısı."""
    from . import store
    return {p["subject"]: store.bank_count(bank_key_for(p, grade_label, difficulty)) for p in plan}


def _relaxed_ok(q, kept):
    """Gevşetilmiş çeşitlilik: yalnızca (neredeyse) birebir kopyayı reddeder."""
    w = _qwords(q)
    for k in kept:
        wk = _qwords(k)
        if w and wk and len(w & wk) / len(w | wk) > 0.9:
            return False
    return True


def generate_mc(plan, grade_label, difficulty, scope_label, avoid=None, focus="", on_progress=None, use_bank=True, deposit=True, keys=None, verify=False, count=True):
    """plan: [{subject, n, topics}] -> (questions, errors).
    Her ders BAĞIMSIZ ilerler (başka dersi beklemez): bankadan al -> paralel üret -> eksik kaldıkça yeniden tamamla
    (turlar ilerledikçe daha çok yedek ister, çeşitlilik kuralını gevşetir, en son görselsiz moda geçer).
    Amaç: istenen sayının TAM karşılanması."""
    avoid = {k: list(v) for k, v in (avoid or {}).items()}
    gk, mk = (keys if keys else load_keys()) if not demo_mode() else ([], [])
    no_keys = not demo_mode() and not gk and not mk and not extra_keys()
    bank_ok = use_bank and not demo_mode() and not focus.strip()
    dep_ok = deposit and not demo_mode() and not focus.strip()
    seen = set(s for v in avoid.values() for s in v)
    seen_lock = threading.Lock()
    prog_lock = threading.Lock()
    prog = {"done": 0, "total": max(1, sum(-(-p["n"] // CHUNK) for p in plan))}
    state = [{"p": p, "qs": [], "reserve": [], "over": [], "fails": 0, "err": None, "bank_stems": []} for p in plan]
    T0 = time.time()
    E = ThreadPoolExecutor(max_workers=WORKERS)

    def take(st_, batch, relax=False):
        p, qs_, res_ = st_["p"], st_["qs"], st_["reserve"]
        with seen_lock:
            for i, q in enumerate(batch):
                if len(qs_) >= p["n"]:
                    st_["over"].extend(batch[i:])  # fazlalık atılmaz, bankaya gider
                    break
                s = _stem(q)
                if not s:
                    continue
                if s in seen:
                    res_.append(q)
                elif (_relaxed_ok(q, qs_) if relax else accept_diverse(q, qs_, p["n"])):
                    seen.add(s)
                    qs_.append(q)
                else:
                    res_.append(q)

    def work_chunk(st_, c_ask, use_focus, extra_avoid, plain):
        p = st_["p"]
        subj, idx = p["subject"], next(_UID)
        try:
            if demo_mode():
                return _demo_mc(subj, c_ask, p["topics"]), None
            av = list(avoid.get(subj, [])) + list(extra_avoid)
            prompt = mc_prompt(grade_label, subj, c_ask, p["topics"], difficulty, scope_label, av, focus if use_focus else "", plain=plain)

            def validate(items):
                out = []
                for q in items:
                    try:
                        x = _norm_q(q, subj)
                    except Exception:  # tek bozuk soru tüm üretimi bozmasın
                        x = None
                    if x:
                        out.append(x)
                return out

            qs, err = _ask_questions(prompt, gk, mk, idx, validate, reasoning=GEN_REASONING.get(subj))
            if verify and qs and (not VERIFY_SUBJECTS or subj in VERIFY_SUBJECTS) and (gk or mk or extra_keys()):  # yalnız arka plan banka dolumunda
                try:
                    qs = verify_questions(qs, gk, mk, offset=idx)
                except Exception:  # doğrulayıcı hatası üretimi engellemesin
                    pass
            return qs, (err if not qs else None)
        except Exception as e:
            return [], f"{type(e).__name__}: {str(e)[:80]}"

    def run_item(st_):
        p = st_["p"]
        subj, n = p["subject"], p["n"]
        try:
            if bank_ok:  # 0) bankadan doldur
                try:
                    from . import store
                    key = bank_key_for(p, grade_label, difficulty)
                    fresh, purge = [], []
                    for q in store.bank_peek(key, n * 2 + 4):
                        s = _stem(q)
                        if not s or s in seen:  # daha önce çözülmüş: bankadan da temizle
                            purge.append(s)
                        else:
                            fresh.append(q)
                    take(st_, fresh)
                    st_["reserve"], st_["over"] = [], []  # elenenler bankada kalır
                    got = [_stem(q) for q in st_["qs"]]
                    store.bank_remove(key, got + purge)
                    st_["bank_stems"] = got
                except Exception:
                    pass  # banka hatası üretimi engellemesin
            for rnd in range(MAX_ROUNDS + 1):
                need = n - len(st_["qs"])
                if need <= 0 or (no_keys and not demo_mode()):
                    break
                if rnd > 0 and (time.time() - T0 > GEN_BUDGET or st_["fails"] >= 3):
                    break
                sizes, left = [], need
                while left > 0:
                    c = min(CHUNK, left)
                    sizes.append(c)
                    left -= c
                extra_av = [_stem(q) for q in st_["qs"]] + st_["bank_stems"]
                futs = [E.submit(work_chunk, st_, c + EXTRA_FIRST + min(rnd, 3), rnd == 0 and k == 0, extra_av, rnd >= 3) for k, c in enumerate(sizes)]
                before = len(st_["qs"])
                for f in futs:
                    qs, err = f.result()
                    if err:
                        st_["err"] = err
                    take(st_, qs, relax=rnd >= 2)
                    if on_progress:
                        with prog_lock:
                            prog["done"] += 1
                            on_progress(min(prog["done"], prog["total"]), prog["total"], subj)
                st_["fails"] = 0 if len(st_["qs"]) > before else st_["fails"] + 1
        except Exception as e:
            st_["err"] = f"{type(e).__name__}: {str(e)[:80]}"

    try:
        with ThreadPoolExecutor(max_workers=max(1, len(state))) as SX:
            list(SX.map(run_item, state))
    finally:
        E.shutdown(wait=False)
    if no_keys and not any(s_["qs"] for s_ in state):
        return [], ["API anahtarı bulunamadı"]
    errors, questions = [], []
    for st_ in state:
        p, qs_ = st_["p"], st_["qs"]
        if len(qs_) < p["n"] and st_["reserve"]:  # son çare: elenenlerden (tam kopya olmayanlar) tamamla
            have = [_qwords(q) for q in qs_]
            for q in st_["reserve"]:
                if len(qs_) >= p["n"]:
                    break
                w = _qwords(q)
                if any(h and w and len(h & w) / len(h | w) > 0.85 for h in have):
                    continue
                qs_.append(q)
                have.append(w)
        if len(qs_) < p["n"]:
            errors.append(f"{p['subject']}: {len(qs_)}/{p['n']} soru hazırlanabildi (yoğunluk nedeniyle); tekrar denersen tamamlanır" if _quota_like(st_.get("err")) else
                          f"{p['subject']}: {len(qs_)}/{p['n']} soru üretilebildi" + (f" ({st_['err'][:90]})" if st_.get("err") and not qs_ else ""))
        questions += qs_[:p["n"]]
    if dep_ok:  # artan sağlam soruları bankaya ekle
        try:
            from . import store
            for st_ in state:
                p = st_["p"]
                used = {_stem(q) for q in st_["qs"][:p["n"]]}
                extra = [q for q in st_["over"] + st_["reserve"] if _stem(q) and _stem(q) not in used and _stem(q) not in seen]
                if extra:
                    store.bank_put(bank_key_for(p, grade_label, difficulty), _bank_meta(p, grade_label, difficulty), extra)
        except Exception:
            pass
    for i, q in enumerate(questions, 1):
        q["id"] = i
    if count:
        try:
            store.count_generated(len(questions))
        except Exception:
            pass
    return questions, errors


_FILLING = set()
_FILL_LOCK = threading.Lock()


def bank_topup_async(plan, grade_label, difficulty, scope_label, used_qs=()):
    """Sınav üretildikten sonra arka planda, bu kapsamın bankasını bir sonraki sınav için tamamlar (en fazla bir sınav boyu).
    Ana iş parçacığında çağrılır; anahtarlar ve kaçınılacak soru listesi burada alınır, işi daemon iş parçacığı yapar."""
    if demo_mode() or not plan:
        return False
    try:
        from . import store
        gk, mk = load_keys()
        if not gk and not mk and not extra_keys():
            return False
        avoid = {k: list(v) for k, v in store.recent_stems().items()}
        for q in used_qs:
            avoid.setdefault(q.get("subject", "Genel"), []).append(_stem(q))
        todo = []
        for p in plan:
            key = bank_key_for(p, grade_label, difficulty)
            need = p["n"] - store.bank_count(key)
            with _FILL_LOCK:
                if need > 0 and key not in _FILLING:
                    _FILLING.add(key)
                    todo.append((key, {**p, "n": need}))
        if not todo:
            return False
    except Exception:
        return False

    def run():
        try:
            sub = [p for _, p in todo]
            qs, _e = generate_mc(sub, grade_label, difficulty, scope_label, avoid=avoid, use_bank=False, deposit=False, keys=(gk, mk), verify=True, count=False)
            for key, p in todo:
                mine = [q for q in qs if q.get("subject") == p["subject"]]
                store.bank_put(key, _bank_meta(p, grade_label, difficulty), mine)
        except Exception:
            pass
        finally:
            with _FILL_LOCK:
                for key, _p in todo:
                    _FILLING.discard(key)

    threading.Thread(target=run, daemon=True).start()
    return True


def fill_bank(plan, grade_label, difficulty, scope_label, avoid=None, on_progress=None):
    """Soruları KULLANMADAN üretip bankaya koyar (sonraki sınav anında açılsın). -> (eklenen, hatalar)"""
    if demo_mode():
        return 0, []
    from . import store
    qs, errs = generate_mc(plan, grade_label, difficulty, scope_label, avoid=avoid, on_progress=on_progress, use_bank=False, deposit=False, verify=True, count=False)
    added = 0
    for p in plan:
        mine = [q for q in qs if q.get("subject") == p["subject"]]
        added += store.bank_put(bank_key_for(p, grade_label, difficulty), _bank_meta(p, grade_label, difficulty), mine)
    return added, errs


def _valid_oyss(q):
    if not isinstance(q, dict):
        return False
    if len(str(q.get("question", "")).strip()) < 8 or not str(q.get("answer", "")).strip():
        return False
    rub = q.get("rubric")
    return isinstance(rub, list) and any(isinstance(r, dict) for r in rub)


def generate_oyss(subject_tables, grade_label, difficulty, avoid=None, on_progress=None):
    """subject_tables: [{subject, rows:[{code,topic,unit,n}]}] -> (questions, errors).
    Dersler paralel; her kazanım-soru 'yuvası' ayrı takip edilir, eksik yuvalar küçük gruplar hâlinde yeniden istenir:
    kazanım dağılımı ve soru sayısı TAM tutar."""
    from . import oyss as oy
    from . import visuals as _v
    avoid = avoid or {}
    gk, mk = load_keys() if not demo_mode() else ([], [])
    if not demo_mode() and not gk and not mk and not extra_keys():
        return [], ["API anahtarı bulunamadı"]
    seen = set(s for v in avoid.values() for s in v)
    seen_lock = threading.Lock()
    T0 = time.time()
    E = ThreadPoolExecutor(max_workers=WORKERS)

    def run_subject(si):
        st_ = subject_tables[si]
        subj, rows = st_["subject"], st_["rows"]
        total = sum(r["n"] for r in rows)
        labels = oy.difficulty_labels(total)
        random.shuffle(labels)
        slots, pos = [], 0
        for r in rows:
            for j in range(r["n"]):
                slots.append({"kazanim": f"{r['code']} – {r['topic']}", "code": str(r["code"]), "label": labels[pos + j]})
            pos += r["n"]
        errs = []
        if demo_mode():
            qs = []
            for j, sl in enumerate(slots):
                qs.append({"kazanim": sl["kazanim"], "type": "Açık uçlu" if j % 3 else "Kısa cevaplı", "difficulty": sl["label"],
                           "passage": "", "question": f"[{subj}] Demo açık uçlu soru {uuid.uuid4().hex[:4]}", "shape": None,
                           "answer": "Demo cevap", "rubric": [{"step": "Adım 1", "points": 5}, {"step": "Adım 2", "points": 5}]})
        else:
            filled = [None] * total
            av = list(avoid.get(subj, []))
            last_err, fails = None, 0

            def ask(batch):
                items = []
                for i in batch:
                    sl = slots[i]
                    if items and items[-1]["kazanim"] == sl["kazanim"]:
                        items[-1]["n"] += 1
                        items[-1]["labels"].append(sl["label"])
                    else:
                        items.append({"kazanim": sl["kazanim"], "n": 1, "labels": [sl["label"]]})
                done_stems = [_stem(q) for q in filled if q]
                return _ask_questions(oyss_prompt(grade_label, subj, items, difficulty, av + done_stems), gk, mk, next(_UID),
                                      lambda its: [q for q in its if _valid_oyss(q)], reasoning=GEN_REASONING.get(subj))

            for rnd in range(MAX_ROUNDS):
                missing = [i for i, f in enumerate(filled) if f is None]
                if not missing:
                    break
                if rnd > 0 and (time.time() - T0 > GEN_BUDGET or fails >= 3):
                    break
                batches = [missing[i:i + OYSS_CHUNK] for i in range(0, len(missing), OYSS_CHUNK)]
                futs = [(b, E.submit(ask, b)) for b in batches]
                progress = False
                for b, f in futs:
                    try:
                        got, err = f.result()
                    except Exception as e:
                        got, err = [], f"{type(e).__name__}: {str(e)[:80]}"
                    if err and not got:
                        last_err = err
                    free = list(b)
                    for q in got:
                        if not free:
                            break
                        s = _stem(q)
                        with seen_lock:
                            if not s or s in seen:
                                continue
                            j = next((i for i in free if slots[i]["code"] and slots[i]["code"] in str(q.get("kazanim", ""))), free[0])
                            free.remove(j)
                            seen.add(s)
                        q["kazanim"], q["difficulty"] = slots[j]["kazanim"], slots[j]["label"]
                        if q.get("type") not in ("Açık uçlu", "Kısa cevaplı"):
                            q["type"] = "Açık uçlu"
                        filled[j] = q
                        progress = True
                fails = 0 if progress else fails + 1
            qs = [q for q in filled if q is not None]
            if not qs:
                errs.append(f"{subj}: {last_err or 'geçersiz yanıt'}")
            elif len(qs) < total:
                errs.append(f"{subj}: {len(qs)}/{total} soru üretilebildi")
        pts = oy.point_split(len(qs))
        for q, p in zip(qs, pts):
            q["subject"] = subj
            q["points"] = p
            rub = [r for r in (q.get("rubric") or []) if isinstance(r, dict)]
            tot = sum(float(r.get("points", 0) or 0) for r in rub) or 1
            acc = 0
            for i, r in enumerate(rub):
                v = round(p * float(r.get("points", 0) or 0) / tot) if i < len(rub) - 1 else p - acc
                r["points"] = max(0, v)
                acc += r["points"]
            q["rubric"] = rub
            q["passage"] = q.get("passage") if str(q.get("passage")).lower() not in ("none", "null", "") else ""
            _sh = _v.normalize_shape(q.get("shape"))
            _sh = _sh if _sh and _sh.get("type") in ALLOWED_SHAPES.get(subj, {"table"}) else None
            q["shape"], _ = coherent_shape(_sh, f"{q.get('kazanim', '')} {q.get('question', '')} {q.get('passage', '')}")
            q["answer"] = str(q.get("answer", ""))
        return qs, errs

    questions, errors = [], []
    try:
        with ThreadPoolExecutor(max_workers=max(1, len(subject_tables))) as SX:
            outs = list(SX.map(lambda si: _safe_subject(run_subject, si, subject_tables[si]["subject"]), range(len(subject_tables))))
    finally:
        E.shutdown(wait=False)
    for si, (qs, errs) in enumerate(outs):
        questions += qs
        errors += errs
        if on_progress:
            on_progress(si + 1, len(subject_tables), subject_tables[si]["subject"])
    for i, q in enumerate(questions, 1):
        q["id"] = i
    return questions, errors


def _safe_subject(fn, si, subj):
    try:
        return fn(si)
    except Exception as e:  # bir dersin çökmesi diğerlerini etkilemesin
        return [], [f"{subj}: {type(e).__name__}: {str(e)[:80]}"]



# ---------------------------------------------------------------- yapay zekâ öğretmen: açık uçlu değerlendirme
TEACHER_SYSTEM = ("Sen deneyimli, adil ve gerçekçi bir Türkiye ortaokul öğretmenisin. MEB yazılı sınavı kâğıdı okur gibi puanlarsın: "
                  "puanlama anahtarındaki her adımı ayrı ayrı kontrol eder, öğrencinin yazdığı bilgiyi/işlemi görürsen o adımın puanını verir, "
                  "kısmen doğruysa kısmi puan verir. Boş ya da konu dışı cevaba 0 verirsin. Cömert de acımasız da olma; yazım hatası için puan kırma. "
                  "Geri bildirimin samimi, öğretmen ağzıyla, öğrenciye 'sen' diye hitap eden, kısa ve yol göstericidir. Yalnızca geçerli JSON döndür.")


def _teacher_prompt(items, grade_label):
    blocks = []
    for k, (i, q, ans) in enumerate(items, 1):
        rub = "; ".join(f"{r.get('step', '')} ({r.get('points', '')} p)" for r in (q.get("rubric") or []) if isinstance(r, dict))
        blocks.append(f"### Soru {k} (id={i}) — en çok {q.get('points')} puan\nKazanım: {q.get('kazanim', '')}\n"
                      f"Metin: {q.get('passage') or '-'}\nSoru: {q.get('question')}\nBeklenen cevap: {q.get('answer')}\n"
                      f"Puanlama anahtarı: {rub or 'yok'}\nÖĞRENCİ CEVABI: {ans or '(boş)'}")
    return (f"{grade_label} öğrencisinin yazılı sınav cevaplarını değerlendir.\n\n" + "\n\n".join(blocks) +
            '\n\nYalnızca şu JSON: {"results":[{"id":<soru id>,"points":<0 ile en çok puan arası sayı, 0.5 adımlı>,'
            '"verdict":"Tam|Kısmi|Yetersiz|Boş","feedback":"2-3 cümle öğretmen yorumu: neyi doğru yaptı, neyi eksik bıraktı","tip":"1 cümle somut çalışma önerisi"}]}')


def _words(t):
    return {w for w in re.sub(r"[^\w\s]", " ", str(t).lower()).split() if len(w) > 3}


def _demo_grade(q, ans):
    mx = float(q.get("points", 0))
    if not str(ans).strip():
        return {"points": 0.0, "verdict": "Boş", "feedback": "Bu soruyu boş bırakmışsın. Bilmesen bile bildiğin kısmı yazmak kısmi puan getirir.", "tip": "Kazanımı tekrar oku."}
    ref = _words(q.get("answer", ""))
    got = len(ref & _words(ans)) / max(1, len(ref))
    p = round(mx * min(1, got * 1.3) * 2) / 2
    return {"points": p, "verdict": "Tam" if p >= mx * .9 else "Kısmi" if p > 0 else "Yetersiz",
            "feedback": "Cevabındaki anahtar kavramları beklenen cevapla karşılaştırdım (demo değerlendirme).", "tip": "Beklenen cevabı oku ve eksik adımları tamamla."}


def grade_open(questions, open_answers, grade_label):
    """Açık uçlu cevapları yapay zekâ öğretmenle puanlar. -> ({idx: {points, verdict, feedback, tip}}, hatalar)"""
    from concurrent.futures import ThreadPoolExecutor
    out, errs = {}, []
    todo = []
    for i, q in enumerate(questions):
        ans = str(open_answers.get(i, "")).strip()
        if not ans:
            out[i] = {"points": 0.0, "verdict": "Boş", "feedback": "Bu soruyu boş bırakmışsın. Bilmediğin soruda bile bildiğin kısmı yazmak kısmi puan getirir.",
                      "tip": "Kazanımı tekrar edip beklenen cevapla karşılaştır."}
        else:
            todo.append((i, q, ans))
    if demo_mode():
        for i, q, a in todo:
            out[i] = _demo_grade(q, a)
        return out, errs
    gk, mk = load_keys()
    chunks = [todo[k:k + 4] for k in range(0, len(todo), 4)]

    def work(arg):
        n, ch = arg
        raw, err = multi_pool_generate(_teacher_prompt(ch, grade_label), gk, mk, offset=n, temperature=0.2)
        data = parse_json(raw) if raw else None
        return ch, data, err

    with ThreadPoolExecutor(max_workers=min(4, max(1, len(chunks)))) as ex:
        for ch, data, err in ex.map(work, list(enumerate(chunks))):
            res = {}
            for r in ((data or {}).get("results") or []) if isinstance(data, dict) else []:
                try:
                    res[int(r.get("id"))] = r
                except Exception:
                    pass
            for i, q, a in ch:
                r = res.get(i)
                if not r:
                    errs.append(f"Soru {i + 1} yapay zekâ ile puanlanamadı" + (f" ({err})" if err else ""))
                    continue
                mx = float(q.get("points", 0))
                try:
                    pts = max(0.0, min(mx, round(float(r.get("points", 0)) * 2) / 2))
                except Exception:
                    pts = 0.0
                out[i] = {"points": pts, "verdict": str(r.get("verdict") or ""), "feedback": str(r.get("feedback") or ""), "tip": str(r.get("tip") or "")}
    return out, errs
'''
MODULES['core/coach'] = r'''# -*- coding: utf-8 -*-
"""Öğrenci koçu: aralıklı tekrar, seri/hedef/seviye, çalışma planı, süre analizi, yapay zekâ anlatımı."""
import datetime as _dt
import time
from . import store, ai_engine as ai

INTERVALS = [1, 3, 7, 21, 60]  # gün: kutu 0..4
DAY = 86400
TR_DAYS = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
LEVELS = ["Çaylak", "Meraklı", "Gayretli", "Kararlı", "Usta", "Uzman", "Şampiyon", "Efsane"]


def _day(ts):
    return _dt.date.fromtimestamp(ts)


# ------------------------------------------------------------ aralıklı tekrar (Leitner)
def due_items(now=None):
    now = now or time.time()
    out = [w for w in store.wrong() if w.get("kind") == "mc" and w.get("due", 0) <= now]
    return sorted(out, key=lambda w: (w.get("box", 0), w.get("due", 0)))


def upcoming_count():
    now = time.time()
    return sum(1 for w in store.wrong() if w.get("kind") == "mc" and w.get("due", 0) > now)


def review_result(key, ok):
    """Doğruysa bir sonraki kutuya (aralık uzar), yanlışsa başa döner."""
    w = next((x for x in store.wrong() if x.get("key") == key), None)
    if not w:
        return
    box = min(w.get("box", 0) + 1, len(INTERVALS)) if ok else 0
    days = INTERVALS[min(box, len(INTERVALS) - 1)] if ok else 1
    store.update_wrong(key, box=box, due=int(time.time() + days * DAY), last_review=int(time.time()))
    s = store.settings()
    t = _dt.date.today().isoformat()
    s["reviews"][t] = s["reviews"].get(t, 0) + 1
    store.save_settings(reviews=s["reviews"])
    return days


# ------------------------------------------------------------ seri / hedef / seviye
def daily_counts(hist=None):
    hist = store.history() if hist is None else hist
    d = {}
    for h in hist:
        k = _day(h["ts"]).isoformat()
        d[k] = d.get(k, 0) + int(h.get("total", 0))
    for k, v in store.settings()["reviews"].items():
        d[k] = d.get(k, 0) + v
    return d


def streak(counts=None):
    c = daily_counts() if counts is None else counts
    day = _dt.date.today()
    if c.get(day.isoformat(), 0) == 0:
        day -= _dt.timedelta(days=1)  # bugün henüz çalışılmadıysa seri dünden sayılır
    n = 0
    while c.get(day.isoformat(), 0) > 0:
        n += 1
        day -= _dt.timedelta(days=1)
    return n


def today_count():
    return daily_counts().get(_dt.date.today().isoformat(), 0)


def xp_level(hist=None):
    hist = store.history() if hist is None else hist
    xp = sum(int(h.get("correct", 0)) * 10 + int(h.get("total", 0)) * 2 for h in hist) + sum(store.settings()["reviews"].values()) * 5
    lv = int((xp / 60) ** 0.5)
    nxt = ((lv + 1) ** 2) * 60
    base = (lv ** 2) * 60
    return {"xp": xp, "level": lv + 1, "title": LEVELS[min(lv, len(LEVELS) - 1)], "pct": 100 * (xp - base) / max(1, nxt - base), "next": nxt}


# ------------------------------------------------------------ zayıf kazanımlar & plan
def weak_topics(hist=None, last=10, limit=12):
    hist = (store.history() if hist is None else hist)[-last:]
    agg = {}
    for h in hist:
        for s, tps in (h.get("topics") or {}).items():
            for t, v in tps.items():
                if t and t != "Genel" and v[1]:
                    a = agg.setdefault((s, t), [0.0, 0.0])
                    a[0] += v[0]
                    a[1] += v[1]
    rows = [(s, t, 100 * a / b, b) for (s, t), (a, b) in agg.items() if b >= 1]
    return sorted([r for r in rows if r[2] < 75] or rows, key=lambda r: (r[2], -r[3]))[:limit]


def subject_stats(hist=None, last=10):
    hist = (store.history() if hist is None else hist)[-last:]
    d = {}
    for h in hist:
        for s, v in (h.get("per") or {}).items():
            e = d.setdefault(s, {"pct": [], "sec": []})
            e["pct"].append(v.get("pct", 0))
            if v.get("sec"):
                e["sec"].append(v["sec"])
    return {s: {"pct": sum(e["pct"]) / len(e["pct"]), "sec": (sum(e["sec"]) / len(e["sec"])) if e["sec"] else None, "n": len(e["pct"])} for s, e in d.items()}


def week_plan(hist=None):
    """7 günlük plan: zayıf kazanımlar, tekrar, yaprak test, hafta sonu deneme."""
    weak = weak_topics(hist)
    due = len(due_items())
    plan = []
    wi = 0
    for i, day in enumerate(TR_DAYS):
        if i == 6:
            plan.append({"day": day, "icon": "🏆", "title": "Mini deneme + değerlendirme", "detail": "Haftanın kazanımlarından 20 soruluk deneme çöz, yanlışlarını arşive ekle.", "action": "weekly"})
        elif i == 5:
            plan.append({"day": day, "icon": "🔁", "title": f"Genel tekrar ({due} soru sırada)" if due else "Genel tekrar", "detail": "Günlük Tekrar'daki soruları bitir; yanlış arşivinden eksikleri kapat.", "action": "review"})
        elif i % 2 == 0 and weak:
            s, t, p, _ = weak[wi % len(weak)]
            wi += 1
            plan.append({"day": day, "icon": "🎯", "title": f"{s}: {t}", "detail": f"Bu kazanımda başarın %{p:.0f}. 10 soruluk yaprak test çöz.", "action": "leaf", "subject": s})
        elif weak:
            s, t, p, _ = weak[wi % len(weak)]
            wi += 1
            plan.append({"day": day, "icon": "📖", "title": f"{s}: {t} konu tekrarı", "detail": "Konu özetini oku, yanlış yaptığın soruları 'Bana anlat' ile incele.", "action": "archive", "subject": s})
        else:
            plan.append({"day": day, "icon": "📝", "title": "Konu tarama", "detail": "Bir ders ve ünite seç, 15 soruluk konu tarama çöz.", "action": "topic"})
    return plan


def time_analysis(qs, answers, qtime, mc=True, expected=90):
    """Soru başı süre: hızlı-yanlış (aceleci), uzun düşünülen, ders ortalamaları."""
    per, fast_wrong, slow, rows = {}, 0, 0, []
    for i, q in enumerate(qs):
        t = float(qtime.get(i, 0))
        s = q.get("subject", "Genel")
        per.setdefault(s, []).append(t)
        ua = answers.get(i)
        if mc and ua and ua != q.get("answer") and t < 15:
            fast_wrong += 1
        if t > expected * 1.8:
            slow += 1
        rows.append(t)
    return {"avg": {s: sum(v) / len(v) for s, v in per.items()}, "fast_wrong": fast_wrong, "slow": slow,
            "total": sum(rows), "n": len(qs), "expected": expected}


# ------------------------------------------------------------ yapay zekâ: öğretmen yorumu & anlatım
def _ask(prompt, system=ai.TEACHER_SYSTEM, temperature=0.4):
    if ai.demo_mode():
        return None
    gk, mk = ai.load_keys()
    raw, err = ai.multi_pool_generate(prompt, gk, mk, temperature=temperature)
    return ai.parse_json(raw) if raw else None


def teacher_comment(grade_label, stats, weak, streak_n):
    lines = [f"- {s}: ort. %{v['pct']:.0f}" + (f", soru başı {v['sec']:.0f} sn" if v.get("sec") else "") for s, v in stats.items()]
    wk = [f"- {s} / {t}: %{p:.0f}" for s, t, p, _ in weak[:6]]
    fb = "Düzenli çalışıyorsun; önce en düşük başarılı kazanımlardan başla, her gün kısa ama sürekli çalış."
    r = _ask(f"{grade_label} öğrencisinin son denemeleri:\n" + "\n".join(lines) + "\nZayıf kazanımlar:\n" + "\n".join(wk) +
             f"\nÇalışma serisi: {streak_n} gün.\nÖğrenciye 'sen' diye hitap eden, motive edici ama dürüst, 4-5 cümlelik bir öğretmen değerlendirmesi ve haftalık çalışma tavsiyesi yaz. "
             'Yalnızca JSON: {"comment":"..."}')
    return (r or {}).get("comment") or fb


def explain(q, user_answer, grade_label):
    """Yanlış çözülen soruyu öğretmen ağzıyla anlatır + daha kolay benzer örnek. -> dict"""
    opts = q.get("options") or {}
    correct = opts.get(q.get("answer"), "")
    r = _ask(f"{grade_label} {q.get('subject', '')} sorusunu öğrenciye anlat.\nMetin: {q.get('passage') or '-'}\nSoru: {q.get('question')}\n"
             f"Şıklar: {opts}\nDoğru cevap: {q.get('answer')}) {correct}\nÖğrencinin cevabı: {user_answer or 'boş'}\n"
             "Öğretmen ağzıyla, samimi ve sabırlı anlat: 1) soruda ne isteniyor, 2) adım adım çözüm, 3) öğrenci muhtemelen neden yanlış şıkkı seçti, 4) aynı kazanımdan DAHA KOLAY, "
             "çözümlü kısa bir benzer örnek. Yalnızca JSON: "
             '{"steps":["adım 1","adım 2"],"why_wrong":"..","easy_example":{"question":"..","answer":".."},"tip":"tek cümle ipucu"}')
    if r:
        return r
    return {"steps": [q.get("explanation") or "Çözüm açıklaması bulunamadı."], "why_wrong": "Soruyu yeniden oku ve her şıkkı eleyerek ilerle.",
            "easy_example": None, "tip": "Kazanımı tekrar oku."}
'''
MODULES['ui/theme'] = r'''# -*- coding: utf-8 -*-
import streamlit as st

CSS = """
<style>
.main, [data-testid="stAppViewContainer"] { background: #f1f5f9; }
.block-container { padding-top: 1.6rem; max-width: 1280px; }

/* ---- Kenar çubuğu ---- */
[data-testid="stSidebar"] { background: linear-gradient(180deg,#0f172a 0%,#1e293b 100%); }
[data-testid="stSidebar"] * { color: #e2e8f0; }
[data-testid="stSidebar"] hr { border-color: #334155; }
[data-testid="stSidebar"] div.stButton > button:first-child {
    background: rgba(255,255,255,.06); color:#e2e8f0; border:1px solid #334155; box-shadow:none;
    font-size:.95rem; padding:.7rem .9rem; border-radius:12px; text-align:left; justify-content:flex-start; }
[data-testid="stSidebar"] div.stButton > button:first-child:hover { background: rgba(56,189,248,.18); border-color:#38bdf8; transform:none; }
.brand { font-size:1.35rem; font-weight:900; letter-spacing:.3px; color:#f8fafc; }
.brand span { color:#fb923c; }
.side-chip { background:#0b1220; border:1px solid #334155; border-radius:12px; padding:.6rem .8rem; font-size:.82rem; margin:.3rem 0; }

/* ---- Kenar çubuğu butonları: eş boyut + renkli ---- */
[data-testid="stSidebar"] [class*="st-key-nv_"], [data-testid="stSidebar"] [class*="st-key-nv_"] > div, [data-testid="stSidebar"] [class*="st-key-nv_"] div.stButton { width:100% !important; }
[data-testid="stSidebar"] [class*="st-key-nv_"] button > div, [data-testid="stSidebar"] [class*="st-key-nv_"] button [data-testid="stMarkdownContainer"] { width:100%; justify-content:flex-start; text-align:left; }
[data-testid="stSidebar"] [class*="st-key-nv_"] button { width:100% !important; height:3.2rem !important; min-height:3.2rem !important; max-height:3.2rem !important;
    border-radius:14px !important; border:none !important; justify-content:flex-start !important; text-align:left; padding:0 1rem !important; white-space:nowrap;
    box-shadow:0 8px 16px -8px rgba(0,0,0,.5) !important; transition:all .2s ease; }
[data-testid="stSidebar"] [class*="st-key-nv_"] button:hover { transform:translateX(4px); filter:brightness(1.12); }
[data-testid="stSidebar"] [class*="st-key-nv_"] button p { color:#fff !important; font-weight:800; font-size:.98rem; margin:0; }
[data-testid="stSidebar"] .st-key-nv_home button { background:linear-gradient(135deg,#38bdf8,#1d4ed8) !important; }
[data-testid="stSidebar"] .st-key-nv_leaf button { background:linear-gradient(135deg,#4ade80,#15803d) !important; }
[data-testid="stSidebar"] .st-key-nv_rep button  { background:linear-gradient(135deg,#a78bfa,#6d28d9) !important; }
[data-testid="stSidebar"] .st-key-nv_arc button  { background:linear-gradient(135deg,#fbbf24,#b45309) !important; }
[data-testid="stSidebar"] .st-key-nv_bdg button  { background:linear-gradient(135deg,#f472b6,#be185d) !important; }

/* ---- Koç: seri şeridi, öğretmen kutusu, plan kartları ---- */
.strip { display:grid; grid-template-columns:1fr 2fr 1fr 1fr; gap:.7rem; margin:.2rem 0 1rem; }
.strip .sc { background:linear-gradient(135deg,#f5f3ff,#ecfeff); border:2px solid #ddd6fe; border-radius:18px; padding:.7rem .9rem; }
.strip .sc.wide { grid-column:auto; }
.strip .sv { font-size:1.35rem; font-weight:900; color:#4c1d95; } .strip .sl { font-size:.78rem; color:#475569; font-weight:700; margin:.15rem 0; }
@media (max-width:760px) { .strip { grid-template-columns:1fr 1fr; } .strip .sc.wide { grid-column:1 / -1; order:5; } }
.teach { background:linear-gradient(135deg,#faf5ff,#f0fdfa); border:2px solid #c4b5fd; border-radius:18px; padding:1rem 1.2rem; margin:.6rem 0; color:#1e293b; line-height:1.6; }
.teach.ex { border-color:#5eead4; } .teach-h { font-weight:900; color:#6d28d9; margin-bottom:.3rem; } .teach ol { margin:.2rem 0 .4rem 1.1rem; } .teach details { cursor:pointer; color:#0f766e; }
.plan-card { background:#fff; border:2px solid #e2e8f0; border-radius:18px; padding:.9rem 1.1rem; margin-bottom:.35rem; box-shadow:0 8px 18px -16px rgba(15,23,42,.6); }
.plan-card.today { border-color:#7c3aed; background:linear-gradient(135deg,#f5f3ff,#ecfeff); }
.plan-card .pd { font-size:.75rem; font-weight:900; color:#7c3aed; text-transform:uppercase; letter-spacing:.5px; } .plan-card .pt { font-weight:900; color:#0f172a; margin:.15rem 0; } .plan-card .pi { font-size:.85rem; color:#64748b; }
[data-testid="stSidebar"] .st-key-nv_rev button  { background:linear-gradient(135deg,#2dd4bf,#0f766e) !important; }
[data-testid="stSidebar"] .st-key-nv_plan button { background:linear-gradient(135deg,#818cf8,#4338ca) !important; }

/* ---- Hazır ekranı: geri sayım penceresiyle aynı tarz ---- */
.ready-aura { position:fixed; inset:0; z-index:0; pointer-events:none; background:rgba(15,23,42,.78); backdrop-filter:blur(6px); }
.block-container:has(.ready-aura) { padding-top:.6rem; padding-bottom:.6rem; min-height:100vh; display:flex; flex-direction:column; justify-content:center; }
.st-key-ready_card { position:relative; z-index:1; background:#fff; border-radius:28px; padding:1.5rem 1.6rem 1.1rem; text-align:center; width:min(440px,92vw); margin:0 auto;
    box-shadow:0 30px 70px -20px rgba(0,0,0,.6); }
.st-key-ready_card [data-testid="stVerticalBlock"] { gap:.5rem; align-items:center; }
.ready-t { font-size:1.3rem; font-weight:900; color:#0f172a; line-height:1.3; }
.ready-s { color:#64748b; font-size:.9rem; margin:.1rem 0 .3rem; }
.ready-chips { display:flex; flex-wrap:wrap; gap:.4rem; justify-content:center; margin:.2rem 0 .6rem; }
.ready-chips span { background:#f5f3ff; border:1.5px solid #ddd6fe; color:#4c1d95; font-weight:800; font-size:.8rem; padding:.2rem .7rem; border-radius:999px; }
.st-key-bigstart { display:flex; justify-content:center; padding:.4rem 0 .8rem; }
.st-key-bigstart div.stButton, .st-key-bigstart [data-testid="stButton"] { width:auto !important; }
.st-key-bigstart button { position:relative; width:clamp(120px,26vh,170px) !important; height:clamp(120px,26vh,170px) !important; min-height:clamp(120px,26vh,170px) !important; max-height:clamp(120px,26vh,170px) !important; padding:0 !important; border-radius:50% !important;
    background:#fff !important; border:10px solid #e2e8f0 !important; box-shadow:none !important; color:#0f172a !important; display:flex !important; align-items:center; justify-content:center; overflow:visible; transition:transform .2s ease; box-sizing:border-box; }
.st-key-bigstart button > *, .st-key-bigstart button [data-testid="stMarkdownContainer"] { display:flex !important; flex-direction:column; align-items:center; justify-content:center; width:100% !important; height:100%; margin:0 !important; padding:0 !important; gap:.35rem; text-align:center; }
.st-key-bigstart button:after { content:''; position:absolute; left:-10px; top:-10px; width:calc(100% + 20px); height:calc(100% + 20px); box-sizing:border-box; border-radius:50%; border:10px solid transparent; border-top-color:#7c3aed; border-right-color:#14b8a6; animation:genspin 1.1s linear infinite; pointer-events:none; }
.st-key-bigstart button:hover { transform:scale(1.06); }
.st-key-bigstart button:active { transform:scale(.96); }
.st-key-bigstart button p { margin:0; text-align:center; line-height:1; }
.st-key-bigstart button p:first-child { font-size:3.4rem; font-weight:900; color:#7c3aed !important; margin:0 !important; transform:translateX(.07em); animation:genpulse 1.2s ease-in-out infinite; }
.st-key-bigstart button p:nth-child(2) { font-size:1rem; font-weight:900; letter-spacing:3px; text-indent:3px; color:#0f766e !important; margin:0 !important; }
.ready-bar { background:#e2e8f0; border-radius:999px; height:8px; overflow:hidden; width:100%; } .ready-bar i { display:block; height:8px; width:100%; background:linear-gradient(90deg,#7c3aed,#14b8a6); border-radius:999px; }
@media (max-height:640px) { .ready-hint, .ready-bar { display:none; } .st-key-ready_card { padding:1rem 1.2rem .8rem; } }
.ready-hint { color:#94a3b8; font-size:.8rem; font-weight:700; margin:.3rem 0 .2rem; }
.st-key-ready_card [class*="st-key-ready_"] button { min-height:2.4rem; font-size:.88rem; padding:.4rem .8rem; }
@keyframes genspin{to{transform:rotate(360deg)}} @keyframes genpulse{50%{transform:scale(1.08)}}

/* ---- Başlık ---- */
.hero { background: linear-gradient(120deg,#0f172a 0%,#1d4ed8 60%,#0ea5e9 100%); color:white; border-radius:22px;
        padding:1.6rem 2rem; margin-bottom:1.2rem; box-shadow:0 18px 40px -18px rgba(15,23,42,.6); }
.hero h1 { margin:0; font-size:1.9rem; font-weight:900; color:white; }
.hero p { margin:.3rem 0 0; opacity:.9; }
.sec-title { font-weight:900; color:#0f172a; font-size:1.15rem; margin:1.1rem 0 .6rem; }

/* ---- Dashboard kartları (st.button, key = card_<renk>_<id>) ---- */
[class*="st-key-card_"] button { min-height:150px; border-radius:22px !important; color:white !important; border:none !important;
    text-align:left; justify-content:flex-start; align-items:flex-start; padding:1.2rem 1.3rem !important;
    box-shadow:0 14px 28px -14px rgba(15,23,42,.55) !important; transition:all .25s ease; white-space:normal; }
[class*="st-key-card_"] button:hover { transform:translateY(-4px) scale(1.01); filter:brightness(1.07); }
[class*="st-key-card_"] button p { color:white !important; margin:0 0 .35rem; font-size:.92rem; line-height:1.35; text-align:left; }
[class*="st-key-card_"] button p:first-child { font-size:1.35rem; font-weight:900; }
[class*="st-key-card_"] button:disabled { background:#cbd5e1 !important; opacity:.75; box-shadow:none !important; }
[class*="st-key-card_"] button:disabled p { color:#475569 !important; }
[class*="st-key-card_teal"] button   { background:linear-gradient(135deg,#14b8a6,#0f766e) !important; }
[class*="st-key-card_blue"] button   { background:linear-gradient(135deg,#38bdf8,#1d4ed8) !important; }
[class*="st-key-card_violet"] button { background:linear-gradient(135deg,#a78bfa,#6d28d9) !important; }
[class*="st-key-card_pink"] button   { background:linear-gradient(135deg,#f472b6,#be185d) !important; }
[class*="st-key-card_orange"] button { background:linear-gradient(135deg,#fb923c,#c2410c) !important; }
[class*="st-key-card_red"] button    { background:linear-gradient(135deg,#f87171,#b91c1c) !important; }
[class*="st-key-card_green"] button  { background:linear-gradient(135deg,#4ade80,#15803d) !important; }
[class*="st-key-card_amber"] button  { background:linear-gradient(135deg,#fbbf24,#b45309) !important; }
[class*="st-key-card_indigo"] button { background:linear-gradient(135deg,#818cf8,#3730a3) !important; }
[class*="st-key-card_slate"] button  { background:linear-gradient(135deg,#64748b,#1e293b) !important; }
[class*="st-key-small_"] button { min-height:64px; }

/* ---- Adım adım ekranlar ---- */
.wz-head { background:white; border:1px solid #e2e8f0; border-radius:20px; padding:1.1rem 1.4rem; margin-bottom:1.2rem; box-shadow:0 10px 24px -16px rgba(15,23,42,.4); }
.wz-title { font-size:1.4rem; font-weight:900; color:#0f172a; } .wz-sub { color:#64748b; font-size:.9rem; margin:.15rem 0 .7rem; }
.stepper { display:flex; flex-wrap:wrap; gap:.4rem; }
.stp { padding:.28rem .8rem; border-radius:999px; background:#f1f5f9; color:#94a3b8; font-weight:800; font-size:.8rem; }
.stp.on { background:linear-gradient(135deg,#0284c7,#1d4ed8); color:#fff; } .stp.done { background:#dcfce7; color:#15803d; }
[class*="st-key-opt_"] button, [class*="st-key-optsel_"] button { min-height:118px; border-radius:18px !important; text-align:left; justify-content:flex-start; align-items:flex-start;
    padding:1rem 1.1rem !important; white-space:normal; transition:all .2s ease; }
[class*="st-key-opt_"] button { background:#fff !important; color:#0f172a !important; border:2px solid #e2e8f0 !important; box-shadow:0 8px 18px -14px rgba(15,23,42,.5) !important; }
[class*="st-key-opt_"] button:hover { border-color:#38bdf8 !important; transform:translateY(-3px); }
[class*="st-key-opt_"] button p { color:#0f172a !important; margin:0 0 .25rem; font-size:.85rem; text-align:left; line-height:1.35; }
[class*="st-key-opt_"] button p:first-child { font-size:1.08rem; font-weight:900; }
[class*="st-key-optsel_"] button { background:linear-gradient(135deg,#0284c7,#1d4ed8) !important; border:2px solid #1d4ed8 !important; color:#fff !important; box-shadow:0 12px 24px -12px rgba(29,78,216,.7) !important; }
[class*="st-key-optsel_"] button p { color:#fff !important; margin:0 0 .25rem; font-size:.85rem; text-align:left; line-height:1.35; }
[class*="st-key-optsel_"] button p:first-child { font-size:1.08rem; font-weight:900; }

/* ---- Butonlar: hepsi modern kart ---- */
div.stButton > button, div.stDownloadButton > button, div[data-testid="stFormSubmitButton"] > button {
    width:100%; border-radius:16px; font-weight:800; font-size:1rem; padding:.8rem 1.1rem; min-height:3rem;
    background:#fff; color:#0f172a; border:2px solid #e2e8f0; box-shadow:0 8px 18px -14px rgba(15,23,42,.55); transition:all .2s ease; }
div.stButton > button:hover, div.stDownloadButton > button:hover, div[data-testid="stFormSubmitButton"] > button:hover {
    border-color:#38bdf8; color:#0369a1; transform:translateY(-2px); box-shadow:0 12px 22px -14px rgba(2,132,199,.6); }
button[data-testid="stBaseButton-primary"], button[kind="primary"], button[kind="primaryFormSubmit"] {
    background:linear-gradient(135deg,#f97316 0%,#ea580c 100%) !important; color:#fff !important; border:2px solid #ea580c !important;
    box-shadow:0 10px 20px -8px rgba(249,115,22,.55) !important; }
button[data-testid="stBaseButton-primary"]:hover, button[kind="primary"]:hover { color:#fff !important; filter:brightness(1.06); }
button[data-testid="stBaseButton-primary"] p, button[kind="primary"] p { color:#fff !important; }
[class*="st-key-nav_"] button { background:linear-gradient(135deg,#0284c7,#0369a1) !important; color:#fff !important; border-color:#0369a1 !important; }
[class*="st-key-sel_"] button { background:#fff !important; color:#0f172a !important; border:2px solid #cbd5e1 !important; box-shadow:none !important; padding:.55rem .2rem !important; font-size:.9rem !important; min-height:3.6rem; line-height:1.25; }
[class*="st-key-sel_"] button p { font-size:.88rem; font-weight:800; margin:0; text-align:center; }
[class*="st-key-sel_"] button p:nth-child(2) { font-size:.74rem; font-weight:600; color:#64748b; }
[class*="st-key-sel_on_"] button p:nth-child(2) { color:#e0f2fe !important; }
[class*="st-key-sel_on_"] button { background:linear-gradient(135deg,#0284c7,#1d4ed8) !important; color:#fff !important; border-color:#1d4ed8 !important; }
[class*="st-key-sel_on_"] button p { color:#fff !important; }
[class*="st-key-sel_mon_"] button { border-color:#f97316 !important; }
[class*="st-key-back"] button, [class*="st-key-wz_back"] button { background:#fff !important; color:#334155 !important; border:2px solid #cbd5e1 !important; box-shadow:none !important; }

/* ---- Seçim kartları (zorluk / soru sayısı): mor + turkuaz ---- */
[class*="st-key-dif_"] button, [class*="st-key-cnt_"] button { min-height:84px; border-radius:20px !important; white-space:normal; transition:all .2s ease; }
[class*="st-key-dif_off_"] button, [class*="st-key-cnt_off_"] button { background:linear-gradient(135deg,#f5f3ff 0%,#ecfeff 100%) !important; color:#4c1d95 !important;
    border:2px solid #c4b5fd !important; box-shadow:0 8px 18px -14px rgba(109,40,217,.6) !important; }
[class*="st-key-dif_off_"] button:hover, [class*="st-key-cnt_off_"] button:hover { border-color:#14b8a6 !important; transform:translateY(-3px); }
[class*="st-key-dif_off_"] button p, [class*="st-key-cnt_off_"] button p { color:#4c1d95 !important; }
[class*="st-key-dif_on_"] button, [class*="st-key-cnt_on_"] button { background:linear-gradient(135deg,#7c3aed 0%,#0d9488 100%) !important; color:#fff !important;
    border:2px solid #5b21b6 !important; box-shadow:0 14px 26px -12px rgba(109,40,217,.7) !important; }
[class*="st-key-dif_on_"] button p, [class*="st-key-cnt_on_"] button p { color:#fff !important; font-weight:900; }
[class*="st-key-cnt_"] button p { font-size:1.5rem; font-weight:900; text-align:center; }
.pick-lbl { font-weight:900; color:#4c1d95; margin:.8rem 0 .4rem; font-size:1.05rem; }

/* ---- Üret düğmeleri: büyük, mor, tam genişlik ---- */
[class*="st-key-gen_"] button { min-height:4.4rem !important; font-size:1.25rem !important; border-radius:22px !important; background:linear-gradient(135deg,#8b5cf6 0%,#6d28d9 55%,#5b21b6 100%) !important;
    border:2px solid #5b21b6 !important; color:#fff !important; box-shadow:0 16px 30px -12px rgba(109,40,217,.7) !important; letter-spacing:.3px; }
[class*="st-key-gen_"] button p { color:#fff !important; font-weight:900; font-size:1.25rem; }
[class*="st-key-gen_"] button:hover { filter:brightness(1.08); transform:translateY(-3px); color:#fff !important; }

/* ---- Radyo / seçenekler kart gibi ---- */
div[role="radiogroup"] { gap:.55rem; }
div[role="radiogroup"] > label { background:#fff; border:2px solid #e2e8f0; border-radius:16px; padding:.75rem 1rem; width:100%; box-shadow:0 8px 18px -16px rgba(15,23,42,.55); transition:all .2s ease; }
div[role="radiogroup"] > label:hover { border-color:#38bdf8; transform:translateY(-1px); }
div[role="radiogroup"] > label:has(input:checked) { border-color:#1d4ed8; background:#eff6ff; box-shadow:0 10px 20px -14px rgba(29,78,216,.7); }
div[role="radiogroup"][aria-orientation="horizontal"] > label, div[data-testid="stRadio"] div[role="radiogroup"]:not([aria-orientation="vertical"]) > label { width:auto; }
div[data-baseweb="select"] > div { border-radius:14px; }
[data-testid="stExpander"] { border-radius:16px; border:1px solid #e2e8f0; background:#fff; }

/* ---- Telefon / tablet ---- */
@media (max-width: 760px) {
  .block-container { padding:1rem .7rem 3rem; }
  .hero { padding:1.1rem 1.1rem; border-radius:18px; } .hero h1 { font-size:1.4rem; }
  div[data-testid="stHorizontalBlock"]:has([class*="st-key-sel_"]) { flex-wrap:wrap !important; gap:.35rem !important; }
  div[data-testid="stHorizontalBlock"]:has([class*="st-key-sel_"]) > div[data-testid="stColumn"] { min-width:calc(33.3% - .4rem) !important; flex:1 1 calc(33.3% - .4rem) !important; width:auto !important; }
  div[data-testid="stHorizontalBlock"]:has([class*="st-key-card_"]) > div[data-testid="stColumn"],
  div[data-testid="stHorizontalBlock"]:has([class*="st-key-opt"]) > div[data-testid="stColumn"] { min-width:100% !important; }
  [class*="st-key-card_"] button { min-height:110px; }
  div[data-testid="stHorizontalBlock"]:has(.kpi) { flex-wrap:wrap !important; gap:.5rem !important; }
  div[data-testid="stHorizontalBlock"]:has(.kpi) > div[data-testid="stColumn"] { min-width:calc(50% - .5rem) !important; flex:1 1 calc(50% - .5rem) !important; }

}

/* ---- Soru kartı ---- */
.question-card { background:white; padding:2rem; border-radius:18px; box-shadow:0 10px 25px -5px rgba(0,0,0,.06); border:1px solid #e2e8f0; margin-bottom:1.2rem; }
.question-title { font-size:1.35rem !important; font-weight:800 !important; color:#1e293b !important; line-height:1.6 !important; margin:.8rem 0 1rem; }
.passage-box { background:#f1f5f9; border-left:5px solid #0284c7; padding:1.1rem; border-radius:8px; font-size:1.08rem; color:#334155; margin-bottom:1rem; line-height:1.7; }
.timer-box { background:linear-gradient(135deg,#1e293b,#0f172a); color:#38bdf8; padding:1rem; border-radius:16px; text-align:center; font-size:2rem; font-weight:900;
    box-shadow:0 10px 25px -5px rgba(15,23,42,.3); border:2px solid #38bdf8; letter-spacing:2px; }
.timer-box.low { color:#f87171; border-color:#f87171; }
.badge { background:#e0f2fe; color:#0369a1; padding:.35rem .85rem; border-radius:20px; font-weight:700; font-size:.88rem; margin-right:.3rem; display:inline-block; }

/* ---- KPI / paneller ---- */
.kpi { background:white; border-radius:18px; padding:1rem 1.2rem; border:1px solid #e2e8f0; box-shadow:0 8px 20px -12px rgba(15,23,42,.35); }
.kpi .v { font-size:1.9rem; font-weight:900; color:#0f172a; line-height:1.1; }
.kpi .l { font-size:.8rem; color:#64748b; font-weight:700; text-transform:uppercase; letter-spacing:.5px; }
.kpi .d { font-size:.85rem; font-weight:800; margin-top:.2rem; }
.up { color:#16a34a; } .down { color:#dc2626; } .flat { color:#64748b; }
.panel { background:white; border-radius:18px; padding:1.1rem 1.3rem; border:1px solid #e2e8f0; margin-bottom:1rem; box-shadow:0 8px 20px -14px rgba(15,23,42,.3); }
.pill { display:inline-block; padding:.18rem .6rem; border-radius:999px; font-size:.78rem; font-weight:800; color:white; }
.bar-bg { background:#e2e8f0; border-radius:999px; height:10px; overflow:hidden; }
.bar-fg { height:10px; border-radius:999px; }
.rozet { background:white; border:2px solid #fbbf24; border-radius:18px; padding:1rem; text-align:center; box-shadow:0 10px 22px -14px rgba(180,83,9,.6); height:100%; }
.rozet.locked { border-color:#cbd5e1; filter:grayscale(1); opacity:.6; box-shadow:none; }
.rozet .ic { font-size:2.2rem; } .rozet .t { font-weight:900; color:#0f172a; } .rozet .s { font-size:.8rem; color:#64748b; }

/* ---- Tablolar ---- */
.custom-table-container { overflow-x:auto; margin:12px 0; border-radius:12px; box-shadow:0 4px 15px -3px rgba(0,0,0,.08); border:1px solid #e2e8f0; }
.custom-table { width:100%; border-collapse:collapse; font-size:.93rem; background:#fff; text-align:left; }
.custom-table th { background:linear-gradient(135deg,#0284c7,#0369a1); color:#fff; padding:11px 15px; font-weight:700; }
.custom-table td { padding:10px 15px; border-bottom:1px solid #f1f5f9; color:#334155; }
.custom-table tr:nth-child(even) { background:#f8fafc; }
.custom-table tr:hover { background:#eef6ff; }
.custom-table td.num, .custom-table th.num { text-align:center; }
</style>
"""


def inject():
    st.markdown(CSS, unsafe_allow_html=True)


def card(key, color, title, desc, on_click=None, args=(), disabled=False):
    st.button(f"{title}\n\n{desc}", key=f"card_{color}_{key}", on_click=on_click, args=args,
              disabled=disabled, use_container_width=True)


def cells(items, per, fn):
    """Izgara: her satır ayrı st.columns -> telefonda/tablette sıra bozulmaz (4-5-6 / 7-8-LGS)."""
    items = list(items)
    for r in range(0, len(items), per):
        cols = st.columns(per)
        for c, it in zip(cols, items[r:r + per]):
            with c:
                fn(it)


def pick_cards(skey, options, default, per, prefix, label_fn=str, label=""):
    """Kart şeklinde tek seçim. Seçim session_state[skey]'de tutulur, tek tıkla güncellenir."""
    options = list(options)
    if st.session_state.get(skey) not in options:
        st.session_state[skey] = default
    if label:
        st.markdown(f"<div class='pick-lbl'>{label}</div>", unsafe_allow_html=True)
    cur_v = st.session_state[skey]

    def one(o):
        i = options.index(o)
        st.button(label_fn(o), key=f"{prefix}_{'on' if o == cur_v else 'off'}_{skey}_{i}", use_container_width=True,
                  on_click=lambda o=o: st.session_state.update({skey: o}))
    cells(options, per, one)
    return st.session_state[skey]


def kpi(label, value, delta=None, good_up=True):
    d = ""
    if delta is not None:
        cls = "flat" if abs(delta) < 1e-9 else ("up" if (delta > 0) == good_up else "down")
        arrow = "▲" if delta > 0 else ("▼" if delta < 0 else "■")
        d = f"<div class='d {cls}'>{arrow} {abs(delta):.1f}</div>"
    st.markdown(f"<div class='kpi'><div class='l'>{label}</div><div class='v'>{value}</div>{d}</div>", unsafe_allow_html=True)


def pct_color(p):
    return "#16a34a" if p >= 75 else ("#f59e0b" if p >= 50 else "#dc2626")


def bar(p):
    return f"<div class='bar-bg'><div class='bar-fg' style='width:{max(0, min(100, p)):.0f}%;background:{pct_color(p)}'></div></div>"


def html_table(headers, rows, num_cols=()):
    h = "<div class='custom-table-container'><table class='custom-table'><thead><tr>"
    h += "".join(f"<th class='{'num' if i in num_cols else ''}'>{x}</th>" for i, x in enumerate(headers)) + "</tr></thead><tbody>"
    for r in rows:
        h += "<tr>" + "".join(f"<td class='{'num' if i in num_cols else ''}'>{c}</td>" for i, c in enumerate(r)) + "</tr>"
    st.markdown(h + "</tbody></table></div>", unsafe_allow_html=True)


OVERLAY_CSS = ("<style>.gen-ov{position:fixed;inset:0;z-index:999999;background:rgba(15,23,42,.78);backdrop-filter:blur(6px);display:flex;align-items:center;justify-content:center}"
 ".gen-card{background:#fff;border-radius:28px;padding:2rem 2.4rem 1.6rem;text-align:center;box-shadow:0 30px 70px -20px rgba(0,0,0,.6);width:min(420px,90vw)}"
 ".gen-ov *,.gen-ov *:before,.gen-ov *:after{box-sizing:border-box}"
 ".gen-ring{position:relative;width:170px;height:170px;margin:0 auto 1.1rem;display:block;flex:none}"
 ".gen-ring:before{content:'';position:absolute;left:0;top:0;width:170px;height:170px;border-radius:50%;border:10px solid #e2e8f0}"
 ".gen-ring:after{content:'';position:absolute;left:0;top:0;width:170px;height:170px;border-radius:50%;border:10px solid transparent;border-top-color:#0284c7;border-right-color:#38bdf8;animation:genspin 1.1s linear infinite;transform-origin:50% 50%}"
 ".gen-cd{position:absolute;left:0;top:0;width:170px;height:170px;font-size:3.2rem;font-weight:900;color:#0f172a;line-height:1}"
 ".gen-cd span{position:absolute;left:0;top:0;width:170px;height:170px;display:flex;align-items:center;justify-content:center;text-align:center;opacity:0;animation:gencd 1s linear forwards;margin:0;padding:0}"
 ".gen-cd span.z{font-size:1.05rem;line-height:1.25;color:#0284c7;padding:0 26px;animation:genz .5s linear forwards,genpulse 1.2s ease-in-out infinite}"
 ".gen-t{font-size:1.25rem;font-weight:900;color:#0f172a}.gen-s{color:#64748b;font-size:.9rem;margin:.3rem 0 1rem}"
 ".gen-bar{background:#e2e8f0;border-radius:999px;height:8px;overflow:hidden}.gen-bar i{display:block;height:8px;width:0;background:linear-gradient(90deg,#0284c7,#38bdf8);border-radius:999px;animation:genbar linear forwards}"
 "@keyframes genspin{to{transform:rotate(360deg)}}@keyframes gencd{0%,97%{opacity:1}100%{opacity:0}}@keyframes genz{to{opacity:1}}"
 "@keyframes genpulse{50%{transform:scale(1.08)}}@keyframes genbar{to{width:100%}}</style>")


def overlay_html(seconds, title, sub=""):
    """Ekran ortasında geriye sayan daire. Sayaç tarayıcıda (CSS) çalışır; sunucu meşgulken de akar."""
    n = max(5, min(int(seconds), 240))
    spans = "".join(f"<span style='animation-delay:{i}s'>{n - i}</span>" for i in range(n))
    spans += f"<span class='z' style='animation-delay:{n}s'>Son rötuşlar…</span>"
    return (OVERLAY_CSS + f"<div class='gen-ov'><div class='gen-card'><div class='gen-ring'><div class='gen-cd'>{spans}</div></div>"
            f"<div class='gen-t'>{title}</div><div class='gen-s'>{sub}</div><div class='gen-bar'><i style='animation-duration:{n}s'></i></div></div></div>")
'''
MODULES['ui/state'] = r'''# -*- coding: utf-8 -*-
import copy
import streamlit as st

DEFAULTS = {
    "page": "home", "grade": None, "mode": None,
    "questions": [], "meta": {}, "answers": {}, "open_answers": {}, "cur": 0, "start": None,
    "duration": 0, "result": None, "saved": False, "self_scores": {}, "ai_grades": None, "qtime": {}, "q_last": None,
    "sel_week": 1, "sel_month": 1, "scope_tab": "week",
    "leaf_subject": None,
}


def init():
    for k, v in DEFAULTS.items():
        if k not in st.session_state:
            st.session_state[k] = copy.deepcopy(v)


def nav(page, **kw):
    """on_click callback: sayfa değiştir."""
    st.session_state.page = page
    for k, v in kw.items():
        st.session_state[k] = v


def reset_exam():
    for k in ("questions", "meta", "answers", "open_answers", "cur", "start", "duration", "result", "saved", "self_scores", "ai_grades", "qtime", "q_last"):
        st.session_state[k] = copy.deepcopy(DEFAULTS[k])
'''
MODULES['ui/setup'] = r'''# -*- coding: utf-8 -*-
import time
import random
import uuid
import streamlit as st
from core import curriculum as cur, oyss as oy, ai_engine as ai, store, pdf_export
from . import theme
from .state import nav, reset_exam

SEC_PER_Q = 90  # eski kodla aynı: soru başına 90 sn

GRADE_CARDS = [
    ("4", "teal", "🎒", "4. Sınıf", "İlkokul son sınıf • Maarif Modeli"),
    ("5", "blue", "📘", "5. Sınıf", "Ortaokula giriş • 36 hafta"),
    ("6", "violet", "🧪", "6. Sınıf", "Beceri temelli müfredat"),
    ("7", "pink", "🚀", "7. Sınıf", "LGS'ye hazırlık basamağı"),
    ("8", "orange", "🎯", "8. Sınıf", "Sınıf müfredatı • 36 hafta"),
    ("LGS", "red", "🏆", "LGS Hazırlık", "80 soruluk deneme • 8. sınıf müfredatı"),
]


# ------------------------------------------------------------------ ana sayfa
def home():
    st.markdown("<div class='hero'><h1>🎓 Denemematik</h1><p>Yapay zekâ ile sınırsız, her seferinde farklı MEB yeni nesil soruları. "
                "Önce sınıfını seç.</p></div>", unsafe_allow_html=True)
    try:
        from . import study
        study.strip()
    except Exception:
        pass
    try:  # yalnızca sorun varsa görünen küçük not
        ps = ai.pool_status()
        if ps.get("bad_keys"):
            st.caption("⚠️ Anahtarlardan biri geçersiz görünüyor; diğerleri kullanılıyor. secrets.toml'u kontrol et.")
        elif ps.get("cooling", 0) >= 8:
            st.caption("⏳ Bazı yapay zekâ modelleri kısa süre dinleniyor; üretim biraz yavaşlayabilir.")
    except Exception:
        pass
    st.markdown("<div class='sec-title'>🎓 Sınıfını Seç</div>", unsafe_allow_html=True)
    theme.cells(GRADE_CARDS, 3, lambda c: theme.card(f"g{c[0]}", c[1], f"{c[2]} {c[3]}", c[4], pick_grade, (c[0],)))
    st.markdown("<div class='sec-title'>🧰 Araçlar</div>", unsafe_allow_html=True)
    tools = [("leaf", "green", "📄 Yaprak Test", "Tek kazanımlık hızlı çalışma kâğıdı + PDF", "leaf_start"),
             ("review", "teal", "🔁 Günlük Tekrar", "Yanlışların tam zamanında geri gelir (aralıklı tekrar)", "review"),
             ("plan", "violet", "🗓️ Çalışma Planım", "Zayıf kazanımlarına göre 7 günlük kişisel plan", "plan"),
             ("reports", "indigo", "📊 Performans & Raporlar", "Grafikler, ders karşılaştırmaları", "reports"),
             ("archive", "amber", "🗂️ Yanlış Arşivim", "Yanlış yaptığın sorulardan kişisel test", "archive"),
             ("badges", "slate", "🏅 Rozet & Sertifika", "Başarılarını topla, sertifika al", "badges")]
    theme.cells(tools, 3, lambda x: theme.card(f"tool_{x[0]}", x[1], x[2], x[3], _tool_go, (x[4],)))


def _tool_go(page):
    if page == "leaf_start":
        st.session_state.wz = {"step": 1}
        st.session_state.mode = "leaf"
        st.session_state.page = "setup"
        if not st.session_state.grade:
            st.session_state.grade = "5"
    else:
        st.session_state.page = page


def pick_grade(g):
    st.session_state.grade = g
    st.session_state.page = "modes"
    st.session_state.wz = {"step": 1}


def pick_mode(m):
    st.session_state.mode = m
    st.session_state.page = "setup"
    st.session_state.wz = {"step": 1}


# ------------------------------------------------------------------ mod seçimi
def modes():
    g = st.session_state.grade
    gl = cur.GRADE_LABELS[g]
    st.button("⬅ Sınıf seçimi", key="back_modes", on_click=nav, args=("home",))
    st.markdown(f"<div class='hero'><h1>{gl}</h1><p>Hangi sınav türünü çözmek istersin?</p></div>", unsafe_allow_html=True)
    official = g in oy.OFFICIAL_GRADES
    full = "Resmî LGS (90 soru, 155 dk) dâhil hazır formatlar" if g in ("8", "LGS") else "Mini 20 • Standart 40 • Tam 60 soru"
    items = [
        ("weekly", "blue", "📅 Haftalık Deneme", f"36 haftanın her biri için • {full}"),
        ("agis", "indigo", "🗓️ AGİS", "Akademik Gelişim İzleme Sınavı • ayın ilk haftasında, önceki ayı ölçer"),
        ("oyss", "orange", "📝 MEB OYSS Genel Deneme",
         "Ortak Yazılı Sınav • 5 senaryo • 100 puan • 40 dk" if official else "OYSS formatında antrenman (resmî uygulama 5-6-7. sınıfta)"),
        ("topic", "violet", "🎯 Konu Tarama", "Ünite ve kazanım seç • 10-30 soru"),
        ("bank", "pink", "🧠 Yeni Nesil Soru Bankası", "Beceri temelli • görsel ve veri yoğun karma sorular"),
        ("leaf", "green", "📄 Yaprak Test", "Tek kazanım • 6-12 soru • PDF'e hazır"),
    ]
    theme.cells(items, 3, lambda x: theme.card(f"m_{x[0]}", x[1], x[2], x[3], pick_mode, (x[0],)))


# ------------------------------------------------------------------ ortak bileşenler
def difficulty_select(key):
    return theme.pick_cards(f"v_{key}", cur.DIFFICULTIES, cur.DIFFICULTIES[2], 3, "dif", label="📊 Soru Zorluk Derecesi (Kademe Seçimi)")


WEIGHTS = [0.5, 0.75, 1.0, 1.25, 1.5, 2.0]


def _auto_weights(g):
    per = {}
    for h in store.history():
        if h["grade"] == g:
            for s, d in h["per"].items():
                per.setdefault(s, []).append(d["pct"])
    out = {}
    for s, v in per.items():
        a = sum(v[-3:]) / len(v[-3:])
        out[s] = 1.5 if a < 50 else 1.25 if a < 70 else 0.75 if a > 90 else 1.0
    return out


def weight_panel(g, key, boxed=True):
    """Ders ağırlıkları: soru sayısını çarpan. Otomatik mod, geçmiş başarına göre zayıf derslere ağırlık verir."""
    auto = st.toggle("📉 Zayıf derslerime otomatik ağırlık ver (geçmiş sınavlarıma göre)", key=f"auto_{key}")
    aw = _auto_weights(g) if auto else {}
    out = {}
    import contextlib
    with (st.expander("⚖️ Ders ağırlıkları (soru sayısını çarpan)", expanded=auto) if boxed else contextlib.nullcontext()):
        def _w(s):
            out[s] = st.select_slider(f"{cur.SUBJECT_ICONS.get(s, '')} {s}", WEIGHTS, value=aw.get(s, 1.0),
                                      key=f"w_{key}_{s}_{int(auto)}", format_func=lambda x: f"×{x:g}")
        theme.cells(cur.subjects_for(g), 2, _w)
    return out


def subject_counts(g, defaults, key):
    out = {}
    with st.expander("⚙️ Ders başına soru sayıları", expanded=False):
        def _c(s):
            out[s] = st.number_input(f"{cur.SUBJECT_ICONS.get(s, '')} {s}", 0, 40, int(defaults.get(s, 0)), key=f"{key}_{s}")
        theme.cells(cur.subjects_for(g), 2, _c)
    out = {k: v for k, v in out.items() if v > 0}
    st.caption(f"Toplam: **{sum(out.values())} soru** • Süre: **{sum(out.values()) * SEC_PER_Q // 60} dk** (soru başına 90 sn)")
    return out


def _avoid():
    return store.recent_stems()


def _finish(qs, errs, meta):
    want = sum(int(b[1]) for b in meta.get("briefing", []) if len(b) > 1 and str(b[1]).isdigit()) if meta.get("kind") == "mc" else 0
    if errs and not (want and len(qs) >= want):  # istenen sayıya ulaşıldıysa uyarı gösterme
        st.warning("⚠️ " + " | ".join(errs[:4]))
    if not qs:
        st.error("❌ Soru üretilemedi. API anahtarlarınızı/bağlantıyı kontrol edin.")
        return
    reset_exam()
    meta["id"] = uuid.uuid4().hex[:8]
    meta["n"] = len(qs)
    if meta["kind"] == "mc" and "duration_sec" not in meta:
        meta["duration_sec"] = len(qs) * SEC_PER_Q
    st.session_state.questions = qs
    st.session_state.meta = meta
    store.add_stems(qs)
    st.session_state.page = "ready"
    st.rerun()


def _meta_common(gl, mode, title, scope, diff, plan):
    n = sum(p["n"] for p in plan)
    return {"grade": st.session_state.grade, "grade_label": gl, "mode": mode, "title": title, "scope": scope, "difficulty": diff,
            "kind": "mc", "subtitle": f"{scope} • {diff.split('/')[0][2:].strip()}", "info_line": f"{n} soru • {n * SEC_PER_Q // 60} dk",
            "briefing": [(p["subject"], p["n"], p.get("short", p["topics"])) for p in plan]}


def with_overlay(seconds, title, sub, fn):
    """Uzun işlemi, ekran ortasında geriye sayan daire ile çalıştırır."""
    ph = st.empty()
    ph.markdown(theme.overlay_html(seconds, title, sub), unsafe_allow_html=True)
    try:
        return fn()
    finally:
        ph.empty()


def est_seconds_mc(plan):
    import math
    chunks = sum(math.ceil(p["n"] / ai.CHUNK) for p in plan)
    waves = math.ceil(chunks / ai.WORKERS)
    try:
        per = float(store.settings().get("gen_wave_s", 0)) or 10.0
    except Exception:
        per = 10.0
    return int(max(8, min(120, 4 + per * waves)))


def with_overlay_progress(seconds, title, sub, fn):
    """Üretimi arka plan iş parçacığında çalıştırır; ekranda 'hazır %' rozetini canlı günceller. fn(on_progress) -> sonuç."""
    import threading
    ph, pill = st.empty(), st.empty()
    ph.markdown(theme.overlay_html(seconds, title, sub), unsafe_allow_html=True)
    box = {"d": 0, "t": 0, "res": None, "err": None}

    def cb(done, total, *_a):
        box["d"], box["t"] = done, total

    def run():
        try:
            box["res"] = fn(cb)
        except BaseException as e:  # noqa
            box["err"] = e

    th = threading.Thread(target=run, daemon=True)
    th.start()
    last = -1
    try:
        while th.is_alive():
            if box["t"] and box["d"] != last:
                last = box["d"]
                pill.markdown("<div style='position:fixed;left:50%;bottom:8%;transform:translateX(-50%);z-index:1000000;background:#0f172a;color:#fff;"
                              f"padding:.45rem 1.1rem;border-radius:99px;font-weight:800;font-size:.95rem'>⚡ %{min(100, int(100 * box['d'] / max(1, box['t'])))} hazır</div>", unsafe_allow_html=True)
            th.join(0.4)
    finally:
        ph.empty()
        pill.empty()
    if box["err"] is not None:
        raise box["err"]
    return box["res"]


def _remember_plan(plan, meta, scope_label):
    """Son 3 farklı sınav planını saklar; uygulama açılınca bankaları arka planda hazır tutulur."""
    try:
        e = {"plan": plan, "gl": meta["grade_label"], "diff": meta["difficulty"], "scope": scope_label}
        lst = [x for x in store.settings().get("recent_plans", []) if not (x.get("gl") == e["gl"] and x.get("diff") == e["diff"] and x.get("plan") == plan)]
        store.save_settings(recent_plans=([e] + lst)[:3])
    except Exception:
        pass


def _gen_mc(plan, meta, scope_label, focus="", use_bank=True):
    n = sum(p["n"] for p in plan)
    avoid = _avoid()  # Streamlit'e ait çağrılar ana iş parçacığında kalsın
    _t0 = time.time()
    qs, errs = with_overlay_progress(est_seconds_mc(plan), "Sorular hazırlanıyor", f"{n} yeni nesil soru ve görselleri yapay zekâ ile üretiliyor…",
                                     lambda cb: ai.generate_mc(plan, meta["grade_label"], meta["difficulty"], scope_label, avoid=avoid, focus=focus, use_bank=use_bank, on_progress=cb))
    try:  # ölçülen gerçek süre: sonraki geri sayım buna uyar (bankadan anında gelenler ölçüme katılmaz)
        import math
        _el = time.time() - _t0
        if _el > 6 and qs:
            _w = max(1, math.ceil(sum(math.ceil(p["n"] / ai.CHUNK) for p in plan) / ai.WORKERS))
            _old = float(store.settings().get("gen_wave_s", 0)) or (_el - 4) / _w
            store.save_settings(gen_wave_s=round(max(4.0, min(40.0, .5 * _old + .5 * (_el - 4) / _w)), 2))
    except Exception:
        pass
    if use_bank and qs and not focus.strip():  # sonraki sınav için bankayı arka planda tazele
        _remember_plan(plan, meta, scope_label)
        try:
            ai.bank_topup_async(plan, meta["grade_label"], meta["difficulty"], scope_label, qs)
        except Exception:
            pass
    _finish(qs, errs, meta)


# ------------------------------------------------------------------ sınav öncesi bilgilendirme
def pdf_bytes(with_solutions=True):
    key = (st.session_state.meta.get("id"), with_solutions)
    cache = st.session_state.setdefault("pdf_cache", {})
    if key not in cache:
        cache[key] = pdf_export.build_pdf(st.session_state.questions, st.session_state.meta, include_solutions=with_solutions)
    return cache[key]


def pdf_panel(prefix=""):
    """PDF indirme: önce hazırla, sonra indir (ağır işlem sadece isteyince)."""
    m = st.session_state.meta
    fn = "".join(ch if ch.isalnum() else "_" for ch in m.get("title", "deneme"))[:60] + ".pdf"
    c1, c2 = st.columns(2)
    with c1:
        if st.button("📄 PDF Hazırla (soru kitapçığı + cevap anahtarı)", key=f"{prefix}mkpdf"):
            with st.spinner("PDF hazırlanıyor…"):
                pdf_bytes(True)
    key = (m.get("id"), True)
    if key in st.session_state.get("pdf_cache", {}):
        with c2:
            st.download_button("⬇️ PDF'i İndir", st.session_state.pdf_cache[key], file_name=fn, mime="application/pdf", key=f"{prefix}dlpdf")


def pre():
    m = st.session_state.meta
    qs = st.session_state.questions
    if not qs:
        st.session_state.page = "home"
        st.rerun()
    st.markdown(f"<div class='hero'><h1>📋 Sınav Bilgilendirme</h1><p>{m['title']}</p></div>", unsafe_allow_html=True)
    k = st.columns(4)
    with k[0]:
        theme.kpi("Soru", len(qs))
    with k[1]:
        theme.kpi("Süre", f"{m['duration_sec'] // 60} dk")
    with k[2]:
        theme.kpi("Puan" if m["kind"] == "open" else "Zorluk", "100" if m["kind"] == "open" else m["difficulty"][:2])
    with k[3]:
        theme.kpi("Kapsam", m["scope"][:22])
    st.markdown("<div class='sec-title'>Bu sınavda hangi dersler ve konular çıkacak?</div>", unsafe_allow_html=True)
    theme.html_table(["Ders", "Soru", "Konu / Kazanım"], [(f"{cur.SUBJECT_ICONS.get(s, '')} {s}", n, t) for s, n, t in m["briefing"]], num_cols=(1,))
    if m["kind"] == "open":
        for t in m.get("oyss_tables", []):
            with st.expander(f"{t['subject']} • Senaryo {m['scenario']} kazanım-soru dağılımı", expanded=False):
                theme.html_table(["Kazanım", "Ünite / Konu", "Soru"], [(r["code"], r["topic"], r["n"]) for r in t["rows"]], num_cols=(2,))
    pdf_panel("pre_")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🎯 Sınavı Şimdi Başlat", key="start_exam", type="primary"):
            import time
            st.session_state.start = time.time()
            st.session_state.page = "exam"
            st.rerun()
    with c2:
        st.button("↩ Vazgeç", key="back_pre", on_click=nav, args=("home",))


# ------------------------------------------------------------------ sorular hazır: kocaman BAŞLAT
def _start_now():
    import time
    st.session_state.start = time.time()
    st.session_state.page = "exam"


def ready():
    m, qs = st.session_state.meta, st.session_state.questions
    if not qs:
        st.session_state.page = "home"
        st.rerun()
    subs = sorted({q.get("subject", "") for q in qs})
    mins = m["duration_sec"] // 60
    st.markdown("<div class='ready-aura'></div>", unsafe_allow_html=True)
    dtxt = (m.get("difficulty") or "")
    dlab = f"{dtxt[:2]} {dtxt.split('/')[0][2:].strip()}" if dtxt else ""
    with st.container(key="ready_card"):
        st.markdown(f"<div class='ready-t'>✨ Sınavın hazır!</div><div class='ready-s'>{m['title']}</div>", unsafe_allow_html=True)
        st.button("▶\n\nBAŞLAT", key="bigstart", on_click=_start_now)
        st.markdown(f"<div class='ready-bar'><i></i></div><div class='ready-hint'>Hazır olduğunda dokun • süre başladığı anda işler</div>"
                    f"<div class='ready-chips'><span>📝 {len(qs)} soru</span><span>⏱ {mins} dk</span><span>{dlab}</span>"
                    f"<span>📚 {', '.join(cur.SUBJECT_ICONS.get(x, '') + ' ' + x for x in subs[:3])}{' +' + str(len(subs) - 3) if len(subs) > 3 else ''}</span></div>", unsafe_allow_html=True)
        b1, b2 = st.columns(2)
        with b1:
            st.button("📋 Konu özeti & PDF", key="ready_pre", on_click=nav, args=("pre",), use_container_width=True)
        with b2:
            st.button("↩ Vazgeç", key="ready_back", on_click=nav, args=("home",), use_container_width=True)
'''
MODULES['ui/wizard'] = r'''# -*- coding: utf-8 -*-
"""Sınıf seçiminden sonraki sade, adım adım ekranlar. Her sayfada tek karar; seçince otomatik ilerler."""
import streamlit as st
from core import curriculum as cur, oyss as oy, store
from . import theme
from .state import nav
from . import setup as su

RATIO = {cur.TR: 20, cur.MAT: 20, cur.FEN: 20, cur.SOS: 10, cur.INK: 10, cur.DIN: 10, cur.ING: 10}
OFFICIAL_IDS = ("lgs90", "sozel", "sayisal")


# ------------------------------------------------------------------ yardımcılar
def wz():
    return st.session_state.setdefault("wz", {"step": 1})


def go(**kw):
    """Seç ve sonraki adıma geç (on_click)."""
    w = wz()
    w.update(kw)
    w["step"] = w.get("step", 1) + 1


def setv(**kw):
    wz().update(kw)


def back(first_page):
    w = wz()
    if w.get("step", 1) > 1:
        w["step"] -= 1
    else:
        st.session_state.page = first_page


def toggle_in(field, val):
    w = wz()
    lst = list(w.get(field) or [])
    if val in lst:
        lst.remove(val)
    else:
        lst.append(val)
    w[field] = lst


def head(title, sub, labels):
    step = wz().get("step", 1)
    pills = "".join(f"<span class='stp {'on' if i == step else 'done' if i < step else ''}'>{i}. {l}</span>" for i, l in enumerate(labels, 1))
    st.markdown(f"<div class='wz-head'><div class='wz-title'>{title}</div><div class='wz-sub'>{sub}</div><div class='stepper'>{pills}</div></div>", unsafe_allow_html=True)


def choice(key, icon, title, desc, selected=False, cb=None, args=(), kwargs=None):
    st.button(f"{icon} {title}\n\n{desc}", key=f"opt{'sel' if selected else ''}_{key}", on_click=cb, args=args, kwargs=kwargs or {}, use_container_width=True)


def footer(first_page="modes", nxt=None, nxt_label="İleri →", disabled=False):
    step = wz().get("step", 1)
    c1, c2 = st.columns(2)
    with c1:
        st.button("← Geri", key=f"wz_back_{step}", on_click=back, args=(first_page,))
    if nxt:
        with c2:
            st.button(nxt_label, key=f"wz_next_{step}", on_click=nxt, disabled=disabled)


def main_subjects(g):
    return [s for s in cur.subjects_for(g) if s != cur.ALM]


def ratio_counts(g, total):
    subs = main_subjects(g)
    tot = sum(RATIO[s] for s in subs)
    raw = {s: total * RATIO[s] / tot for s in subs}
    out = {s: int(v) for s, v in raw.items()}
    for s in sorted(subs, key=lambda x: raw[x] - out[x], reverse=True)[: total - sum(out.values())]:
        out[s] += 1
    return out


def formats(g):
    """Gerçek sınav yapısına uygun hazır formatlar."""
    if g in ("8", "LGS"):
        sozel = {cur.TR: 20, cur.INK: 10, cur.DIN: 10, cur.ING: 10}
        say = {cur.MAT: 20, cur.FEN: 20}
        return [
            dict(id="lgs90", icon="🏆", title="Resmî LGS", desc="90 soru • 155 dk • Türkçe 20, Mat 20, Fen 20, İnkılap 10, Din 10, İng 10", counts=cur.LGS_OFFICIAL, min=155),
            dict(id="sozel", icon="📖", title="Sözel oturum", desc="50 soru • 75 dk • Türkçe, İnkılap, Din, İngilizce", counts=sozel, min=75),
            dict(id="sayisal", icon="🔢", title="Sayısal oturum", desc="40 soru • 80 dk • Matematik, Fen Bilimleri", counts=say, min=80),
            dict(id="lgs80", icon="🎯", title="80 soruluk deneme", desc="Türkçe 15, Mat 15, Fen 15, İnkılap 15, Din 10, İng 10", counts=cur.weekly_counts("LGS"), min=120),
            dict(id="mini", icon="⚡", title="Mini deneme", desc="30 soru • 50 dk • oransal dağılım", counts=ratio_counts(g, 30), min=50),
        ]
    return [
        dict(id="mini", icon="⚡", title="Mini deneme", desc="20 soru • 30 dk", counts=ratio_counts(g, 20), min=30),
        dict(id="std", icon="🎯", title="Standart deneme", desc="40 soru • 60 dk", counts=ratio_counts(g, 40), min=60),
        dict(id="tam", icon="🏆", title="Tam deneme", desc="60 soru • 90 dk", counts=ratio_counts(g, 60), min=90),
    ]


def subject_cards(prefix, g, w):
    """Tek dokunuşla ders seç -> sonraki ekran. 'Tüm dersler' kartı da var."""
    subs = cur.subjects_for(g)
    cards = [(s, cur.SUBJECT_ICONS.get(s, ""), s, "", [s]) for s in subs] + [("all", "🌟", "Tüm dersler", "hepsi birden", list(subs))]
    cur_sel = w.get("subs") or []
    theme.cells(cards, 4, lambda c: choice(f"{prefix}_{c[0]}", c[1], c[2], c[3], cur_sel == c[4], go, kwargs=dict(subs=c[4])))


# ------------------------------------------------------------------ giriş
def run():
    try:
        _run()
    except Exception as e:  # beklenmeyen durumda sihirbazı sıfırla
        st.session_state.wz = {"step": 1}
        st.warning(f"Bir şey ters gitti, adım başa alındı. ({type(e).__name__})")
        st.button("Yeniden başla", key="wz_reset", type="primary")


def _run():
    mode = st.session_state.mode
    {"weekly": weekly, "agis": weekly, "oyss": oyss, "topic": topic, "leaf": topic, "bank": bank}.get(mode, weekly)()


# ------------------------------------------------------------------ HAFTALIK DENEME  /  AGİS (aylık)
def weekly():
    g = st.session_state.grade
    gl = cur.GRADE_LABELS[g]
    w = wz()
    agis = st.session_state.mode == "agis"
    step = w.get("step", 1)
    if step >= 3 and not (w.get("month") if agis else w.get("week")) or (step >= 4 and not w.get("fmt")):
        w.clear(); w["step"] = step = 1
    if agis:
        head(f"🗓️ {gl} • AGİS", "Akademik Gelişim İzleme Sınavı • ayın ilk haftasında çözülür, önceki ayı ölçer", ["Ay", "Format", "Üret"])
    else:
        head(f"📅 {gl} • Haftalık Deneme", "36 öğretim haftasının her biri için bir deneme", ["Hafta", "Format", "Üret"])
    if step == 1:
        if not agis:
            cw = cur.current_week()
            dflt = 1 if (not cw or cw <= 18) else 2
            term = theme.pick_cards("v_wterm", [1, 2], dflt, 2, "dif",
                                    label_fn=lambda t: "📘 1. Dönem\nEylül – Ocak • 1-18. hafta" if t == 1 else "📗 2. Dönem\nŞubat – Haziran • 19-36. hafta",
                                    label="Hangi dönem?")
            st.markdown(f"<div class='pick-lbl'>{term}. Dönem • hafta seç <small style='color:#64748b;font-weight:600'>(📍 = bu hafta • seçince otomatik ilerler)</small></div>", unsafe_allow_html=True)
            weeks = range((term - 1) * 18 + 1, term * 18 + 1)

            def _wk(n):
                a = cur.WEEK_STARTS[n - 1]
                st.button(f"{'📍 ' if n == cw else ''}{n}. Hafta\n{cur.fmt_date(a)}", key=f"sel_{'on' if w.get('week') == n else 'off'}_w{n}", on_click=go, kwargs=dict(week=n))
            theme.cells(weeks, 6, _wk)
        else:
            sug = cur.suggested_month()
            st.markdown("#### Ay seç")
            st.info(f"📌 AGİS ayın ilk haftasında çözülür ve **bir önceki ayı** ölçer. Bugüne göre önerilen: **{cur.MONTHS[sug - 1]['name']}**.")
            term = theme.pick_cards("v_mterm", [1, 2], 1 if sug <= 5 else 2, 2, "dif",
                                    label_fn=lambda t: "📘 1. Dönem\nEylül – Ocak" if t == 1 else "📗 2. Dönem\nŞubat – Haziran", label="Hangi dönem?")
            rng = range(1, 6) if term == 1 else range(6, cur.NUM_MONTHS + 1)
            st.markdown(f"<div class='pick-lbl'>{term}. Dönem • ay seç <small style='color:#64748b;font-weight:600'>(📌 = önerilen • seçince otomatik ilerler)</small></div>", unsafe_allow_html=True)
            theme.cells(rng, 5, lambda m: st.button(f"{'📌 ' if m == sug else ''}{cur.MONTHS[m - 1]['name']}\n{cur.MONTHS[m - 1]['a']}-{cur.MONTHS[m - 1]['b']}. hafta",
                                                    key=f"sel_{'on' if w.get('month') == m else 'off'}_m{m}", on_click=go, kwargs=dict(month=m)))
        footer("modes")
    elif step == 2:
        if agis:
            st.caption(f"🗓️ {cur.month_note(w['month'])}")
        else:
            st.caption(f"📆 {w['week']}. hafta • {cur.week_dates(w['week'])}")
        st.markdown("#### Kaç soruluk deneme?")
        fm = formats(g)
        theme.cells(fm, 3 if len(fm) > 3 else len(fm), lambda f: choice(f"fmt_{f['id']}", f["icon"], f["title"], f["desc"], w.get("fmt") == f["id"], go, kwargs=dict(fmt=f["id"])))
        footer("modes")
    else:
        scope = cur.month_scope(w["month"]) if agis else {"type": "week", "w": w["week"]}
        label = cur.scope_label(scope)
        f = next((x for x in formats(g) if x["id"] == w.get("fmt")), formats(g)[0])
        st.markdown(f"#### ✅ Özet: **{label}** • **{f['title']}**")
        counts = dict(f["counts"])
        official = f["id"] in OFFICIAL_IDS
        wts = {}
        with st.expander("⚙️ Gelişmiş (isteğe bağlı — dokunmasan da olur)", expanded=False):
            diff = su.difficulty_select("diff_wz")
            if not official:
                wts = su.weight_panel(g, f"wz_{g}", boxed=False)
            focus = st.text_input("🔍 Özel konu (isteğe bağlı)", key="focus_wz", placeholder="Örn: Açılar, Hücre, Paragraf…")
        if not official:
            counts = {s: max(0, round(n * wts.get(s, 1.0))) for s, n in counts.items()}
            counts = {s: n for s, n in counts.items() if n > 0}
        n = sum(counts.values())
        same = all(abs(wts.get(s, 1.0) - 1.0) < 1e-9 for s in wts)
        minutes = f["min"] if same else max(1, n * su.SEC_PER_Q // 60)
        rows = [(f"{cur.SUBJECT_ICONS.get(s, '')} {s}", c, cur.scope_short(g, s, scope) or "—") for s, c in counts.items()]
        theme.html_table(["Ders", "Soru", "Kapsanan üniteler"], rows, num_cols=(1,))
        st.caption(f"Toplam **{n} soru** • süre **{minutes} dk**")
        plan = [{"subject": s, "n": c, "topics": cur.scope_topic_text(g, s, scope), "short": cur.scope_short(g, s, scope)} for s, c in counts.items()]
        go_btn = st.button("🚀 Soruları Üret", key="gen_wz", type="primary", use_container_width=True)
        st.button("← Geri", key="wz_back_4", on_click=back, args=("modes",), use_container_width=True)
        if go_btn and counts:
            title = f"{gl} {label} • {f['title']}"
            meta = su._meta_common(gl, "agis" if agis else "weekly", title, label, diff, plan)
            meta["duration_sec"] = minutes * 60
            meta["info_line"] = f"{n} soru • {minutes} dk"
            su._gen_mc(plan, meta, label, focus)


# ------------------------------------------------------------------ OYSS
def oyss():
    g = st.session_state.grade
    gl = cur.GRADE_LABELS[g]
    w = wz()
    step = w.get("step", 1)
    head(f"📝 {gl} • MEB OYSS", f"Ortak Yazılı Sınav: açık uçlu + kısa cevaplı • {oy.TOTAL_POINTS} puan • {oy.DURATION_MIN} dk • en fazla {oy.MAX_PAGES} sayfa", ["Dönem", "Senaryo", "Ders", "Üret"])
    if g not in oy.OFFICIAL_GRADES and step == 1:
        st.warning(f"ℹ️ OYSS resmî olarak 5-6-7. sınıflarda uygulanır. {gl} için bu bölüm OYSS formatında antrenmandır.")
    if step == 1:
        st.markdown("#### Hangi yazılı?")
        def _yz(ty):
            t, y = ty
            a, b = oy.window_weeks(t, y)
            choice(f"oy_{t}{y}", "📄", f"{t}. Dönem {y}. Yazılı", f"Hafta {a}-{b}", w.get("term") == t and w.get("yaz") == y, go, kwargs=dict(term=t, yaz=y))
        theme.cells([(1, 1), (1, 2), (2, 1), (2, 2)], 2, _yz)
        footer("modes")
    elif step == 2:
        st.markdown("#### Senaryo seç")
        st.caption("Senaryo, hangi kazanımdan kaç soru çıkacağını belirleyen dağılım şablonudur.")
        theme.cells(list(oy.SCENARIOS), 3, lambda s: choice(f"sc_{s}", "🎲", f"Senaryo {s}", oy.profile_name(s), w.get("scen") == s, go, kwargs=dict(scen=s)))
        footer("modes")
    elif step == 3:
        st.markdown("#### Hangi ders?")
        st.caption("Dokunman yeterli, otomatik ilerler. Her ders ayrı bir yazılı kâğıdıdır.")
        subject_cards("os", g, w)
        footer("modes")
    else:
        if not all(k in w for k in ("term", "yaz", "scen", "subs")):
            w.clear(); w["step"] = 1
            st.rerun()
        t, yz, sc = w["term"], w["yaz"], w["scen"]
        tables = []
        for s in w["subs"]:
            tb = oy.scenario_table(g, s, t, yz, sc)
            tables.append({"subject": s, **tb})
        st.markdown(f"#### ✅ Özet: **{t}. Dönem {yz}. Yazılı • Senaryo {sc}**")
        rows = [(f"{cur.SUBJECT_ICONS.get(x['subject'], '')} {x['subject']}", x["total"], "✅ MEB/ÖDSGM tablosu" if x["verified"] else "🧩 MEB şablonuna göre türetildi") for x in tables]
        theme.html_table(["Ders", "Soru", "Dağılım kaynağı"], rows, num_cols=(1,))
        for x in tables:
            with st.expander(f"{x['subject']} • kazanım-soru dağılımı"):
                theme.html_table(["Kazanım", "Ünite / Konu", "Soru"], [(r["code"], r["topic"], r["n"]) for r in x["rows"]], num_cols=(2,))
        diff = su.difficulty_select("diff_oyss")
        go_btn = st.button("🚀 OYSS Sorularını Üret", key="gen_oyss", type="primary", use_container_width=True)
        st.button("← Geri", key="wz_back_4", on_click=back, args=("modes",), use_container_width=True)
        if go_btn:
            from core import ai_engine as ai
            qs, errs = su.with_overlay(15 + 14 * len(tables), "OYSS soruları hazırlanıyor", "Açık uçlu ve kısa cevaplı sorular ile puanlama anahtarları yazılıyor…",
                                       lambda: ai.generate_oyss(tables, gl, diff, avoid=store.recent_stems()))
            meta = {"grade": g, "grade_label": gl, "mode": "oyss", "kind": "open", "title": f"{gl} OYSS {t}. Dönem {yz}. Yazılı • Senaryo {sc}",
                    "scope": f"{t}. Dönem {yz}. Yazılı", "difficulty": diff, "scenario": sc, "term": t, "yazili": yz,
                    "subtitle": f"MEB Ortak Yazılı Sınav Sistemi • Senaryo {sc} • {oy.TOTAL_POINTS} puan • {oy.DURATION_MIN} dk",
                    "info_line": f"{len(qs)} soru • {oy.TOTAL_POINTS} puan", "duration_sec": oy.DURATION_MIN * 60 * len(tables), "oyss_tables": tables,
                    "briefing": [(x["subject"], x["total"], "; ".join(f"{r['code']}×{r['n']}" for r in x["rows"])) for x in tables]}
            su._finish(qs, errs, meta)


# ------------------------------------------------------------------ KONU TARAMA / YAPRAK TEST
def topic():
    g = st.session_state.grade
    leaf = st.session_state.mode == "leaf"
    w = wz()
    step = w.get("step", 1)
    if leaf:
        grades = ["4", "5", "6", "7", "8"]
        if g not in grades:
            g = st.session_state.grade = "5"
    gl = cur.GRADE_LABELS[g]
    head(("📄 Yaprak Test" if leaf else "🎯 Konu Tarama") + f" • {gl}", "Tek bir kazanıma odaklı kısa test." if leaf else "Ünite ve kazanım seç, kazanım kazanım çalış.", ["Ders", "Ünite", "Kazanım", ])
    first = "home" if leaf else "modes"
    if step == 1:
        if leaf:
            theme.cells(grades, 3, lambda x: choice(f"lg_{x}", "🎓", cur.GRADE_LABELS[x], "", x == g, lambda x=x: st.session_state.update(grade=x)))
        st.markdown("#### Hangi ders?")
        subs = cur.subjects_for(g)
        theme.cells(subs, 4, lambda s: choice(f"ts_{s}", cur.SUBJECT_ICONS.get(s, ""), s, "", w.get("subj") == s, go, kwargs=dict(subj=s, unit=None, tops=None)))
        footer(first)
    elif step == 2:
        st.markdown(f"#### {w['subj']} • Hangi ünite?")
        us = cur.units(g, w["subj"])
        theme.cells(list(enumerate(us)), 3, lambda it: choice(f"tu_{it[0]}", "📚", it[1][0].split(" (MAT")[0][:60], f"{len(it[1][1])} kazanım", w.get("unit") == it[1][0], go, kwargs=dict(unit=it[1][0], tops=None)))
        footer(first)
    else:
        tps = dict(cur.units(g, w["subj"])).get(w.get("unit"))
        if not tps:
            w["step"] = 1
            st.rerun()
        st.markdown(f"#### {w['unit'].split(' (MAT')[0]} • Kazanımlar ve soru sayısı")
        st.caption("Kazanım kartlarına dokunarak seç (birden fazla seçebilirsin). Hiçbiri seçili değilse ünitenin tamamı gelir.")
        sel = [t for t in (w.get("tops") or []) if t in tps]
        if sel != (w.get("tops") or []):
            w["tops"] = sel
        items = [("all", "📚", "Ünitenin tamamı", f"{len(tps)} kazanım", not sel)] + [(str(i), "🎯", t[:110], "seçildi ✓" if t in sel else "dokun ve seç", t in sel) for i, t in enumerate(tps)]

        def _tp(it):
            i = it[0]
            choice(f"tk_{i}", it[1], it[2], it[3], it[4], (lambda: setv(tops=[])) if i == "all" else toggle_in, args=() if i == "all" else ("tops", tps[int(i)]))
        theme.cells(items, 2, _tp)
        chosen = sel
        opts = [6, 8, 10, 12] if leaf else [10, 15, 20, 30]
        n = theme.pick_cards("v_wz_n_" + st.session_state.mode, opts, opts[2 if leaf else 1], 4, "cnt", label_fn=lambda x: f"{x}\nsoru", label="🔢 Kazanım soru sayısı")
        diff = su.difficulty_select("diff_tp")
        go_btn = st.button("🚀 Testi Üret", key="gen_tp", type="primary", use_container_width=True)
        st.button("← Geri", key="wz_back_3", on_click=back, args=(first,), use_container_width=True)
        if go_btn:
            tt = chosen or tps
            plan = [{"subject": w["subj"], "n": n, "topics": f"{w['unit']}: " + ", ".join(tt), "short": ", ".join(tt)}]
            unit_short = w["unit"].split(" (MAT")[0]
            meta = su._meta_common(gl, "leaf" if leaf else "topic", f"{gl} {w['subj']} " + ("Yaprak Test" if leaf else f"Konu Tarama • {unit_short}"),
                                   ", ".join(tt) if leaf else unit_short, diff, plan)
            meta["topic_info"] = {"subject": w["subj"], "unit": w["unit"]}
            su._gen_mc(plan, meta, w["unit"])


# ------------------------------------------------------------------ SORU BANKASI
def bank():
    import random
    g = st.session_state.grade
    gl = cur.GRADE_LABELS[g]
    w = wz()
    step = w.get("step", 1)
    head(f"🧠 {gl} • Yeni Nesil Soru Bankası", "Beceri temelli, görsel ve veri yoğun karma sorular.", ["Ders", "Format"])
    if step == 1:
        st.markdown("#### Hangi ders?")
        st.caption("Dokunman yeterli, otomatik ilerler.")
        subject_cards("bs", g, w)
        footer("modes")
    else:
        if not w.get("subs"):
            w["step"] = 1
            st.rerun()
        st.markdown("#### Ders başına kaç soru?")
        theme.cells([("a", "Mini", "ders başına 5 soru", 5), ("b", "Standart", "ders başına 10 soru", 10), ("c", "Yoğun", "ders başına 15 soru", 15)], 3,
                    lambda x: choice(f"bn_{x[0]}", "🧩", x[1], x[2], w.get("per", 10) == x[3], setv, kwargs=dict(per=x[3])))
        per = w.get("per", 10)
        bw = su.weight_panel(g, f"bk_{g}")
        diff = su.difficulty_select("diff_bk")
        go_btn = st.button("🚀 Testi Üret", key="gen_bk", type="primary", use_container_width=True)
        st.button("← Geri", key="wz_back_b2", on_click=back, args=("modes",), use_container_width=True)
        if go_btn:
            plan = []
            for s in w["subs"]:
                tp = cur.all_topics(g, s)
                pick = random.sample(tp, min(6, len(tp)))
                plan.append({"subject": s, "n": max(1, round(per * bw.get(s, 1.0))), "short": "Karma kazanımlar",
                             "topics": "; ".join(f"{u}: {t}" for u, t in pick) + " (görsel/tablo/grafik ağırlıklı, beceri temelli)"})
            su._gen_mc(plan, su._meta_common(gl, "bank", f"{gl} Yeni Nesil Soru Bankası", "Karma", diff, plan), "Yıl geneli karma", use_bank=False)
'''
MODULES['ui/exam'] = r'''# -*- coding: utf-8 -*-
import hashlib
import re
import time
import altair as alt
import pandas as pd
import streamlit as st
from core import curriculum as cur, store, ai_engine as ai, coach
from core.visuals import draw_geometry_shape
from . import theme
from .state import nav, reset_exam
from .setup import pdf_panel



# ------------------------------------------------------------------ kalem (not alma): istenince açılıp kapanan çizim katmanı
_PEN_JS = r"""
(function(){
if(window.__penV===2)return; window.__penV=2;
var _ob=document.getElementById('pen-bar');if(_ob)_ob.remove();var _oc=document.getElementById('pen-cv');if(_oc)_oc.remove();
var S={on:false,color:'#dc2626',tool:'pen',q:'',data:{},drawing:false,miss:0,cur:null};
var cv=null,ctx=null,bar=null,btns={};
function hostEl(){return document.querySelector('[data-testid="stMainBlockContainer"]')||document.querySelector('.block-container')||document.querySelector('[data-testid="stMain"]');}
function strokes(){return S.data[S.q]||(S.data[S.q]=[]);}
function drawStroke(s){
  var W=cv.width,e=s.t==='e';ctx.globalCompositeOperation=e?'destination-out':'source-over';
  ctx.lineCap='round';ctx.lineJoin='round';ctx.strokeStyle=s.c;ctx.lineWidth=e?18:3;ctx.beginPath();
  var p=s.p;ctx.moveTo(p[0][0]*W,p[0][1]);
  if(p.length===1)ctx.lineTo(p[0][0]*W+.1,p[0][1]+.1);
  for(var i=1;i<p.length;i++)ctx.lineTo(p[i][0]*W,p[i][1]);
  ctx.stroke();ctx.globalCompositeOperation='source-over';}
function redraw(){if(!cv)return;ctx.clearRect(0,0,cv.width,cv.height);var a=strokes();for(var i=0;i<a.length;i++)drawStroke(a[i]);}
function layout(){
  var h=hostEl();if(!h)return false;
  if(!cv){cv=document.createElement('canvas');cv.id='pen-cv';ctx=cv.getContext('2d');bind();}
  if(cv.parentNode!==h){if(getComputedStyle(h).position==='static')h.style.position='relative';h.appendChild(cv);}
  cv.style.cssText='position:absolute;left:0;top:0;z-index:50;display:none';
  var w=h.clientWidth,hh=h.scrollHeight;
  cv.style.display='block';
  cv.style.width=w+'px';cv.style.height=hh+'px';
  cv.style.pointerEvents=S.on?'auto':'none';cv.style.touchAction=S.on?'none':'auto';cv.style.cursor=S.on?'crosshair':'default';
  if(cv.width!==w||cv.height!==hh){cv.width=w;cv.height=hh;redraw();}
  return true;}
function measure(){ // tuval yüksekliği sayfanın GERÇEK içerik yüksekliğini şişirmesin
  var h=hostEl();if(!h||!cv)return;cv.style.display='none';var hh=h.scrollHeight,w=h.clientWidth;cv.style.display='block';
  if(cv.width!==w||cv.height!==hh){cv.style.width=w+'px';cv.style.height=hh+'px';cv.width=w;cv.height=hh;redraw();}}
function pos(e){var r=cv.getBoundingClientRect();return [(e.clientX-r.left)/cv.width,e.clientY-r.top];}
function bind(){
  cv.addEventListener('pointerdown',function(e){if(!S.on)return;e.preventDefault();try{cv.setPointerCapture(e.pointerId);}catch(x){}
    S.drawing=true;S.cur={c:S.color,t:S.tool==='eraser'?'e':'p',p:[pos(e)]};strokes().push(S.cur);drawStroke(S.cur);});
  cv.addEventListener('pointermove',function(e){if(!S.drawing||!S.cur)return;e.preventDefault();var a=pos(e),l=S.cur.p[S.cur.p.length-1];
    S.cur.p.push(a);ctx.globalCompositeOperation=S.cur.t==='e'?'destination-out':'source-over';ctx.lineCap='round';ctx.lineJoin='round';
    ctx.strokeStyle=S.cur.c;ctx.lineWidth=S.cur.t==='e'?18:3;ctx.beginPath();ctx.moveTo(l[0]*cv.width,l[1]);ctx.lineTo(a[0]*cv.width,a[1]);ctx.stroke();ctx.globalCompositeOperation='source-over';});
  function up(){S.drawing=false;S.cur=null;}
  cv.addEventListener('pointerup',up);cv.addEventListener('pointercancel',up);cv.addEventListener('pointerleave',up);}
function setOn(v){S.on=!!v;paintBar();layout();}
function paintBar(){
  if(!bar)return;
  btns.tog.style.background=S.on?'#7c3aed':'#fff';btns.tog.style.color=S.on?'#fff':'#0f172a';
  btns.tog.textContent=S.on?'✏️ Kalem: AÇIK':'✏️ Kalem';
  btns.tools.style.display=S.on?'flex':'none';
  ['#dc2626','#2563eb','#111827'].forEach(function(c,i){btns['c'+i].style.outline=(S.tool==='pen'&&S.color===c)?'3px solid #a78bfa':'none';});
  btns.er.style.outline=S.tool==='eraser'?'3px solid #a78bfa':'none';}
function mk(txt,css,fn){var b=document.createElement('button');b.type='button';b.textContent=txt;b.style.cssText='border:1px solid #cbd5e1;border-radius:999px;padding:.35rem .8rem;font-weight:800;font-size:.85rem;cursor:pointer;background:#fff;color:#0f172a;'+css;b.addEventListener('click',function(e){e.preventDefault();e.stopPropagation();fn();});return b;}
function buildBar(){
  bar=document.createElement('div');bar.id='pen-bar';
  btns.tools=document.createElement('div');btns.tools.style.cssText='display:none;align-items:center;gap:.35rem';
  ['#dc2626','#2563eb','#111827'].forEach(function(c,i){btns['c'+i]=mk('',  'width:26px;height:26px;padding:0;background:'+c+';border-color:'+c,function(){S.color=c;S.tool='pen';paintBar();});btns.tools.appendChild(btns['c'+i]);});
  btns.er=mk('🧽 Silgi','',function(){S.tool='eraser';paintBar();});btns.tools.appendChild(btns.er);
  btns.cl=mk('🗑️ Temizle','',function(){S.data[S.q]=[];redraw();});btns.tools.appendChild(btns.cl);
  btns.tog=mk('✏️ Kalem','',function(){setOn(!S.on);});
  bar.appendChild(btns.tog);bar.appendChild(btns.tools);place();paintBar();}
function place(){ // kalem, 'Sınavı Tamamla' düğmesinin yanındaki boşluğa; yoksa sağ alta sabit
  if(!bar)return;var sl=document.querySelector('.pen-slot');
  if(sl){if(bar.parentNode!==sl){sl.appendChild(bar);}
    bar.style.cssText='display:flex;align-items:center;gap:.4rem;flex-wrap:wrap;justify-content:flex-start;font-family:system-ui,sans-serif;min-height:2.5rem';}
  else{if(bar.parentNode!==document.body){document.body.appendChild(bar);}
    bar.style.cssText='position:fixed;right:14px;bottom:14px;z-index:1000001;display:flex;align-items:center;gap:.4rem;background:rgba(255,255,255,.96);padding:.4rem .5rem;border-radius:999px;box-shadow:0 8px 24px -6px rgba(0,0,0,.35);border:1px solid #e2e8f0;font-family:system-ui,sans-serif';}}
function show(v){if(bar){place();bar.style.display=v?'flex':'none';}if(cv)cv.style.display=v?'block':'none';}
window.__penSetQ=function(k){S.q=k;S.miss=0;if(!bar)buildBar();place();show(true);layout();redraw();};
setInterval(function(){
  var alive=!!document.querySelector('iframe[data-pen]');
  if(!alive){S.miss++;if(S.miss>=4&&bar&&bar.style.display!=='none'){S.on=false;S.data={};show(false);paintBar();}return;}
  S.miss=0;if(bar&&bar.style.display==='none')show(true);place();measure();
},600);
})();
"""


def _pen_html(key):
    import json
    return ("<script>(function(){var W=window.parent,D=W.document;"
            "try{window.frameElement.setAttribute('data-pen','1');}catch(e){}"
            "if(!W.__penV){var s=D.createElement('script');s.textContent=" + json.dumps(_PEN_JS) + ";D.head.appendChild(s);}"
            "if(W.__penSetQ)W.__penSetQ(" + json.dumps(str(key)) + ");})();</script>")


def _pen(key):
    """Soru sayfasında kalem: sağ alttaki düğmeyle açılır/kapanır; çizimler soru bazında saklanır."""
    try:
        import streamlit.components.v1 as components
        components.html(_pen_html(key), height=1)
    except Exception:
        pass


# ------------------------------------------------------------------ hesaplama
def compute_result():
    m, qs = st.session_state.meta, st.session_state.questions
    per, topics = {}, {}
    if m["kind"] == "mc":
        for i, q in enumerate(qs):
            s = q.get("subject", "Genel")
            ua = st.session_state.answers.get(i)
            d = per.setdefault(s, {"correct": 0, "wrong": 0, "empty": 0, "total": 0})
            d["total"] += 1
            tp = topics.setdefault(s, {}).setdefault(q.get("topic") or "Genel", [0, 0])
            tp[1] += 1
            if not ua:
                d["empty"] += 1
            elif ua == q["answer"]:
                d["correct"] += 1
                tp[0] += 1
            else:
                d["wrong"] += 1
        for s, d in per.items():
            d["net"] = round(d["correct"] - d["wrong"] / 3, 2)
            d["pct"] = round(100 * d["correct"] / d["total"], 1) if d["total"] else 0
        C = sum(d["correct"] for d in per.values())
        W = sum(d["wrong"] for d in per.values())
        E = sum(d["empty"] for d in per.values())
        T = len(qs)
        res = {"kind": "mc", "per": per, "topics": topics, "correct": C, "wrong": W, "empty": E, "total": T,
               "net": round(C - W / 3, 2), "pct": round(100 * C / T, 1) if T else 0}
    else:
        for i, q in enumerate(qs):
            s = q.get("subject", "Genel")
            got = float(st.session_state.self_scores.get(i, 0))
            d = per.setdefault(s, {"points": 0.0, "max": 0.0, "total": 0, "correct": 0, "wrong": 0, "empty": 0})
            d["points"] += got
            d["max"] += q.get("points", 0)
            d["total"] += 1
            tp = topics.setdefault(s, {}).setdefault(q.get("kazanim") or "Genel", [0, 0])
            tp[0] += got
            tp[1] += q.get("points", 0)
            if got >= q.get("points", 0) * .99:
                d["correct"] += 1
            elif not str(st.session_state.open_answers.get(i, "")).strip():
                d["empty"] += 1
            else:
                d["wrong"] += 1
        for d in per.values():
            d["pct"] = round(100 * d["points"] / d["max"], 1) if d["max"] else 0
            d["net"] = d["points"]
        P, Mx = sum(d["points"] for d in per.values()), sum(d["max"] for d in per.values())
        res = {"kind": "open", "per": per, "topics": {s: {k: [v[0], v[1]] for k, v in t.items()} for s, t in topics.items()},
               "correct": sum(d["correct"] for d in per.values()), "wrong": sum(d["wrong"] for d in per.values()),
               "empty": sum(d["empty"] for d in per.values()), "total": len(qs), "net": round(P, 1),
               "pct": round(100 * P / Mx, 1) if Mx else 0, "points": round(P, 1), "max": Mx}
    res["duration"] = st.session_state.duration
    try:
        tan = coach.time_analysis(qs, st.session_state.answers, st.session_state.get("qtime", {}), mc=(m["kind"] == "mc"))
        for sname, v in tan["avg"].items():
            if sname in per and v > 0:
                per[sname]["sec"] = round(v, 1)
        res["tan"] = tan
    except Exception:
        res["tan"] = None
    return res


def persist(res):
    m, qs = st.session_state.meta, st.session_state.questions
    store.add_attempt({"grade": m["grade"], "grade_label": m["grade_label"], "mode": m["mode"], "title": m["title"], "scope": m["scope"],
                       "difficulty": m["difficulty"], "kind": m["kind"], "per": res["per"], "topics": res["topics"], "net": res["net"],
                       "pct": res["pct"], "correct": res["correct"], "wrong": res["wrong"], "empty": res["empty"], "total": res["total"],
                       "duration": res["duration"], "topic_info": m.get("topic_info")})
    items = []
    for i, q in enumerate(qs):
        bad = False
        if m["kind"] == "mc":
            bad = st.session_state.answers.get(i) != q["answer"]
        else:
            bad = st.session_state.self_scores.get(i, 0) < q.get("points", 0) * .6
        if bad:
            key = hashlib.md5((q.get("subject", "") + q.get("question", "")).encode()).hexdigest()[:12]
            items.append({"key": key, "grade": m["grade"], "grade_label": m["grade_label"], "subject": q.get("subject", ""),
                          "topic": q.get("topic") or q.get("kazanim", ""), "q": q, "kind": m["kind"],
                          "user": st.session_state.answers.get(i) if m["kind"] == "mc" else st.session_state.open_answers.get(i, ""),
                          "ts": int(time.time()), "box": 0, "due": int(time.time()) + 86400})
    store.add_wrong(items)


def _tick(idx=None):
    """Soru başı süre: bir önceki ekranda geçen süreyi o soruya yazar."""
    S = st.session_state
    now = time.time()
    last = S.get("q_last")
    if last:
        qt = S.setdefault("qtime", {})
        qt[last[1]] = qt.get(last[1], 0) + min(now - last[0], 240)
    S.q_last = (now, idx) if idx is not None else None


def finish():
    _tick(None)
    st.session_state.duration = int(time.time() - (st.session_state.start or time.time()))
    if st.session_state.meta["kind"] == "open":
        st.session_state.page = "selfscore"
    else:
        st.session_state.result = compute_result()
        st.session_state.page = "result"


# ------------------------------------------------------------------ sınav ekranı
def _set_answer(idx):
    v = st.session_state.get(f"q_{idx}")
    if v:
        st.session_state.answers[idx] = v


def _set_open(idx):
    st.session_state.open_answers[idx] = st.session_state.get(f"open_{idx}", "")


def _go(delta=0, to=None):
    n = len(st.session_state.get("questions") or []) or 1
    c = to if to is not None else st.session_state.get("cur", 0) + delta
    st.session_state.cur = max(0, min(int(c), n - 1))


def _clear(idx):
    st.session_state.answers.pop(idx, None)
    st.session_state.pop(f"q_{idx}", None)


def _jump():
    _go(to=st.session_state.get("jump_sel", 0))


@st.fragment(run_every=1)
def timer_box(total, start):
    if st.session_state.get("page") != "exam" or not start:
        return
    rem = max(0, total - int(time.time() - start))
    h, mi, s = rem // 3600, (rem % 3600) // 60, rem % 60
    cls = "timer-box low" if rem < 300 else "timer-box"
    st.markdown(f"<div class='{cls}'>⏳ {h:02d}:{mi:02d}:{s:02d}</div>", unsafe_allow_html=True)
    if rem == 0:
        finish()
        st.rerun()


def exam():
    m, qs = st.session_state.meta, st.session_state.questions
    if not qs:
        st.session_state.page = "home"
        st.rerun()
    total = len(qs)
    idx = max(0, min(int(st.session_state.get("cur", 0) or 0), total - 1))
    st.session_state.cur = idx
    _tick(idx)
    q = qs[idx]
    h1, h2 = st.columns([2, 1])
    with h1:
        st.markdown(f"### 📋 {m['title']}")
        done = len(st.session_state.answers) if m["kind"] == "mc" else sum(1 for v in st.session_state.open_answers.values() if str(v).strip())
        st.markdown(f"<span class='badge'>Soru {idx + 1} / {total}</span><span class='badge'>Cevaplanan {done}</span>"
                    f"<span class='badge'>{m['difficulty'][:2]} {m['difficulty'].split('/')[0][2:].strip()}</span>", unsafe_allow_html=True)
        st.progress(done / total)
    with h2:
        timer_box(m["duration_sec"], st.session_state.start)
    st.markdown("---")
    st.markdown("<div class='question-card'>", unsafe_allow_html=True)
    sub = q.get("subject", "Genel")
    if q.get("kazanim") or q.get("topic"):
        st.caption(f"{cur.SUBJECT_ICONS.get(sub, '')} {sub} • {q.get('kazanim') or q.get('topic')}")
    pas = str(q.get("passage") or "").strip()
    if pas and pas.lower() != "null":
        st.markdown(f"<div class='passage-box'><b>📖 Metin / Öncül / Diyalog:</b><br>{pas}</div>", unsafe_allow_html=True)
    if isinstance(q.get("shape"), dict):
        draw_geometry_shape(q["shape"])
    if not isinstance(q.get("options"), dict) and m["kind"] == "mc":
        q["options"] = {"A": "-", "B": "-", "C": "-", "D": "-"}
    pts = f" ({q['points']} puan)" if q.get("points") else ""
    st.markdown(f"<p class='question-title'>Soru {idx + 1} [{sub}]{pts}:\n\n{q['question']}</p>", unsafe_allow_html=True)
    if m["kind"] == "mc":
        opts = q["options"]
        keys = list(opts)
        cv = st.session_state.answers.get(idx)
        st.radio(f"**Soru {idx + 1} Şıkları:**", keys, index=keys.index(cv) if cv in keys else None,
                 format_func=lambda x: f"{x}) {opts[x]}", key=f"q_{idx}", on_change=_set_answer, args=(idx,))
        st.button("🧹 Cevabı temizle", key=f"clr_{idx}", on_click=_clear, args=(idx,))
    else:
        st.text_area("Cevabınız", value=st.session_state.open_answers.get(idx, ""), height=180, key=f"open_{idx}",
                     on_change=_set_open, args=(idx,))
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<div class='nav-btn-container'>", unsafe_allow_html=True)
    n1, n2, n3 = st.columns([1, 1, 1])
    with n1:  # Sonraki üstte (telefonda alt alta dizilince de yukarıda kalır)
        if idx < total - 1:
            st.button("➡ Sonraki Soru", key="next", on_click=_go, args=(1,), type="primary", use_container_width=True)
    with n2:
        st.markdown(f"<div style='text-align:center;font-weight:900;color:#4c1d95;padding-top:.6rem'>Soru {idx + 1} / {total}</div>", unsafe_allow_html=True)
    with n3:
        if idx > 0:
            st.button("⬅️ Önceki Soru", key="prev", on_click=_go, args=(-1,), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("---")
    fb1, fb2 = st.columns([3, 2])
    with fb1:
        st.button("🏁 Deneme Sınavını Tamamla ve Sonuçları Gör", key="finish_btn", on_click=finish, type="primary")
    with fb2:
        st.markdown("<div class='pen-slot'></div>", unsafe_allow_html=True)
    _pen(f"{m.get('id', '')}:{idx}")


# ------------------------------------------------------------------ OYSS: yapay zekâ öğretmen değerlendirmesi
VERDICT_ICON = {"Tam": "🟢", "Kısmi": "🟡", "Yetersiz": "🔴", "Boş": "⚪"}


def selfscore():
    from . import setup as su
    m, qs = st.session_state.meta, st.session_state.questions
    st.markdown("<div class='hero'><h1>👩‍🏫 Yapay Zekâ Öğretmen Değerlendirmesi</h1><p>Cevap kâğıdın puanlama anahtarına göre adım adım okunuyor. "
                "Puanlar öneridir; katılmadığın bir soruda puanı kendin değiştirebilirsin.</p></div>", unsafe_allow_html=True)
    if st.session_state.get("ai_grades") is None:
        grades, errs = su.with_overlay(10 + 4 * len(qs), "Öğretmen kâğıdını okuyor", "Cevapların puanlama anahtarıyla karşılaştırılıyor…",
                                       lambda: ai.grade_open(qs, st.session_state.open_answers, m.get("grade_label", "")))
        st.session_state.ai_grades = grades
        st.session_state.ai_grade_errs = errs
    grades = st.session_state.ai_grades or {}
    if st.session_state.get("ai_grade_errs"):
        st.warning("⚠️ " + " | ".join(st.session_state.ai_grade_errs[:3]) + " — bu sorular için puanı kendin girebilirsin.")
    tot = sum(float(g.get("points", 0)) for g in grades.values())
    mx = sum(float(q.get("points", 0)) for q in qs)
    k = st.columns(3)
    with k[0]:
        theme.kpi("Öğretmen puanı", f"{tot:.1f} / {mx:.0f}")
    with k[1]:
        theme.kpi("Başarı", f"%{100 * tot / mx:.0f}" if mx else "—")
    with k[2]:
        theme.kpi("Değerlendirilen soru", len(grades))
    with st.form("selfscore_form"):
        for i, q in enumerate(qs):
            g = grades.get(i, {})
            ic = VERDICT_ICON.get(g.get("verdict"), "📝")
            with st.expander(f"{ic} Soru {i + 1} • {q.get('subject', '')} • {q.get('kazanim', '')} • {g.get('points', 0):g}/{q.get('points')} puan", expanded=(i == 0)):
                if q.get("passage"):
                    st.markdown(f"> {q['passage']}")
                if isinstance(q.get("shape"), dict):
                    draw_geometry_shape(q["shape"])
                st.markdown(f"**{q['question']}**")
                st.markdown(f"**Senin cevabın:** {st.session_state.open_answers.get(i) or '_(boş)_'}")
                if g.get("feedback"):
                    st.info(f"👩‍🏫 **Öğretmen yorumu:** {g['feedback']}" + (f"\n\n💡 {g['tip']}" if g.get("tip") else ""))
                st.success(f"**Beklenen cevap:** {q.get('answer', '')}")
                if q.get("rubric"):
                    theme.html_table(["Puanlama adımı", "Puan"], [(r.get("step", ""), r.get("points", "")) for r in q["rubric"] if isinstance(r, dict)], num_cols=(1,))
                st.number_input("Puan (gerekirse değiştir)", 0.0, float(q.get("points", 0)), float(g.get("points", 0)), step=0.5, key=f"self_in_{i}")
        ok = st.form_submit_button("📊 Sonucu Göster", type="primary")
    if ok:
        st.session_state.self_scores = {i: st.session_state.get(f"self_in_{i}", 0) for i in range(len(qs))}
        st.session_state.result = compute_result()
        st.session_state.page = "result"
        st.rerun()


# ------------------------------------------------------------------ sonuç
def _prev_attempt(m, current_id=None):
    for a in reversed(store.history()):
        if a["grade"] == m["grade"] and a["mode"] == m["mode"] and a["id"] != current_id:
            return a
    return None


def _report(q, flag):
    try:
        store.report_bad(q)
    except Exception:
        pass
    st.session_state[flag] = True


def _tip_of(q, n=150):
    t = re.sub(r"<[^>]+>|\s+", " ", str(q.get("explanation") or "")).strip()
    if not t:
        return ""
    cut = re.split(r"(?<=[.!?])\s", t, maxsplit=1)[0]
    return (cut if len(cut) <= n else cut[:n].rsplit(" ", 1)[0] + "…")


def _study_summary(res, qs, m):
    """Yanlış/boş soruları konuya göre gruplar; en çok kayıp veren 3 konuyu, soru numaraları ve örnek çözüm ipucuyla gösterir."""
    if res.get("kind") != "mc":
        return
    groups = {}
    for i, q in enumerate(qs):
        ua = st.session_state.answers.get(i)
        if ua != q.get("answer"):
            g = groups.setdefault((q.get("subject", "Genel"), q.get("topic") or "Genel"), {"idx": [], "boş": 0, "q": q})
            g["idx"].append(i + 1)
            g["boş"] += 0 if ua else 1
    st.markdown("<div class='sec-title'>🧭 Çalışma Özeti</div>", unsafe_allow_html=True)
    if not groups:
        st.success("Hiç yanlışın yok. Bir sonraki denemede zorluğu bir kademe artırmayı dene.")
        return
    top = sorted(groups.items(), key=lambda kv: -len(kv[1]["idx"]))[:3]
    st.markdown(f"**{sum(len(g['idx']) for g in groups.values())} sorudaki kaybın büyük kısmı şu {len(top)} konuda:**")
    for (subj, topic), g in top:
        nums = ", ".join(str(x) for x in g["idx"][:8])
        tip = _tip_of(g["q"])
        st.markdown(f"- **{cur.SUBJECT_ICONS.get(subj, '')} {subj} • {topic}** — {len(g['idx'])} soru (Soru {nums})" + (f"  \n  💡 *{tip}*" if tip else ""))
    st.button("🔁 Yanlışlarımı şimdi tekrar et", key="sum_review", on_click=nav, args=("review",))


def result():
    m, qs, res = st.session_state.meta, st.session_state.questions, st.session_state.result
    if not res:
        st.session_state.page = "home"
        st.rerun()
    if not st.session_state.saved:
        st.session_state.prev_attempt = _prev_attempt(m)
        persist(res)
        st.session_state.saved = True
        st.balloons()
    prev = st.session_state.get("prev_attempt")
    mins = res["duration"] // 60
    st.markdown(f"<div class='hero'><h1>🎉 Sınav Tamamlandı</h1><p>{m['title']} • Süre: {mins} dk {res['duration'] % 60} sn</p></div>", unsafe_allow_html=True)
    k = st.columns(6)
    dprev = (lambda key: (res[key] - prev[key]) if prev else None)
    labs = [("✅ Doğru", res["correct"], dprev("correct"), True), ("❌ Yanlış", res["wrong"], dprev("wrong"), False),
            ("⚪ Boş", res["empty"], dprev("empty"), False), ("🎯 Net" if res["kind"] == "mc" else "🎯 Puan", res["net"], dprev("net"), True),
            ("📈 Başarı %", f"{res['pct']:.0f}", dprev("pct"), True), ("⏱ Süre (dk)", mins, None, True)]
    for col, (l, v, d, up) in zip(k, labs):
        with col:
            theme.kpi(l, v, d, up)
    if prev:
        st.caption(f"Karşılaştırma: önceki aynı tür sınav — {prev['title']}")
    st.markdown("<div class='sec-title'>📚 Ders Bazlı Değerlendirme</div>", unsafe_allow_html=True)
    rows, chart = [], []
    for s, d in res["per"].items():
        pp = prev["per"].get(s) if prev else None
        delta = (d["pct"] - pp["pct"]) if pp else None
        dtxt = "—" if delta is None else (f"<span class='{'up' if delta > 0 else 'down' if delta < 0 else 'flat'}'>{'▲' if delta > 0 else '▼' if delta < 0 else '■'} {abs(delta):.1f}</span>")
        sc = f"{d['points']:.0f}/{d['max']:.0f}" if res["kind"] == "open" else d["net"]
        rows.append((f"{cur.SUBJECT_ICONS.get(s, '')} {s}", d["total"], d["correct"], d["wrong"], d["empty"], sc,
                     f"{theme.bar(d['pct'])}<small><b>%{d['pct']:.0f}</b></small>", f"{pp['pct']:.0f}" if pp else "—", dtxt))
        for lab, key in (("Doğru", "correct"), ("Yanlış", "wrong"), ("Boş", "empty")):
            chart.append({"Ders": s, "Durum": lab, "Adet": d[key]})
    theme.html_table(["Ders", "Soru", "D", "Y", "B", "Net/Puan", "Başarı", "Önceki %", "Değişim"], rows, num_cols=(1, 2, 3, 4, 5, 7, 8))
    tan = res.get("tan")
    if tan and tan.get("total", 0) > 5:
        st.markdown("<div class='sec-title'>⏱ Süre Analizi</div>", unsafe_allow_html=True)
        avg_all = tan["total"] / max(1, tan["n"])
        kk = st.columns(3)
        with kk[0]:
            theme.kpi("Soru başı ortalama", f"{avg_all:.0f} sn", avg_all - tan["expected"], good_up=False)
        with kk[1]:
            theme.kpi("Aceleci yanlış (<15 sn)", tan["fast_wrong"])
        with kk[2]:
            theme.kpi("Çok uzun düşünülen", tan["slow"])
        rows_t = [(f"{cur.SUBJECT_ICONS.get(s_, '')} {s_}", f"{v:.0f} sn", "⚡ Hızlı" if v < tan["expected"] * .6 else "🐢 Uzun" if v > tan["expected"] * 1.3 else "✅ Dengeli") for s_, v in tan["avg"].items()]
        theme.html_table(["Ders", "Soru başı", "Tempo"], rows_t)
        tips = []
        if tan["fast_wrong"] >= 2:
            tips.append(f"{tan['fast_wrong']} soruyu 15 saniyenin altında yanlış yaptın: acele ediyorsun, soruyu iki kez okumayı dene.")
        if tan["slow"] >= 2:
            tips.append(f"{tan['slow']} soruda çok uzun düşündün: takılırsan işaretleyip sona bırak, süre kazanırsın.")
        if avg_all > tan["expected"] * 1.2:
            tips.append("Genel tempon hedefin üstünde: süre tutarak kısa testler çözmek hızını artırır.")
        for t_ in tips or ["Tempon dengeli görünüyor, böyle devam!"]:
            st.markdown(f"- 💡 {t_}")
    cA, cB = st.columns([1.3, 1])
    with cA:
        st.markdown("**Ders bazında doğru / yanlış / boş dağılımı**")
        df = pd.DataFrame(chart)
        ch = alt.Chart(df).mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4).encode(
            x=alt.X("Ders:N", sort=None, axis=alt.Axis(labelAngle=-20, title=None)), y=alt.Y("Adet:Q", title=None),
            color=alt.Color("Durum:N", scale=alt.Scale(domain=["Doğru", "Yanlış", "Boş"], range=["#16a34a", "#dc2626", "#94a3b8"]), legend=alt.Legend(orient="bottom", title=None)),
            tooltip=["Ders", "Durum", "Adet"]).properties(height=280)
        st.altair_chart(ch, use_container_width=True)
    with cB:
        st.markdown("**Kazanım analizi**")
        weak, strong = [], []
        for s, t in res["topics"].items():
            for tp, (a, b) in t.items():
                if b:
                    (weak if a / b < .5 else strong).append((s, tp, 100 * a / b))
        st.markdown("🔴 **Tekrar edilmesi gerekenler**")
        for s, tp, p in sorted(weak, key=lambda x: x[2])[:8] or [("", "Harika! Zayıf kazanım yok.", 0)]:
            st.markdown(f"- {s} • {tp} {'(%' + format(p, '.0f') + ')' if s else ''}")
        st.markdown("🟢 **Güçlü kazanımlar**")
        for s, tp, p in sorted(strong, key=lambda x: -x[2])[:5] or [("", "—", 0)]:
            st.markdown(f"- {s} • {tp} {'(%' + format(p, '.0f') + ')' if s else ''}")
    _study_summary(res, qs, m)
    st.markdown("<div class='sec-title'>📄 PDF Çıktısı</div>", unsafe_allow_html=True)
    pdf_panel("res_")
    b1, b2, b3 = st.columns(3)
    with b1:
        st.button("📊 Performans & Raporlar", key="to_rep", on_click=nav, args=("reports",))
    with b2:
        st.button("🗂️ Yanlış Arşivim", key="to_arc", on_click=nav, args=("archive",))
    with b3:
        st.button("🏠 Ana Sayfa", key="to_home", on_click=lambda: (reset_exam(), nav("home")))
    with st.expander("📖 Detaylı Soru Çözüm, Cevap Anahtarı ve Tüm Şıkları İncele", expanded=any(str(k).startswith("expl_") for k in st.session_state)):
        for i, q in enumerate(qs):
            if m["kind"] == "mc":
                u, c = st.session_state.answers.get(i, "Boş"), q["answer"]
                st.markdown(f"### Soru {i + 1} [{q.get('subject', '')}] {'✅' if u == c else '❌'}")
                if q.get("passage"):
                    st.markdown(f"> **📖** {q['passage']}")
                if isinstance(q.get("shape"), dict):
                    draw_geometry_shape(q["shape"])
                st.markdown(f"**Soru:** {q['question']}")
                for ok, ov in q["options"].items():
                    pre_ = "✅ **(Doğru Cevabınız)**" if ok == c == u else "🟢 **(Doğru Cevap)**" if ok == c else "❌ **(Sizin Cevabınız)**" if ok == u else "   "
                    st.markdown(f"- {pre_} **{ok})** {ov}")
                st.markdown(f"<div style='background:#f8f9fa;padding:12px;border-radius:6px;border-left:4px solid #4e73df;margin:10px 0 20px'><b>💡 Çözüm:</b><br>{q.get('explanation') or 'Açıklama yok.'}</div>", unsafe_allow_html=True)
                if u != c:
                    from .study import explain_box
                    explain_box(q, u if u != "Boş" else None, f"res_{i}", m.get("grade_label", ""))
                if st.session_state.get(f"rep_{i}"):
                    st.caption("🚩 Bildirildi: bu soru bir daha çıkmayacak.")
                else:
                    st.button("🚩 Bu soru hatalı", key=f"repb_{i}", on_click=_report, args=(q, f"rep_{i}"))
            else:
                st.markdown(f"### Soru {i + 1} [{q.get('subject', '')}] — {st.session_state.self_scores.get(i, 0)}/{q.get('points')} puan")
                st.markdown(f"**{q['question']}**\n\n**Beklenen cevap:** {q.get('answer', '')}")
                fb = (st.session_state.get("ai_grades") or {}).get(i, {}).get("feedback")
                if fb:
                    st.info(f"👩‍🏫 {fb}")
            st.markdown("---")
'''
MODULES['ui/reports'] = r'''# -*- coding: utf-8 -*-
import datetime
import json
import altair as alt
import pandas as pd
import streamlit as st
from core import curriculum as cur, store
from . import theme
from .state import nav

SPARK = "▁▂▃▄▅▆▇█"
MODE_NAMES = {"weekly": "Haftalık", "agis": "AGİS", "monthly": "AGİS", "oyss": "OYSS", "topic": "Konu Tarama", "bank": "Soru Bankası", "leaf": "Yaprak Test", "archive": "Arşiv Testi"}


def spark(vals):
    if not vals:
        return ""
    lo, hi = min(vals), max(vals)
    return "".join(SPARK[0 if hi == lo else int((v - lo) / (hi - lo) * 7)] for v in vals)


def _d(delta):
    if delta is None:
        return "—"
    c = "up" if delta > 0 else "down" if delta < 0 else "flat"
    return f"<span class='{c}'>{'▲' if delta > 0 else '▼' if delta < 0 else '■'} {abs(delta):.1f}</span>"


def _date(ts):
    return datetime.datetime.fromtimestamp(ts).strftime("%d.%m.%Y %H:%M")


def reports():
    st.markdown("<div class='hero'><h1>📊 Performans & Raporlar</h1><p>Tüm denemelerin, derslerin ve kazanımların profesyonel analizi; önceki sınavlarla karşılaştırma.</p></div>", unsafe_allow_html=True)
    hist = store.history()
    if not hist:
        st.info("Henüz tamamlanmış sınav yok. İlk denemeni çözdükten sonra grafikler ve tablolar burada görünecek.")
        _backup(hist)
        return
    f1, f2 = st.columns(2)
    grades = ["Tümü"] + sorted({h["grade_label"] for h in hist})
    modes = ["Tümü"] + sorted({MODE_NAMES.get(h["mode"], h["mode"]) for h in hist})
    gsel = f1.selectbox("Sınıf", grades, key="rp_g")
    msel = f2.selectbox("Sınav türü", modes, key="rp_m")
    H = [h for h in hist if (gsel == "Tümü" or h["grade_label"] == gsel) and (msel == "Tümü" or MODE_NAMES.get(h["mode"], h["mode"]) == msel)]
    if not H:
        st.warning("Bu filtreye uygun sınav yok.")
        return
    pcts = [h["pct"] for h in H]
    last, prev = H[-1], (H[-2] if len(H) > 1 else None)
    k = st.columns(5)
    with k[0]:
        theme.kpi("Çözülen Sınav", len(H))
    with k[1]:
        theme.kpi("Ortalama Başarı", f"%{sum(pcts) / len(pcts):.0f}")
    with k[2]:
        theme.kpi("Son Sınav", f"%{last['pct']:.0f}", (last["pct"] - prev["pct"]) if prev else None)
    with k[3]:
        theme.kpi("En İyi", f"%{max(pcts):.0f}")
    with k[4]:
        theme.kpi("Toplam Soru", sum(h["total"] for h in H))

    # --- otomatik analiz
    subj_hist = {}
    for h in H:
        for s, d in h["per"].items():
            subj_hist.setdefault(s, []).append(d["pct"])
    if subj_hist:
        avg3 = {s: sum(v[-3:]) / len(v[-3:]) for s, v in subj_hist.items()}
        weak = min(avg3, key=avg3.get)
        best = max(avg3, key=avg3.get)
        imp = {s: v[-1] - v[-2] for s, v in subj_hist.items() if len(v) > 1}
        txt = f"💡 **Analiz:** En güçlü dersin **{best}** (son 3 ort. %{avg3[best]:.0f}); en çok desteğe ihtiyaç duyan **{weak}** (%{avg3[weak]:.0f})."
        if imp:
            up = max(imp, key=imp.get)
            dn = min(imp, key=imp.get)
            txt += f" Son sınavda en büyük yükseliş **{up}** ({imp[up]:+.0f} puan)" + (f", en büyük düşüş **{dn}** ({imp[dn]:+.0f})." if imp[dn] < 0 else ".")
        st.markdown(f"<div class='panel'>{txt}<br><small>Öneri: {weak} için Konu Tarama ve Yaprak Test ile zayıf kazanımları çalış; Yanlış Arşivim'den kişisel test çöz.</small></div>", unsafe_allow_html=True)

    t1, t2, t3, t4, t5, t6 = st.tabs(["📈 Genel Gidiş", "📚 Ders Karşılaştırma", "🔥 Isı Haritası", "🧩 Kazanım Analizi", "🧾 Sınav Geçmişi", "💾 Yedek"])
    with t1:
        df = pd.DataFrame([{"Sınav": i + 1, "Başarı %": h["pct"], "Başlık": h["title"], "Tarih": _date(h["ts"]), "Tür": MODE_NAMES.get(h["mode"], h["mode"])} for i, h in enumerate(H)])
        line = alt.Chart(df).mark_line(point=alt.OverlayMarkDef(size=70), color="#0284c7", strokeWidth=3).encode(
            x=alt.X("Sınav:O", title="Sınav sırası"), y=alt.Y("Başarı %:Q", scale=alt.Scale(domain=[0, 100])),
            tooltip=["Başlık", "Tarih", "Tür", "Başarı %"])
        rule = alt.Chart(pd.DataFrame({"y": [sum(pcts) / len(pcts)]})).mark_rule(strokeDash=[6, 4], color="#ea580c").encode(y="y:Q")
        st.altair_chart((line + rule).properties(height=300), use_container_width=True)
        st.caption("Turuncu kesikli çizgi: ortalama başarın.")
        by = pd.DataFrame([{"Tür": MODE_NAMES.get(h["mode"], h["mode"]), "Başarı %": h["pct"]} for h in H]).groupby("Tür", as_index=False).mean()
        st.markdown("**Sınav türüne göre ortalama başarı**")
        st.altair_chart(alt.Chart(by).mark_bar(cornerRadiusEnd=5, color="#8b5cf6").encode(y=alt.Y("Tür:N", sort="-x", title=None), x=alt.X("Başarı %:Q", scale=alt.Scale(domain=[0, 100]))).properties(height=40 * len(by) + 30), use_container_width=True)
    with t2:
        rows = []
        for s, v in subj_hist.items():
            rows.append((f"{cur.SUBJECT_ICONS.get(s, '')} {s}", len(v), f"%{v[-1]:.0f}", f"%{v[-2]:.0f}" if len(v) > 1 else "—", _d(v[-1] - v[-2]) if len(v) > 1 else "—",
                         f"%{sum(v) / len(v):.0f}", f"%{max(v):.0f}", f"<span style='font-size:1.1rem;color:#0284c7;letter-spacing:1px'>{spark(v[-10:])}</span>"))
        st.markdown("**Her ders için son sınav ↔ önceki sınav karşılaştırması**")
        theme.html_table(["Ders", "Sınav", "Son", "Önceki", "Değişim", "Ortalama", "En iyi", "Gidiş (son 10)"], rows, num_cols=(1, 2, 3, 4, 5, 6))
        sub = st.selectbox("Ders detayı", list(subj_hist), key="rp_sub")
        pts = [(i + 1, h["title"], h["per"][sub]) for i, h in enumerate(H) if sub in h["per"]]
        dfl = pd.DataFrame([{"Sınav": i, "Başarı %": d["pct"], "Başlık": t} for i, t, d in pts])
        a, b = st.columns(2)
        with a:
            st.markdown(f"**{sub} — başarı trendi**")
            st.altair_chart(alt.Chart(dfl).mark_line(point=True, color=cur.SUBJECT_COLORS.get(sub, "#0284c7"), strokeWidth=3).encode(
                x=alt.X("Sınav:O"), y=alt.Y("Başarı %:Q", scale=alt.Scale(domain=[0, 100])), tooltip=["Başlık", "Başarı %"]).properties(height=260), use_container_width=True)
        with b:
            st.markdown(f"**{sub} — doğru / yanlış / boş**")
            dd = []
            for i, t, d in pts[-8:]:
                for lab, key in (("Doğru", "correct"), ("Yanlış", "wrong"), ("Boş", "empty")):
                    dd.append({"Sınav": i, "Durum": lab, "Adet": d.get(key, 0)})
            st.altair_chart(alt.Chart(pd.DataFrame(dd)).mark_bar().encode(
                x=alt.X("Sınav:O"), y="Adet:Q", color=alt.Color("Durum:N", scale=alt.Scale(domain=["Doğru", "Yanlış", "Boş"], range=["#16a34a", "#dc2626", "#94a3b8"]), legend=alt.Legend(orient="bottom", title=None))).properties(height=260), use_container_width=True)
        st.markdown("**Tüm derslerin son sınavlardaki seyri**")
        dm = pd.DataFrame([{"Sınav": i + 1, "Ders": s, "Başarı %": d["pct"]} for i, h in enumerate(H) for s, d in h["per"].items()])
        st.altair_chart(alt.Chart(dm).mark_line(point=True).encode(x="Sınav:O", y=alt.Y("Başarı %:Q", scale=alt.Scale(domain=[0, 100])), color=alt.Color("Ders:N", legend=alt.Legend(orient="bottom", title=None)), tooltip=["Ders", "Sınav", "Başarı %"]).properties(height=300), use_container_width=True)
    with t3:
        N = H[-8:]
        head = ["Ders"] + [f"#{len(H) - len(N) + i + 1}" for i in range(len(N))]
        body = []
        for s in subj_hist:
            cells = [f"{cur.SUBJECT_ICONS.get(s, '')} {s}"]
            for h in N:
                d = h["per"].get(s)
                if d:
                    p = d["pct"]
                    cells.append(f"<div style='background:{theme.pct_color(p)};color:white;border-radius:8px;padding:4px 0;font-weight:800'>%{p:.0f}</div>")
                else:
                    cells.append("—")
            body.append(cells)
        theme.html_table(head, body, num_cols=tuple(range(1, len(head))))
        st.caption("🟢 ≥75 • 🟠 50-74 • 🔴 <50. Sütunlar: son 8 sınav.")
    with t4:
        agg = {}
        for h in H:
            for s, t in (h.get("topics") or {}).items():
                for tp, (a, b) in t.items():
                    x = agg.setdefault((s, tp), [0, 0])
                    x[0] += a
                    x[1] += b
        rows = sorted([(s, tp, 100 * a / b, b) for (s, tp), (a, b) in agg.items() if b], key=lambda r: r[2])
        st.markdown("**En zayıf kazanımlar (tüm sınavlar)**")
        theme.html_table(["Ders", "Kazanım / Konu", "Başarı", "Soru"], [(f"{cur.SUBJECT_ICONS.get(s, '')} {s}", tp, f"{theme.bar(p)}<small><b>%{p:.0f}</b></small>", n) for s, tp, p, n in rows[:15]], num_cols=(3,))
        with st.expander("En güçlü kazanımlar"):
            theme.html_table(["Ders", "Kazanım / Konu", "Başarı", "Soru"], [(s, tp, f"%{p:.0f}", n) for s, tp, p, n in rows[::-1][:10]], num_cols=(3,))
    with t5:
        rows = [(len(H) - i, _date(h["ts"]), h["grade_label"], MODE_NAMES.get(h["mode"], h["mode"]), h["title"], h["correct"], h["wrong"], h["empty"], h["net"], f"%{h['pct']:.0f}", f"{h['duration'] // 60} dk") for i, h in enumerate(reversed(H))]
        theme.html_table(["#", "Tarih", "Sınıf", "Tür", "Sınav", "D", "Y", "B", "Net/Puan", "Başarı", "Süre"], rows, num_cols=(0, 5, 6, 7, 8, 9, 10))
    with t6:
        _parent_report(hist)
        _backup(hist)


def _parent_report(hist):
    from core import coach, pdf_export
    st.markdown("<div class='sec-title'>👨‍👩‍👧 Veli / Öğretmen Raporu</div>", unsafe_allow_html=True)
    name = st.text_input("Öğrenci adı", value=store.settings().get("name", ""), key="rp_name")
    if name != store.settings().get("name", ""):
        store.save_settings(name=name)
    if st.button("📄 Tek sayfalık raporu hazırla", key="rp_make", type="primary"):
        stats, weak = coach.subject_stats(hist), coach.weak_topics(hist)
        cm = st.session_state.get("plan_comment") or ""
        st.session_state["rp_pdf"] = pdf_export.report_pdf(name, hist[-1].get("grade_label", ""), hist, stats, weak, coach.streak(), coach.xp_level(hist), cm)
    if st.session_state.get("rp_pdf"):
        st.download_button("⬇️ Raporu indir (PDF)", st.session_state["rp_pdf"], file_name="gelisim_raporu.pdf", mime="application/pdf", key="rp_dl")
        st.caption("İpucu: Çalışma Planım sayfasında 'Öğretmen yorumu al' dersen yorum rapora da eklenir.")


def _backup(hist):
    st.markdown("**Yedekle / Geri yükle** — Streamlit Cloud geçici disk kullanır; verini düzenli yedekle.")
    blob = json.dumps({"history": hist, "wrong": store.wrong(), "bank": store.bank_all(), "stems": store.recent_stems()}, ensure_ascii=False).encode("utf-8")
    bs = store.bank_stats()
    st.caption(f"Yedeğe dahil: {len(hist)} sınav • {len(store.wrong())} yanlış soru • 🏦 {bs['total']} bankadaki soru")
    st.download_button("⬇️ Yedeği indir (JSON)", blob, file_name="denemematik_yedek.json", mime="application/json", key="bk_dl")
    up = st.file_uploader("Yedeği geri yükle", type="json", key="bk_up")
    if up is not None and st.button("♻️ Geri yükle", key="bk_go"):
        try:
            d = json.loads(up.read().decode("utf-8"))
            store.replace_history(d.get("history", []))
            store.replace_wrong(d.get("wrong", []))
            if "bank" in d:  # eski yedeklerde banka yoktur; varsa geri yükle
                store.replace_bank(d.get("bank", {}))
            if "stems" in d:
                store.replace_stems(d.get("stems", {}))
            st.success("Yedek geri yüklendi.")
            st.rerun()
        except Exception as e:
            st.error(f"Geçersiz yedek dosyası: {e}")
'''
MODULES['ui/extras'] = r'''# -*- coding: utf-8 -*-
import streamlit as st
from core import curriculum as cur, store, ai_engine as ai, pdf_export
from core.visuals import draw_geometry_shape
from . import theme
from .state import nav
from .setup import _finish, SEC_PER_Q


# ------------------------------------------------------------------ yanlış arşivi
def archive():
    st.markdown("<div class='hero'><h1>🗂️ Yanlış Yaptığım Sorular Arşivi</h1><p>Her sınavdaki yanlış/boş sorular buraya düşer. Filtrele, PDF al ya da yapay zekâya benzer yeni sorular ürettir.</p></div>", unsafe_allow_html=True)
    W = store.wrong()
    if not W:
        st.info("Arşiv boş — yanlış yaptığın sorular sınav sonunda otomatik buraya eklenir.")
        return
    c1, c2 = st.columns(2)
    subs = ["Tümü"] + sorted({w["subject"] for w in W})
    grs = ["Tümü"] + sorted({w["grade_label"] for w in W})
    s = c1.selectbox("Ders", subs, key="ar_s")
    g = c2.selectbox("Sınıf", grs, key="ar_g")
    F = [w for w in W if (s == "Tümü" or w["subject"] == s) and (g == "Tümü" or w["grade_label"] == g)]
    k = st.columns(3)
    with k[0]:
        theme.kpi("Arşivdeki Soru", len(F))
    by = {}
    for w in F:
        by[w["subject"]] = by.get(w["subject"], 0) + 1
    with k[1]:
        theme.kpi("En Çok Hata", max(by, key=by.get) if by else "—")
    with k[2]:
        theme.kpi("Ders Sayısı", len(by))
    mc = [w for w in F if w.get("kind") == "mc"]
    a, b = st.columns(2)
    with a:
        if mc and st.button("🧪 Benzer Sorulardan Kişisel Test Üret", key="ar_gen", type="primary"):
            plan, gl = [], mc[0]["grade_label"]
            for sub in sorted({w["subject"] for w in mc}):
                items = [w for w in mc if w["subject"] == sub]
                tops = "; ".join(sorted({w["topic"] for w in items if w["topic"]})) or sub
                stems = " | ".join(w["q"]["question"][:80] for w in items[:4])
                plan.append({"subject": sub, "n": min(10, max(5, len(items))), "topics": f"{tops} (bu kazanımlarda ÖĞRENCİNİN YANLIŞ YAPTIĞI konulara benzer ama farklı sorular; örnekler: {stems})", "short": tops})
            diff = cur.DIFFICULTIES[2]
            from .setup import with_overlay, est_seconds_mc
            qs, errs = with_overlay(est_seconds_mc(plan), "Kişisel testin hazırlanıyor", "Yanlış yaptığın konulara benzer yeni sorular yazılıyor…",
                                    lambda: ai.generate_mc(plan, gl, diff, "Yanlış arşivi", avoid=store.recent_stems(), use_bank=False, deposit=False))
            n = sum(p["n"] for p in plan)
            meta = {"grade": mc[0]["grade"], "grade_label": gl, "mode": "archive", "title": f"{gl} Kişisel Hata Telafi Testi", "scope": "Yanlış arşivi",
                    "difficulty": diff, "kind": "mc", "subtitle": "Yanlışlarına özel hazırlanmış test", "info_line": f"{n} soru",
                    "briefing": [(p["subject"], p["n"], p["short"]) for p in plan]}
            _finish(qs, errs, meta)
    with b:
        if mc and st.button("📄 Arşivi PDF Yap", key="ar_pdf"):
            meta = {"title": "Yanlış Soru Arşivim", "subtitle": "Tekrar edilecek sorular", "grade_label": g if g != "Tümü" else "KARMA", "kind": "mc", "info_line": f"{len(mc)} soru"}
            st.session_state["ar_pdf_bytes"] = pdf_export.build_pdf([w["q"] for w in mc], meta)
        if st.session_state.get("ar_pdf_bytes"):
            st.download_button("⬇️ PDF'i İndir", st.session_state["ar_pdf_bytes"], file_name="yanlis_arsivi.pdf", mime="application/pdf", key="ar_dl")
    st.markdown("---")
    for w in F:
        q = w["q"]
        with st.expander(f"{cur.SUBJECT_ICONS.get(w['subject'], '')} {w['subject']} • {w.get('topic') or ''} • {w['grade_label']}"):
            if q.get("passage"):
                st.markdown(f"> {q['passage']}")
            if isinstance(q.get("shape"), dict):
                draw_geometry_shape(q["shape"])
            st.markdown(f"**{q['question']}**")
            if w.get("kind") == "mc":
                for ok, ov in q["options"].items():
                    mark = "🟢 **(Doğru)**" if ok == q["answer"] else ("❌ **(Senin cevabın)**" if ok == w.get("user") else "")
                    st.markdown(f"- **{ok})** {ov} {mark}")
                st.info(f"💡 {q.get('explanation') or 'Açıklama yok.'}")
            else:
                st.success(f"Beklenen cevap: {q.get('answer', '')}")
            st.button("✅ Öğrendim — arşivden çıkar", key=f"ar_rm_{w['key']}", on_click=store.remove_wrong, args=(w["key"],))


# ------------------------------------------------------------------ rozetler & sertifikalar
def _badges(H):
    out = []
    n = len(H)
    out.append(("🌱", "İlk Adım", "İlk sınavını tamamla", n >= 1))
    out.append(("📚", "Düzenli Öğrenci", "5 sınav çöz", n >= 5))
    out.append(("🔥", "Kararlı", "15 sınav çöz", n >= 15))
    out.append(("🏆", "Deneme Şampiyonu", "40 sınav çöz", n >= 40))
    out.append(("💯", "Tam Puan", "Bir sınavda %100", any(h["pct"] >= 99.5 for h in H)))
    out.append(("🚀", "Yükseliş", "Bir önceki sınava göre +10 puan", n > 1 and H[-1]["pct"] - H[-2]["pct"] >= 10))
    out.append(("🎯", "Konu Avcısı", "5 konu tarama / yaprak test", sum(h["mode"] in ("topic", "leaf") for h in H) >= 5))
    out.append(("📝", "OYSS Kahramanı", "OYSS'de %70+ başarı", any(h["mode"] == "oyss" and h["pct"] >= 70 for h in H)))
    out.append(("🗓️", "AGİS Ustası", "3 AGİS (aylık gelişim sınavı)", sum(h["mode"] in ("agis", "monthly") for h in H) >= 3))
    sv = {}
    for h in H:
        for s, d in h["per"].items():
            sv.setdefault(s, []).append(d["pct"])
    for s in cur.SUBJECT_ICONS:
        v = sv.get(s, [])
        out.append((cur.SUBJECT_ICONS[s], f"{s} Ustası", "3+ sınav, ortalama %80", len(v) >= 3 and sum(v) / len(v) >= 80))
    return out


def badges():
    st.markdown("<div class='hero'><h1>🏅 Ünite Başarı Sertifikaları & Rozetler</h1><p>Çalıştıkça rozet kazan; konu tarama/yaprak testte %85 üstü başarıyla sertifika al.</p></div>", unsafe_allow_html=True)
    H = store.history()
    bd = _badges(H)
    st.markdown(f"**Kazanılan rozet: {sum(1 for b in bd if b[3])} / {len(bd)}**")
    theme.cells(bd, 4, lambda b: st.markdown(f"<div class='rozet {'' if b[3] else 'locked'}'><div class='ic'>{b[0]}</div><div class='t'>{b[1]}</div><div class='s'>{b[2]}</div></div><br>", unsafe_allow_html=True))
    st.markdown("<div class='sec-title'>📜 Sertifikalar</div>", unsafe_allow_html=True)
    cert = [h for h in H if h["mode"] in ("topic", "leaf") and h["pct"] >= 85 and h["total"] >= 8]
    if not cert:
        st.info("Konu tarama veya yaprak testte en az 8 soruda %85 başarıya ulaşınca sertifikan burada görünür.")
        return
    name = st.text_input("Sertifikada yazacak ad soyad", key="cert_name")
    for i, h in enumerate(reversed(cert[-10:])):
        ti = h.get("topic_info") or {}
        subj = ti.get("subject") or next(iter(h["per"]), "")
        pdf = pdf_export.certificate_pdf(name, subj, h["grade_label"], h["pct"], ti.get("unit", "").split(" (MAT")[0])
        st.download_button(f"📜 {h['title']} — %{h['pct']:.0f}", pdf, file_name=f"sertifika_{i}.pdf", mime="application/pdf", key=f"cert_{h['id']}")
'''
MODULES['ui/study'] = r'''# -*- coding: utf-8 -*-
"""Öğrenci koçu ekranları: günlük tekrar, çalışma planı, 'bana anlat', seri/hedef şeridi."""
import time
import streamlit as st
from core import curriculum as cur, store, coach
from . import theme
from .state import nav
from . import setup as su


# ------------------------------------------------------------------ ortak: Bana anlat
def explain_box(q, user_answer, key, grade_label=""):
    ck = f"expl_{key}"
    if st.session_state.get(ck) is None:
        if st.button("👩‍🏫 Bana anlat", key=f"btn_{ck}", type="primary"):
            r = su.with_overlay(12, "Öğretmen anlatıyor", "Çözüm adım adım ve daha kolay bir örnekle hazırlanıyor…", lambda: coach.explain(q, user_answer, grade_label))
            st.session_state[ck] = r
            st.rerun()
        return
    r = st.session_state[ck]
    steps = "".join(f"<li>{x}</li>" for x in (r.get("steps") or []))
    st.markdown(f"<div class='teach'><div class='teach-h'>👩‍🏫 Öğretmenin anlatımı</div><ol>{steps}</ol>"
                + (f"<p><b>Neden yanlış olmuş olabilir?</b> {r['why_wrong']}</p>" if r.get("why_wrong") else "") + "</div>", unsafe_allow_html=True)
    ex = r.get("easy_example")
    if isinstance(ex, dict) and ex.get("question"):
        st.markdown(f"<div class='teach ex'><div class='teach-h'>🌱 Daha kolay benzer örnek</div><p>{ex.get('question')}</p>"
                    f"<details><summary>Cevabı gör</summary><p><b>{ex.get('answer', '')}</b></p></details></div>", unsafe_allow_html=True)
    if r.get("tip"):
        st.caption(f"💡 {r['tip']}")


# ------------------------------------------------------------------ seri / hedef şeridi (ana sayfa)
def strip():
    cnt, goal = coach.today_count(), store.settings()["goal"]
    sk, lv = coach.streak(), coach.xp_level()
    due = len(coach.due_items())
    pct = min(100, 100 * cnt / max(1, goal))
    st.markdown(
        f"<div class='strip'>"
        f"<div class='sc'><div class='sv'>🔥 {sk}</div><div class='sl'>gün seri</div></div>"
        f"<div class='sc wide'><div class='sl'>Günlük hedef: {cnt}/{goal} soru</div><div class='bar-bg'><div class='bar-fg' style='width:{pct:.0f}%;background:linear-gradient(90deg,#7c3aed,#14b8a6)'></div></div>"
        f"<div class='sl'>{'🎉 Hedef tamam!' if cnt >= goal else f'{goal - cnt} soru kaldı'}</div></div>"
        f"<div class='sc'><div class='sv'>⭐ Sv.{lv['level']}</div><div class='sl'>{lv['title']} • {lv['xp']} XP</div></div>"
        f"<div class='sc'><div class='sv'>🔁 {due}</div><div class='sl'>bugünkü tekrar</div></div></div>", unsafe_allow_html=True)


# ------------------------------------------------------------------ GÜNLÜK TEKRAR
def _answer_review(key, ok):
    days = coach.review_result(key, ok)
    st.session_state.rev_msg = (ok, days)
    st.session_state.rev_done = st.session_state.get("rev_done", 0) + 1
    st.session_state.rev_ok = st.session_state.get("rev_ok", 0) + (1 if ok else 0)


def _rev_pick(key):
    ok_key = st.session_state.get("rev_cur")
    st.session_state.rev_checked = True


def review():
    S = st.session_state
    st.markdown("<div class='hero'><h1>🔁 Günlük Tekrar</h1><p>Yanlış yaptığın sorular unutmadan tam zamanında geri gelir: doğru bilirsen aralık uzar (1 → 3 → 7 → 21 → 60 gün), yanlış bilirsen yarın tekrar sorulur.</p></div>", unsafe_allow_html=True)
    due = coach.due_items()
    if S.get("rev_msg"):
        ok, days = S.rev_msg
        (st.success if ok else st.warning)(f"{'✅ Doğru! Bu soru ' + str(days) + ' gün sonra tekrar gelecek.' if ok else '❌ Yanlış. Sorun yarın tekrar karşına çıkacak.'}")
        S.rev_msg = None
    if not due:
        done = S.get("rev_done", 0)
        st.markdown(f"<div class='panel' style='text-align:center'><div style='font-size:3rem'>🎉</div><h3>Bugünlük tekrar tamam!</h3>"
                    f"<p>{('Bu oturumda ' + str(done) + ' soru çözdün (' + str(S.get('rev_ok', 0)) + ' doğru). ') if done else ''}Sırada bekleyen {coach.upcoming_count()} soru ileriki günlere planlandı.</p></div>", unsafe_allow_html=True)
        st.button("🏠 Ana sayfa", key="rev_home", on_click=nav, args=("home",))
        return
    w = due[0]
    q = w["q"]
    st.markdown(f"<span class='badge'>Bugün sırada: {len(due)} soru</span><span class='badge'>{cur.SUBJECT_ICONS.get(w['subject'], '')} {w['subject']}</span>"
                f"<span class='badge'>Kutu {w.get('box', 0) + 1}/5</span>", unsafe_allow_html=True)
    st.progress(min(1.0, S.get("rev_done", 0) / max(1, S.get("rev_done", 0) + len(due))))
    st.markdown("<div class='question-card'>", unsafe_allow_html=True)
    if str(q.get("passage") or "").strip() not in ("", "null"):
        st.markdown(f"<div class='passage-box'><b>📖</b> {q['passage']}</div>", unsafe_allow_html=True)
    if isinstance(q.get("shape"), dict):
        from core.visuals import draw_geometry_shape
        draw_geometry_shape(q["shape"])
    st.markdown(f"<p class='question-title'>{q['question']}</p>", unsafe_allow_html=True)
    opts = q["options"]
    keys = list(opts)
    checked = S.get("rev_checked_key") == w["key"]
    pick = st.radio("Cevabın", keys, index=None, format_func=lambda x: f"{x}) {opts[x]}", key=f"rev_pick_{w['key']}", disabled=checked)
    st.markdown("</div>", unsafe_allow_html=True)
    if not checked:
        if st.button("✔️ Kontrol et", key="rev_check", type="primary", disabled=pick is None):
            S.rev_checked_key = w["key"]
            S.rev_last_pick = pick
            st.rerun()
        return
    pick = S.get("rev_last_pick")
    ok = pick == q["answer"]
    (st.success if ok else st.error)(f"{'✅ Doğru!' if ok else '❌ Yanlış.'} Doğru cevap: {q['answer']}) {opts[q['answer']]}")
    st.info(f"💡 {q.get('explanation') or 'Açıklama yok.'}")
    if not ok:
        explain_box(q, opts.get(pick), f"rev_{w['key']}", w.get("grade_label", ""))

    def nxt(ok=ok, key=w["key"]):
        _answer_review(key, ok)
        S.rev_checked_key = None
    st.button("➡ Sıradaki soru", key="rev_next", on_click=nxt, type="primary")


# ------------------------------------------------------------------ ÇALIŞMA PLANI
def _plan_go(action, subject=None):
    S = st.session_state
    if not S.get("grade"):
        S.grade = "5"
    if action == "review":
        nav("review")
    elif action == "archive":
        nav("archive")
    elif action == "leaf":
        su._tool_go("leaf_start")
    elif action in ("weekly", "topic"):
        su.pick_mode(action)
    else:
        nav("home")


def plan():
    S = st.session_state
    st.markdown("<div class='hero'><h1>🗓️ Çalışma Planım</h1><p>Son denemelerindeki zayıf kazanımlara göre sana özel 7 günlük plan. Her gün kısa, net bir görev.</p></div>", unsafe_allow_html=True)
    hist = store.history()
    if not hist:
        st.info("Plan, ilk denemeni çözdükten sonra senin sonuçlarına göre hazırlanır. Şimdilik bir deneme çöz ya da Konu Tarama ile başla.")
        st.button("🏠 Ana sayfa", key="plan_home", on_click=nav, args=("home",))
        return
    g = hist[-1].get("grade_label", "")
    stats = coach.subject_stats(hist)
    weak = coach.weak_topics(hist)
    sk = coach.streak()
    k = st.columns(3)
    with k[0]:
        theme.kpi("Çalışma serisi", f"🔥 {sk} gün")
    with k[1]:
        theme.kpi("Zayıf kazanım", len(weak))
    with k[2]:
        theme.kpi("Bugünkü tekrar", len(coach.due_items()))
    st.markdown("<div class='sec-title'>👩‍🏫 Öğretmenin değerlendirmesi</div>", unsafe_allow_html=True)
    sig = f"{len(hist)}_{len(weak)}"
    if S.get("plan_sig") != sig:
        S.plan_sig = sig
        S.plan_comment = None
    if S.get("plan_comment") is None:
        if st.button("✨ Öğretmen yorumu al", key="plan_ai", type="primary"):
            S.plan_comment = su.with_overlay(12, "Öğretmen planını hazırlıyor", "Son denemelerin değerlendiriliyor…", lambda: coach.teacher_comment(g, stats, weak, sk))
            st.rerun()
    else:
        st.markdown(f"<div class='teach'>{S.plan_comment}</div>", unsafe_allow_html=True)
    st.markdown("<div class='sec-title'>📅 Bu haftanın planı</div>", unsafe_allow_html=True)
    days = coach.week_plan(hist)
    import datetime
    today = datetime.date.today().weekday()

    def card(item):
        i = days.index(item)
        st.markdown(f"<div class='plan-card {'today' if i == today else ''}'><div class='pd'>{item['day']}{' • BUGÜN' if i == today else ''}</div>"
                    f"<div class='pt'>{item['icon']} {item['title']}</div><div class='pi'>{item['detail']}</div></div>", unsafe_allow_html=True)
        st.button("Başla →", key=f"plan_go_{i}", on_click=_plan_go, args=(item["action"], item.get("subject")), use_container_width=True)
    theme.cells(days, 2, card)
    if weak:
        st.markdown("<div class='sec-title'>🔴 Öncelikli kazanımlar</div>", unsafe_allow_html=True)
        theme.html_table(["Ders", "Kazanım", "Başarı"], [(f"{cur.SUBJECT_ICONS.get(s, '')} {s}", t, f"{theme.bar(p)}<small><b>%{p:.0f}</b></small>") for s, t, p, _ in weak[:8]])
    with st.expander("🎯 Günlük soru hedefini ayarla"):
        goal = st.slider("Günde kaç soru?", 5, 100, int(store.settings()["goal"]), 5, key="goal_sl")
        if goal != store.settings()["goal"]:
            store.save_settings(goal=goal)
            st.rerun()
'''

ORDER = ['core/curriculum', 'core/oyss', 'core/fenfig', 'core/visuals', 'core/pdf_export', 'core/store', 'core/meb_live', 'core/ai_engine', 'core/coach', 'ui/theme', 'ui/state', 'ui/setup', 'ui/wizard', 'ui/exam', 'ui/reports', 'ui/extras', 'ui/study']


def _load_modules():
    import hashlib
    ver = hashlib.md5("".join(MODULES[k] for k in ORDER).encode("utf-8")).hexdigest()
    if getattr(sys.modules.get("core"), "_ver", None) == ver and all(("core." if k.startswith("core") else "ui.") + k.split("/")[1] in sys.modules for k in ORDER):
        return  # aynı sürüm zaten yüklü
    for k in list(sys.modules):  # eski sürüm kalıntılarını temizle
        if k in ("core", "ui") or k.startswith(("core.", "ui.")):
            del sys.modules[k]
    for pkg in ("core", "ui"):
        p = types.ModuleType(pkg)
        p.__path__ = []
        p.__file__ = os.path.join(APPDIR, pkg, "__init__.py")
        sys.modules[pkg] = p
    sys.modules["core"]._ver = ver
    for key in ORDER:
        pkg, name = key.split("/")
        full = pkg + "." + name
        mod = types.ModuleType(full)
        mod.__package__ = pkg
        mod.__file__ = os.path.join(APPDIR, pkg, name + ".py")
        sys.modules[full] = mod
        setattr(sys.modules[pkg], name, mod)
        exec(compile(MODULES[key], mod.__file__, "exec"), mod.__dict__)


_load_modules()
from core import ai_engine, curriculum as cur, meb_live
from ui import theme, state, setup, wizard, exam, reports, extras, study

theme.inject()
state.init()
if "meb_loaded" not in st.session_state:
    st.session_state.meb_loaded = True
    st.session_state.meb_ts = meb_live.load_cache()
    # MEB müfredatı: arka planda (arayüzü bekletmeden) güncellenir; yerleşik müfredat anında hazırdır
    try:
        import threading
        if not ai_engine.demo_mode() and meb_live.needs_refresh() and not getattr(sys.modules["core"], "_meb_thread", None):
            _t = threading.Thread(target=lambda: meb_live.refresh(deadline=60), daemon=True)
            sys.modules["core"]._meb_thread = _t
            _t.start()
    except Exception:
        pass

GROQ_KEYS, GEMINI_KEYS = ai_engine.load_keys()
if not GROQ_KEYS and not GEMINI_KEYS and not ai_engine.extra_keys() and not ai_engine.demo_mode():
    st.error("⚠️ `.streamlit/secrets.toml` dosyasında API anahtarları bulunamadı!")
    st.code('[api_keys]\ngroq_keys = ["gsk_...", "gsk_..."]      # istediğin kadar anahtar ekleyebilirsin\ngemini_keys = ["AIza...", "AIza..."]\n# İsteğe bağlı ek havuz (kota artırır): cerebras_keys, openrouter_keys, mistral_keys, sambanova_keys, nvidia_keys, github_keys', language="toml")
    st.stop()

# ------------------------------------------------------------------ açılışta: son planların bankası arka planda hazırlanır
if "warm_done" not in st.session_state:
    st.session_state.warm_done = True
    try:
        if not ai_engine.demo_mode():
            import threading as _th
            from core import store as _store
            _rp = _store.settings().get("recent_plans", [])[:2]
            for _i, _e in enumerate(_rp):
                _call = lambda e=_e: ai_engine.bank_topup_async(e["plan"], e["gl"], e["diff"], e["scope"])
                if _i == 0:
                    _call()
                else:
                    _th.Timer(25 * _i, _call).start()
    except Exception:
        pass

# ------------------------------------------------------------------ kenar çubuğu
with st.sidebar:
    st.markdown("<div class='brand'>🎓 Deneme<span>matik</span></div>", unsafe_allow_html=True)
    st.markdown("---")
    st.button("🏠 Ana Sayfa", key="nv_home", use_container_width=True, on_click=lambda: (state.reset_exam(), state.nav("home")))
    st.button("📄 Yaprak Test", key="nv_leaf", use_container_width=True, on_click=setup._tool_go, args=("leaf_start",))
    st.button("🔁 Günlük Tekrar", key="nv_rev", use_container_width=True, on_click=state.nav, args=("review",))
    st.button("🗓️ Çalışma Planım", key="nv_plan", use_container_width=True, on_click=state.nav, args=("plan",))
    st.button("📊 Performans & Raporlar", key="nv_rep", use_container_width=True, on_click=state.nav, args=("reports",))
    st.button("🗂️ Yanlış Arşivim", key="nv_arc", use_container_width=True, on_click=state.nav, args=("archive",))
    st.button("🏅 Rozet & Sertifika", key="nv_bdg", use_container_width=True, on_click=state.nav, args=("badges",))
    try:
        from core import store as _gstore
        _gd, _gw, _gm = _gstore.gen_totals()
        st.markdown("---")
        st.markdown(f"<div style='font-size:.85rem;line-height:1.7'><b>📈 Üretilen soru</b><br>Bugün: <b>{_gd}</b><br>Bu hafta: <b>{_gw}</b><br>Bu ay: <b>{_gm}</b></div>", unsafe_allow_html=True)
    except Exception:
        pass

# ------------------------------------------------------------------ yönlendirme
PAGE = st.session_state.page
if PAGE in ("exam", "ready"):  # soru çözerken dikkat dağıtan hiçbir şey olmasın
    st.markdown("<style>[data-testid='stSidebar'],[data-testid='stSidebarCollapsedControl'],[data-testid='collapsedControl']{display:none !important}</style>", unsafe_allow_html=True)
ROUTES = {
    "home": setup.home, "modes": setup.modes, "setup": wizard.run, "ready": setup.ready, "pre": setup.pre,
    "exam": exam.exam, "selfscore": exam.selfscore, "result": exam.result,
    "reports": reports.reports, "review": study.review, "plan": study.plan, "archive": extras.archive, "badges": extras.badges,
}
try:
    ROUTES.get(PAGE, setup.home)()
except st.errors.StreamlitAPIException:
    raise
except Exception as e:  # sayfa çökmesin: nazik hata + ana sayfaya dön
    if type(e).__name__ in ("RerunException", "StopException"):
        raise
    st.error(f"⚠️ Beklenmeyen bir sorun oluştu ({type(e).__name__}). Aşağıdaki düğmeyle devam edebilirsin.")
    with st.expander("Teknik ayrıntı"):
        st.code(f"{type(e).__name__}: {e}")
    st.button("🏠 Ana sayfaya dön", key="err_home", type="primary", on_click=lambda: (state.reset_exam(), state.nav("home")))
