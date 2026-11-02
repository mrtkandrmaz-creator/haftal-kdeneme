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


def units(g, subject):
    b = base_grade(g)
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
        ("Temel Geometrik Çizimler ve İnşalar", "MAT.5.3.1", [1, 1, 1, 1, 1]),
        ("Temel Geometrik Çizimler ve İnşalar", "MAT.5.3.2", [1, 1, 0, 1, 1]),
        ("Açı Ölçme", "MAT.5.3.3", [1, 1, 2, 2, 2]),
        ("Açı Ölçme", "MAT.5.3.4", [1, 1, 2, 1, 2]),
        ("Çokgenler ve Çember", "MAT.5.3.5", [1, 1, 1, 1, 1]),
        ("Çokgenler ve Çember", "MAT.5.3.6", [1, 2, 1, 0, 0]),
        ("Çokgenler ve Çember", "MAT.5.3.7", [1, 0, 0, 0, 0]),
    ],
    ("5", cur.MAT, 1, 2): [
        ("Çokgenler ve Çember", "MAT.5.3.5", [0, 0, 1, 0, 1]),
        ("Çokgenler ve Çember", "MAT.5.3.6", [0, 1, 0, 1, 1]),
        ("Çokgenler ve Çember", "MAT.5.3.7", [2, 2, 1, 1, 1]),
        ("Basamak Değerlerini Çözümleme", "MAT.5.1.1", [2, 2, 2, 2, 1]),
        ("Doğal Sayılarla Dört İşlem İçeren Problem Çözme", "MAT.5.1.2", [2, 2, 2, 2, 2]),
        ("Dikdörtgenin Çevre Uzunluğu ve Alanı", "MAT.5.4.1", [1, 1, 1, 0, 0]),
        ("Dikdörtgenin Çevre Uzunluğu ve Alanı", "MAT.5.4.2", [1, 0, 0, 0, 0]),
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
        rows = [{"unit": u, "code": c, "topic": u, "n": cnt[scen - 1]}
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


_DISPATCH = {
    "triangle": _triangle, "circle": _circle, "rectangle": _rectangle,
    "bar_chart": _bar, "science_chart": _bar, "line_chart": _line, "pie_chart": _pie,
    "science_space": _space, "space_orbit": _space, "eclipse": _space, "moon_phases": _space,
    "dynamometer": _dynamometer, "thermometer": _thermometer, "number_line": _numberline,
    "forces": _forces, "cylinder": _cylinder,
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
    k = min(max_w / iw, max_h / ih, 1.6 * 72 / 72)
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
                if u:
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


def apply(data):
    cur.LIVE.clear()
    for k, v in data.items():
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
SYSTEM = ("Sen MEB Türkiye Yüzyılı Maarif Modeli soru hazırlama uzmanısın. Bağlam temelli, görsel ve veri yoğun, "
          "yorum ve mantık yürütmeye dayalı yeni nesil sorular yazarsın. Paragraf, metin, tablo ve şema sorularında "
          "asla kesinti yapmaz, eksiksiz üretirsin. Yalnızca geçerli JSON döndürürsün.")
CHUNK = 8


def load_keys():
    import streamlit as st
    try:
        g = list(st.secrets["api_keys"].get("groq_keys", []))
        m = list(st.secrets["api_keys"].get("gemini_keys", []))
    except Exception:
        g, m = [], []
    return g, m


def demo_mode():
    return os.environ.get("DENEMEMATIK_DEMO") == "1"


# ---------------------------------------------------------------- API çağrıları (eski düzen)
def call_groq_with_key(api_key, prompt_text, system=SYSTEM):
    from groq import Groq
    client = Groq(api_key=api_key)
    completion = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "system", "content": system}, {"role": "user", "content": prompt_text}],
        temperature=0.85, max_tokens=8000, response_format={"type": "json_object"})
    return completion.choices[0].message.content


def call_gemini_with_key(api_key, prompt_text, system=SYSTEM):
    from google import genai
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(model=GEMINI_MODEL, contents=system + "\n\n" + prompt_text)
    text = response.text
    if "```json" in text:
        text = text.split("```json")[1].split("```")[0].strip()
    elif "```" in text:
        text = text.split("```")[1].split("```")[0].strip()
    return text


def multi_pool_generate(prompt_text, groq_keys, gemini_keys, offset=0):
    attempts = []
    gk = [k for k in groq_keys if str(k).strip()]
    if gk:
        gk = gk[offset % len(gk):] + gk[:offset % len(gk)]  # paralel işlerde yükü dağıt
    attempts = [(call_groq_with_key, k) for k in gk] + [(call_gemini_with_key, k) for k in gemini_keys if str(k).strip()]
    if not attempts:
        return None, "Geçerli API anahtarı bulunamadı!"
    last = None
    for func, key in attempts:
        try:
            r = func(key, prompt_text)
            if r:
                return r, None
        except Exception as e:  # sıradaki anahtara geç
            last = e
            time.sleep(.4)
    return None, str(last)


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


