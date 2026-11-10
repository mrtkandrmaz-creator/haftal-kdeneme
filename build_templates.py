"""Matematik şablon üreticisi (gece çalışır): MODEL hikâye/şablon yazar, KOD sayıları ve cevabı hesaplar.

Her ünite için model ~5 şablon (JSON) yazar. Şablon şu denetimlerden geçerse templates/<sınıf>/matematik.json'a girer:
  1) biçim denetimi (tpl_schema_ok), 2) en az 12 farklı örnek üretilebiliyor, 3) 3 örnek _norm_q'dan geçiyor,
  4) 3 örnek, cevap anahtarı GÖSTERİLMEDEN iki bağımsız çözücüden geçip anahtarla aynı şıkkı veriyor.
Cevap kodla hesaplandığı için aynı şablon sonsuz kez yeni sayılarla çıkar; API'ye gerek kalmaz.
Kullanım:  python tools/build_templates.py --grades 5 --per-unit 4 --minutes 20
"""
import argparse, json, os, random, re, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_pool as bp

ROOT = bp.ROOT

PROMPT = """Sen MEB {grade} Matematik dersi için SORU ŞABLONU yazan bir öğretmensin.
Ünite: {unit}
Konular: {topics}

{n} adet FARKLI şablon yaz. Şablon = sayıları değişken olan soru. Sayıları ve cevabı bir PROGRAM hesaplayacak; sen yalnızca hikâyeyi ve formülleri yaz.
Çıktı SADECE şu JSON olsun:
{{"templates":[{{"topic":"alt konu adı","text":"Soru metni, değişkenler {{a}} gibi süslü parantezle","vars":{{"a":{{"lo":2,"hi":9}},"p":{{"lo":10,"hi":40,"step":5}},"k":{{"choices":[2,4,5]}}}},"derived":{{"t":"a*p"}},"constraints":["a*p<400"],"answer":"a*p","wrong":["a+p","p-a","a*p+p"],"unit":"TL","explanation":"{{a}} x {{p}} = {{ans}}","positive":true}}]}}

KURALLAR:
- Değişken aralıkları {grade} düzeyine uygun, tam sayı; sonuçlar en fazla 2 ondalıklı olsun (bölme kullanıyorsan constraints ile "x % y == 0" gibi tam bölünmeyi garanti et).
- answer ve wrong[0..2] YALNIZCA şunları kullanabilir: değişken adları, sayılar, + - * / // % **, parantez, karşılaştırma, min max abs round int gcd lcm. Başka hiçbir şey yazma.
- wrong tam 3 tane olmalı ve öğrencinin TİPİK HATALARINI temsil etmeli (işlem karıştırma, birimi çevirmeme, adımı atlama vb.); rastgele sayı olmasın. 4 şık hiçbir sayıda eşit çıkmamalı.
- unit alanı şıklara eklenecek ölçü birimidir (TL, cm, kg, adet, ...); birim yoksa "" bırak. Metindeki değişkenin hemen yanına ek (-de, -in, 'lık vb.) yapıştırma; "{{a}} kg", "{{p}} TL'den" yerine "{{a}} kg", "kilosu {{p}} TL olan" gibi ek gerektirmeyen cümleler kur.
- Metinde sorulan şey ile answer formülü TAM aynı olsun. Metindeki her sayı değişkenle verilsin; metinde olmayan sayıyı formülde kullanma (sabit sayı gerekiyorsa metinde belirt).
- Her şablon FARKLI bağlam/hikâye kullansın (market, okul, spor, yolculuk, mutfak, bahçe...). Kişi adı kullanacaksan ek almayan adlar seç (Ali, Elif, Mert gibi, "Ali'nin" yazma; "Ali" ile bitir).
- Görsel/şekil gerektiren soru YAZMA. Her şeyi metinle ver.
- Soru köküyle bitsin ("Buna göre ... kaçtır?").
JSON dışında hiçbir şey yazma."""


def _gen_templates(ai, gk, mk, grade_label, unit, topics, n, offset):
    prompt = PROMPT.format(grade=grade_label, unit=unit, topics=topics, n=n)
    raw, err = ai.multi_pool_generate(prompt, gk, mk, offset=offset, temperature=0.8)
    if not raw:
        return [], err
    data = ai.parse_json(raw)
    tps = (data or {}).get("templates") if isinstance(data, dict) else None
    return [t for t in (tps or []) if isinstance(t, dict)], None


