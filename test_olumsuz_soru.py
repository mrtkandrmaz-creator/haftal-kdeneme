import os as _os
_ROOT = _os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
APP = _os.path.join(_ROOT, "app.py")
TOOLS = _os.path.join(_ROOT, "tools")
import sys,json; sys.path.insert(0,TOOLS)
import build_pool as bp
ai,cur,store=bp.load_pkg(APP)
neg=["Aşağıdakilerden hangisi yanlıştır?","Bu verilere göre aşağıdakilerden hangisi söylenemez?","Buna göre aşağıdakilerden hangisi Güneş'in özelliği değildir?",
     "Güneş ile ilgili öğrencilerin verdiği bilgilerden hangisi yanlıştır?","Which of the following is NOT a hobby?"]
pos=["Buna göre aşağıdakilerden hangisi söylenebilir?","Buna göre hangisi doğrudur?","Bu verilere göre ABC üçgeninin çevresi kaç cm'dir?",
     "I. Güneş bir yıldızdır.\nII. Ay bir uydudur.\nIII. Dünya gezegendir.\nBuna göre yukarıdakilerden hangileri doğrudur?",
     "I. A\nII. B\nBuna göre I ve II numaralı ifadelerden hangileri yanlıştır?"]
for t in neg: assert ai._negative_stem({"question":"Bir öğrenci deney yapıyor. "+t}),t
for t in pos: assert not ai._negative_stem({"question":"Bir öğrenci deney yapıyor. "+t}),t
p=ai.mc_prompt("5. Sınıf","Fen Bilimleri",3,"Gökyüzündeki Komşularımız ve Biz: Güneş","Orta","Hafta 1","")
assert "BAŞ YAZAR" in p and "SORU KÖKÜ POLİTİKASI" in p and "ÇOKLU VARYANT" in p and "SON KONTROL" in p and "OLUMSUZ kök (yanlıştır" in p
# critique_fix sahte model
base=lambda q,o,a,sh=None:{"subject":"Fen Bilimleri","topic":"Güneş","passage":"","question":q,"shape":sh,"options":o,"answer":a,"explanation":"x"}
O={"A":"Güneş bir yıldızdır","B":"Ay kendi ışığını yayar","C":"Dünya bir yıldızdır","D":"Ay bir yıldızdır"}
qs=[base("Güneş ile ilgili aşağıdakilerden hangisi yanlıştır?",O,"B"),
    base("Güneş ile ilgili aşağıdakilerden hangisi doğrudur?",O,"A"),
    base("Güneş ile ilgili hangisi doğrudur?",O,"A",{"type":"geo"}),
    base("Hatalı soru, iki doğru şık var. Hangisi doğrudur?",O,"A")]
reply={"reviews":[{"id":1,"verdict":"FIX","issue":"olumsuz kök","fixed":{"passage":None,"question":"Güneş ile ilgili öğrencilerin ifadelerinden hangisi bilimsel olarak doğrudur?","options":O,"answer":"A","explanation":"Güneş bir yıldızdır."}},
 {"id":2,"verdict":"OK"},{"id":3,"verdict":"FIX","issue":"x","fixed":{"question":"x?","options":O,"answer":"A","explanation":"x"}},{"id":4,"verdict":"DROP","issue":"çift doğru"}]}
ai.multi_pool_generate=lambda *a,**k:(json.dumps(reply),None)
r=ai.critique_fix(qs,["k"],[])
print([(q["question"][:40],q.get("crit")) for q in r])
assert len(r)==2 and r[0].get("crit")==1 and "doğrudur" in r[0]["question"] and r[1]["question"].startswith("Güneş ile ilgili aşağıdakilerden hangisi doğrudur")
# API'ye ulaşılamazsa soru kalır
ai.multi_pool_generate=lambda *a,**k:(None,"hata")
assert len(ai.critique_fix(qs,["k"],[]))==4
print("OK")