# ---------------------------------------------------------------- prompt
SHAPE_RULES = (
    "🚨 GÖRSEL KURALLARI (`shape` nesnesi). Matematik, fen ve veri okuma sorularında konuya UYGUN şemayı mutlaka ekle:\n"
    '- Üçgen: {"type":"triangle","sub_type":"right|scalene|equilateral","A":"A","B":"B","C":"C","side_ab":"3 cm","side_bc":"4 cm","angle_a":"60°"}\n'
    '- Çember: {"type":"circle","center":"O","radius":"5 cm","show_diameter":true}\n'
    '- Dikdörtgen: {"type":"rectangle","width":8,"height":5,"width_label":"8 cm","height_label":"5 cm"}\n'
    '- Çubuk: {"type":"bar_chart","labels":[...],"values":[...],"title":"..."}   Çizgi: {"type":"line_chart","labels":[...],"values":[...],"title":"..."}\n'
    '- Daire grafiği: {"type":"pie_chart","labels":[...],"values":[...],"title":"..."}\n'
    '- Tablo: {"type":"table","title":"...","headers":[...],"rows":[[...],[...]]}\n'
    '- Sayı doğrusu: {"type":"number_line","min":0,"max":10,"step":1,"marks":[{"label":"A","value":2.5}]}\n'
    '- Dinamometre (kuvvet ölçme): {"type":"dynamometer","value":6.5,"max_value":10,"unit":"N","mass_label":"m"}\n'
    '- Termometre: {"type":"thermometer","value":23,"min":-10,"max":50,"step":10,"unit":"°C"}\n'
    '- Dereceli silindir: {"type":"cylinder","max":100,"level":62,"step":10,"unit":"mL"}\n'
    '- Kuvvetler: {"type":"forces","left":[20],"right":[35],"unit":"N","object_label":"Kutu"}\n'
    '- Ay evreleri (8 evre, harf etiketli, adı yazmaz): {"type":"science_space","sub_type":"moon_phases","phases":[0,1,2,3,4,5,6,7],"labels":["A","B","C","D","E","F","G","H"],"title":"..."}  (phases: 0 yeni ay,2 ilk dördün,4 dolunay,6 son dördün)\n'
    '- Ay'"'"'ın Dünya çevresindeki 8 konumu (numaralı): {"type":"science_space","sub_type":"moon_orbit","title":"..."}\n'
    '- Güneş/Ay tutulması: {"type":"science_space","sub_type":"solar_eclipse|lunar_eclipse","title":"..."}; Yörünge: {"type":"science_space","sub_type":"orbit"}\n'
    "⛔ Şemanın başlığı, etiketleri ve değerleri sorunun CEVABINI veya İPUCUNU ASLA içermesin; yalnızca ham veriyi göstersin.\n"
    "Görsel gerektirmeyen sorularda 'shape' değerini null yap. Her seferinde konuya uygun FARKLI görsel türü seç.\n"
    "Metinlerde LaTeX KULLANMA; üs için x², kök için √, çarpma için ×, bölme için ÷ gibi Unicode karakterleri kullan.\n")

SUBJECT_HINT = {
    "Türkçe": "Paragraf, sözel mantık, dil bilgisi, görsel/tablo okuma, deyim-atasözü. Metinleri ASLA KISALTMA, eksiksiz yaz.",
    "Matematik": "Problem, geometri, veri analizi, olasılık. Grafik/tablo/şekil kullan; işlem sonucu tek ve kesin olsun.",
    "Fen Bilimleri": "Deney, veri, grafik, günlük hayat bağlamı. Ay-Güneş-Dünya konularında konuya özel şema seç; kuvvet ölçmede dinamometre kullan.",
    "Sosyal Bilgiler": "Tarih/coğrafya/vatandaşlık bağlamı; kaynak metin, harita, tablo, kronoloji yorumlama.",
    "T.C. İnkılap Tarihi ve Atatürkçülük": "Kaynak/belge yorumlama, neden-sonuç, kronoloji; Atatürk dönemi olayları.",
    "Din Kültürü ve Ahlak Bilgisi": "Ayet/hadis meali yorumlama, değerler eğitimi, vaka analizi. Saygılı ve doğru bilgi.",
    "İngilizce": "Sorular İNGİLİZCE yazılır (yönerge dahil). Diyalog tamamlama, okuma parçası, tablo/kart eşleştirme, kelime.",
    "Almanca": "Sorular ALMANCA yazılır. A1 düzeyi: diyalog, okuma, kelime, dilbilgisi.",
}


