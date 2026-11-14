import os as _os
_ROOT = _os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
APP = _os.path.join(_ROOT, "app.py")
TOOLS = _os.path.join(_ROOT, "tools")
import sys, os, json, tempfile
sys.path.insert(0,TOOLS)
import build_pool
ai,cur,store=build_pool.load_pkg(APP)
g=vars(ai)
ev=g["_tpl_eval"]
# güvenli eval
assert ev("a*b+2",{"a":3,"b":4})==14
for bad in ["__import__('os')","a.__class__","open('x')","[1]","a if a else 2","'x'","9**9"]:
    try: ev(bad,{"a":1}); print("FAIL",bad); sys.exit(1)
    except Exception: pass
t={"id":"t1","topic":"Ondalık Gösterim","topics":"ondalık","text":"Bir manav {a} kg elmayı kilosu {p} TL'den satıyor. Kaç TL kazanır?","vars":{"a":{"lo":2,"hi":9},"p":{"lo":10,"hi":40,"step":5}},"derived":{},"constraints":["a*p<400"],"answer":"a*p","wrong":["a+p","p-a","a*p+p"],"unit":"TL","explanation":"{a} x {p} = {ans}","positive":True}
assert g["tpl_schema_ok"](t)
bad=dict(t,text="{zzz} kg"); assert not g["tpl_schema_ok"](bad)
seen=set()
for _ in range(30):
    q=g["tpl_instantiate"](t); assert q and len(set(q["options"].values()))==4
    assert q["options"][q["answer"]].startswith(str(int(eval(q["explanation"].split("=")[-1].strip().split()[0]))))
    seen.add(q["question"])
assert len(seen)>5
d=tempfile.mkdtemp(); os.makedirs(d+"/5"); json.dump({"qs":[t]},open(d+"/5/matematik.json","w"))
os.environ["DENEMEMATIK_TPL_DIR"]=d
os.environ.pop("DENEMEMATIK_NO_POOL",None)
try:
    r=g["tpl_questions"]("5. Sınıf",3,"ondalık")
    print(len(r), r[0].get("tpl_id") if r else None, r[0]["question"] if r else None)
except Exception as e:
    import traceback; traceback.print_exc()

for _ in range(5):
    r=g["tpl_questions"]("5. Sınıf",3,"ondalık"); assert len(r)==1 and r[0]["tpl_id"]=="t1" and r[0]["topic"]=="Ondalık Gösterim",r
assert g["tpl_questions"]("5. Sınıf",3,"geometri")==[]
assert g["tpl_questions"]("6. Sınıf",3,"")==[]
print("OK")
