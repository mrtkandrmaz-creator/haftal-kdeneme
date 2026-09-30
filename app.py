import asyncio
import time
from groq import Groq
from google import genai
import streamlit as st

# --- Akıllı ve Dayanıklı AI İçerik Üretim Altyapısı ---
async def _async_ai_icerik_uret(prompt: str) -> str:
    groq_key = st.secrets.get("GROQ_API_KEY", "")
    gemini_key = st.secrets.get("GEMINI_API_KEY", "")

    groq_hata_mesaji = None
    loop = asyncio.get_running_loop()

    # 1. Adım: Önce Groq ile yanıt almayı dene (Eğer 403 verirse hemen Gemini'ye geçer)
    if groq_key:
        try:
            client_groq = Groq(api_key=groq_key)
            def call_groq():
                res = client_groq.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                )
                return res.choices[0].message.content
            
            return await loop.run_in_executor(None, call_groq)
        except Exception as e:
            groq_hata_mesaji = str(e)

    # 2. Adım: Gemini için Yedekli ve Tekrarlamalı (Retry) Bağlantı
    # Farklı modelleri sırayla dener, 503 alsa bile bekleyip tekrar dener.
    denenecek_modeller = ['gemini-3.8-flash', 'gemini-3.6-flash', 'gemini-2.5-flash']
    gemini_hata_mesaji = ""

    client_gemini = genai.Client(api_key=gemini_key)

    for model_adi in denenecek_modeller:
        for deneme in range(2): # Her model için 2 kez şans ver
            try:
                def call_gemini():
                    response = client_gemini.models.generate_content(
                        model=model_adi,
                        contents=prompt,
                    )
                    return response.text
                
                return await loop.run_in_executor(None, call_gemini)
            except Exception as e:
                gemini_hata_mesaji = str(e)
                # Eğer hata 503 (yoğunluk) ise 2 saniye bekleyip tekrar dene
                if "503" in str(e) or "UNAVAILABLE" in str(e):
                    await asyncio.sleep(2)
                    continue
                else:
                    # Başka tür bir hataysa (örn. model adı geçersizse) direkt sonraki modele geç
                    break

    # Tüm denemeler başarısız olursa detaylı hata fırlat
    raise RuntimeError(
        f"Kritik Hata: Yapay zeka servisleri yanıt vermedi.\n"
        f"- Groq Hatası: {groq_hata_mesaji}\n"
        f"- Gemini Son Hatası: {gemini_hata_mesaji}"
    )

def ai_icerik_uret(prompt: str) -> str:
    try:
        return asyncio.run(_async_ai_icerik_uret(prompt))
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop.run_until_complete(_async_ai_icerik_uret(prompt))