def mc_prompt(grade_label, subject, n, topics, difficulty, scope_label, avoid, focus="", start_id=1):
    nonce = uuid.uuid4().hex[:8]
    seed_themes = random.sample(["spor", "market", "okul", "doğa", "müze", "tarım", "ulaşım", "teknoloji", "sanat", "sağlık",
                                 "hayvanlar", "mutfak", "tatil", "kütüphane", "çevre", "şehir yaşamı", "bilim insanı", "festival"], 4)
    av = ("\nAŞAĞIDAKİ SORULARI/KONULARI TEKRARLAMA (farklı bağlam ve veri kullan):\n- " + "\n- ".join(avoid[-18:])) if avoid else ""
    fc = f"\nODAK KONU: '{focus}' (soruların yaklaşık 1/3'ünde bu konuya odaklan, kalanı diğer kazanımlardan)." if focus.strip() else ""
    return (
        f"Türkiye Cumhuriyeti MEB {grade_label} {subject} dersi resmî öğretim programı (Türkiye Yüzyılı Maarif Modeli) kazanımlarına "
        f"tam uygun, TAM {n} adet ÇOKTAN SEÇMELİ (A,B,C,D) yeni nesil soru hazırla.\n"
        f"KAPSAM: {scope_label}\nKONULAR/KAZANIMLAR: {topics}{fc}\n"
        f"ZORLUK KADEMESİ: '{difficulty}'. Bu kademeye kesin uy.\n"
        f"DERS YÖNERGESİ: {SUBJECT_HINT.get(subject, '')}\n"
        "MEB yeni nesil soru anlayışı: günlük hayat bağlamı (senaryo/metin/tablo/grafik), yorum ve muhakeme, beceri temelli. "
        "Yalnızca bilgi ezberi sorma. Çeldiriciler makul olsun, doğru cevap TEK olsun ve gerçekten doğru olsun (hesapla, doğrula).\n"
        f"Çeşitlilik tohumu: {nonce}; önerilen bağlam temaları: {', '.join(seed_themes)}. Her soru birbirinden bağımsız ve farklı olsun."
        f"{av}\n\n{SHAPE_RULES}\n"
        "Her soruda: kısa 'topic' (kazanım adı), gerekirse 'passage', 'question', 4 şık, 'answer' (A/B/C/D) ve 2-3 cümlelik 'explanation' (çözüm) olsun.\n"
        'ÇIKTI SADECE şu JSON: {"questions":[{"id":%d,"subject":"%s","topic":"...","passage":"... veya null","question":"...",'
        '"shape":null,"options":{"A":"..","B":"..","C":"..","D":".."},"answer":"A","explanation":"..."}]}' % (start_id, subject))


def oyss_prompt(grade_label, subject, items, difficulty, avoid):
    """items: [{kazanim, n, difficulty_labels:[..]}]"""
    nonce = uuid.uuid4().hex[:8]
    lines = []
    for it in items:
        lines.append(f"- Kazanım: {it['kazanim']} → {it['n']} soru (zorluk etiketleri: {', '.join(it['labels'])})")
    av = ("\nTekrar etme:\n- " + "\n- ".join(avoid[-12:])) if avoid else ""
    return (
        f"MEB Ortak Yazılı Sınav Sistemi (OYSS) için {grade_label} {subject} dersi yazılı sınavı soruları hazırla. "
        "Sorular AÇIK UÇLU ve KISA CEVAPLI olacak (çoktan seçmeli DEĞİL); yaklaşık 1/3'ü kısa cevaplı, kalanı açık uçlu. "
        "Her soru tek bir kazanımı ölçsün, beceri temelli ve bağlamlı olsun; öğrencinin yazarak cevaplayacağı şekilde kurgulansın.\n"
        f"DAĞILIM (kazanım başına tam soru sayısı):\n" + "\n".join(lines) + "\n"
        f"KALİTE KADEMESİ: '{difficulty}'. Etiket (Kolay/Orta/Zor) ile birlikte bu kademeye uy.\n"
        f"DERS YÖNERGESİ: {SUBJECT_HINT.get(subject, '')}\nÇeşitlilik tohumu: {nonce}.{av}\n\n{SHAPE_RULES}\n"
        "Her soru için: beklenen 'answer', ve puanlama anahtarı 'rubric' (adımlar ve göreli puanlar; toplam 10 olsun).\n"
        'ÇIKTI SADECE şu JSON: {"questions":[{"kazanim":"..","type":"Açık uçlu|Kısa cevaplı","difficulty":"Kolay|Orta|Zor",'
        '"passage":"... veya null","question":"..","shape":null,"answer":"..","rubric":[{"step":"..","points":5},{"step":"..","points":5}]}]}')


