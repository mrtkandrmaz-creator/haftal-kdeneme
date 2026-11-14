import os as _os, tempfile as _tf
_TMP = _tf.mkdtemp() + "/"
_ROOT = _os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
APP = _os.path.join(_ROOT, "app.py")
TOOLS = _os.path.join(_ROOT, "tools")
import sys,re,collections; sys.path.insert(0,TOOLS)
import build_pool as bp
ai,cur,store=bp.load_pkg(APP)
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt, core.visuals as V
ok=0; kinds=collections.Counter(); shots={}
for i in range(400):
    raw=ai._mf_ntri("Matematik")
    if not raw: continue
    q=ai._norm_q(raw,"Matematik")
    assert q,(raw["question"],raw["options"])
    ok+=1; sh=raw["shape"]; ans=q["options"][q["answer"]]
    mode=sh["mode"]; kinds[mode]+=1
    if mode=="fan": assert int(ans)==(sh["m"]+2)*(sh["m"]+1)//2
    if mode=="grid": assert int(ans)=={2:5,3:13}[sh["n"]]
    if mode=="midpoint":
        a=int(sh["outer"].split()[0]); b=int(sh["inner"].split()[0])
        assert int(ans.split()[0]) in (3*a+3*b, 3*(a-b))
        assert sh["outer"] in raw["question"] and sh["inner"] in raw["question"]
    shots.setdefault((mode,sh.get("m",sh.get("n"))),sh)
print(ok,kinds)
for k,(key,sh) in enumerate(list(shots.items())[:6]):
    fig,ax=plt.subplots(figsize=(3.6,3.2)); ax.axis("off"); V._geo(ax,sh); fig.savefig(f"{_TMP}nt_{k}.png",dpi=60); plt.close(fig)
from PIL import Image
S=_TMP
n=min(6,len(shots)); ims=[Image.open(S+f"nt_{k}.png") for k in range(n)]; w,h=ims[0].size; W=Image.new("RGB",(w*3,h*2),"white")
for i,im in enumerate(ims): W.paste(im,((i%3)*w,(i//3)*h))
W.save(S+"nt_all.png"); print("OK")
