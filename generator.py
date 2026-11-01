"""Yapay zekâ soru üretimi. ÖNCE GROQ, sonra Gemini (havuz düzeni korunmuştur).
Streamlit'ten bağımsızdır; anahtarlar set_keys() ile verilir."""
import json
import random
import re
import time
import hashlib
from concurrent.futures import ThreadPoolExecutor, as_completed

from visuals import VISUAL_SPEC
import curriculum as C

GROQ_KEYS, GEMINI_KEYS = [], []


def set_keys(groq_keys, gemini_keys):
    global GROQ_KEYS, GEMINI_KEYS
    GROQ_KEYS = [k for k in (groq_keys or []) if str(k).strip()]
    GEMINI_KEYS = [k for k in (gemini_keys or []) if str(k).strip()]


# ------------------------------------------------ API ÇAĞRILARI (orijinal düzen)
def call_groq_with_key(api_key, prompt_text):
    from groq import Groq
    client = Groq(api_key=api_key)
    completion = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": "Sen MEB müfredatı soru hazırlama uzmanısın. Paragraf, metin, tablo ve fen bilimleri grafik/şema sorularında asla kesinti yapmaz, eksiksiz üretirsin."},
            {"role": "user", "content": prompt_text},
        ],
        temperature=0.85,
        max_tokens=8000,
        response_format={"type": "json_object"},
    )
    return completion.choices[0].message.content


def call_gemini_with_key(api_key, prompt_text):
    from google import genai
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(model="gemini-3.6-flash", contents=prompt_text)
    text = response.text
    if "```json" in text:
        text = text.split("```json")[1].split("```")[0].strip()
    elif "```" in text:
        text = text.split("```")[1].split("```")[0].strip()
    return text


def multi_pool_generate(prompt_text):
    attempts = []
    for i, key in enumerate(GROQ_KEYS):
        attempts.append(("Groq", i + 1, key, call_groq_with_key))
    for i, key in enumerate(GEMINI_KEYS):
        attempts.append(("Gemini", i + 1, key, call_gemini_with_key))
    if not attempts:
        return None, "Geçerli API anahtarı bulunamadı!"
    last_error = None
    # Çağrılar arası anahtar dengelemesi: başlangıç anahtarını döndür, Groq her zaman önce
    g = [a for a in attempts if a[0] == "Groq"]
    if len(g) > 1:
        r = random.randrange(len(g)); g = g[r:] + g[:r]
    attempts = g + [a for a in attempts if a[0] != "Groq"]
    for provider, index, key, func in attempts:
        try:
            result = func(key, prompt_text)
            if result:
                return result, None
        except Exception as e:
            last_error = e
            continue
    return None, str(last_error)


# ------------------------------------------------ PROMPT PARÇALARI
FLAVORS = [
    "günlük yaşamdan bir olay", "bir bilim insanının gözlem günlüğü", "okul etkinliği ve proje çalışması",
    "bir müze/gezi senaryosu", "market ve alışveriş", "spor müsabakası", "doğa gözlemi ve çevre", "teknoloji ve yazılım kulübü",
    "aile bütçesi ve tasarruf", "tarihî bir belge/mektup", "harita ve yolculuk", "mutfakta bilim", "kütüphane ve kitap okuma",
    "şehir planlama", "tarım ve üretim", "sağlık ve beslenme", "uzay ve gökyüzü gözlemi", "sosyal medya ve dijital okuryazarlık",
]

STYLE = (
    "MEB 'yeni nesil' soru anlayışı ve Türkiye Yüzyılı Maarif Modeli: bağlam temelli (gerçek yaşam senaryosu), veri/görsel yoğun, "
    "yorumlama, çıkarım, akıl yürütme ve problem çözme becerisi ölçen, ezber değil beceri temelli sorular. "
    "Matematiksel ifadelerde LaTeX KULLANMA; Unicode (², √, ½, ×, ÷, °) ve düz yazım kullan. Kesirleri 'a/b' yaz."
)


def _rules(difficulty):
    return f"ZORLUK KADEMESİ VE KALİTE KRİTERİ: '{difficulty}'. Şıklar mantıklı çeldiriciler içermeli; doğru cevap şıklara dengeli dağılmalı (A,B,C,D yaklaşık eşit). Soru metninde veya görselde cevabı ele veren ifade olmasın."


MCQ_SCHEMA = (
    'Çıktıyı KESİNLİKLE şu JSON formatında ver, başka açıklama ekleme:\n'
    '{"questions":[{"subject":"..","unit":"..","kazanim":"kısa kazanım ifadesi","difficulty":"kolay|orta|zor","passage":"bağlam/metin (yoksa null)",'
    '"question":"soru kökü","shape":null veya şema,"options":{"A":"..","B":"..","C":"..","D":".."},"answer":"A","explanation":"adım adım kısa çözüm"}]}'
)