# ---------------------------------------------------------------- doğrulama
_NOSHUF = re.compile(r"hepsi|yukarıdakilerin|yalnız|yalnızca|ve [IV]+|[IV]+ ve|I, II|hiçbiri|all of|none of|beide|alle", re.I)


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
    if not any(_NOSHUF.search(v) for v in opts.values()):  # şık konumu dengesi: doğru cevap dağılımı
        vals = list(opts.values())
        correct = opts[ans]
        random.shuffle(vals)
        opts = dict(zip("ABCD", vals))
        ans = [k for k, v in opts.items() if v == correct][0]
    from . import visuals
    shape = visuals.normalize_shape(q.get("shape"))
    out = {"subject": subject, "topic": str(q.get("topic") or ""), "passage": q.get("passage") if str(q.get("passage")).lower() not in ("none", "null", "") else "",
           "question": str(q["question"]).strip(), "shape": shape, "options": opts, "answer": ans, "explanation": str(q.get("explanation") or "")}
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
def generate_mc(plan, grade_label, difficulty, scope_label, avoid=None, focus="", on_progress=None):
    """plan: [{subject, n, topics}] -> (questions, errors)"""
    avoid = avoid or {}
    gk, mk = load_keys() if not demo_mode() else ([], [])
    if not demo_mode() and not gk and not mk:
        return [], ["API anahtarı bulunamadı"]
    tasks = []
    for p in plan:
        left, k = p["n"], 0
        while left > 0:
            c = min(CHUNK, left)
            tasks.append((p, c, k))
            left -= c
            k += 1
    errors, results = [], {}
    done = [0]

    def work(idx_task):
        idx, (p, c, k) = idx_task
        subj = p["subject"]
        if demo_mode():
            return idx, _demo_mc(subj, c, p["topics"]), None
        prompt = mc_prompt(grade_label, subj, c, p["topics"], difficulty, scope_label, avoid.get(subj, []), focus if k == 0 else "")
        raw, err = multi_pool_generate(prompt, gk, mk, offset=idx)
        data = parse_json(raw)
        qs = [x for x in (_norm_q(q, subj) for q in (data or {}).get("questions", [])) if x]
        if on_progress:
            done[0] += 1
            on_progress(done[0], len(tasks), subj)
        return idx, qs, (err if not qs else None)

    with ThreadPoolExecutor(max_workers=min(4, max(1, len(tasks)))) as ex:
        for idx, qs, err in ex.map(work, list(enumerate(tasks))):
            results[idx] = qs
            if err:
                errors.append(err)
    questions, seen = [], set(s for v in avoid.values() for s in v)
    for p in plan:
        subj_qs = []
        for idx, (pp, c, k) in enumerate(tasks):
            if pp is p:
                for q in results.get(idx, []):
                    s = _stem(q)
                    if s and s not in seen:
                        seen.add(s)
                        subj_qs.append(q)
        short = p["n"] - len(subj_qs)
        if short > 0 and (demo_mode() or gk or mk):  # eksik kalanı bir kez tamamla
            _, extra, err = work((900, (p, min(short + 2, CHUNK), 1)))
            for q in extra:
                s = _stem(q)
                if s not in seen and len(subj_qs) < p["n"]:
                    seen.add(s)
                    subj_qs.append(q)
        if len(subj_qs) < p["n"]:
            errors.append(f"{p['subject']}: {len(subj_qs)}/{p['n']} soru üretilebildi")
        questions += subj_qs[:p["n"]]
    for i, q in enumerate(questions, 1):
        q["id"] = i
    return questions, errors