def validate(ai, t, strict):
    """Şablonu sıkı biçimde sına. (ok, neden)"""
    if not ai.tpl_schema_ok(t):
        return False, "biçim"
    insts, texts = [], set()
    for _ in range(40):
        x = ai.tpl_instantiate(t)
        if x:
            texts.add(x["question"])
            if len(insts) < 3 and x["question"] not in [i["question"] for i in insts]:
                insts.append(x)
        if len(texts) >= 12 and len(insts) >= 3:
            break
    if len(texts) < 12 or len(insts) < 3:
        return False, "az örnek"
    normed = []
    for x in insts:
        try:
            nq = ai._norm_q(x, "Matematik")
        except Exception:
            nq = None
        if not nq:
            return False, "norm"
        normed.append(nq)
    ok = strict(normed)
    if len(ok) < len(normed):
        return False, "çözücü"
    return True, ""


def build(ai, cur, args, gen=None, strict=None):
    ai_gk = ai_mk = None
    if gen is None:
        ai_gk, ai_mk = ai.load_keys()
        gen = lambda label, unit, topics, n, off: _gen_templates(ai, ai_gk, ai_mk, label, unit, topics, n, off)
    if strict is None:
        strict = lambda qs: ai.verify_strict(qs, ai_gk, ai_mk)
    t0 = time.time()
    total = 0
    for g in args.grades.split(","):
        g = g.strip()
        label = cur.GRADE_LABELS.get(g, g + ". Sınıf")
        path = os.path.join(args.out, g, "matematik.json")
        try:
            have = (json.load(open(path, encoding="utf-8")) or {}).get("qs", [])
        except Exception:
            have = []
        # kötü bildirilen şablonları at (soru kimliği tpl_id ile bad.json'a değil, karantinaya düşer)
        stems = {ai._stem({"question": re.sub(r"\{\w+\}", "0", t.get("text", ""))}) for t in have}
        units = list(cur.units(g, "Matematik"))
        units.sort(key=lambda u: sum(1 for t in have if t.get("topic") == u[0] or t.get("unit_name") == u[0]))
        for unit, topics in units:
            if (time.time() - t0) / 60 > args.minutes:
                break
            mine = sum(1 for t in have if t.get("unit_name") == unit)
            if mine >= args.max_per_unit:
                continue
            cands, err = gen(label, unit, topics, args.per_unit, int(time.time()) % 97)
            add = rej = 0
            for t in cands:
                st = ai._stem({"question": re.sub(r"\{\w+\}", "0", str(t.get("text", "")))})
                if st in stems:
                    rej += 1
                    continue
                ok, why = validate(ai, t, strict)
                if not ok:
                    rej += 1
                    print(f"   ✗ {why}: {str(t.get('text'))[:70]}")
                    continue
                stems.add(st)
                t["id"] = f"m{g}-{len(have) + 1:04d}"
                t["unit_name"] = unit
                t["topics"] = topics
                t.setdefault("topic", unit)
                have.append(t)
                add += 1
            total += add
            print(f"{label} Matematik / {unit}: +{add} şablon, elenen {rej}" + (f" ({err})" if err else ""))
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"qs": have}, f, ensure_ascii=False, indent=1)
    print("TOPLAM yeni şablon:", total)
    return total


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--grades", default="5")
    ap.add_argument("--per-unit", type=int, default=1)
    ap.add_argument("--max-per-unit", type=int, default=30)
    ap.add_argument("--minutes", type=float, default=20)
    ap.add_argument("--out", default=os.path.join(ROOT, "templates"))
    args = ap.parse_args()
    os.environ["DENEMEMATIK_NO_FACTORY"] = "1"
    os.environ["DENEMEMATIK_NO_POOL"] = "1"
    os.environ["DENEMEMATIK_SRC_DIR"] = os.path.join(ROOT, "sources")
    ai, cur, _s = bp.load_pkg(os.path.join(ROOT, "app.py"))
    gk, mk = ai.load_keys()
    if not gk and not mk and not ai.extra_keys():
        sys.exit("API anahtarı yok (GROQ_API_KEYS / GEMINI_API_KEYS ...)")
    build(ai, cur, args)


if __name__ == "__main__":
    main()
