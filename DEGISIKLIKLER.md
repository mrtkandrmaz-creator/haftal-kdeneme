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

## Din Kültürü şekilli/tablolu soru artışı (2026-11-22)
- 13 yeni şekilli aile: Allah'ın güzel isimleri (durum cümlesi, anlam, farklı grup), Kur'an (sure ayet sayıları tablosu, kavramlar: ayet/sure/cüz/mushaf, sure açıklamaları), Namaz (vakitten sonraki namaz, duruş tarifi, farz rekât tablosu), Peygamberler (kıssa ters soru, ilahî kitaplar), Cami (bölümler + şadırvan, cami–il).
- Havuz kurucusunda şekilli sorular için yineleme anahtarı değişti: açılış cümlesi ve harf/rakam farkı soruyu "farklı" saymıyor, içerik (şekildeki sözcükler, sorulan öge, cevap) farklıysa farklı sayılıyor. Aile başına üst sınır 30 → 60 (deneme 250).
- Din havuzu 1660 → 2828; şekilli/tablolu soru 293 (%18) → 813 (%29). Hatalı/yinelenen 0; run_checks 12/12.
- Bazı ailelerde (ör. dört vakit, dört kavram) içerik gerçekten 4 farklı soruyla sınırlı; fazlası için yeni bilgi gerekir.

## 7/8. sınıf deneme havuzu ve LGS (2026-11-22)
- Havuz kurucusu 7 ve 8. sınıf için çalışıyor: pool/7/matematik.json (9 soru), pool/8/matematik.json (13 soru). Doğrulandı (cevap şıklarda, şıklar tekil, yineleme yok). Soru az: bu sınıflar için soru kalıbı çok az; havuzu büyütmek için önce kalıp yazılmalı.
- LGS hatası: LGS Hazırlık seçilince hazır havuz `pool/lgs/` klasöründe aranıyordu (yok), yani LGS'de hazır havuz hiç kullanılmıyordu. Artık LGS = 8. sınıf havuzu (`pool/8/`).

## İngilizce şekilli genişletme (2026-11-23)
- Neighbourhood/Nature/Universe üniteleri için 10 yeni şekilli aile: evler, eğlence yerleri, kroki (above/below), bina yüksekliği grafiği, hayvan türleri, habitatlar, hayvan hızı grafiği, mevsimler, gezegenler, kıtalar.
- Havuz kurucusunda yineleme anahtarı tüm şekilli sorulara genişletildi (açılış cümlesi, harf ve grafikte soruyla ilgisiz çubuklar soruyu farklı saymaz).
- İngilizce havuzu 1197 → 2583 soru (şekilli ~1590); hatalı/yinelenen 0; run_checks 12/12.

## Matematik 5 · MAT.5.1.1 Maarif karşılaştırması ve genişletme (2026-11-23)
- Resmî Maarif programı (tymm.meb.gov.tr) MAT.5.1.1: "Altı basamaklı sayıları okuma ve yazmayı çok basamaklı sayılara genelleyebilme". Kapsam: bölük kavramı ve okunuşla ilişkisi, en çok 12 basamaklı sayılar, ara basamakta/bölükte 0 bulunan sayıların (3 000 000, 3 241 123, 3 000 085) okunuş-yazılış karşılaştırması, basamak değeri ve büyüklük karşılaştırma, bağlamlar (nüfus, enerji, bütçe).
- Eksik bulunanlar: 9'dan fazla basamak yoktu (milyar bölüğü yok), bölük kavramına özel soru neredeyse yoktu, sıfır içeren bölük karşılaştırması ve genelleme önermeleri yoktu.
- 10 yeni aile: bölük tablosundan okunuş (8–12 basamak), okunuştan yazılış, bölük sayısı, işaretli rakamın bölüğü, 12 basamağa kadar basamak değeri, sıfırlı sayı kartları (tablo), en büyük/küçük sayı (tablo), bağlam tablosu (elektrik, ziyaretçi, bütçe), I–II–III önermeler, hesap makinesi (9 999 + 1). Basamak tablosu milyar bölüğüne kadar çiziliyor.
- MAT.5.1.1 havuzu 1178 → 2712; Matematik 5. sınıf toplam 17 794 (aile başına 60 sınırıyla yeniden kuruldu; dosya ≈14 MB). Hatalı/yinelenen 0; run_checks 12/12.
- Sınır: "sayı doğrusu" ve "yuvarlama" bu çıktıda resmî metinde açıkça yok; mevcut aileler zaten var, değiştirilmedi.
- (2026-11-23, devam) 8 yeni biçim daha: yanlış/doğru ifade seçimi, "kaç sıfır kullanılır", gizli rakam (?) tablosu, bölük tablosundan sayı oluşturma, bölüklü çözümleme (430 × 1 000 000 + …), iki öğrencinin okunuşunu karşılaştırma, n basamaklı en büyük/küçük sayı, üç sayıyı harfle sıralama. Sorular 4–5 farklı kök cümlesiyle çeşitlendi. MAT.5.1.1 havuzu 2963, Matematik 5 toplam 18 049; hatalı/yinelenen 0.