def generate_oyss(subject_tables, grade_label, difficulty, avoid=None, on_progress=None):
    """subject_tables: [{subject, rows:[{code,topic,unit,n}]}] -> (questions, errors)"""
    from . import oyss as oy
    avoid = avoid or {}
    gk, mk = load_keys() if not demo_mode() else ([], [])
    if not demo_mode() and not gk and not mk:
        return [], ["API anahtarı bulunamadı"]
    questions, errors = [], []
    for si, st_ in enumerate(subject_tables):
        subj, rows = st_["subject"], st_["rows"]
        total = sum(r["n"] for r in rows)
        labels = oy.difficulty_labels(total)
        random.shuffle(labels)
        items, pos = [], 0
        for r in rows:
            items.append({"kazanim": f"{r['code']} – {r['topic']}", "n": r["n"], "labels": labels[pos:pos + r["n"]]})
            pos += r["n"]
        if demo_mode():
            qs = []
            for it in items:
                for j in range(it["n"]):
                    qs.append({"kazanim": it["kazanim"], "type": "Açık uçlu" if j % 3 else "Kısa cevaplı", "difficulty": it["labels"][j],
                               "passage": "", "question": f"[{subj}] Demo açık uçlu soru {uuid.uuid4().hex[:4]}", "shape": None,
                               "answer": "Demo cevap", "rubric": [{"step": "Adım 1", "points": 5}, {"step": "Adım 2", "points": 5}]})
        else:
            raw, err = multi_pool_generate(oyss_prompt(grade_label, subj, items, difficulty, avoid.get(subj, [])), gk, mk, offset=si)
            data = parse_json(raw)
            qs = [q for q in (data or {}).get("questions", []) if isinstance(q, dict) and q.get("question")]
            if not qs:
                errors.append(f"{subj}: {err or 'geçersiz yanıt'}")
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
            q["shape"] = q["shape"] if isinstance(q.get("shape"), dict) and q["shape"].get("type") else None
            q["answer"] = str(q.get("answer", ""))
        questions += qs
        if on_progress:
            on_progress(si + 1, len(subject_tables), subj)
    for i, q in enumerate(questions, 1):
        q["id"] = i
    return questions, errors
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
[class*="st-key-sel_"] button { background:#fff !important; color:#0f172a !important; border:2px solid #cbd5e1 !important; box-shadow:none !important; padding:.55rem .2rem !important; font-size:.9rem !important; min-height:2.8rem; }
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
  div[data-testid="stHorizontalBlock"]:has([class*="st-key-sel_"]) > div[data-testid="stColumn"] { min-width:calc(20% - .4rem) !important; flex:1 1 calc(20% - .4rem) !important; width:auto !important; }
  div[data-testid="stHorizontalBlock"]:has([class*="st-key-card_"]) > div[data-testid="stColumn"],
  div[data-testid="stHorizontalBlock"]:has([class*="st-key-opt"]) > div[data-testid="stColumn"] { min-width:100% !important; }
  [class*="st-key-card_"] button { min-height:110px; }
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
 ".gen-ring{position:relative;width:170px;height:170px;margin:0 auto 1.1rem}"
 ".gen-ring:before{content:'';position:absolute;inset:0;border-radius:50%;border:10px solid #e2e8f0}"
 ".gen-ring:after{content:'';position:absolute;inset:0;border-radius:50%;border:10px solid transparent;border-top-color:#0284c7;border-right-color:#38bdf8;animation:genspin 1.1s linear infinite}"
 ".gen-cd{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:3.2rem;font-weight:900;color:#0f172a}"
 ".gen-cd span{position:absolute;opacity:0;animation:gencd 1s linear forwards}"
 ".gen-cd span.z{font-size:1.05rem;line-height:1.2;color:#0284c7;animation:genz .5s linear forwards,genpulse 1.2s ease-in-out infinite}"
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
    "duration": 0, "result": None, "saved": False, "self_scores": {},
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
    for k in ("questions", "meta", "answers", "open_answers", "cur", "start", "duration", "result", "saved", "self_scores"):
        st.session_state[k] = copy.deepcopy(DEFAULTS[k])
'''
MODULES['ui/setup'] = r'''# -*- coding: utf-8 -*-
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
    st.markdown("<div class='sec-title'>🎓 Sınıfını Seç</div>", unsafe_allow_html=True)
    theme.cells(GRADE_CARDS, 3, lambda c: theme.card(f"g{c[0]}", c[1], f"{c[2]} {c[3]}", c[4], pick_grade, (c[0],)))
    st.markdown("<div class='sec-title'>🧰 Araçlar</div>", unsafe_allow_html=True)
    tools = [("leaf", "green", "📄 Yaprak Test", "Tek kazanımlık hızlı çalışma kâğıdı + PDF", "leaf_start"),
             ("reports", "indigo", "📊 Performans & Raporlar", "Grafikler, ders karşılaştırmaları", "reports"),
             ("archive", "amber", "🗂️ Yanlış Arşivim", "Yanlış yaptığın sorulardan kişisel test", "archive"),
             ("badges", "slate", "🏅 Rozet & Sertifika", "Başarılarını topla, sertifika al", "badges")]
    theme.cells(tools, 2, lambda x: theme.card(f"tool_{x[0]}", x[1], x[2], x[3], _tool_go, (x[4],)))


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


def weight_panel(g, key):
    """Ders ağırlıkları: soru sayısını çarpan. Otomatik mod, geçmiş başarına göre zayıf derslere ağırlık verir."""
    auto = st.toggle("📉 Zayıf derslerime otomatik ağırlık ver (geçmiş sınavlarıma göre)", key=f"auto_{key}")
    aw = _auto_weights(g) if auto else {}
    out = {}
    with st.expander("⚖️ Ders ağırlıkları (soru sayısını çarpan)", expanded=auto):
        cols = st.columns(4)
        for i, s in enumerate(cur.subjects_for(g)):
            with cols[i % 4]:
                out[s] = st.select_slider(f"{cur.SUBJECT_ICONS.get(s, '')} {s}", WEIGHTS, value=aw.get(s, 1.0),
                                          key=f"w_{key}_{s}_{int(auto)}", format_func=lambda x: f"×{x:g}")
    return out


def subject_counts(g, defaults, key):
    out = {}
    with st.expander("⚙️ Ders başına soru sayıları", expanded=False):
        cols = st.columns(4)
        for i, s in enumerate(cur.subjects_for(g)):
            with cols[i % 4]:
                out[s] = st.number_input(f"{cur.SUBJECT_ICONS.get(s, '')} {s}", 0, 40, int(defaults.get(s, 0)), key=f"{key}_{s}")
    out = {k: v for k, v in out.items() if v > 0}
    st.caption(f"Toplam: **{sum(out.values())} soru** • Süre: **{sum(out.values()) * SEC_PER_Q // 60} dk** (soru başına 90 sn)")
    return out


def _avoid():
    return store.recent_stems()


def _finish(qs, errs, meta):
    if errs:
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
    st.session_state.page = "pre"
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
    return 12 + 14 * math.ceil(chunks / 4)


def _gen_mc(plan, meta, scope_label, focus=""):
    n = sum(p["n"] for p in plan)
    qs, errs = with_overlay(est_seconds_mc(plan), "Sorular hazırlanıyor", f"{n} yeni nesil soru ve görselleri yapay zekâ ile üretiliyor…",
                            lambda: ai.generate_mc(plan, meta["grade_label"], meta["difficulty"], scope_label, avoid=_avoid(), focus=focus))
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
    lst = list(w.get(field, []))
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
            st.markdown("#### Hafta seç")
            st.caption("📍 = bu hafta • MEB 2026-2027 çalışma takvimi (ara tatiller hariç 36 öğretim haftası). Seçince otomatik ilerler.")
            theme.cells(range(1, 37), 6, lambda n: st.button(f"{'📍' if n == cw else ''}{n}. Hf", key=f"sel_{'on' if w.get('week') == n else 'off'}_w{n}", on_click=go, kwargs=dict(week=n)))
        else:
            sug = cur.suggested_month()
            st.markdown("#### Ay seç")
            st.info(f"📌 AGİS ayın ilk haftasında çözülür ve **bir önceki ayı** ölçer. Bugüne göre önerilen: **{cur.MONTHS[sug - 1]['name']}**.")
            theme.cells(range(1, cur.NUM_MONTHS + 1), 5, lambda m: st.button(f"{'📌 ' if m == sug else ''}{cur.MONTHS[m - 1]['name']}", key=f"sel_{'on' if w.get('month') == m else 'off'}_m{m}", on_click=go, kwargs=dict(month=m)))
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
        diff = su.difficulty_select("diff_wz")
        counts = dict(f["counts"])
        official = f["id"] in OFFICIAL_IDS
        wts = {}
        if not official:
            with st.expander("⚖️ Ders ağırlığı (isteğe bağlı)"):
                wts = su.weight_panel(g, f"wz_{g}")
            counts = {s: max(0, round(n * wts.get(s, 1.0))) for s, n in counts.items()}
            counts = {s: n for s, n in counts.items() if n > 0}
        focus = st.text_input("🔍 Özel konu (isteğe bağlı)", key="focus_wz", placeholder="Örn: Açılar, Hücre, Paragraf…")
        n = sum(counts.values())
        same = all(abs(wts.get(s, 1.0) - 1.0) < 1e-9 for s in wts)
        minutes = f["min"] if same else max(1, n * su.SEC_PER_Q // 60)
        rows = [(f"{cur.SUBJECT_ICONS.get(s, '')} {s}", c, cur.scope_short(g, s, scope) or "—") for s, c in counts.items()]
        theme.html_table(["Ders", "Soru", "Kapsanan üniteler"], rows, num_cols=(1,))
        st.caption(f"Toplam **{n} soru** • süre **{minutes} dk**")
        c1, c2 = st.columns(2)
        with c1:
            st.button("← Geri", key="wz_back_4", on_click=back, args=("modes",))
        with c2:
            go_btn = st.button("🚀 Soruları Üret", key="gen_wz", type="primary")
        if go_btn and counts:
            plan = [{"subject": s, "n": c, "topics": cur.scope_topic_text(g, s, scope), "short": cur.scope_short(g, s, scope)} for s, c in counts.items()]
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
        c1, c2 = st.columns(2)
        with c1:
            st.button("← Geri", key="wz_back_4", on_click=back, args=("modes",))
        with c2:
            go_btn = st.button("🚀 OYSS Sorularını Üret", key="gen_oyss", type="primary")
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
        chosen = st.multiselect("Kazanım / konu (boş bırakırsan ünitenin tamamı)", tps, key=f"wz_tops_{w['subj']}_{w['unit']}")
        opts = [6, 8, 10, 12] if leaf else [10, 15, 20, 30]
        n = theme.pick_cards("v_wz_n_" + st.session_state.mode, opts, opts[2 if leaf else 1], 4, "cnt", label_fn=lambda x: f"{x}\nsoru", label="🔢 Kazanım soru sayısı")
        diff = su.difficulty_select("diff_tp")
        c1, c2 = st.columns(2)
        with c1:
            st.button("← Geri", key="wz_back_3", on_click=back, args=(first,))
        with c2:
            go_btn = st.button("🚀 Testi Üret", key="gen_tp", type="primary")
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
        with st.expander("⚖️ Ders ağırlığı (isteğe bağlı)"):
            bw = su.weight_panel(g, f"bk_{g}")
        diff = su.difficulty_select("diff_bk")
        c1, c2 = st.columns(2)
        with c1:
            st.button("← Geri", key="wz_back_b2", on_click=back, args=("modes",))
        with c2:
            go_btn = st.button("🚀 Testi Üret", key="gen_bk", type="primary")
        if go_btn:
            plan = []
            for s in w["subs"]:
                tp = cur.all_topics(g, s)
                pick = random.sample(tp, min(6, len(tp)))
                plan.append({"subject": s, "n": max(1, round(per * bw.get(s, 1.0))), "short": "Karma kazanımlar",
                             "topics": "; ".join(f"{u}: {t}" for u, t in pick) + " (görsel/tablo/grafik ağırlıklı, beceri temelli)"})
            su._gen_mc(plan, su._meta_common(gl, "bank", f"{gl} Yeni Nesil Soru Bankası", "Karma", diff, plan), "Yıl geneli karma")
'''
MODULES['ui/exam'] = r'''# -*- coding: utf-8 -*-
import hashlib
import time
import altair as alt
import pandas as pd
import streamlit as st
from core import curriculum as cur, store
from core.visuals import draw_geometry_shape
from . import theme
from .state import nav, reset_exam
from .setup import pdf_panel


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
                          "ts": int(time.time())})
    store.add_wrong(items)


