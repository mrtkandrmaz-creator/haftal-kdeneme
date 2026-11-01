"""Dashboard teması. Kartlar st.container(key="card_c{renk}_{id}") ile renklendirilir (Streamlit >= 1.39)."""

GRADIENTS = [
    ("#22c55e", "#15803d"), ("#3b82f6", "#1d4ed8"), ("#a855f7", "#6d28d9"), ("#f97316", "#c2410c"),
    ("#ef4444", "#b91c1c"), ("#eab308", "#a16207"), ("#06b6d4", "#0e7490"), ("#ec4899", "#be185d"),
    ("#14b8a6", "#0f766e"), ("#64748b", "#334155"),
]


def css():
    card_rules = "\n".join(
        f'div[class*="st-key-card_c{i}_"] {{ background: linear-gradient(135deg, {a} 0%, {b} 100%); '
        f'box-shadow: 0 14px 28px -10px {b}99; }}' for i, (a, b) in enumerate(GRADIENTS))
    return f"""
<style>
.stApp {{ background: radial-gradient(1200px 500px at 85% -10%, #e0f2fe 0%, transparent 60%), #f8fafc; }}
.block-container {{ padding-top: 1.4rem; max-width: 1280px; }}
section[data-testid="stSidebar"] {{ background: linear-gradient(180deg,#0f172a 0%,#1e293b 100%); }}
section[data-testid="stSidebar"] * {{ color: #e2e8f0; }}
section[data-testid="stSidebar"] div.stButton > button {{ background: rgba(255,255,255,.08); border: 1px solid rgba(255,255,255,.18);
  color: #fff; font-weight: 700; border-radius: 12px; text-align: left; }}
section[data-testid="stSidebar"] div.stButton > button:hover {{ background: rgba(249,115,22,.9); border-color: #f97316; }}
.brand {{ font-weight: 900; font-size: 1.5rem; letter-spacing: .5px; color: #fff; }}
.brand span {{ color: #f97316; }}
.hero {{ background: linear-gradient(120deg,#0f172a,#1e3a8a 55%,#0284c7); color:#fff; border-radius: 22px; padding: 1.6rem 2rem;
  box-shadow: 0 20px 40px -18px rgba(2,132,199,.6); margin-bottom: 1.2rem; }}
.hero h1 {{ margin:0; font-size: 2rem; font-weight: 900; color:#fff; }}
.hero p {{ margin:.3rem 0 0; color:#bae6fd; font-size: 1.02rem; }}
.sec-title {{ font-weight: 900; color:#0f172a; font-size: 1.15rem; margin: 1.1rem 0 .6rem; }}
{card_rules}
div[class*="st-key-card_"] {{ border-radius: 20px; padding: 1.1rem 1.2rem .9rem; margin-bottom: .6rem; transition: transform .2s ease; min-height: 190px; }}
div[class*="st-key-card_"]:hover {{ transform: translateY(-4px); }}
div[class*="st-key-card_"] p, div[class*="st-key-card_"] span, div[class*="st-key-card_"] div {{ color: #fff; }}
.c-icon {{ font-size: 2.2rem; line-height: 1; }}
.c-title {{ font-size: 1.28rem; font-weight: 900; margin-top: .3rem; color:#fff; }}
.c-desc {{ font-size: .88rem; opacity: .92; margin: .15rem 0 .4rem; color:#fff; min-height: 2.4em; }}
.c-pill {{ display:inline-block; background: rgba(255,255,255,.22); border-radius: 999px; padding: .1rem .6rem; font-size: .72rem; font-weight: 800; color:#fff; }}
div[class*="st-key-card_"] div.stButton > button {{ width: 100%; background: rgba(255,255,255,.95); color: #0f172a !important; border: none;
  font-weight: 900; border-radius: 12px; padding: .5rem; }}
div[class*="st-key-card_"] div.stButton > button p {{ color: #0f172a !important; }}
div[class*="st-key-card_"] div.stButton > button:hover {{ background: #fff7ed; transform: scale(1.02); }}
div.stButton > button, div.stDownloadButton > button {{ width: 100%; }}
div.stButton > button:first-child {{ border-radius: 12px; font-weight: 800; }}
div.stDownloadButton > button {{ border-radius: 12px; font-weight: 800; background: linear-gradient(135deg,#0ea5e9,#0369a1); color:#fff; border:none; padding:.6rem 1rem; }}
div.stDownloadButton > button p {{ color:#fff; }}
.primary-btn div.stButton > button {{ background: linear-gradient(135deg,#f97316,#ea580c); color:#fff; border:none; font-size:1.1rem; padding:.9rem; box-shadow: 0 8px 18px -6px rgba(249,115,22,.55); }}
.primary-btn div.stButton > button p {{ color:#fff; }}
.kpi {{ background:#fff; border:1px solid #e2e8f0; border-radius:18px; padding:1rem 1.2rem; box-shadow:0 8px 20px -12px rgba(15,23,42,.25); }}
.kpi .v {{ font-size:1.9rem; font-weight:900; color:#0f172a; line-height:1.1; }}
.kpi .l {{ color:#64748b; font-size:.82rem; font-weight:700; text-transform:uppercase; letter-spacing:.4px; }}
.kpi .d {{ font-size:.85rem; font-weight:800; }}
.up {{ color:#16a34a; }} .down {{ color:#dc2626; }} .flat {{ color:#64748b; }}
.question-card {{ background:#fff; padding:1.6rem 2rem; border-radius:18px; box-shadow:0 10px 25px -8px rgba(0,0,0,.08); border:1px solid #e2e8f0; margin-bottom:1rem; }}
.question-title {{ font-size:1.3rem; font-weight:800; color:#1e293b; line-height:1.6; margin:.6rem 0 .8rem; }}
.passage-box {{ background:#f1f5f9; border-left:5px solid #0284c7; padding:1.1rem; border-radius:8px; font-size:1.05rem; color:#334155; margin-bottom:1rem; line-height:1.7; }}
.timer-box {{ background: linear-gradient(135deg,#1e293b,#0f172a); color:#38bdf8; padding:.9rem; border-radius:16px; text-align:center; font-size:2rem; font-weight:900; border:2px solid #38bdf8; letter-spacing:2px; }}
.badge {{ background:#e0f2fe; color:#0369a1; padding:.35rem .85rem; border-radius:20px; font-weight:700; font-size:.88rem; margin-right:.3rem; }}
.zumre {{ background:#fef3c7; color:#92400e; padding:.2rem .6rem; border-radius:10px; font-weight:800; font-size:.8rem; }}
.custom-table-container {{ overflow-x:auto; margin:12px 0; border-radius:12px; box-shadow:0 4px 15px -3px rgba(0,0,0,.08); border:1px solid #e2e8f0; }}
.custom-table {{ width:100%; border-collapse:collapse; font-size:.93rem; background:#fff; text-align:left; }}
.custom-table th {{ background: linear-gradient(135deg,#0284c7,#0369a1); color:#fff; padding:11px 15px; font-weight:700; }}
.custom-table td {{ padding:10px 15px; border-bottom:1px solid #f1f5f9; color:#334155; }}
.custom-table tr:nth-child(even) {{ background:#f8fafc; }}
.bar-bg {{ background:#e2e8f0; border-radius:99px; height:10px; width:100%; }}
.bar-fg {{ height:10px; border-radius:99px; }}
.badge-card {{ background:#fff; border:1px solid #e2e8f0; border-radius:18px; padding:1rem; text-align:center; }}
.badge-card.off {{ filter: grayscale(1); opacity:.45; }}
.badge-card .ic {{ font-size:2.4rem; }}
.badge-card .t {{ font-weight:900; color:#0f172a; }}
.badge-card .ds {{ font-size:.8rem; color:#64748b; }}
.scen {{ background:#fff7ed; border:1px solid #fed7aa; border-radius:14px; padding:.9rem 1.1rem; }}
</style>
"""


def html_table(headers, rows, extra_class=""):
    h = "".join(f"<th>{x}</th>" for x in headers)
    b = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f"<div class='custom-table-container'><table class='custom-table {extra_class}'><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table></div>"


def bar(pct, color=None):
    pct = max(0, min(100, pct))
    color = color or ("#16a34a" if pct >= 75 else "#f59e0b" if pct >= 50 else "#ef4444")
    return f"<div class='bar-bg'><div class='bar-fg' style='width:{pct:.0f}%;background:{color}'></div></div>"


def delta(v, suffix=""):
    if v is None:
        return "<span class='flat'>—</span>"
    if abs(v) < 0.05:
        return f"<span class='flat'>● 0{suffix}</span>"
    cls, ar = ("up", "▲") if v > 0 else ("down", "▼")
    return f"<span class='{cls}'>{ar} {abs(v):.1f}{suffix}</span>"