def _nonce():
    return hashlib.md5(f"{time.time()}{random.random()}".encode()).hexdigest()[:8]


def build_mcq_prompt(grade, subject, n, units, difficulty, topic="", avoid=None, start_no=1):
    gl = C.GRADES[grade]["label"]
    flavors = ", ".join(random.sample(FLAVORS, 4))
    foc = f"\nÖZEL ODAK KONU: '{topic}' (soruların yaklaşık 1/3'ü bu konuya odaklansın)." if topic.strip() else ""
    av = ""
    if avoid:
        av = "\nŞU SORULARA BENZER SORU ÜRETME (daha önce soruldu): " + " | ".join(a[:70] for a in avoid[:25])
    extra = ""
    if subject == C.TR:
        extra = "\nTürkçe: paragraf/metin sorularında metni EKSİKSİZ ve özgün yaz (en az 4-6 cümle); sözel mantık, dil bilgisi, görsel okuma (tablo/afiş) da kullan."
    if subject == C.ING:
        extra = "\nİngilizce: soru ve şıklar İngilizce; diyalog tamamlama, tablo/kart okuma, kelime bilgisi; Türkçe çeviri sorma."
    if subject == C.ALM:
        extra = "\nAlmanca: soru ve şıklar Almanca (A1 düzeyi, MEB ortaokul Almanca programı); diyalog tamamlama ve kelime bilgisi."
    if subject == C.DIN:
        extra = "\nDin Kültürü: ayet/hadis ve değerler eğitimi bağlamında yorum; ayet/hadis metni uydurma, emin olmadığın yerde anlamını kısaca özetle."
    return (
        f"Türkiye Cumhuriyeti MEB {gl} '{subject}' dersi resmi öğretim programına tam uygun, TAM {n} adet özgün çoktan seçmeli (4 şıklı) soru hazırla.\n"
        f"Kapsanacak üniteler/öğrenme alanları: {', '.join(units)}. Soruları bu ünitelere dengeli dağıt; her soruda 'unit' alanına ünite adını AYNEN yaz.\n"
        f"{STYLE}\nBağlam fikirleri (çeşitlilik için): {flavors}. Üretim kodu: {_nonce()} — her üretimde farklı sayılar, isimler ve senaryolar kullan.{foc}{av}{extra}\n"
        f"{_rules(difficulty)}\n'subject' alanına '{subject}' yaz.\n\n{VISUAL_SPEC}\n\n{MCQ_SCHEMA}"
    )


def build_open_prompt(grade, subject, term, exam_no, scen, plan_levels, difficulty, topic=""):
    gl = C.GRADES[grade]["label"]
    items = []
    k = 0
    for unit, cnt in scen["dist"]:
        for _ in range(cnt):
            lvl, pts = plan_levels[k]
            items.append(f'{k+1}. soru → ünite: {unit} | güçlük: {lvl} | puan: {pts}')
            k += 1
    flavors = ", ".join(random.sample(FLAVORS, 3))
    return (
        f"MEB Ortak Yazılı Sınav Sistemi (OYSS) formatında {gl} '{subject}' {term}. dönem {exam_no}. yazılı sınavı için TAM {k} adet "
        "AÇIK UÇLU, beceri temelli soru hazırla. Sorular öğrencinin gerekçelendirme, yorumlama ve problem çözme yapmasını istesin; çoktan seçmeli DEĞİL.\n"
        "Her soru için:\n" + "\n".join(items) + "\n"
        f"{STYLE}\nBağlam fikirleri: {flavors}. Üretim kodu: {_nonce()}. {_rules(difficulty)}\n"
        + (f"ÖZEL ODAK: '{topic}'\n" if topic.strip() else "") +
        "Her soruya 'answer_key' alanında PUANLAMA ANAHTARI yaz: beklenen cevap + puanın adımlara bölünmüş hali (toplamı soru puanına eşit).\n\n"
        f"{VISUAL_SPEC}\n\nÇıktı JSON:\n"
        '{"questions":[{"subject":"..","unit":"..","kazanim":"..","difficulty":"Kolay|Orta|Zor","points":10,"passage":"bağlam veya null","question":"..","shape":null,"answer_key":"..","explanation":"kısa çözüm"}]}'
    )


# ------------------------------------------------ DOĞRULAMA
def _clean_shape(sh):
    if not isinstance(sh, dict) or not sh.get("type"):
        return None
    return sh