## Az soru üreten aileler (2026-11-23)
- Neden: havuz kurucusu yinelenen soruyu soru metninin ilk 70 karakterine bakarak eliyordu; kök cümlesi aynı olan ama içeriği (şekildeki sözcükler, öncüller, cevap) farklı sorular yok sayılıyordu. Ör. `_df_yn_r_allah` 252 farklı soru üretiyor, havuzda 1 vardı.
- Çözüm (tools/build_local_pool.py): şekilli sorularda şekil içeriğine, metinli/öncüllü sorularda öncül metnine ve cevaba bakan yineleme anahtarı; aynı kalıptan en çok 3 sınırı da öncül metnini hesaba katıyor.
- 5. sınıf havuzu yeniden kuruldu (hepsinde hatalı/yinelenen 0, run_checks 12/12): Fen 6305 → 15 234, Türkçe 2643 → 5327, Sosyal 1747 → 3702, İngilizce 1197 → 3055, Din 1660 → 2965, Matematik 18 049. Toplam ≈ 48 000 soru, pool klasörü ≈ 45 MB (Fen ve Matematik ≈ 15 MB'er; yüklenmesi 0,3 sn).
- Hâlâ az soru üretenler gerçekten içerik sınırlı: ör. dört terim/dört vakit/dört kavram kartı (4 farklı soru), tek bilgiye dayalı kalıplar. Bunlar için yeni bilgi/kalıp yazmak gerekir.

## İngilizce bilgi bankası genişletmesi (2026-11-23)
- Neighbourhood, Nature, Universe ünitelerine 48 yeni bilgi maddesi (kazanım başına 3: eğlence yerleri, ev türleri, karşılaştırma, ’s, there is/are; hayvan türleri, vahşi hayvanlar, yaşam alanları, can, must, üstünlük/karşılaştırma; gezegenler, kıtalar, iklim, mevsimler, tatil, be going to). Her madde tek doğru, doğru ifade ve öncüllü kalıplara dönüşüyor.
- Havuz 3055 → 3087; bu ünitelerde bilgi tabanlı aile sayısı 29→39, 13→23, 10→20. Artış küçük: bilgi tabanlı kalıplar her madde için yalnız birkaç soru üretiyor.
- Hata düzeltildi (yayına çıkmadı): ek maddeler bilgi–kazanım hizasını bozup bilgi tabanlı ailelerin tamamını devre dışı bırakıyordu; maddeler ek bilgi listesi (`_FACT_EXTRA`) üzerinden eklenerek giderildi.

## Temizlik (2026-11-24)
- Hiçbir yerden çağrılmayan 41 işlev/sabit (266 satır) kaldırıldı (ör. kullanılmayan şekil çizicileri, eski banka yardımcıları, `gh_delete_profile_async`). app.py 42 133 → 41 792 satır; run_checks 12/12.
- Depo kökündeki eski/yinelenen dosyalar kaldırıldı: `build_pool.py`, `build_templates.py`, `build_pool.yml` (gerçekleri `tools/` ve `.github/workflows/` içinde), `requirements`, `requirements.txt.txt` (gerçeği `requirements.txt`).
- Ölçüm: app.py yüklenmesi ≈0,8 sn; dosya boyutu takılmaların nedeni değil. Olası nedenler: GitHub eşitleme, 45 MB havuzun okunması, soru üretim döngüleri (`?admin=1` ile ölçülür).

## Havuz parçalama (2026-11-24)
- `pool/<sınıf>/<ders>.json` tek dosyası yerine `pool/<sınıf>/<ders>/<ünite>_<hash>.json` parçaları + `_index.json` (ünite→dosya, kazanım kodları).
- Çalışma zamanı (`_pool_load`) yalnızca seçilen ünite/tema parçalarını okur (Matematik: kz kodundan tema eşleşmesi indeksle yapılır); en çok 14 parça önbellekte. Eski tek dosya yoksa/klasör yoksa geri dönüş (fallback) çalışır.
- Ölçüm: Fen ilk çağrı 1,5 sn → 0,04 sn; tüm dersler yüklenince bellek ≈160 MB → yalnızca kullanılan parçalar. Eski/yeni aday kümeleri tüm ders/ünite için birebir aynı (fark 0).
- `tools/build_pool.py` `read_pool/write_pool` parça düzenini kullanır; `yerel_havuz.yml` değişmedi.

## Sosyal Bilgiler ve Türkçe bilgi bankası genişletmesi (2026-11-24)
- Sosyal Bilgiler: 6 üniteye 55 yeni bilgi maddesi (grup–rol, bayram/dil kültürü, imece; yön bilgisi, afet hazırlığı, komşu devletler; Göbeklitepe/Çatalhöyük/UNESCO, tekerlek, Frigler; oy verme yaşı, hak–sorumluluk, vergi, polis; bütçe açığı, madencilik, balıkçılık, ticaret; iletişim/ulaşım teknolojisi, güvenli internet, psikoloji).
- Türkçe: 6 üniteye 64 yeni madde (geleneksel oyunlar, hakem, zıt anlam, yansıma; Atatürk: ilk okul, Gazi unvanı, harf devrimi 1928, kadınlara seçme hakkı 1934; duygular ve beden dili; Hıdırellez, Nevruz, kilim, hat, keşkek, aşure, deyim/atasözü; dize/kıta, 5N1K; sağlıklı beslenme, ilk yardım).
- Her madde tek doğru, doğru ifade ve öncüllü kalıplara dönüşür (`_FACT_EXTRA` ile, bilgi–kazanım hizası korunarak).
- Havuz: Sosyal 3702 → 3761, Türkçe 5327 → 5377. Artış küçük: bilgi tabanlı kalıplar madde başına birkaç soru üretir; hatalı/yinelenen 0, run_checks 12/12.
- Bu maddeleri ben yazdım; bir öğretmen gözden geçirmeli (özellikle tarihler, Göbeklitepe yaşı ve uyku süresi).

## Konu sızıntısı temizliği — 5. sınıf tüm dersler (2026-11-25)
- **Matematik · MAT.5.1.1 (çok basamaklı sayıları okuma-yazma):** kapsam dışı 8 kalıp kendi kazanımına taşındı: yuvarlama (4 kalıp), tablodan toplam/fark (nüfus, 2 kalıp), sayı doğrusunda fark → MAT.5.1.2; azalan sayı örüntüsü → MAT.5.2.3. Altı/çok basamaklı sayı kazanımında artık yalnızca okunuş–yazılış, basamak/bölük, basamak değeri, çözümleme, karşılaştırma–sıralama, rakam kartları ve sayı doğrusunda konum soruları var (64 aile, 2615 soru).
- **Matematik · market ve arı kanadı problemleri:** fiyat tablosu sorusu (`_mf_market`) olasılık ve alan-çevre kazanımlarına, arı problemi alan-çevre kazanımına bağlıydı; kazanım kodları düzeltildi (MAT.5.6.2 ve 5.4.4 altında artık yok).
- **Türkçe:** "gelenek" anahtar sözcüğü "Geleneksel çocuk oyunları" ile eşleştiği için Oyun Dünyası ünitesine Geleneklerimiz maddeleri (Nevruz, kına gecesi, halk oyunları) karışıyordu; anahtar sözcük "gelenek ve görenek" yapıldı.
- **İngilizce:** genel okuma metni (`_en_read`) "Life in…" anahtarıyla World/Nature/Universe ünitelerine, mahalle haritası ve ev soruları okul/sınıf ünitelerine, sınıf "there is" sorusu Neighbourhood ünitesine giriyordu; anahtar sözcükler daraltıldı.
- Havuz yeniden kuruldu: Türkçe 5377 → 4960, İngilizce 3097 → 2554 (çıkanlar konu dışı sorulardı), Matematik 18 384; hatalı 0, run_checks 12/12. Fen, Sosyal ve Din'de ünite denetimi (`_unit_guard`) tüm havuzda ret vermedi.
- Bilinçli bırakılanlar: Türkçe'de belge/afiş okuma kalıpları (kermes, davetiye, tarife…) "Görselle iletilen anlam" ve "Bilgilendirici metin" kazanımlarına bağlı olduğu için birden çok ünitede kalıyor.

## Konu saflığı testi (2026-11-25)
- Yeni test `tools/tests/test_konu_saflik.py` (run_checks'te 13. test, ≈2 sn): (1) Matematik havuzundaki kazanım kodları kalıbın güncel eşlemesini aşamaz, MAT.5.1.1 altında yuvarlama/tablodan toplam/örüntü kalıpları ve olasılık–alan çevre altında market sorusu bulunamaz; (2) diğer derslerde soru, kalıbının anahtar sözcüklerinin eşleştiği ünite dışında çıkamaz, bilgi bankası kalıbı yalnızca kendi ünitesinde çıkar; (3) Fen/Sosyal/Din havuzunda `_unit_guard` ret vermez.
- Doğrulama: aynı test eski (düzeltmeden önceki) havuzda 1 062 sorun buluyor (Matematik kz 518, kapsam dışı 458, market 60, Türkçe banka 15, anahtar eşleşmeyen 11); yeni havuzda 0.
- Havuz yeniden kurulduktan sonra test geçmezse push edilmemeli; yeni kalıp eklerken kazanım kodunu `_MF_ITEMCODE`'a yazmayı unutmayın.

## Kalıp başına tek kazanım — Matematik 5 (2026-11-25)
- 84 kalıp 2–4 kazanıma birden bağlıydı (açı, çember/çokgen, doğru/ışın, çevre-alan, kesir, veri, olasılık, market…). Her biri içeriğine göre tek kazanıma bağlandı (`_M5_SINGLE`); bir kazanım seçilince artık yalnızca o kazanımın kalıpları gelir. Örnek: çevre → MAT.5.4.1, alan/birim kare → 5.4.2, alanı verilip çevre → 5.4.3, problem → 5.4.4; basit kesir işlemleri → 5.1.3, kesir karşılaştırma/sadeleştirme → 5.1.4; veri yorumu → 5.5.2.
- Test genişletildi: havuzdaki her Matematik sorusunun tam bir kazanım kodu olmalı (399 aile, 0 ihlal). Havuz yeniden kuruldu: 18 390 soru; run_checks 13/13.
- Dağılım (kazanım: soru): 5.1.1 2616 · 5.1.2 1970 · 5.1.3 3233 · 5.1.4 941 · 5.2.1 245 · 5.2.2 111 · 5.2.3 164 · 5.2.4 335 · 5.3.1 1385 · 5.3.2 216 · 5.3.3 1412 · 5.3.4 1561 · 5.3.5 303 · 5.3.6 440 · 5.3.7 120 · 5.4.1 169 · 5.4.2 249 · 5.4.3 253 · 5.4.4 375 · 5.5.1 1612 · 5.5.2 300 · 5.6.1 71 · 5.6.2 309. İnce kalan kazanımlar: 5.6.1, 5.2.2, 5.3.7, 5.2.3, 5.4.1 (yeni kalıp yazılacak alanlar).

## Kapsam raporu ve etiket denetimi (2026-11-25)
- Yeni araç `tools/kapsam_raporu.py [sınıf] [çıktı.md]`: ders/ünite/(Matematik kazanım)/alt konu bazında soru, kalıp ve şekilli oranı; ince alanları (⚠ az soru/kalıp, 🖼 görsel az) işaretler. 5. sınıf raporu proje belgelerinde: `claude/KAPSAM_RAPORU_5.md`.
- Rapor sırasında yeni sızıntılar bulundu ve kapatıldı: Türkçe Oyun Dünyası'na girmeye devam eden bayram/el sanatı/deyim kalıpları ("gelenek" anahtarı → "gelenek ve görenek"), İngilizce School Life'a başka ünitelerin diyalogları, İngilizce Personal/Family Life dışındaki ünitelere sızan etiketler, Fen Elektrik'e su tüketimi grafiği (İnsan ve Çevre konusu).
- Genel kural (`build_pool.topic_other_unit`): sorunun etiketi yalnızca başka bir ünitenin kazanımı ise o üniteye alınmaz. Havuz kurucusu ve `test_konu_saflik` aynı kuralı uygular (izin listesi: Simple Present→Personal/Family Life, Comparatives and superlatives→Neighbourhood).
- Havuz yeniden kuruldu (Fen 15 198, Türkçe 4 838, Sosyal 3 758, Din 2 966, İngilizce 2 567); run_checks 13/13.

## Matematik 5: ince kazanımlar için yeni görselli kalıplar (2026-11-25)
- Eklendi (16 kalıp, hepsi tablo/şekilli; cevaplar kodla hesaplanır): olasılık MAT.5.6.1 (`_mf5_pr_olasi_tab`, `_mf5_pr_kutu`, `_mf5_pr_kart`), günlük hayat işlem önceliği MAT.5.2.2 (`_mf5_cb_fis`, `_mf5_cb_para_ustu`, `_mf5_cb_ifade_tab`, `_mf5_cb_adim_tab`), örüntü MAT.5.2.3 (`_mf5_ort_tab`, `_mf5_ort_kural`), iki çemberin kesişimiyle üçgen MAT.5.3.7 (`_mf5_ck_tur/_cevre/_eksik/_esit`), çevre MAT.5.4.1 (`_mf5_cv_dik_tab`, `_mf5_cv_dik_sekil`, `_mf5_cv_eksik_kenar`).
- Metindeki tüm değerler (yarıçap, |AB|, çevre vb.) şekilde/tabloda da yazılıdır; dik üçgen çıkabilecek ölçüler "kenara göre tür" sorusundan elenir (çift doğru önlenir).
- Kalite kapısı dersleri: tablo en az 2 satır olmalı; cevap metni tabloda aynen geçmemeli (sızıntı); şıkların rakam dizisi birbirinden farklı olmalı.
- Havuz yeniden kuruldu: MAT.5.6.1 71→251, 5.2.2 111→303, 5.3.7 120→312, 5.4.1 169→325 soru. MAT.5.2.3 (92) hâlâ ince; ek örüntü kalıbı gerekir.
- run_checks 13/13 yeşil.

## MAT.5.2.3 ek örüntü kalıpları (2026-11-25)
- 5 yeni tablolu kalıp: kibrit/çubuk şekil örüntüsünde n. şekil, kaçıncı adımda X sayısı, eksik terim, azalan örüntü (depodaki su), iki kişinin birikimi hangi günde eşit. Cevaplar kodla hesaplanır.
- Neden havuza geç girdi: konu etiketi "Örüntüler" Veri Toplama ünitesinin etiketiydi, etiket denetimi soruları Cebirsel Düşünme'den eliyordu; etiket "Sayı ve şekil örüntüleri" yapıldı (eski `_mf5_ort_tab`/`_mf5_ort_kural` de bu yüzden az soru veriyordu).
- MAT.5.2.3: 92 → 452 soru, 3 → 10 kalıp, %92 şekilli. Matematik 5 havuzu 18 750; run_checks 13/13.

## Sosyal Bilgiler ve Türkçe tablolu soru artışı (2026-11-26)
- 7 yeni tablolu kalıp: Birlikte Yaşamak (grup–rol–görev eşleştirme, farklı kültürlere saygı davranışı), Yaşayan Demokrasimiz (kurum–görev eşleştirme, hak mı sorumluluk mu), Atatürk'ü Tanımak (olay–tarih eşleştirme), İletişim (iyi dinleyici davranışı), Oyun Dünyası (kurallı oyunda davranış). Şıklar yalnızca satır harfidir (K–N); cevap tabloda tek başına yazılmaz; yanlış/doğru satır kodla belirlenir, iki yönlü sorulur ("yanlıştır" / "doğrudur", "hak" / "sorumluluk").
- Havuz kurucusunda bu tabloların satır içeriği yineleme anahtarına girer (`_CONTENT_TITLES`); önceden aynı kökten en çok 3 soru alındığı için içeriği farklı sorular elenirdi.
- Türkçe İletişim ünitesi için anahtar sözcük "sosyal" (ünite adındaki noktalı i yüzünden "sosyal ilişkiler" eşleşmiyordu).
- Şekilli oran: Birlikte Yaşamak %14→%28, Yaşayan Demokrasimiz %22→%33, Atatürk'ü Tanımak %23→%29, Oyun Dünyası %28→%34, İletişim %25→%32. Sosyal 3 784, Türkçe 5 020 soru; run_checks 13/13.

## Din Kültürü tablolu soru artışı (2026-11-26)
- 6 yeni tablolu kalıp: namaz–kılınma zamanı, caminin bölümü–işlevi (mihrap, minber, kubbe, minare, şadırvan), Kur'an kavramları (sure, cüz, ayet, mushaf, hatim), peygamber–olay–öğüt eşleştirme (Nuh, Eyüp, Yunus, İbrahim, Süleyman); Kur'an'a saygı ve nimetlere şükür davranışları. Sosyal/Türkçe'deki eşleştirme/davranış yapısı: şıklar yalnızca satır harfi, doğru/yanlış satır kodla belirlenir, iki yönlü sorulur.
- Din 5. sınıf: 2 966 → 3 319 soru, 115 → 121 kalıp, şekilli oran %22 → %30 (Allah İnancı %34, Kur'an %31, Mimari %30, Namaz %25, Peygamber %32). run_checks 13/13.
- Not: eşleştirme içerikleri (özellikle peygamber kıssası öğütleri) bir Din Kültürü öğretmeni tarafından gözden geçirilmeli.

## Hatalı / konu dışı bildirim ve beğenilen soruya benzer üretim (2026-11-26)
- İnceleme: havuzdan gelen soruda kalıp (fam) bilgisi ekrana taşınmıyordu. "Hatalı" bildirimi yalnız aynı soru ve aynı soru biçimini engelliyor, kalıbın kendisini kapatmıyordu; "beğendim" benzer soruyu yalnızca yapay zekâ anahtarıyla (arka planda) üretiyordu, anahtar yoksa hiçbir şey olmuyordu.
- Düzeltme: havuz sorusu artık kalıp adını (`fam`) ve ünitesini (`_pu`) taşır.
  - Hatalı bildirim: soru + biçim engellenir ve kalıp "Devre dışı kalıplar"a düşer (kenar çubuğundaki yönetici listesinden yeniden açılır); havuz bu kalıbı çalışma anında atlar.
  - Yeni neden "Konu dışı (seçtiğim üniteye uymuyor)": kalıp bozuk sayılmaz; yalnız (kalıp, ünite) çifti ve o soru dışlanır (`offtopic.json`), kalıp başka ünitelerde çalışmaya devam eder.
  - Beğendim: kalıptan gelen sorular için yapay zekâsız, anında 8 benzer soru (aynı kalıp, farklı değerler) beğeni havuzuna eklenir; yapay zekâ anahtarı varsa eski arka plan üretimi de çalışır. Beğeni havuzunda kalıp soruları artık içerikle ayırt edilir (kökü aynı olan tablo soruları birbirini silmez).
- Sınır: gece havuz kurucusu konu dışı listesini henüz okumuyor; çalışma anı filtresi yeterli. run_checks 13/13.
