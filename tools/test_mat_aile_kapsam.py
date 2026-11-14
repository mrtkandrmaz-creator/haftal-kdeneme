import os as _os
_ROOT = _os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
APP = _os.path.join(_ROOT, "app.py")
TOOLS = _os.path.join(_ROOT, "tools")
import sys,collections; sys.path.insert(0,TOOLS)
import build_pool as bp
ai,cur,store=bp.load_pkg(APP)
def Q(t,topic="x",o=None,sh=None): return {"subject":"Matematik","topic":topic,"question":t,"passage":"","options":o or {"A":"1","B":"2","C":"3","D":"4"},"shape":sh}
U={u[:2]:str(t) for u,t in cur.units("5","Matematik")}
units=cur.units("5","Matematik")
geo=str(units[3][1]); nic=str(units[4][1]); cebir=str(units[2][1]); say=str(units[0][1]); kes=str(units[1][1]); ol=str(units[6-1][1]); ist=str(units[5-1][1])
basamak="Bir doğal sayıda 5 rakamının basamak değeri kaçtır? Hangisi doğrudur?"
assert not ai._on_topic(Q(basamak),geo) and not ai._on_topic(Q(basamak),nic)
assert ai._on_topic(Q(basamak),say)
assert not ai._on_topic(Q("Yarıçapı 3 cm olan çemberin çapı kaç cm?"),say)
assert not ai._on_topic(Q("Yarıçapı 3 cm olan çemberin çapı kaç cm?"),cebir)
assert ai._on_topic(Q("Bir işlemde 3 + 4 × 2 sonucu kaçtır?"),cebir)
assert ai._on_topic(Q("Çevresi 20 cm olan dikdörtgenin bir kenarı 4 cm ise alanı kaçtır?"),nic)
assert ai._on_topic(Q("Şekildeki O merkezli çemberde |BC|=10 cm çaptır. |OA| kaç cm'dir?"),geo)
assert not ai._on_topic(Q("3/4 kesri ile 1/2 kesrini karşılaştır."),geo)
assert not ai._on_topic(Q("Bir zarın atılmasında 7 gelmesi imkânsız bir olaydır."),geo)
print("units:",[ (u[:20]) for u,_ in units])
# fabrika: her ünitede çıkan kalıplar
for i,(u,t) in enumerate(units):
    print(i,u[:30],collections.Counter(q.get("tpl") for q in ai.math_questions("5. Sınıf",12,str(t))).most_common(8))
# geçmiş imza benzerliği
A=Q("Şekilde O merkezli bir çemberde OA yarıçap, BC çap ve DE kiriştir. |BC| = 10 cm ve |DE| = 5 cm olduğuna göre |OA| kaç cm'dir?")
B=Q("Şekilde O merkezli bir çemberde OB yarıçap, CD çap ve EF kiriştir. |CD| = 14 cm ve |EF| = 6 cm olduğuna göre |OB| kaç cm'dir?")
sig=[set(x) for x in [ai.store.__dict__ if False else []]]
import core.store as st
st.add_stems([A]); hs=ai._hist_sets({"Matematik"}); 
assert ai._hist_similar(B,hs["Matematik"]); 
assert not ai._hist_similar(Q("Bir manav 5 kg elma ve 3 kg armut satıyor, kilosu 20 TL ise toplam kaç TL kazanır?"),hs["Matematik"])
print("rec stems:",st.recent_stems()["Matematik"])
print("OK")