def validate_mcq(q, subject):
    if not isinstance(q, dict) or not q.get("question"):
        return None
    opts = q.get("options")
    if isinstance(opts, list) and len(opts) >= 4:
        opts = {k: v for k, v in zip("ABCD", opts[:4])}
    if not isinstance(opts, dict):
        return None
    opts = {str(k).strip().upper()[:1]: str(v) for k, v in opts.items()}
    if not all(k in opts for k in "ABCD"):
        return None
    ans = str(q.get("answer", "")).strip().upper()[:1]
    if ans not in "ABCD" or not ans:
        return None
    p = q.get("passage")
    p = "" if p is None or str(p).strip().lower() in ("null", "none", "") else str(p).strip()
    return {
        "subject": subject, "unit": str(q.get("unit", "")), "kazanim": str(q.get("kazanim", "")),
        "difficulty": str(q.get("difficulty", "")), "passage": p, "question": str(q["question"]).strip(),
        "shape": _clean_shape(q.get("shape")), "options": {k: opts[k] for k in "ABCD"}, "answer": ans,
        "explanation": str(q.get("explanation", "")), "type": "mcq",
    }


def validate_open(q, subject, lvl, pts):
    if not isinstance(q, dict) or not q.get("question"):
        return None
    p = q.get("passage")
    p = "" if p is None or str(p).strip().lower() in ("null", "none", "") else str(p).strip()
    return {
        "subject": subject, "unit": str(q.get("unit", "")), "kazanim": str(q.get("kazanim", "")), "difficulty": lvl,
        "passage": p, "question": str(q["question"]).strip(), "shape": _clean_shape(q.get("shape")),
        "answer_key": str(q.get("answer_key", "")), "explanation": str(q.get("explanation", "")),
        "points": pts, "type": "open",
    }


def _parse(raw):
    try:
        return json.loads(raw).get("questions", [])
    except Exception:
        m = re.search(r"\{.*\}", raw or "", re.S)
        if m:
            try:
                return json.loads(m.group(0)).get("questions", [])
            except Exception:
                return []
    return []


# ------------------------------------------------ ÜRETİM
CHUNK = 8


def _gen_mcq_block(grade, subject, n, units, difficulty, topic, avoid):
    got, err = [], None
    for _ in range(3):
        need = n - len(got)
        if need <= 0:
            break
        raw, err = multi_pool_generate(build_mcq_prompt(grade, subject, need, units, difficulty, topic, avoid))
        if not raw:
            continue
        for q in _parse(raw):
            v = validate_mcq(q, subject)
            if v and v["question"][:60] not in {g["question"][:60] for g in got}:
                got.append(v)
    return got[:n], err


def generate_mcq_exam(grade, plan, difficulty, topic="", avoid=None, progress=None):
    """plan: [{'subject','n','units'}]. Dönüş: (sorular, hata)."""
    jobs = []
    for p in plan:
        left, i = p["n"], 0
        while left > 0:
            c = min(CHUNK, left)
            ulist = p["units"] or ["Genel kazanımlar"]
            sub_units = ulist if len(ulist) <= 4 else random.sample(ulist, 4)
            jobs.append((p["subject"], c, sub_units))
            left -= c; i += 1
    results, errs, done = {}, [], 0
    with ThreadPoolExecutor(max_workers=3) as ex:
        futs = {ex.submit(_gen_mcq_block, grade, s, c, u, difficulty, topic, avoid): (idx, s)
                for idx, (s, c, u) in enumerate(jobs)}
        for f in as_completed(futs):
            idx, s = futs[f]
            try:
                qs, err = f.result()
            except Exception as e:
                qs, err = [], str(e)
            results[idx] = qs
            if err and not qs:
                errs.append(err)
            done += 1
            if progress:
                progress(done, len(jobs), s)
    order = {p["subject"]: i for i, p in enumerate(plan)}
    allq = [q for idx in sorted(results) for q in results[idx]]
    allq.sort(key=lambda q: order.get(q["subject"], 99))
    return allq, (errs[-1] if errs and not allq else None)


def generate_open_exam(grade, subject, term, exam_no, scen, difficulty, topic="", progress=None):
    from curriculum import oyss_points
    levels = oyss_points(scen["n"])
    raw, err = multi_pool_generate(build_open_prompt(grade, subject, term, exam_no, scen, levels, difficulty, topic))
    if progress:
        progress(1, 1, subject)
    if not raw:
        return [], err
    out = []
    for i, q in enumerate(_parse(raw)[:scen["n"]]):
        lvl, pts = levels[min(i, len(levels) - 1)]
        v = validate_open(q, subject, lvl, pts)
        if v:
            out.append(v)
    return out, (None if out else "Yanıt çözümlenemedi")
