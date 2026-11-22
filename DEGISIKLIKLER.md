# Denemematik — Son Dönem İyileştirmeler (5. sınıf odaklı)

Bu belge, son günlerde yapılan tüm iyileştirmeleri özetler. Matematik ve Fen Bilimleri ayrı başlıklar altında, genel (tüm dersler) iyileştirmeler en başta.

## Tüm dersler
- **Kazanım dağılımı dengelendi.** Sınavda tek bir kazanıma yığılma azaltıldı; seçilen ünitelerin kazanımları dengeli kapsanıyor. Din Kültürü'ndeki tekrarlar giderildi.
- **Sınav sayısı garantisi korundu.** Seçilen soru sayısı her zaman üretiliyor.
- **Tekrar önleme.** Ardışık sınavlarda aynı ya da benzer soru çıkmaması için kalıp/kök takibi var.
- **"Hatalı" işaretlenen soru bir daha gelmiyor.** Hatalı bildirilen sorular (ve bilgi bankası maddeleri) kalıcı olarak engelleniyor. Kenar çubuğunda bildirilen sorular listesi ve öz-denetim var.
- **Bilgi bankası (5. sınıf Fen, Sosyal, Türkçe, İngilizce, Din).** Her kazanım için ayrı bilgi–soru üreten kalıplar (tek doğru, doğru ifade, I–II–III öncüllü). Yaklaşık 270 ek bilgi eklendi.
- **Bilgi bankası doğrulaması.** Butonla ve gece çalışan `tools/verify_bank.py` ile bankadaki bilgiler yapay zekâyla taranıyor; şüpheli maddeler ayrılıyor.
- **Gece havuz üretimi.** GitHub Actions ile havuz, şablon ve banka doğrulaması otomatik çalışıyor.
- **Soru kökü çeşitliliği.** Tek kalıplı sorulara birden çok ifade biçimi eklendi (Matematik, Fen ve Sosyal Bilgiler'in dar kalıpları). Anlam ve metindeki değerler değişmiyor.
- **Metin–görsel–şık uyumu** kuralı korunuyor: metinde verilen her değer (açı, uzunluk, dinamometre vb.) görselde de yazılı.

## Matematik (5. sınıf)
- **Kazanım kodu eşlemesi (MAT.5.x).** Kalıpların kazanımlara eşlenmesi tamamlandı; eksik sanılan MAT.5.4.3 kalıplarının sadece eşlenmemiş olduğu düzeltildi.
- **Yeni istatistik kalıpları.** Tablo/sütun grafiği yorumu, çetele, veriye dayalı karar ve benzeri temalar; yorum cümlelerinin dil bilgisi düzeltildi.
- **Tek kalıplı kazanımlara yeni kalıplar:**
  - MAT.5.2.1: dağılma/değişme/ters işlem ve eşitliğin korunumu
  - MAT.5.2.2: gerçek yaşam problemlerinde işlem önceliği
  - MAT.5.4.4: şekilli dikdörtgen problemleri (çit, halı, alan–çevre)
  - MAT.5.1.4: şişelerle kesir karşılaştırma
- **Mevcut kalıplara yeni soru türleri:**
  - Doğru–ışın–doğru parçası: özellik cümleleriyle ve "değildir" biçimiyle soru
  - Çevre/alan sayma: alan verilen dikdörtgen sayısı, en büyük/en küçük alan
  - Kartlarla sayı: en küçük ve ikinci en büyük
  - Tahmin: toplama tahmini
  - Yüzde hesabı: altı farklı senaryo
- **Soru kökü çeşitlemesi** yaklaşık 45 kalıba (açı, EBOB–EKOK, örüntü, kesir sıralama, yüzde, çevre vb.) eklendi; "15'dir" gibi ek hatası giderildi.
- **Kalite kuralları.** Negatif şıklar reddediliyor; geometri sorularında şekil zorunlu; yinelenen şıklar reddediliyor.
- **Matematik havuzunun genişletilmesi (2026-11-22).** 5. sınıf Matematik'te 370 ailenin 268'i sabit soru kökü yüzünden yalnızca 1–6 soru üretiyordu (toplam 609). Bu ailelere 16 yansız açılış cümlesi eklendi (ör. "Aşağıdaki soruyu dikkatle okuyunuz."). Sınav kurulurken aynı kalıptan en çok 2 soru alındığı için havuz büyüdü ama sınavda benzer soru artmadı. Matematik 5. sınıf havuzu 2940 → yaklaşık 8000 soru; Çevre ve Alan (MAT.5.4.x) yaklaşık 40 → 260–330, MAT.5.5.2 27 → 220.
- **MAT.5.2.4 aritmetik işlem algoritmaları:** 5 yeni aile: basamaklı toplama ve çıkarmada silinen rakamlar (A, B; tek çözüm doğrulamalı, tablo görselli), çarpmada kısmi çarpımlar tablosu, bölme algoritması (bölünen = bölen × bölüm + kalan, en büyük kalan), çok adımlı işlemler. MAT.5.2.4: 30 → yaklaşık 120 soru.
- **Düzeltilen hata:** Matematik tablolu sorulara Fen'e özgü "Deney tablosuna göre" ifadesi karışıyordu; artık yalnızca fen derslerinde kullanılıyor. Konu denetiminde "algoritma" ünitesinde rakam/basamak sözcükleri konu dışı sayılmıyor.
- **Konu sızıntısı taraması (2026-11-21).** Her Matematik ünitesi için canlı üretimde hangi kalıpların çıktığı tarandı. Kazanım kodu seçildiğinde (MAT.5.x.y) artık başka kazanıma ait kalıplar anahtar sözcükle (basamak, işlem, problem) sızmıyor; ör. Cebirsel Düşünme'de dört işlem, Dört İşlem'de basamak değeri, Veri Toplama'da denklem/örüntü soruları geliyordu. Kodsuz 30 kadar kalıba kazanım kodu verildi (MAT.5.1.1, 5.1.2, 5.2.2). Tarama sonucu: kodlu sızıntı 0. Matematik 5. sınıf havuzu 2940 soru.
- **Altı basamaklı sayılar / MAT.5.1.1 (2026-11-21).** Bu konu seçilince başka konudan soru geliyordu: arı kanadı (dört işlem) problemi "basamak" sözcüğüyle içeri sızıyordu, kapatıldı. Mevcut basamak aileleri 6–8 basamağa dağılıyordu; artık ağırlıklı olarak altı basamaklı. 13 yeni görselli/şekilli aile eklendi: sayı doğrusunda okunuş, toplam/fark, iki sayı arası, en yakın yüz bine/on bine yuvarlama; sayı örüntüsü tablosu; tablodan sıralama (nüfus, stadyum, ziyaretçi); basamak tablosunda basamak değerleri toplamı/farkı; I–II–III öncüllü; okunuş–yazılış; çözümlemede boşluk; en küçük/en büyük altı basamaklı, bir önceki/sonraki sayı. Sayı doğrusu etiketleri 100 000 biçiminde (binlik boşluklu). MAT.5.1.1 havuzu 238 → 591 soru (Matematik 5. sınıf toplam 2963).
- **Maarif uyumu (2026-11-21).** Kitap/program karşılaştırmasında MAT.5.6 (olasılık) için hiç soru yoktu, MAT.5.2.x en fazla 7 soruyla zayıftı. İki yeni ünite eklendi ve 13 yeni soru ailesi yazıldı:
  - **Veriden Olasılığa (MAT.5.6.1-2):** olasılık çizgisi (imkânsız–kesin), çark, torba, tablo ve aralık soruları; iki yeni görsel (`prob`: renkli çark/torba/olasılık çizgisi, `orun`: birim kareli şekil örüntüsü). Metindeki sayılar görselde yazılı.
  - **İşlemlerle Cebirsel Düşünme (MAT.5.2.1-4):** şekil ve sayı örüntüleri (tablolu), terazi ile eşitliğin korunumu, kayıp sayı, değişme/birleşme/dağılma, parantezli işlem önceliği, para üstü ifadesi, algoritmalar.
  - Konu denetimi: şekil örüntüleri "birim kare" dediği için yanlışlıkla geometri sanılıyordu; cebir konusunda bu artık serbest.
  - Matematik 5. sınıf havuzu 1324 → 2009 soru; MAT.5.6.1: 45, MAT.5.6.2: 79, MAT.5.2.1–4: 49/32/32/16. run_checks 12/12.

## Fen Bilimleri (5. sınıf)
- **MEB 2018 programına geçiş (7 ünite):** Güneş, Dünya ve Ay · Canlılar Dünyası · Kuvvetin Ölçülmesi ve Sürtünme · Madde ve Değişim · Işığın Yayılması · İnsan ve Çevre · Elektrik Devre Elemanları.
- **Yeni ünite "Canlılar Dünyası"** (sınıflandırma, mikroskobik canlılar, şapkalı mantarlar, mikroskop gözlemi, bitki–hayvan gruplama).
- **Kapsam dışı konular çıkarıldı:** hücre, besin zinciri, Ay–Güneş tutulması (7. sınıf), afet soruları (Sosyal Bilgiler). (Destek ve hareket sistemi artık ayrı ünite, aşağıya bakınız.)
- **Yaklaşık 60 yeni bilgi** eklendi; her kazanım için daha fazla soru çeşidi.
- **Ünite sınıflayıcı düzeltmesi:** "doğrudur/ünite/bilgi" gibi genel sözcükler artık yanlış üniteye atamaya yol açmıyor.
- **Soru kökü çeşitlemesi:** Ay'ın evreleri, yay uzaması, ağırlık, sürtünme tablosu, geri dönüşüm vb. kalıplara yeni ifadeler.
- **Canlılar Dünyası görsel genişletmesi (2026-11-21).** MEB kitap görselleri birebir kopyalanmadı; özgün, ders kitabı tarzı çizimler eklendi: ayçiçeği, kaktüs, buğday, salyangoz, arı, örümcek, kaplumbağa, yılan; 6 yeni şekilli soru ailesi.
- **Tüm Fen ünitelerinde şekilli soru artışı.** Sabit soru kökleri yüzünden 100'e yakın şekilli aile havuzda 1–3 soruda kalıyordu; açılış cümleleriyle çeşitlendirildi. Ortak soru kökü listesindeki bozuk ifadeler ("…inceleyen bir öğrenci şu soruyu yanıtlayınız") düzeltildi; tablolu sorularda "Tabloya göre" gibi ifadeler kullanılıyor.
- **MEB soru tarzları eklendi:** gerekçeli doğru/yanlış ("Doğru; çünkü…"), ışığın doğrusal yayılması için borulu ağaç çizimi (3 aile), Ay evresi sıralama ve hafta hesabı, ısı iletimi tablosu (mumun erime süresi), ampul parlaklığı hipotezi ve değişken kontrolü tablosu.
- **Maarif uyumu (2026-11-21).** Güncel MEB (Maarif) programındaki "Canlıların Yapısına Yolculuk" ünitesine karşılık **"Destek ve Hareket Sistemi"** ünitesi eklendi (14 aile, yaklaşık 196 soru): iskelet çizimi (harfli kemik/eklem), kemik–eklem–kas tablosu, görevler, sağlık davranışları, öncüllü ve gerekçeli sorular. Ünite kartlarında her Fen ünitesinin Maarif adı da gösteriliyor (ör. Işığın Yayılması • Maarif: Işığın Dünyası).
- Fen 5. sınıf havuzu yaklaşık 3270 soru; run_checks 12/12.

## TÜBİTAK ve Olimpiyat (yeni, 2026-11-21)
- Ana sayfada **Araçlar** bölümüne ve kenar çubuğuna **"🏆 TÜBİTAK ve Olimpiyat"** kartı eklendi. Akış: kart → sınıf seçimi (4–8, LGS) → sınıfa uygun olimpiyat/yarışma listesi → ayrıntı sayfası.
- Liste TÜBİTAK'ın resmî sayfalarına göre: 5–8. sınıf için Ulusal Ortaokul Bilim Olimpiyatı (Matematik, Bilgisayar) ve 2204-B Ortaokul Araştırma Projeleri Yarışması; 8. sınıf ve LGS için ayrıca Ulusal Bilim Olimpiyatları (Fizik, Kimya, Biyoloji, Astronomi-Astrofizik, Coğrafya). 4. sınıfta başvuru olmadığı için hazırlık mesajı gösterilir.
- Ayrıntı sayfası: program/aşamalar, hazırlık konuları, resmî TÜBİTAK bağlantısı ve (proje dışındakiler için) Yeni Nesil Soru Bankası ile antrenman düğmesi. Gerçek olimpiyat soruları değildir.
- Sınırlar: tarih ve kurallar her yıl değişir (ekranda uyarı var); başvuru koşullarının bir kısmı 2018 duyurusundan alındı. Ortaokul 2204-B'de sınıf aralığı sayfada açık yazmadığı için "ortaokul öğrencileri" denildi.

- **TÜBİTAK müfredatı (2026-11-21).** Olimpiyat ayrıntı sayfasına "📚 Müfredat" bölümü eklendi: Matematik/Bilgisayar için 5. sınıftan seçilen sınıfa kadar her sınıfın Maarif ünite ve kazanımları (sekmeli); 8. sınıf Fizik/Kimya/Biyoloji/Astronomi için Fen Bilimleri üniteleri, ilgili olanlar 🎯 ile işaretli; Coğrafya için 7. sınıf Sosyal Bilgiler. TÜBİTAK'ın kendi resmî konu listesi doğrulanamadı; ekranda bu belirtiliyor.

## Zihinden Matematik (yeni, 2026-11-22)
- Sol panele ve ana sayfa **Araçlar** bölümüne **"🧮 Zihinden Matematik"** eklendi. Yapay zekâ gerekmez; sorular kodla üretilir, cevaplar kodla doğrulanır (45 000 üretilmiş sorunun cevabı bağımsız hesapla kontrol edildi, hata 0).
- Ekran: sınıf düzeyi (4–8), zorluk (Kolay/Orta/Zor), tür (10/20/30 soru ya da 60 saniye) ve sınıfa göre açılan 15 antrenman türü + Karma: Hızlı Toplama, Hızlı Çıkarma, Çarpım Tablosu, Kısa Yol Çarpma (×5, ×9, ×11, ×25, ×99), Bölme ve Kalan, Tamamlama, Eksik Sayıyı Bul, İşlem Önceliği, 10-100-1000 ile Çarpma/Bölme, Ondalık Toplama-Çıkarma, Yüzde Zihinden, Kesir Zihinden, Kare ve Küp, EBOB-EKOK, Üslü Sayı ve Karekök.
- Oyun akışı: cevabı yaz + Enter; her soruda doğru/yanlış ve süre; bitişte doğruluk, ortalama süre, yanlışlar için kısa yol ipucu, en yavaş çözülenler; tür başına kişisel rekor profilde saklanır (60 sn modunda en çok doğru, soru modunda %90+ doğrulukla en düşük sn/soru).
- **Günlük hedef ve seri (2026-11-22):** menünün başında günlük hedef paneli (3/5/10/15/20 dk, varsayılan 5), bugünkü süre ve soru sayısı, 🔥 seri (üst üste hedef tamamlanan gün; bugün henüz bitmediyse dünden sayılır), son 7 gün çizelgesi (🟩 hedef tamam, 🟨 çalıştın). Her tur bitince süre/soru/doğru profile eklenir (son 90 gün saklanır); sonuç ekranında hedefe kalan süre gösterilir.
- **Zihinden Matematik 2 (2026-11-22):** (1) **Otomatik zorluk:** üst üste 3 hızlı ve doğru cevapta seviye yükselir, 2 üst üste hatada düşer; bitişte ulaşılan seviye gösterilir. (2) **Zayıf Yönlerimi Çalış:** tür başına doğruluk ve hız profilde tutulur; en zorlanılan 3 tür için ayrı antrenman kartı ve "Türlere göre durumun" listesi. (3) **Kısa Yol Dersleri:** 14 teknik (yuvarla-telafi, ×5/×9/×11/×25/×99, dağılma, tamamlama, yüzde, kesir, 5 ile biten kare, bölmeyi parçalama, virgül kaydırma) adım adım ve örnekli; her dersin altında o türde 20 soruluk antrenman düğmesi. Ders örneklerinin hepsi hesapla doğrulandı.
- Sınır: Enter ile gönderimde kutuya otomatik odak tarayıcıya bağlıdır; çalışmazsa kutuya tıklamak gerekir. Sayaç canlı akmaz, her cevaptan sonra güncellenir (Streamlit sınırı).

## Kararlılık ve profil silme (2026-11-21)
- **Profil silme:** Giriş ekranında profil seçilince ve kenar çubuğunda (giriş yapılmış profil için) "🗑️ Bu profili sil" bölümü eklendi. PIN varsa PIN, ayrıca profil adını yazarak onay istenir. Profilin yerel verisi ve GitHub yedeği (data/profiles/<id>) silinir; yeniden başlatmada geri gelmez. Misafir profil etkilenmez.
- **Takılma nedenleri ve düzeltmeler:**
  - Günlük banka denetimi tüm denetim boyunca banka kilidini tutuyordu; sınav hazırlayan ana iş parçacığı bu sürede bekliyordu. Denetim kilit dışında yapılıyor, kilit yalnızca silme anında kısa alınıyor; arayüze yer bırakmak için küçük bekleme var.
  - Dosya kaydı aynı geçici dosyayı kullanıyordu; aynı anda iki yazıcı olunca "dosya yok" hatası ("Beklenmeyen sorun") çıkabiliyordu. Her yazıcıya ayrı geçici dosya + kısa kilit.
  - Yeniden başlatma sonrası ilk açılışta GitHub yedeği tek tek (sıralı) indiriliyordu; artık paralel, profiles.json önce, toplam 40 sn sınırlı.
  - MEB müfredat otomatik çekimi (PDF indirme/ayrıştırma) arka planda sunucuyu yavaşlatıyordu; varsayılan KAPALI. Gerekirse secrets'a `meb_live_auto = true` ya da ortam değişkeni `MEB_LIVE_AUTO=1` ile açılır. 5. sınıf ve Matematik zaten yerleşik Maarif listesini kullanıyor.
  - Sınav ekranındayken arka plan banka denetimi ve günlük doldurma başlatılmıyor.
- Not: gerçek Streamlit bu ortamda çalıştırılamadığı için yük altında canlı ölçüm yapılmadı; nedenler kod incelemesi ve eşzamanlılık testiyle bulundu.

## TÜBİTAK ve Olimpiyat — Olimpiyat tarzı antrenman (2026-11-22)
- Matematik ve Bilgisayar olimpiyatı sayfalarına **"🧩 Olimpiyat tarzı antrenman (10 soru)"** düğmesi eklendi (4. sınıf ekranında da var).
- 17 kodla üretilen soru türü: sayı/şekil örüntüsü, yalancı–doğrucu mantığı (tek çözümlü), rakam bulmacaları, kare sayma, tokalaşma, gün döngüsü, çarpma ilkesi, yaş, ortalama, sihirli kare (tablolu), kibrit örüntüsü, sayfa numarası, güvercin yuvası, kalan problemi, boy sıralaması, makine (tersten işlem), ikilik sistem.
- Her sorunun cevabı hesapla bulunur; testlerde bağımsız olarak yeniden doğrulandı (0 hata). 5 şık, tekil; sınıfa göre tür/zorluk seçilir.
- Soru sonrası açıklama, sonuçta tür bazlı skor, yanlışların çözümü ve en iyi skor kaydı var.
- Sorular özgündür; gerçek Kanguru/olimpiyat soruları değildir.

## Diğer derslerde havuz genişletmesi (2026-11-22)
- Matematik'teki gibi diğer 5. sınıf dersleri de dar ayarla (aile başına az soru) üretilmişti. Havuz, aile başına 30 soru ve ünite sınırı kaldırılarak yeniden üretildi: Fen 3272 → 5324, Sosyal Bilgiler 871 → 1747, Türkçe 900 → 2643, Din Kültürü 750 → 1660, İngilizce 933 → 1197.
- Kontroller: tüm sorularda doğru cevap şıklar arasında, şıklar tekil, aynı soru metni yok; run_checks 12/12. Sınav kurulurken aynı kalıptan en çok 2 soru alındığı için sınavda benzerlik artmaz.
- Sınır: Matematik'ten farklı olarak bu derslerde birçok ailenin içeriği sabit (aile başına 1–6 farklı soru). Soru kökü başına açılış cümlesi eklemek aynı soruyu farklı görünüme sokacağı için yapılmadı; daha fazla çeşit için yeni içerik (bilgi/kazanım) eklemek gerekir.

## Takılma izleme (2026-11-22)
- Adres sonuna `?admin=1` eklenince kenar çubuğunda **"⏱️ Yavaş adımlar (bu oturum)"** bölümü görünür: adım başına kaç kez çalıştığı, ortalama ve en uzun süre; son hatalar.
- Ölçülen adımlar: sınav üretimi (`generate_mc`, `generate_oyss`), dosya kaydı/okuma (`_save`, `_load`), GitHub yedeğini ilk indirme (`gh_pull_once`), sayfa çizimi (0,5 sn'den uzunsa) ve sayfa çökmeleri. 0,15 sn altı işlemler kaydedilmez (kayıt şişmez).
- Kayıtlar bellekte tutulur (son 400); sunucu yeniden başlayınca sıfırlanır. Normal kullanıcıya görünmez, belirgin bir yük getirmez.
- Kullanım: takılma olduğunda `?admin=1` ile açıp sürenin hangi adımda biriktiğine bakın; sonucu bana iletirseniz nedeni hedefleyerek çözerim.

## Diğer derslerin Maarif karşılaştırması (2026-11-22)
- **Din Kültürü ve Sosyal Bilgiler:** resmî Maarif programıyla (tymm.meb.gov.tr) karşılaştırıldı; ünite adları, sayıları ve kazanımlar uyumlu, eksik bulunmadı.
- **İngilizce ve Türkçe:** tema/ünite düzeyinde uyumlu; kazanım kodu düzeyinde tam liste resmî sayfalardan alınamadığı için kesin doğrulanamadı.
- **Fen Bilimleri'nde eksik bulundu:** Maarif "Canlıların Yapısına Yolculuk" ünitesi hücreyi de kapsıyor (FB.5.3.1 bitki–hayvan hücresi, FB.5.3.2 hücre–doku–organ–sistem–organizma); uygulamada yalnızca Destek ve Hareket vardı.
- **Yeni ünite "Hücre ve Yapı Düzeyleri"** (Maarif adı: Canlıların Yapısına Yolculuk): özgün hücre çizimi (bitki/hayvan, harfli yapılar), 7 soru ailesi (yapı adı, görev, bitki mi hayvan mı, bitki–hayvan yapı tablosu, yapı düzeyi tablosu, öncüllü, gerekçeli doğru/yanlış); ünite havuzu 136 soru (96'sı şekilli). Fen 5. sınıf havuzu 5455 soru.
- **Hücre ünitesi genişletmesi (2026-11-22):** 136 → 371 soru (229'u şekilli/tablolu), 16 aile. Yeni türler: harften yapı bulma, hayvan hücresinde bulunmayan yapı, bitki hücresi modeli (malzeme–yapı tablosu), organ–sistem tablosu ve organdan sisteme/sistemden organa, doku–görev, yapı–görev eşleştirme (doğru/yanlış), ikinci öncüllü set, ikinci gerekçeli doğru/yanlış seti. Yapı adı/görev sorularına koful eklendi. Her soruda metindeki harf/değerler çizim veya tabloda yazılı; cevap hiçbir yerde açıkça görünmüyor. Soru girişleri 24 farklı cümleyle çeşitlendi (aynı soru farklı görünmesin diye içerik de değişiyor: farklı yapı, harf, malzeme, organ).
- **Yeni ek ünite "Hücre Organelleri (Ek)" (2026-11-22):** mitokondri, endoplazmik retikulum, Golgi aygıtı, lizozom, ribozom, çekirdek, kloroplast, koful, hücre duvarı. Müfredatın dışında/ileri düzey olduğu için ayrı ve "(Ek)" işaretli ünite; öğretmen isterse seçer. Yeni özgün çizim: organelleri harfli hayvan ve bitki hücresi. 13 aile, 335 soru (yaklaşık 215'i şekilli/tablolu): organel adı, harften organel bulma, görev, hayvan hücresinde bulunmayan organel, bitki mi hayvan mı, fabrika benzetmesi (iki yönlü tablo), yapı–görev eşleştirme, mitokondri sayısı tablosundan enerji ihtiyacı, bitki–hayvan yapı tablosu, protein yolu (ribozom → ER → Golgi), öncüllü, gerekçeli doğru/yanlış.
- **Canlılar Dünyası genişletmesi (mantarlar ve mikroskobik canlılar):** 3 yeni çizim türü (mikroskop görüş alanında bakteri çeşitleri — kok/basil/spiral, tomurcuklanan maya hücreleri, ekmek üzerinde küf: hif ve spor kesesi) ve 12 yeni aile: bakteri biçimini adlandırma, çizimde sayma (metindeki sayı çizimle uyumlu), en çok bulunan biçim, maya sayma/tanıma, küf kısımları, mikroskop büyütme hesabı (tablolu: oküler × objektif), objektife göre görüntü, canlı–özellik tablosu, hijyen kuralları (öncüllü), gerekçeli doğru/yanlış.
- Test sırasında rastgele kırılan `_ff6_yanki` (6. sınıf yankı) ailesinin şık havuzu genişletildi.
- Fen 5. sınıf havuzu 6246 soru.
- Koful bilinçli olarak "yalnızca bitkide var" sorularında kullanılmadı (hayvan hücresinde de küçük kofullar olabilir).

## Bilinen sınırlar
- Gerçek Streamlit ve yapay zekâ bağlantısı bu ortamda denenmedi.
- Bilgi bankasındaki maddeleri ben yazdım; bir öğretmen gözden geçirmeli (özellikle Din Kültürü dua/sure anlamları ve yeni Fen gerekçeli ifadeleri).
- Fen kazanım cümleleri MEB PDF'inin özetinden yazıldı; birebir alıntı değil. Maarif ilk dönem kazanım metinlerinin tamamına ulaşılamadı; Destek ve Hareket ünitesi ikinci dönem sınav dağılımındaki kazanımlara göre kuruldu.
- Matematik Maarif karşılaştırması kazanım kodlarına (MAT.5.x) göre yapıldı; ders kitabının kendi soruları birebir alınmadı, aynı tarzda özgün sorular üretildi.
- Altıncı sınıf ve üzeri için Fen 2018 dönüşümü yapılmadı.

## Profil senkron düzeltmesi + Yaprak Test sayıları
- Silinen profil `deleted_profiles.json` ile işaretlenir; yedekten geri gelmez, dosyaları indirilmez.
- Profil oluşturma/silme anında GitHub'a yazılır (`gh_flush`), zamanlayıcıya ve çalışan eşitlemeye bağlı değil; eşzamanlı yedekler kilitle sıraya girer.
- Yaprak Test soru sayısı: 5 / 10 / 20 / 25 (varsayılan 10).

## Havuz üst sınırı (2026-11-22)
- Üretici varsayılanı ünite başına 80 → 3000, aile başına 14 → 30. Gece iş akışı (`yerel_havuz.yml`) 80 ile çalışıp havuzu küçültüyordu; 3000/30 yapıldı.
- Fen 6246 → 6305, Matematik 8143 → 8297 (1000 sınırına dayanan üniteler serbest kaldı). Toplam 21 849 soru; hatalı/yinelenen 0.
- Daha fazla soru için yeni kalıp/bilgi gerekir: kalan sınır ailelerin farklı soru kökü sayısı.
