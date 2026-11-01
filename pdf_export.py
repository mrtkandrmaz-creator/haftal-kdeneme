"""İki sütunlu soru bankası düzeninde PDF üretimi (reportlab + DejaVu Sans: tüm Türkçe karakterler)."""
import io
import os
from xml.sax.saxutils import escape

import matplotlib
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, Image, KeepTogether, NextPageTemplate, PageBreak,
                                PageTemplate, Paragraph, Spacer, Table, TableStyle)

import visuals

_FONT_DIR = os.path.join(matplotlib.get_data_path(), "fonts", "ttf")
_registered = False
SUBJ_COLORS = {"Türkçe": "#e11d48", "Matematik": "#0284c7", "Fen Bilimleri": "#059669", "Sosyal Bilgiler": "#d97706",
               "T.C. İnkılap Tarihi ve Atatürkçülük": "#d97706", "Din Kültürü ve Ahlak Bilgisi": "#7c3aed",
               "İngilizce": "#0891b2", "Almanca": "#be123c"}


def _fonts():
    global _registered
    if _registered:
        return
    for name, f in (("DJ", "DejaVuSans.ttf"), ("DJ-B", "DejaVuSans-Bold.ttf"), ("DJ-I", "DejaVuSans-Oblique.ttf"),
                    ("DJ-BI", "DejaVuSans-BoldOblique.ttf")):
        pdfmetrics.registerFont(TTFont(name, os.path.join(_FONT_DIR, f)))
    pdfmetrics.registerFontFamily("DJ", normal="DJ", bold="DJ-B", italic="DJ-I", boldItalic="DJ-BI")
    _registered = True


def _t(x):
    return escape(str(x if x is not None else "")).replace("\n", "<br/>")


def _styles():
    _fonts()
    S = {}
    S["q"] = ParagraphStyle("q", fontName="DJ", fontSize=8.6, leading=11.4, spaceAfter=2)
    S["qb"] = ParagraphStyle("qb", parent=S["q"], fontName="DJ-B")
    S["pass"] = ParagraphStyle("pass", parent=S["q"], fontSize=8.2, leading=10.8, backColor=colors.HexColor("#f1f5f9"),
                               borderPadding=(3, 4, 3, 4), spaceBefore=3, spaceAfter=5)
    S["opt"] = ParagraphStyle("opt", parent=S["q"], leftIndent=13, firstLineIndent=-13, spaceAfter=1.2)
    S["subj"] = ParagraphStyle("subj", fontName="DJ-B", fontSize=9.5, leading=13, textColor=colors.white, alignment=TA_CENTER,
                               keepWithNext=1, spaceAfter=5, spaceBefore=3)
    S["small"] = ParagraphStyle("small", fontName="DJ", fontSize=7.4, leading=9.6)
    S["h"] = ParagraphStyle("h", fontName="DJ-B", fontSize=14, leading=18)
    S["tbl"] = ParagraphStyle("tbl", fontName="DJ", fontSize=7.6, leading=9.4)
    S["tblh"] = ParagraphStyle("tblh", fontName="DJ-B", fontSize=7.6, leading=9.4, textColor=colors.white)
    return S


def _img(png, max_w, max_h):
    from PIL import Image as PI
    im = PI.open(io.BytesIO(png)); w, h = im.size
    k = min(max_w / w, max_h / h)
    return Image(io.BytesIO(png), width=w * k, height=h * k)


def _table_flow(shape, S, colw):
    headers = [Paragraph(_t(h), S["tblh"]) for h in (shape.get("headers") or [])]
    rows = [[Paragraph(_t(c), S["tbl"]) for c in r] for r in (shape.get("rows") or [])]
    if not headers and not rows:
        return None
    data = [headers] + rows if headers else rows
    n = max(len(r) for r in data)
    data = [r + [""] * (n - len(r)) for r in data]
    t = Table(data, colWidths=[colw / n] * n, repeatRows=1 if headers else 0)
    st = [("GRID", (0, 0), (-1, -1), .4, colors.HexColor("#94a3b8")), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
          ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]
    if headers:
        st.append(("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0369a1")))
    t.setStyle(TableStyle(st))
    cap = Paragraph(f"<b>{_t(shape.get('title', ''))}</b>", S["small"]) if shape.get("title") else None
    return [cap, t, Spacer(1, 4)] if cap else [t, Spacer(1, 4)]


