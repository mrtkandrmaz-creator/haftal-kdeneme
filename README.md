# Denemematik
Kurulum: `pip install -r requirements.txt` → `.streamlit/secrets.toml` (örnek: secrets.toml.example) → `streamlit run app.py`
Dosyalar: app.py (yönlendirme) · core/ (curriculum, oyss, ai_engine, visuals, pdf_export, store) · ui/ (setup, exam, reports, extras, theme, state)
- Müfredat: core/curriculum.py (C sözlüğü) — resmî MEB tablosuna göre düzenleyin.
- OYSS: core/oyss.py VERIFIED sözlüğüne ÖDSGM tablosunu ekledikçe senaryolar birebir resmî olur (şu an 5. sınıf Matematik 1. dönem doğrulandı).
- Çevrimdışı deneme: DENEMEMATIK_DEMO=1 streamlit run app.py
- Veriler ./data/*.json (Streamlit Cloud'da geçici: Raporlar > Yedek sekmesini kullanın).
