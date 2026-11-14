import os as _os
_ROOT = _os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
APP = _os.path.join(_ROOT, "app.py")
TOOLS = _os.path.join(_ROOT, "tools")
import sys; sys.path.insert(0,TOOLS)
import build_pool as bp
ai,cur,store=bp.load_pkg(APP)
def Q(subj,t,topic="x",o=None): return {"subject":subj,"topic":topic,"question":t,"passage":"","options":o or {"A":"1","B":"2","C":"3","D":"4"}}
ay="Güneş'in yapısı, Dünya'nın hareketleri, Ay'ın evreleri, Tutulmalar"
assert ai._on_topic(Q("Fen Bilimleri","Dolunay evresinde Ay nasıl görünür?"),ay)
assert not ai._on_topic(Q("Fen Bilimleri","Dinamometre ile ölçülen kuvvet kaç N'dir?"),ay)
assert not ai._on_topic(Q("Fen Bilimleri","Sürtünme kuvveti hareketi nasıl etkiler?"),ay)
geo="MAT.5.3.1. Temel geometrik inşalar (nokta, doğru, doğru parçası, ışın, açı, çember, dik doğru)"
assert ai._on_topic(Q("Matematik","Bir üçgenin iç açıları toplamı kaç derecedir?"),geo)
assert not ai._on_topic(Q("Matematik","Bir manav 5 kg elma ve 3 kg armut satıyor. Toplam kaç kg?"),geo)
assert not ai._on_topic(Q("Matematik","3/4 kesri ile 1/2 kesrini karşılaştırınız."),geo)
assert ai._on_topic(Q("Matematik","Bir manav 5 kg elma satıyor."),"MAT.5.1.1 Altı basamaklı sayılar")
assert ai._on_topic(Q("Türkçe","herhangi"),"x")
assert ai._kw_hit("ayrıca kuvvet","ay") is False and ai._kw_hit("ay'ın evreleri","ay")
print("OK")
ol="MAT.5.6.1. Herhangi bir olayın olasılığının 0 (imkânsız) ile 1 (kesin) arasında olduğunu (olasılık spektrumu) yorumlayabilme, MAT.5.6.2. Olayları az ya da çok olasılıklı şeklinde yapılandırabilme"
assert not ai._on_topic(Q("Matematik","İki çember en fazla kaç noktada kesişir? Paralel doğrularla kesişen çemberleri düşünelim."),ol)
assert not ai._on_topic({**Q("Matematik","Şekilde iki çember kesişmektedir. Kesişim noktası kaç tanedir?"),"shape":{"type":"geo"}},ol)
assert not ai._on_topic(Q("Matematik","Parçalı bir doğruda kesişen çemberlerde kesin sonuç nedir?"),ol)
assert ai._on_topic(Q("Matematik","Torbadan çekilen bir topun kırmızı olma olasılığı için hangisi doğrudur?"),ol)
assert ai._on_topic(Q("Matematik","Bir zar atıldığında 7 gelmesi imkânsız bir olaydır."),ol)
assert not ai._on_topic(Q("Matematik","Yarıçapı 3 cm olan çemberin çapı kaç cm'dir?"),ol)
print("OK2")