def _question_flow(i, q, S, colw, lines=5):
    parts = []
    is_open = q.get("type") == "open"
    if is_open:
        tag = "  <font color='#b45309'>(Zümre Sorusu)</font>" if q.get("zumre") else ""
        parts.append(Paragraph(f'<font name="DJ-B" color="#0369a1">{i}. Soru</font> <font name="DJ-B">({q.get("points", "")} puan)</font>{tag}', S["q"]))
    if q.get("passage"):
        parts.append(Paragraph(_t(q["passage"]), S["pass"]))
    sh = q.get("shape")
    if visuals.is_table(sh):
        tf = _table_flow(sh, S, colw - 4)
        if tf:
            parts += [x for x in tf if x is not None]
    elif sh:
        png = visuals.render_png(dict(sh), dpi=200)
        if png:
            parts.append(_img(png, colw - 6, 5.2 * cm)); parts.append(Spacer(1, 3))
    if is_open:
        parts.append(Paragraph(_t(q["question"]), S["q"]))
        ln = Table([[""] for _ in range(lines)], colWidths=[colw - 2], rowHeights=[.62 * cm] * lines)
        ln.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, -1), .4, colors.HexColor("#94a3b8"))]))
        parts.append(ln)
    else:
        parts.append(Paragraph(f'<font name="DJ-B" color="#0369a1">{i}.</font> {_t(q["question"])}', S["q"]))
        for k in "ABCD":
            parts.append(Paragraph(f'<font name="DJ-B">{k})</font> {_t(q["options"].get(k, ""))}', S["opt"]))
    parts.append(Spacer(1, 9))
    return KeepTogether(parts)


def _subject_banner(name, S, colw):
    col = colors.HexColor(SUBJ_COLORS.get(name, "#0369a1"))
    t = Table([[Paragraph(_t(name.upper()), S["subj"])]], colWidths=[colw])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), col), ("ROUNDEDCORNERS", [4, 4, 4, 4]), ("TOPPADDING", (0, 0), (-1, -1), 1)]))
    return t


def _answer_key(questions, S, width):
    fl = [Paragraph("CEVAP ANAHTARI", S["h"]), Spacer(1, 6)]
    by = {}
    for i, q in enumerate(questions, 1):
        by.setdefault(q["subject"], []).append((i, q))
    for subj, items in by.items():
        fl.append(_subject_banner(subj, S, width)); fl.append(Spacer(1, 4))
        if items[0][1].get("type") == "open":
            for i, q in items:
                fl.append(Paragraph(f'<b>{i}. Soru ({q.get("points", "")} puan) — {_t(q.get("unit", ""))}</b><br/>{_t(q.get("answer_key", ""))}', S["small"]))
                fl.append(Spacer(1, 4))
            continue
        cells = [f'{i}-{q["answer"]}' for i, q in items]
        per = 10
        rows = [[Paragraph(f"<b>{c}</b>", S["small"]) for c in cells[j:j + per]] for j in range(0, len(cells), per)]
        rows = [r + [""] * (per - len(r)) for r in rows]
        t = Table(rows, colWidths=[width / per] * per)
        t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), .4, colors.HexColor("#cbd5e1")), ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                               ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
        fl += [t, Spacer(1, 8)]
    ex = [(i, q) for i, q in enumerate(questions, 1) if q.get("explanation")]
    if ex:
        fl += [Spacer(1, 6), Paragraph("ÇÖZÜM AÇIKLAMALARI", S["h"]), Spacer(1, 4)]
        for i, q in ex:
            ans = f' — Cevap: {q["answer"]}' if q.get("type") != "open" else ""
            fl.append(Paragraph(f'<b>{i}.{ans}</b> {_t(q["explanation"])}', S["small"]))
            fl.append(Spacer(1, 3))
    return fl


