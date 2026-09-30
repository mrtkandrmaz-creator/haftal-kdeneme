import asyncio
import streamlit as st
from groq import Groq
from google import genai

st.title("Sınav Üreteci")

# Güvenli AI Fonksiyonu
def ai_icerik_uret(prompt: str) -> str:
    groq_key = st.secrets.get("GROQ_API_KEY", "")
    gemini_key = st.secrets.get("GEMINI_API_KEY", "")

    # 1. Groq Dene
    if groq_key:
        try:
            client_groq = Groq(api_key=groq_key)
            res = client_groq.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
            )
            return res.choices[0].message.content
        except Exception as e:
            print(f"Groq atlandı: {e}")

    # 2. Gemini Dene (Güncel google-genai kütüphanesi standart yapısı)
    if gemini_key:
        try:
            client_gemini = genai.Client(api_key=gemini_key)
            # En kararlı çalışan güncel model
            response = client_gemini.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
            )
            return response.text
        except Exception as e:
            raise RuntimeError(f"Tüm yapay zeka servisleri hata verdi. Detay: {e}")
    else:
        raise RuntimeError("Hiçbir API anahtarı (Groq veya Gemini) bulunamadı!")

# Arayüz Kısımları ve Hata Gösterimi (Boş sayfa kalmasını önler)
user_prompt = st.text_area("Sınav için konu veya talimat girin:")

if st.button("Sınav Üret"):
    if not user_prompt:
        st.warning("Lütfen bir talimat girin.")
    else:
        with st.spinner("Yapay zeka sınavı hazırlıyor..."):
            try:
                sonuc = ai_icerik_uret(user_prompt)
                st.success("Sınav başarıyla üretildi!")
                st.write(sonuc)
            except Exception as ex:
                # Boş sayfa yerine hatayı ekranda açıkça gösterir
                st.error(f"Bir hata oluştu:\n\n `{ex}`")