def finish():
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
    n1, n2, n3 = st.columns([1, 2, 1])
    with n1:
        if idx > 0:
            st.button("⬅️ Önceki Soru", key="prev", on_click=_go, args=(-1,))
    with n2:
        st.markdown(f"<div style='text-align:center;font-weight:900;color:#4c1d95;padding-top:.6rem'>Soru {idx + 1} / {total}</div>", unsafe_allow_html=True)
    with n3:
        if idx < total - 1:
            st.button("➡ Sonraki Soru", key="next", on_click=_go, args=(1,), type="primary")
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("---")
    st.button("🏁 Deneme Sınavını Tamamla ve Sonuçları Gör", key="finish_btn", on_click=finish, type="primary")


# ------------------------------------------------------------------ OYSS öz-değerlendirme
def selfscore():
    m, qs = st.session_state.meta, st.session_state.questions
    st.markdown("<div class='hero'><h1>✍️ Puanlama Anahtarıyla Öz Değerlendirme</h1><p>Yazılı sınavlar öğretmen puanlar. Cevabını beklenen cevap ve puanlama anahtarıyla karşılaştırıp her soruya aldığın puanı gir.</p></div>", unsafe_allow_html=True)
    with st.form("selfscore_form"):
        for i, q in enumerate(qs):
            with st.expander(f"Soru {i + 1} • {q.get('subject', '')} • {q.get('kazanim', '')} • {q.get('points')} puan • {q.get('difficulty', '')}", expanded=(i == 0)):
                if q.get("passage"):
                    st.markdown(f"> {q['passage']}")
                if isinstance(q.get("shape"), dict):
                    draw_geometry_shape(q["shape"])
                st.markdown(f"**{q['question']}**")
                st.markdown(f"**Senin cevabın:** {st.session_state.open_answers.get(i) or '_(boş)_'}")
                st.success(f"**Beklenen cevap:** {q.get('answer', '')}")
                if q.get("rubric"):
                    theme.html_table(["Puanlama adımı", "Puan"], [(r.get("step", ""), r.get("points", "")) for r in q["rubric"]], num_cols=(1,))
                st.number_input("Aldığın puan", 0, int(q.get("points", 0)), 0, key=f"self_in_{i}")
        ok = st.form_submit_button("📊 Sonucu Göster")
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
    st.markdown("<div class='sec-title'>📄 PDF Çıktısı</div>", unsafe_allow_html=True)
    pdf_panel("res_")
    b1, b2, b3 = st.columns(3)
    with b1:
        st.button("📊 Performans & Raporlar", key="to_rep", on_click=nav, args=("reports",))
    with b2:
        st.button("🗂️ Yanlış Arşivim", key="to_arc", on_click=nav, args=("archive",))
    with b3:
        st.button("🏠 Ana Sayfa", key="to_home", on_click=lambda: (reset_exam(), nav("home")))
    with st.expander("📖 Detaylı Soru Çözüm, Cevap Anahtarı ve Tüm Şıkları İncele", expanded=False):
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
            else:
                st.markdown(f"### Soru {i + 1} [{q.get('subject', '')}] — {st.session_state.self_scores.get(i, 0)}/{q.get('points')} puan")
                st.markdown(f"**{q['question']}**\n\n**Beklenen cevap:** {q.get('answer', '')}")
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
        _backup(hist)