def build_exam_pdf(title, subtitle, questions, include_key=True, lines=5):
    """questions: sorular listesi (sıralı). Dönüş: bytes."""
    S = _styles()
    buf = io.BytesIO()
    PW, PH = A4
    M = 1.2 * cm
    gap = .8 * cm
    colw = (PW - 2 * M - gap) / 2
    top_first = PH - 3.0 * cm
    top_next = PH - M - 1.3 * cm
    bottom = M + .6 * cm

    note = ("Soruları gerekçelendirerek yanıtlayınız. Puanlama anahtarı sonda yer almaktadır." if questions and questions[0].get("type") == "open"
            else "Her sorunun yalnızca bir doğru cevabı vardır. Cevapları sonda yer alan cevap anahtarıyla kontrol edebilirsin.")

    def header(c, doc, first):
        c.saveState()
        c.setFillColor(colors.HexColor("#0f172a")); c.rect(0, PH - 1.0 * cm, PW, 1.0 * cm, stroke=0, fill=1)
        c.setFillColor(colors.HexColor("#f97316")); c.rect(0, PH - 1.06 * cm, PW, .06 * cm, stroke=0, fill=1)
        c.setFillColor(colors.white); c.setFont("DJ-B", 9.5); c.drawString(M, PH - .67 * cm, title[:70])
        c.setFont("DJ", 8); c.drawRightString(PW - M, PH - .67 * cm, subtitle[:60])
        if first:
            y = PH - 1.5 * cm
            c.setStrokeColor(colors.HexColor("#94a3b8")); c.setLineWidth(.6)
            c.roundRect(M, y - 1.2 * cm, PW - 2 * M, 1.2 * cm, 5, stroke=1, fill=0)
            c.setFillColor(colors.HexColor("#334155")); c.setFont("DJ", 8.5)
            c.drawString(M + .3 * cm, y - .5 * cm, "Adı Soyadı: ____________________________")
            c.drawString(M + 8.0 * cm, y - .5 * cm, "Sınıf / No: ____________")
            c.drawString(M + 13.2 * cm, y - .5 * cm, "Tarih: ___ / ___ / ______")
            c.setFont("DJ", 7.6); c.setFillColor(colors.HexColor("#64748b"))
            c.drawString(M + .3 * cm, y - 1.0 * cm, note)
        c.setStrokeColor(colors.HexColor("#cbd5e1")); c.setLineWidth(.6)
        top = (top_first if first else top_next) + .1 * cm
        c.line(PW / 2, bottom - .1 * cm, PW / 2, top)
        c.setFont("DJ", 7.5); c.setFillColor(colors.HexColor("#64748b"))
        c.drawCentredString(PW / 2, M - .1 * cm, f"— {doc.page} —")
        c.drawString(M, M - .1 * cm, "Denemematik · Yapay Zekâ Destekli Soru Bankası")
        c.restoreState()

    def frames(top):
        h = top - bottom
        return [Frame(M, bottom, colw, h, 0, 0, 0, 0, id="L"), Frame(M + colw + gap, bottom, colw, h, 0, 0, 0, 0, id="R")]

    doc = BaseDocTemplate(buf, pagesize=A4, leftMargin=M, rightMargin=M, topMargin=M, bottomMargin=M, title=title, author="Denemematik")
    keyframe = Frame(M, M, PW - 2 * M, PH - 2 * M - 1.2 * cm, id="K")
    doc.addPageTemplates([
        PageTemplate(id="first", frames=frames(top_first), onPage=lambda c, d: header(c, d, True)),
        PageTemplate(id="next", frames=frames(top_next), onPage=lambda c, d: header(c, d, False)),
        PageTemplate(id="key", frames=[keyframe], onPage=lambda c, d: header(c, d, False)),
    ])
    story = [NextPageTemplate("next")]
    last_subj = None
    for i, q in enumerate(questions, 1):
        if q["subject"] != last_subj:
            story.append(_subject_banner(q["subject"], S, colw)); last_subj = q["subject"]
        story.append(_question_flow(i, q, S, colw, lines))
    if include_key:
        story += [NextPageTemplate("key"), PageBreak()] + _answer_key(questions, S, PW - 2 * M)
    doc.build(story)
    return buf.getvalue()


def build_certificate(name, subject, unit, grade_label, pct):
    _fonts()
    buf = io.BytesIO()
    from reportlab.pdfgen import canvas
    W, H = landscape(A4)
    c = canvas.Canvas(buf, pagesize=(W, H))
    c.setFillColor(colors.HexColor("#fffbeb")); c.rect(0, 0, W, H, stroke=0, fill=1)
    c.setStrokeColor(colors.HexColor("#f59e0b")); c.setLineWidth(6); c.rect(1.2 * cm, 1.2 * cm, W - 2.4 * cm, H - 2.4 * cm)
    c.setLineWidth(1.5); c.rect(1.6 * cm, 1.6 * cm, W - 3.2 * cm, H - 3.2 * cm)
    c.setFillColor(colors.HexColor("#0f172a")); c.setFont("DJ-B", 34); c.drawCentredString(W / 2, H - 4.2 * cm, "ÜNİTE BAŞARI SERTİFİKASI")
    c.setFont("DJ", 14); c.setFillColor(colors.HexColor("#475569"))
    c.drawCentredString(W / 2, H - 6.0 * cm, "Bu belge, aşağıdaki ünitede gösterilen başarı için verilmiştir")
    c.setFont("DJ-B", 26); c.setFillColor(colors.HexColor("#ea580c")); c.drawCentredString(W / 2, H - 8.2 * cm, name or "Öğrenci")
    c.setFont("DJ-B", 18); c.setFillColor(colors.HexColor("#0369a1")); c.drawCentredString(W / 2, H - 10.4 * cm, f"{grade_label} · {subject}")
    c.setFont("DJ", 16); c.setFillColor(colors.HexColor("#1e293b")); c.drawCentredString(W / 2, H - 11.8 * cm, f"Ünite: {unit}")
    c.setFont("DJ-B", 22); c.setFillColor(colors.HexColor("#059669")); c.drawCentredString(W / 2, H - 14 * cm, f"Başarı Oranı: %{pct:.0f}")
    c.setFont("DJ", 10); c.setFillColor(colors.HexColor("#64748b")); c.drawCentredString(W / 2, 2.6 * cm, "Denemematik · Yapay Zekâ Destekli Deneme Platformu")
    c.showPage(); c.save()
    return buf.getvalue()
