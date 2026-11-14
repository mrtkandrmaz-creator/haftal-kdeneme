import os as _os
_ROOT = _os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
APP = _os.path.join(_ROOT, "app.py")
TOOLS = _os.path.join(_ROOT, "tools")
import sys,re,collections; sys.path.insert(0,TOOLS)
import build_pool as bp
ai,cur,store=bp.load_pkg(APP)
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt, core.visuals as V
T="Şekildeki ABC üçgeni ikizkenar üçgen (|AB| = |AC|), ACD üçgeni ise eşkenar üçgendir. m(BAC) = 40° olduğuna göre m(BCD) kaç derecedir?"
O={"A":"110°","B":"120°","C":"130°","D":"140°"}
bad={"type":"geo","sub_type":"polygon","sides":5,"labels":list("ABCDE")}
base=lambda sh:{"subject":"Matematik","topic":"Üçgen","passage":"","question":T,"shape":sh,"options":O,"answer":"C","explanation":"x"}
assert ai._fig_text_mismatch(T,bad)
assert ai._norm_q(base(bad),"Matematik") is None
good={"type":"geo","sub_type":"two_triangles","alpha":40,"angles":{"A":"40°","BCD":"?"}}
assert not ai._fig_text_mismatch(T,good)
n=0
for i in range(300):
    raw=ai._mf_twotri("Matematik")
    if not raw: continue
    q=ai._norm_q(raw,"Matematik"); assert q,raw["question"]
    n+=1
    # bağımsız doğrulama
    m=re.search(r"m\((\w+)\) = (\d+)°",raw["question"]); g=int(m.group(2)); ask=re.search(r"m\((\w+)\) kaç",raw["question"]).group(1)
    al=g if m.group(1)=="BAC" else 180-2*g; be=(180-al)//2
    exp={"BCD":be+60,"BAD":al+60}[ask]
    assert q["options"][q["answer"]]==f"{exp}°",(raw["question"],q["options"],q["answer"],exp)
print(n); assert n>200
for k,sh in enumerate([(lambda r: r)(next(r for r in (ai._mf_twotri("Matematik") for _ in range(50)) if r))["shape"] for _ in range(3)]+[good]):
    fig,ax=plt.subplots(figsize=(4,3.2)); ax.axis("off"); V._two_triangles(ax,sh) if False else V._geo(ax,sh); fig.savefig(f"/tmp/claude-0/-home-claude/fbd79b37-55ab-5b0b-917f-b9653f4bf19c/scratchpad/tt_{k}.png",dpi=70); plt.close(fig)
from PIL import Image
S="/tmp/claude-0/-home-claude/fbd79b37-55ab-5b0b-917f-b9653f4bf19c/scratchpad/"
ims=[Image.open(S+f"tt_{k}.png") for k in range(4)]; w,h=ims[0].size; W=Image.new("RGB",(w*2,h*2),"white")
for i,im in enumerate(ims): W.paste(im,((i%2)*w,(i//2)*h))
W.save(S+"tt_all.png"); print("OK")