def _backup(hist):
    st.markdown("**Yedekle / Geri yükle** — Streamlit Cloud geçici disk kullanır; verini düzenli yedekle.")
    blob = json.dumps({"history": hist, "wrong": store.wrong()}, ensure_ascii=False).encode("utf-8")
    st.download_button("⬇️ Yedeği indir (JSON)", blob, file_name="denemematik_yedek.json", mime="application/json", key="bk_dl")
    up = st.file_uploader("Yedeği geri yükle", type="json", key="bk_up")
    if up is not None and st.button("♻️ Geri yükle", key="bk_go"):
        try:
            d = json.loads(up.read().decode("utf-8"))
            store.replace_history(d.get("history", []))
            store.replace_wrong(d.get("wrong", []))
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
                                    lambda: ai.generate_mc(plan, gl, diff, "Yanlış arşivi", avoid=store.recent_stems()))
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

ORDER = ['core/curriculum', 'core/oyss', 'core/visuals', 'core/pdf_export', 'core/store', 'core/meb_live', 'core/ai_engine', 'ui/theme', 'ui/state', 'ui/setup', 'ui/wizard', 'ui/exam', 'ui/reports', 'ui/extras']


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
from ui import theme, state, setup, wizard, exam, reports, extras

theme.inject()
state.init()
if "meb_loaded" not in st.session_state:
    st.session_state.meb_loaded = True
    st.session_state.meb_ts = meb_live.load_cache()
    # MEB müfredatı otomatik: gerekirse arka planda çek, olmazsa yerleşik müfredat zaten hazır
    try:
        if not ai_engine.demo_mode() and meb_live.needs_refresh():
            _ph = st.empty()
            _ph.markdown(theme.overlay_html(40, "MEB müfredatı güncelleniyor", "Güncel kazanımlar mufredat.meb.gov.tr'den alınıyor…"), unsafe_allow_html=True)
            try:
                meb_live.refresh(deadline=40)
            finally:
                _ph.empty()
            st.session_state.meb_ts = meb_live.load_cache()
    except Exception:
        pass

