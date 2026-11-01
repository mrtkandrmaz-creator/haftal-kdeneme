"""Soruya özel görsel motoru (Streamlit'ten bağımsız). render_png(shape) -> bytes | None

Kural: Görsellerde cevap/ipucu yoktur. Tanımlanması istenen nesneler harfle (A, B, C...) etiketlenir.
"""
import io
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, Wedge, Rectangle, Polygon, FancyBboxPatch, Arc
import numpy as np

plt.rcParams["font.sans-serif"] = ["DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

INK, BLUE, ORANGE, GREEN, GRAY, SUN = "#1e293b", "#0284c7", "#ea580c", "#10b981", "#94a3b8", "#f59e0b"
NAVY = "#0b1b3a"


def _num(v, d=0.0):
    try:
        return float(str(v).replace(",", ".").split()[0])
    except Exception:
        return d


def _nums(vals, default):
    out = []
    for v in (vals or default):
        out.append(_num(v, 10.0))
    return out or list(default)


def _fig(w=6.4, h=3.8, equal=True, axis_off=True):
    fig, ax = plt.subplots(figsize=(w, h))
    if equal:
        ax.set_aspect("equal")
    if axis_off:
        ax.axis("off")
    return fig, ax


def _title(ax, shape, default=""):
    t = str(shape.get("title", default) or "")
    if t:
        ax.set_title(t, fontsize=11, fontweight="bold", color=INK, pad=10)


def _axes_style(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(INK)
        ax.spines[s].set_linewidth(1.3)
    ax.tick_params(colors=INK, labelsize=9)
    ax.grid(axis="y", color="#e2e8f0", linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)


# ------------------------------------------------------------ MATEMATİK
def d_triangle(s):
    fig, ax = _fig()
    sub = str(s.get("sub_type", "scalene")).lower()
    if sub == "right":
        pts = np.array([[0, 0], [4, 0], [0, 3]])
        ax.plot([0, .35, .35, 0], [0, 0, .35, .35], color=INK, lw=1.2)
    elif sub == "equilateral":
        pts = np.array([[0, 0], [4, 0], [2, 2 * math.sqrt(3)]])
    elif sub == "isosceles":
        pts = np.array([[0, 0], [4, 0], [2, 3.6]])
    else:
        pts = np.array([[0, 0], [5, 0], [2, 4.2]])
    ax.add_patch(Polygon(pts, closed=True, fc="#f8fafc", ec=INK, lw=2))
    names = [s.get("B", "B"), s.get("C", "C"), s.get("A", "A")]
    off = [(-.45, -.5), (.2, -.5), (-.1, .25)]
    for p, n, o in zip(pts, names, off):
        ax.text(p[0] + o[0], p[1] + o[1], str(n), fontsize=11, fontweight="bold", color=INK)
    mid = lambda a, b: ((pts[a][0] + pts[b][0]) / 2, (pts[a][1] + pts[b][1]) / 2)
    for key, (a, b), o, ha in (("side_ab", (0, 2), (-.15, 0), "right"), ("side_bc", (0, 1), (0, -.75), "center"),
                               ("side_ac", (1, 2), (.2, .1), "left")):
        if s.get(key):
            m = mid(a, b)
            ax.text(m[0] + o[0], m[1] + o[1], str(s[key]), fontsize=9.5, color=BLUE, fontweight="bold", ha=ha)
    if s.get("angle_a"):
        ax.text(pts[2][0] + .3, pts[2][1] - .9, f"{s['angle_a']}", fontsize=9.5, color=ORANGE, fontweight="bold")
    ax.set_xlim(-1.6, pts[:, 0].max() + 1.8); ax.set_ylim(-1.5, pts[:, 1].max() + 1)
    _title(ax, s); return fig


def d_circle(s):
    fig, ax = _fig(5, 4)
    ax.add_patch(Circle((0, 0), 2.2, fc="#f8fafc", ec=INK, lw=2))
    ax.plot(0, 0, "o", color=ORANGE, ms=5)
    ax.text(.15, -.4, str(s.get("center", "O")), fontsize=11, fontweight="bold", color=ORANGE)
    r = str(s.get("radius", "r"))
    if s.get("show_diameter"):
        ax.plot([-2.2, 2.2], [0, 0], "--", color=GRAY, lw=1.4)
        ax.text(0, .2, f"çap = {r}", fontsize=9.5, fontweight="bold", color=BLUE, ha="center")
    else:
        ax.plot([0, 2.2], [0, 0], color=BLUE, lw=2)
        ax.text(1.1, .15, r, fontsize=9.5, fontweight="bold", color=BLUE, ha="center")
    if s.get("chord"):
        ax.plot([-1.8, 1.8], [-1.25, -1.25], color=GREEN, lw=2)
        ax.text(0, -1.7, str(s["chord"]), fontsize=9.5, fontweight="bold", color=GREEN, ha="center")
    ax.set_xlim(-3, 3); ax.set_ylim(-3, 3); _title(ax, s); return fig


def d_rectangle(s):
    fig, ax = _fig(5.4, 3.6)
    w, h = _num(s.get("width", 6), 6), _num(s.get("height", 4), 4)
    k = 4.0 / max(w, h)
    W, H = w * k, h * k
    ax.add_patch(Rectangle((0, 0), W, H, fc="#e0f2fe", ec=INK, lw=2))
    ax.text(W / 2, -.5, str(s.get("width_label", f"{w:g} cm")), ha="center", fontsize=10, fontweight="bold", color=BLUE)
    ax.text(-.2, H / 2, str(s.get("height_label", f"{h:g} cm")), ha="right", va="center", fontsize=10, fontweight="bold", color=BLUE)
    for i, nm in enumerate(["A", "B", "C", "D"]):
        x, y = [(0, H), (W, H), (W, 0), (0, 0)][i]
        ax.text(x + (-.3 if x == 0 else .12), y + (.12 if y else -.4), nm, fontsize=11, fontweight="bold", color=INK)
    ax.set_xlim(-2, W + 1.5); ax.set_ylim(-1.2, H + 1); _title(ax, s); return fig


def d_bar(s):
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    vals = _nums(s.get("values"), [10, 25, 15, 30])
    labels = [str(x) for x in (s.get("labels") or [f"Öğe {i+1}" for i in range(len(vals))])][:len(vals)]
    labels += [f"Öğe {i+1}" for i in range(len(labels), len(vals))]
    bars = ax.bar(labels, vals, color=BLUE, width=.5, edgecolor=INK, lw=1, zorder=3)
    mx = max(vals) or 10
    for b in bars:
        ax.text(b.get_x() + b.get_width() / 2, b.get_height() + mx * .03, f"{b.get_height():g}", ha="center", fontsize=9, fontweight="bold", color=INK)
    ax.set_ylim(0, mx * 1.3); _axes_style(ax)
    ax.tick_params(axis="x", rotation=15)
    if s.get("y_label"): ax.set_ylabel(str(s["y_label"]), fontsize=9, color=INK)
    _title(ax, s, "Veri Grafiği"); fig.subplots_adjust(bottom=.25, top=.86); return fig


def d_line(s):
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    vals = _nums(s.get("values"), [12, 18, 15, 22, 30])
    labels = [str(x) for x in (s.get("labels") or [f"Ay {i+1}" for i in range(len(vals))])][:len(vals)]
    labels += [f"{i+1}" for i in range(len(labels), len(vals))]
    x = list(range(len(vals)))
    ax.plot(x, vals, "-o", color=ORANGE, lw=2.4, ms=7, mfc=BLUE, mec="white", zorder=3)
    ax.set_xticks(x); ax.set_xticklabels(labels, rotation=15, fontsize=9)
    mx = max(vals) or 10
    for i, v in enumerate(vals):
        ax.text(i, v + mx * .05, f"{v:g}", ha="center", fontsize=9, fontweight="bold", color=INK)
    ax.set_ylim(0, mx * 1.35); _axes_style(ax)
    if s.get("y_label"): ax.set_ylabel(str(s["y_label"]), fontsize=9, color=INK)
    _title(ax, s, "Değişim Grafiği"); fig.subplots_adjust(bottom=.25, top=.86); return fig


def d_pie(s):
    fig, ax = _fig(5, 4)
    vals = _nums(s.get("values"), [40, 30, 20, 10])
    labels = [str(x) for x in (s.get("labels") or list("ABCD"))][:len(vals)]
    cols = ["#0284c7", "#f59e0b", "#10b981", "#ea580c", "#8b5cf6", "#ec4899", "#64748b"]
    ax.pie(vals, labels=labels, colors=cols[:len(vals)], startangle=90, counterclock=False,
           autopct=lambda p: f"%{p:.0f}" if s.get("show_percent", True) else "",
           textprops={"fontsize": 10, "fontweight": "bold", "color": INK}, wedgeprops={"ec": "white", "lw": 2})
    _title(ax, s); return fig


def d_numline(s):
    fig, ax = _fig(7, 1.8, equal=False)
    lo, hi = _num(s.get("min", -5), -5), _num(s.get("max", 5), 5)
    ax.plot([lo - .5, hi + .5], [0, 0], color=INK, lw=2)
    ax.annotate("", xy=(hi + .6, 0), xytext=(hi, 0), arrowprops=dict(arrowstyle="->", color=INK, lw=2))
    step = _num(s.get("step", 1), 1) or 1
    v = lo
    while v <= hi + 1e-9:
        ax.plot([v, v], [-.12, .12], color=INK, lw=1.4)
        ax.text(v, -.4, f"{v:g}", ha="center", fontsize=9, color=INK)
        v += step
    for p in (s.get("points") or []):
        try:
            x = _num(p.get("value"), 0); ax.plot(x, 0, "o", color=ORANGE, ms=9, zorder=3)
            ax.text(x, .35, str(p.get("label", "")), ha="center", fontsize=11, fontweight="bold", color=ORANGE)
        except Exception:
            pass
    ax.set_xlim(lo - 1, hi + 1); ax.set_ylim(-1, 1); _title(ax, s); return fig


def d_angle(s):
    fig, ax = _fig(4.6, 3.4)
    deg = _num(s.get("degrees", 60), 60)
    L = 3
    ax.plot([0, L], [0, 0], color=INK, lw=2.2)
    ax.plot([0, L * math.cos(math.radians(deg))], [0, L * math.sin(math.radians(deg))], color=INK, lw=2.2)
    ax.add_patch(Arc((0, 0), 1.4, 1.4, theta1=0, theta2=deg, color=ORANGE, lw=2))
    mid = math.radians(deg / 2)
    ax.text(1.1 * math.cos(mid), 1.1 * math.sin(mid), str(s.get("label", "")), fontsize=11, fontweight="bold", color=ORANGE, ha="center", va="center")
    ax.text(-.25, -.3, str(s.get("vertex", "O")), fontsize=11, fontweight="bold", color=INK)
    ax.set_xlim(-.8, L + .5); ax.set_ylim(-.8, L + .3); _title(ax, s); return fig


# ------------------------------------------------------------ FEN BİLİMLERİ
def _moon(ax, cx, cy, r, phase):
    """phase: 0 yeni ay, .25 ilk dördün, .5 dolunay, .75 son dördün (kuzey yarım küre görünümü)."""
    ax.add_patch(Circle((cx, cy), r, fc="#2b3445", ec="#64748b", lw=1))
    p = (phase % 1.0) * 2 * math.pi
    lit = "#f1f5f9"
    if p < math.pi:
        ax.add_patch(Wedge((cx, cy), r, -90, 90, fc=lit, ec="none"))
    else:
        ax.add_patch(Wedge((cx, cy), r, 90, 270, fc=lit, ec="none"))
    c = math.cos(p)
    w = abs(c) * 2 * r
    if w > 1e-6:
        ax.add_patch(Ellipse((cx, cy), w, 2 * r, fc="#2b3445" if c > 0 else lit, ec="none"))
    ax.add_patch(Circle((cx, cy), r, fc="none", ec="#94a3b8", lw=1.2))


PHASES = {"new": 0, "waxing_crescent": .125, "first_quarter": .25, "waxing_gibbous": .375, "full": .5,
          "waning_gibbous": .625, "last_quarter": .75, "waning_crescent": .875}


def d_moon(s):
    layout = str(s.get("layout", "strip")).lower()
    if layout == "orbit":
        fig, ax = _fig(6.6, 4.4)
        fig.patch.set_facecolor(NAVY); ax.set_facecolor(NAVY)
        ax.add_patch(Circle((0, 0), .85, fc="#2563eb", ec="#93c5fd", lw=1.5))
        ax.add_patch(Wedge((0, 0), .85, -90, 90, fc="#1e3a8a", ec="none"))
        ax.add_patch(Circle((0, 0), 2.2, fc="none", ec="#475569", ls="--", lw=1))
        for i in range(-3, 4):
            ax.annotate("", xy=(-3.1, i * .42), xytext=(-5.3, i * .42), arrowprops=dict(arrowstyle="->", color="#fbbf24", lw=1.6))
        ax.add_patch(Circle((-6.2, 0), .8, fc=SUN, ec="#fde68a", lw=2))
        letters = list(s.get("letters") or list("ABCDEFGH"))[:8]
        for i in range(8):
            ang = math.radians(180 + i * 45)   # A güneşe bakan taraf (yeni ay konumu)
            x, y = 2.2 * math.cos(ang), 2.2 * math.sin(ang)
            ax.add_patch(Circle((x, y), .38, fc="#2b3445", ec="#94a3b8", lw=1))
            ax.add_patch(Wedge((x, y), .38, 90, 270, fc="#f1f5f9", ec="none"))
            ax.add_patch(Circle((x, y), .38, fc="none", ec="#94a3b8", lw=1))
            lx, ly = 2.85 * math.cos(ang), 2.85 * math.sin(ang)
            ax.text(lx, ly, letters[i] if i < len(letters) else "", color="white", fontsize=12, fontweight="bold", ha="center", va="center")
        ax.set_xlim(-7.2, 3.8); ax.set_ylim(-3.6, 3.6)
        if s.get("title"): ax.set_title(str(s["title"]), color="white", fontsize=11, fontweight="bold")
        return fig
    seq = s.get("sequence") or ["new", "waxing_crescent", "first_quarter", "waxing_gibbous",
                                  "full", "waning_gibbous", "last_quarter", "waning_crescent"]
    seq = [x for x in seq if x in PHASES][:8] or list(PHASES)
    n = len(seq); cols = min(n, 4); rows = math.ceil(n / cols)
    fig, ax = _fig(1.7 * cols + .4, 1.9 * rows + .5)
    fig.patch.set_facecolor(NAVY); ax.set_facecolor(NAVY)
    letters = list(s.get("letters") or [chr(65 + i) for i in range(n)])
    for i, ph in enumerate(seq):
        r_, c_ = divmod(i, cols)
        cx, cy = c_ * 2.2, -r_ * 2.5
        _moon(ax, cx, cy, .85, PHASES[ph])
        ax.text(cx, cy - 1.35, letters[i] if i < len(letters) else "", color="white", fontsize=13, fontweight="bold", ha="center")
    ax.set_xlim(-1.2, cols * 2.2 - 1.0); ax.set_ylim(-rows * 2.5 + .4, 1.2)
    if s.get("title"): ax.set_title(str(s["title"]), color="white", fontsize=11, fontweight="bold")
    return fig


def d_eclipse(s):
    kind = str(s.get("kind", "solar")).lower()
    letters = s.get("letters") or {"sun": "", "moon": "", "earth": ""}
    fig, ax = _fig(7, 3.4)
    fig.patch.set_facecolor(NAVY); ax.set_facecolor(NAVY)
    ax.add_patch(Circle((-6, 0), 1.3, fc=SUN, ec="#fde68a", lw=2.5))
    xm, xe = (-1.5, 2.4) if kind == "solar" else (3.4, -1.5)
    if kind == "solar":
        xm, xe = 1.2, 4.6
        ax.add_patch(Polygon([[xm, .22], [xe, .45], [xe, -.45], [xm, -.22]], fc="#000000", alpha=.55))
        ax.add_patch(Polygon([[xm, .22], [xe + 1.6, 1.3], [xe + 1.6, -1.3], [xm, -.22]], fc="#475569", alpha=.25))
        ax.add_patch(Circle((xm, 0), .3, fc="#cbd5e1", ec="#64748b"))
        ax.add_patch(Circle((xe, 0), .85, fc="#2563eb", ec="#93c5fd", lw=1.5))
        pos = {"sun": (-6, -1.9), "moon": (xm, -.8), "earth": (xe, -1.4)}
    else:
        xe, xm = -.5, 4.6
        ax.add_patch(Polygon([[xe, .85], [xm + 1.6, .45], [xm + 1.6, -.45], [xe, -.85]], fc="#000000", alpha=.55))
        ax.add_patch(Circle((xe, 0), .85, fc="#2563eb", ec="#93c5fd", lw=1.5))
        ax.add_patch(Circle((xm, 0), .3, fc="#7f1d1d", ec="#64748b"))
        pos = {"sun": (-6, -1.9), "earth": (xe, -1.4), "moon": (xm, -.8)}
    for k, (x, y) in pos.items():
        t = letters.get(k, "") if isinstance(letters, dict) else ""
        if t: ax.text(x, y, t, color="white", fontsize=12, fontweight="bold", ha="center")
    ax.set_xlim(-8, 7.5); ax.set_ylim(-2.6, 2.6)
    if s.get("title"): ax.set_title(str(s["title"]), color="white", fontsize=11, fontweight="bold")
    return fig


def d_seasons(s):
    fig, ax = _fig(6.4, 4.4)
    fig.patch.set_facecolor(NAVY); ax.set_facecolor(NAVY)
    ax.add_patch(Circle((0, 0), .9, fc=SUN, ec="#fde68a", lw=2.5))
    ax.add_patch(Ellipse((0, 0), 7.2, 4.6, fc="none", ec="#64748b", ls="--", lw=1.2))
    letters = list(s.get("letters") or list("ABCD"))
    spots = [(3.6, 0), (0, -2.3), (-3.6, 0), (0, 2.3)]
    for (x, y), L in zip(spots, letters):
        ax.add_patch(Circle((x, y), .45, fc="#2563eb", ec="#93c5fd", lw=1.3))
        t = math.radians(23.5)
        ax.plot([x - .8 * math.sin(t), x + .8 * math.sin(t)], [y - .8 * math.cos(t), y + .8 * math.cos(t)], color="#e2e8f0", lw=1.6)
        ax.text(x, y - .95 if y <= 0 else y + .75, L, color="white", fontsize=13, fontweight="bold", ha="center")
    ax.set_xlim(-5, 5); ax.set_ylim(-3.2, 3.2)
    if s.get("title"): ax.set_title(str(s["title"]), color="white", fontsize=11, fontweight="bold")
    return fig


def d_orbit(s):
    fig, ax = _fig(6, 3.6)
    fig.patch.set_facecolor(NAVY); ax.set_facecolor(NAVY)
    ax.add_patch(Circle((-2.4, 0), .9, fc=SUN, ec="#fde68a", lw=2))
    ax.add_patch(Circle((0, 0), 2.4, fc="none", ec="#64748b", ls="--", lw=1.2))
    ax.add_patch(Circle((2.4, 0), .4, fc="#2563eb", ec="#93c5fd", lw=1.3))
    ax.add_patch(Circle((2.4, .95), .14, fc="#cbd5e1", ec="#94a3b8"))
    ax.set_xlim(-4, 3.6); ax.set_ylim(-3, 3)
    if s.get("title"): ax.set_title(str(s["title"]), color="white", fontsize=11, fontweight="bold")
    return fig


def d_dynamometer(s):
    fig, ax = _fig(3.6, 5.2)
    mx = _num(s.get("max", 10), 10)
    val = min(_num(s.get("value", 4), 4), mx)
    unit = str(s.get("unit", "N"))
    ax.add_patch(FancyBboxPatch((-.55, 0), 1.1, 6.2, boxstyle="round,pad=0.05,rounding_size=.25", fc="#f1f5f9", ec=INK, lw=2))
    ax.add_patch(Rectangle((-.28, .35), .56, 5.5, fc="white", ec="#94a3b8", lw=1))
    ax.add_patch(Circle((0, 6.75), .28, fc="none", ec=INK, lw=2.2))
    step = 1 if mx <= 12 else mx / 10
    n = int(round(mx / step))
    for i in range(n + 1):
        y = 5.65 - i * (5.1 / n)
        ax.plot([-.28, -.05 if i % 5 else .0], [y, y], color=INK, lw=1.2)
        ax.text(.68, y, f"{i * step:g}", fontsize=8, va="center", ha="left", color=INK)
    py = 5.65 - (val / mx) * 5.1
    ax.add_patch(Rectangle((-.3, py - .05), .6, .1, fc=ORANGE, ec=ORANGE))
    ax.text(.68, 6.15, unit, fontsize=9, color=BLUE, fontweight="bold")
    ax.plot([0, 0], [0, -.9], color=INK, lw=2.4)
    ax.plot([0, .0], [-.9, -1.0], color=INK, lw=2)
    ax.add_patch(Circle((0, -1.15), .18, fc="none", ec=INK, lw=2.2))
    lab = str(s.get("mass_label", "") or "")
    ax.add_patch(FancyBboxPatch((-.7, -2.7), 1.4, 1.2, boxstyle="round,pad=0.03,rounding_size=.12", fc="#64748b", ec=INK, lw=2))
    ax.plot([0, 0], [-1.32, -1.5], color=INK, lw=2)
    ax.text(0, -2.1, lab, color="white", fontsize=11, fontweight="bold", ha="center", va="center")
    ax.set_xlim(-2.2, 2.2); ax.set_ylim(-3.2, 7.4); _title(ax, s); return fig


def d_thermometer(s):
    fig, ax = _fig(2.8, 5)
    lo, hi = _num(s.get("min", -10), -10), _num(s.get("max", 50), 50)
    val = _num(s.get("value", 20), 20)
    ax.add_patch(FancyBboxPatch((-.18, 0), .36, 6, boxstyle="round,pad=0.02,rounding_size=.18", fc="white", ec=INK, lw=2))
    ax.add_patch(Circle((0, -.1), .5, fc="#dc2626", ec=INK, lw=2))
    top = .9 + (val - lo) / (hi - lo) * 4.7
    ax.add_patch(Rectangle((-.09, -.1), .18, top + .1, fc="#dc2626", ec="none"))
    step = _num(s.get("step", 10), 10) or 10
    v = lo
    while v <= hi + 1e-9:
        y = .9 + (v - lo) / (hi - lo) * 4.7
        ax.plot([.2, .42 if v % (step * 2) == 0 or step >= 10 else .32], [y, y], color=INK, lw=1.3)
        ax.text(.55, y, f"{v:g}", fontsize=8.5, va="center", color=INK)
        v += step
    ax.text(0, 6.4, "°C", fontsize=10, fontweight="bold", color=BLUE, ha="center")
    ax.set_xlim(-1, 1.6); ax.set_ylim(-1, 7); _title(ax, s); return fig


def d_cylinder(s):
    levels = s.get("levels") or [s.get("before", 40), s.get("after", 60)]
    labels = s.get("labels") or ["I", "II", "III"]
    mx = _num(s.get("max", 100), 100)
    n = len(levels)
    fig, ax = _fig(2.6 * n + .8, 4.6)
    for i, lv in enumerate(levels):
        x0 = i * 3.0
        ax.add_patch(Rectangle((x0, 0), 1.2, 6, fc="#f8fafc", ec=INK, lw=2))
        h = _num(lv, 0) / mx * 5.6
        ax.add_patch(Rectangle((x0 + .03, .03), 1.14, h, fc="#7dd3fc", ec="none", alpha=.85))
        for k in range(0, int(mx) + 1, int(max(1, mx // 10))):
            y = k / mx * 5.6
            ax.plot([x0, x0 + (.35 if k % (mx // 5 or 1) == 0 else .22)], [y, y], color=INK, lw=1)
            if k % (mx // 5 or 1) == 0:
                ax.text(x0 + .42, y, f"{k}", fontsize=7.5, va="center", color=INK)
        if s.get("object_in") and i in (s.get("object_in") if isinstance(s.get("object_in"), list) else [1]):
            ax.add_patch(Circle((x0 + .6, .45), .32, fc="#78716c", ec=INK, lw=1.4))
        ax.text(x0 + .6, -.7, labels[i] if i < len(labels) else "", ha="center", fontsize=11, fontweight="bold", color=INK)
    ax.text(0, 6.4, "mL", fontsize=9, color=BLUE, fontweight="bold")
    ax.set_xlim(-.6, 3.0 * n); ax.set_ylim(-1.3, 7); _title(ax, s); return fig


def d_lever(s):
    fig, ax = _fig(7, 3.4)
    ld, rd = _num(s.get("left_dist", 3), 3), _num(s.get("right_dist", 2), 2)
    lf, rf = str(s.get("left_force", "")), str(s.get("right_force", ""))
    ax.add_patch(Polygon([[-.5, -1.2], [.5, -1.2], [0, 0]], fc="#64748b", ec=INK, lw=1.8))
    L = max(ld, rd) + 1
    ax.add_patch(Rectangle((-L, 0), 2 * L, .22, fc="#d6a869", ec=INK, lw=1.8))
    for i in range(-int(L), int(L) + 1):
        ax.plot([i, i], [0, .22], color=INK, lw=.8)
    for x, f, side in ((-ld, lf, -1), (rd, rf, 1)):
        ax.plot([x, x], [0, -.9], color=INK, lw=1.8)
        ax.add_patch(FancyBboxPatch((x - .4, -1.8), .8, .9, boxstyle="round,pad=0.02", fc="#475569", ec=INK))
        ax.text(x, -1.35, f, color="white", fontsize=9.5, fontweight="bold", ha="center", va="center")
    ax.text(0, -1.7, "D", fontsize=11, fontweight="bold", ha="center", color=INK)
    ax.set_xlim(-L - 1, L + 1); ax.set_ylim(-2.4, 1.4); _title(ax, s); return fig


def d_circuit(s):
    kind = str(s.get("kind", "series")).lower()
    n = int(_num(s.get("bulbs", 2), 2)) or 2
    closed = bool(s.get("switch_closed", True))
    fig, ax = _fig(6.4, 3.6)
    ax.plot([0, 0], [0, 3], color=INK, lw=2); ax.plot([0, 6], [3, 3], color=INK, lw=2)
    ax.plot([6, 6], [3, 0], color=INK, lw=2); ax.plot([0, 6], [0, 0], color=INK, lw=2)
    ax.add_patch(Rectangle((-.35, 1.1), .7, .8, fc="white", ec="white", zorder=2))
    ax.plot([-.3, .3], [1.7, 1.7], color=INK, lw=3, zorder=3); ax.plot([-.15, .15], [1.35, 1.35], color=INK, lw=3, zorder=3)
    ax.text(-.8, 1.5, "Pil", fontsize=9, color=INK)
    ax.add_patch(Rectangle((1.3, 2.7), .9, .6, fc="white", ec="white", zorder=2))
    ax.plot([1.3, 1.6], [3, 3], color=INK, lw=2, zorder=3)
    ax.plot([1.6, 2.1 if closed else 2.0], [3, 3 if closed else 3.5], color=INK, lw=2, zorder=3)
    ax.plot([2.1, 2.2], [3, 3], color=INK, lw=2, zorder=3)
    ax.text(1.75, 3.7, "Anahtar", fontsize=8.5, color=INK, ha="center")
    names = list(s.get("labels") or ["K", "L", "M", "N"])
    def bulb(x, y, nm, side=False):
        ax.add_patch(Circle((x, y), .35, fc="#fef08a", ec=INK, lw=1.8, zorder=4))
        ax.plot([x - .24, x + .24], [y - .24, y + .24], color=INK, lw=1, zorder=5); ax.plot([x - .24, x + .24], [y + .24, y - .24], color=INK, lw=1, zorder=5)
        if side: ax.text(x + .55, y, nm, fontsize=10, fontweight="bold", color=INK, ha="left", va="center", zorder=5)
        else: ax.text(x, y - .65, nm, fontsize=10, fontweight="bold", color=INK, ha="center", zorder=5)
    if kind == "series":
        xs = np.linspace(3.2, 5.2, n) if n > 1 else [4.2]
        for i, x in enumerate(xs):
            ax.add_patch(Rectangle((x - .4, 2.7), .8, .6, fc="white", ec="white", zorder=2)); bulb(x, 3, names[i % len(names)])
    else:
        ys = np.linspace(.6, 2.4, n) if n > 1 else [1.5]
        ax.plot([3.6, 3.6], [ys[0], ys[-1]], color=INK, lw=2); ax.plot([5.2, 5.2], [ys[0], ys[-1]], color=INK, lw=2)
        ax.plot([3.6, 3.6], [ys[-1], 3], color=INK, lw=2); ax.plot([5.2, 5.2], [ys[-1], 3], color=INK, lw=2)
        for i, y in enumerate(ys):
            ax.plot([3.6, 5.2], [y, y], color=INK, lw=2, zorder=1)
            bulb(4.4, y, names[i % len(names)], side=True)
    ax.set_xlim(-1.4, 6.8); ax.set_ylim(-.8, 4.2); _title(ax, s); return fig


def d_cell(s):
    plant = str(s.get("kind", "animal")).lower() == "plant"
    fig, ax = _fig(5.4, 4)
    if plant:
        ax.add_patch(FancyBboxPatch((-3, -2.1), 6, 4.2, boxstyle="round,pad=0.05,rounding_size=.3", fc="#dcfce7", ec="#166534", lw=3))
        ax.add_patch(FancyBboxPatch((-2.85, -1.95), 5.7, 3.9, boxstyle="round,pad=0.05,rounding_size=.3", fc="#f0fdf4", ec="#4ade80", lw=1.2))
    else:
        ax.add_patch(Ellipse((0, 0), 6, 4.2, fc="#fef3c7", ec="#b45309", lw=2.6))
    parts = [("nucleus", (-.5, .3)), ("mito", (1.6, -.9)), ("vacuole", (-1.7, -.9) if plant else (1.5, 1.0)), ("chloro", (1.3, .9))]
    ax.add_patch(Circle(parts[0][1], .75, fc="#c4b5fd", ec="#5b21b6", lw=1.8)); ax.add_patch(Circle(parts[0][1], .22, fc="#5b21b6"))
    ax.add_patch(Ellipse(parts[1][1], 1.1, .55, angle=25, fc="#fca5a5", ec="#b91c1c", lw=1.6))
    if plant:
        ax.add_patch(Ellipse((-1.7, -.9), 1.5, 1.2, fc="#bae6fd", ec="#0369a1", lw=1.6))
        ax.add_patch(Ellipse(parts[3][1], 1.0, .5, angle=-20, fc="#4ade80", ec="#166534", lw=1.6))
    else:
        ax.add_patch(Ellipse((1.5, 1.0), .9, .6, fc="#bae6fd", ec="#0369a1", lw=1.6))
    letters = list(s.get("letters") or list("KLMN"))
    pts = [(-.5, 1.3, 0), (1.6, -1.6, 1), ((-1.7, -1.9, 2) if plant else (2.1, 1.5, 2))] + ([(1.5, 1.5, 3)] if plant else [])
    for x, y, i in pts:
        ax.text(x, y, letters[i % len(letters)], fontsize=12, fontweight="bold", color=INK, ha="center")
    ax.set_xlim(-3.6, 3.6); ax.set_ylim(-2.7, 2.7); _title(ax, s); return fig


def d_clock(s):
    fig, ax = _fig(3.4, 3.4)
    ax.add_patch(Circle((0, 0), 1, fc="white", ec=INK, lw=3))
    for i in range(12):
        a = math.radians(90 - i * 30)
        ax.plot([.88 * math.cos(a), .98 * math.cos(a)], [.88 * math.sin(a), .98 * math.sin(a)], color=INK, lw=2)
        ax.text(.76 * math.cos(a), .76 * math.sin(a), str(12 if i == 0 else i), ha="center", va="center", fontsize=10, fontweight="bold", color=INK)
    h, m = _num(s.get("hour", 3), 3) % 12, _num(s.get("minute", 0), 0) % 60
    ah = math.radians(90 - (h + m / 60) * 30); am = math.radians(90 - m * 6)
    ax.plot([0, .45 * math.cos(ah)], [0, .45 * math.sin(ah)], color=INK, lw=4.5)
    ax.plot([0, .7 * math.cos(am)], [0, .7 * math.sin(am)], color=ORANGE, lw=3)
    ax.add_patch(Circle((0, 0), .04, fc=INK))
    ax.set_xlim(-1.2, 1.2); ax.set_ylim(-1.2, 1.2); return fig


DRAWERS = {
    "triangle": d_triangle, "circle": d_circle, "rectangle": d_rectangle,
    "bar_chart": d_bar, "science_chart": d_bar, "line_chart": d_line, "pie_chart": d_pie,
    "number_line": d_numline, "angle": d_angle,
    "moon_phases": d_moon, "eclipse": d_eclipse, "seasons": d_seasons, "orbit": d_orbit,
    "dynamometer": d_dynamometer, "thermometer": d_thermometer, "cylinder": d_cylinder,
    "lever": d_lever, "circuit": d_circuit, "cell": d_cell, "clock": d_clock,
}


def normalize_type(shape: dict) -> str:
    """Eski şema adlarını (science_space + sub_type) yeni türlere eşler."""
    t = str(shape.get("type", "")).strip().lower()
    sub = str(shape.get("sub_type", "")).strip().lower()
    if t == "eclipse":
        if sub in ("lunar_eclipse", "lunar"): shape["kind"] = "lunar"
        elif sub in ("solar_eclipse", "solar"): shape["kind"] = "solar"
        shape.setdefault("kind", "solar")
        return "eclipse"
    if t in ("science_space", "space_orbit"):
        if sub in ("solar_eclipse", "solar"): shape["kind"] = "solar"; return "eclipse"
        if sub in ("lunar_eclipse", "lunar"): shape["kind"] = "lunar"; return "eclipse"
        if sub == "moon_phases": return "moon_phases"
        return "orbit"
    return t


def render_png(shape, dpi=170):
    if not isinstance(shape, dict):
        return None
    t = normalize_type(shape)
    fn = DRAWERS.get(t)
    if not fn:
        return None
    try:
        fig = fn(shape)
        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=dpi, bbox_inches="tight", facecolor=fig.get_facecolor(), pad_inches=.12)
        plt.close(fig)
        return buf.getvalue()
    except Exception:
        plt.close("all")
        return None


def is_table(shape) -> bool:
    return isinstance(shape, dict) and str(shape.get("type", "")).lower() == "table"


VISUAL_SPEC = """GÖRSEL (`shape`) ŞEMALARI — yalnızca bunları kullan, görselde ASLA cevap, ipucu, sonuç veya "doğru" ifadesi bulunmasın.
Tanımlanması/bulunması istenen nesneleri isimle değil HARFLE (A, B, C...) etiketle:
- {"type":"triangle","sub_type":"right|scalene|equilateral|isosceles","A":"A","B":"B","C":"C","side_ab":"5 cm","side_bc":"","side_ac":"","angle_a":"40°"}
- {"type":"circle","center":"O","radius":"5 cm","show_diameter":false,"chord":""}
- {"type":"rectangle","width":8,"height":5,"width_label":"8 cm","height_label":"5 cm"}
- {"type":"angle","degrees":60,"label":"x","vertex":"O"}
- {"type":"number_line","min":-5,"max":5,"step":1,"points":[{"label":"A","value":-3},{"label":"B","value":2}]}
- {"type":"bar_chart","title":"..","labels":[".."],"values":[..],"y_label":".."}
- {"type":"line_chart","title":"..","labels":[".."],"values":[..],"y_label":".."}
- {"type":"pie_chart","title":"..","labels":["A","B","C"],"values":[50,30,20]}
- {"type":"table","title":"..","headers":[".."],"rows":[[".."]]}
- {"type":"moon_phases","layout":"strip","sequence":["new","waxing_crescent","first_quarter","waxing_gibbous","full","waning_gibbous","last_quarter","waning_crescent"] (istediğin alt küme/karışık sıra),"letters":["A","B",..]}
- {"type":"moon_phases","layout":"orbit","letters":["A","B","C","D","E","F","G","H"]}  (Ay'ın Dünya çevresindeki konumları, Güneş solda)
- {"type":"eclipse","kind":"solar|lunar","letters":{"sun":"K","moon":"L","earth":"M"}}
- {"type":"seasons","letters":["A","B","C","D"]}  (Dünya'nın Güneş çevresindeki 4 konumu, eksen eğik)
- {"type":"dynamometer","max":10,"value":4,"unit":"N","mass_label":"m"}
- {"type":"thermometer","min":-10,"max":50,"value":23,"step":10}
- {"type":"cylinder","max":100,"levels":[40,65],"labels":["I","II"],"object_in":[1]}
- {"type":"lever","left_dist":3,"right_dist":2,"left_force":"20 N","right_force":"?"}
- {"type":"circuit","kind":"series|parallel","bulbs":2,"switch_closed":true,"labels":["K","L"]}
- {"type":"cell","kind":"animal|plant","letters":["K","L","M","N"]}
- {"type":"clock","hour":3,"minute":20}
Görsel gerekmeyen sorularda "shape": null. Matematik/Fen/Sosyal sorularının en az yarısında uygun şemayı kullan."""