GROQ_KEYS, GEMINI_KEYS = ai_engine.load_keys()
if not GROQ_KEYS and not GEMINI_KEYS and not ai_engine.demo_mode():
    st.error("⚠️ `.streamlit/secrets.toml` dosyasında API anahtarları bulunamadı!")
    st.code('[api_keys]\ngroq_keys = ["gsk_..."]\ngemini_keys = ["AIza..."]', language="toml")
    st.stop()

# ------------------------------------------------------------------ kenar çubuğu
with st.sidebar:
    st.markdown("<div class='brand'>🎓 Deneme<span>matik</span></div>", unsafe_allow_html=True)
    st.caption("MEB Maarif Modeli • AI ile sınırsız deneme")
    st.markdown("---")
    st.button("🏠 Ana Sayfa", key="nv_home", on_click=lambda: (state.reset_exam(), state.nav("home")))
    st.button("📄 Yaprak Test", key="nv_leaf", on_click=setup._tool_go, args=("leaf_start",))
    st.button("📊 Performans & Raporlar", key="nv_rep", on_click=state.nav, args=("reports",))
    st.button("🗂️ Yanlış Arşivim", key="nv_arc", on_click=state.nav, args=("archive",))
    st.button("🏅 Rozet & Sertifika", key="nv_bdg", on_click=state.nav, args=("badges",))
    st.markdown("---")
    g = st.session_state.grade
    if g:
        st.markdown(f"<div class='side-chip'>🎓 <b>{cur.GRADE_LABELS[g]}</b><br>Seçili tür: {st.session_state.mode or '—'}</div>", unsafe_allow_html=True)
    mode_txt = "DEMO (çevrimdışı)" if ai_engine.demo_mode() else f"Groq {len(GROQ_KEYS)} • Gemini {len(GEMINI_KEYS)}"
    st.markdown(f"<div class='side-chip'>🤖 API havuzu<br><b>{mode_txt}</b><br><small>Önce Groq, sonra Gemini</small></div>", unsafe_allow_html=True)

# ------------------------------------------------------------------ yönlendirme
PAGE = st.session_state.page
ROUTES = {
    "home": setup.home, "modes": setup.modes, "setup": wizard.run, "pre": setup.pre,
    "exam": exam.exam, "selfscore": exam.selfscore, "result": exam.result,
    "reports": reports.reports, "archive": extras.archive, "badges": extras.badges,
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
