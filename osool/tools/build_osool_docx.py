# -*- coding: utf-8 -*-
"""ساخت نسخهٔ قابل‌ویرایش (DOCX) جزوهٔ شب امتحانی اصول خدمات سلامت.

همان ماژول‌های محتوای osool/content را با یک «ضبط‌کننده» اجرا می‌کند و خروجی را
با python-docx به صورت سند راست‌به‌چپ با استایل‌های ساده می‌نویسد؛ بنابراین متن
DOCX همیشه با PDF یکی است.
"""

import os
import re
import sys

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor, Cm
from docx.oxml import OxmlElement

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUTDIR = os.path.join(ROOT, "output")
ASSETS = os.path.join(HERE, "assets")
sys.path.insert(0, ROOT)

MARKS = re.compile(r"[\u064B-\u0652\u0670]")
FA = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")

NAVY = RGBColor(0x16, 0x32, 0x4F)
TEAL = RGBColor(0x0F, 0x76, 0x6E)
GRAY = RGBColor(0x3A, 0x3A, 0x3A)

BOX_COLORS = {
    "تعریف": RGBColor(0x0F, 0x76, 0x6E),
    "نکتهٔ مهم": RGBColor(0xB8, 0x86, 0x0B),
    "قانون کلی": RGBColor(0x0B, 0x51, 0x4B),
    "حفظی — این را به خاطر بسپار": RGBColor(0x2C, 0x3E, 0x75),
    "مقایسه": RGBColor(0x6A, 0x3D, 0x9A),
    "ممنوعیت": RGBColor(0xB0, 0x30, 0x2E),
    "مستعد سؤال": RGBColor(0xC8, 0x6A, 0x1F),
    "رمز یادسپاری": RGBColor(0x2E, 0x7D, 0x32),
}


def _rtl(par):
    pPr = par._p.get_or_add_pPr()
    bidi = OxmlElement("w:bidi")
    bidi.set(qn("w:val"), "1")
    pPr.append(bidi)
    par.alignment = WD_ALIGN_PARAGRAPH.RIGHT


def _run_rtl(run):
    rPr = run._r.get_or_add_rPr()
    rtl = OxmlElement("w:rtl")
    rtl.set(qn("w:val"), "1")
    rPr.append(rtl)


def _clean(text):
    return MARKS.sub("", str(text)).translate(FA)


class DocxJozve:
    """همان API سازندهٔ PDF؛ خروجی: python-docx."""

    def __init__(self, doc):
        self.doc = doc
        self._ch = 0

    # ---------- کمکی ----------
    def _par(self, text, size=11, bold=False, color=GRAY, style=None,
             align_right=True, space_after=4):
        par = self.doc.add_paragraph()
        if style:
            par.style = style
        run = par.add_run(_clean(text))
        run.font.size = Pt(size)
        run.font.bold = bold
        run.font.color.rgb = color
        _run_rtl(run)
        _rtl(par)
        par.paragraph_format.space_after = Pt(space_after)
        return par

    # ---------- ساختار ----------
    def chapter(self, title, subtitle="", num_char=None):
        self._ch += 1
        self.doc.add_page_break()
        par = self._par(f"فصل {_clean(str(self._ch))} — {title}",
                        size=17, bold=True, color=NAVY, space_after=2)
        par.style = self.doc.styles["Heading 1"]
        for run in par.runs:
            run.font.color.rgb = NAVY
        if subtitle:
            self._par(subtitle, size=10.5, color=TEAL, space_after=8)

    def h2(self, text, keep=0):
        par = self._par(text, size=13.5, bold=True, color=TEAL, space_after=4)
        par.style = self.doc.styles["Heading 2"]
        for run in par.runs:
            run.font.color.rgb = TEAL

    def h3(self, text, keep=0):
        par = self._par(text, size=11.5, bold=True, color=NAVY, space_after=3)
        par.style = self.doc.styles["Heading 3"]
        for run in par.runs:
            run.font.color.rgb = NAVY

    def p(self, text, size=None, bold=False):
        self._par(text, size=11, bold=bold)

    def bullet(self, text, indent=0, **kw):
        par = self._par("•  " + str(text), size=10.5, space_after=3)
        par.paragraph_format.right_indent = Cm(0.35 + 0.35 * (1 if indent else 0))

    def bullets(self, items, indent=0):
        for it in items:
            self.bullet(it, indent=indent)

    def numbered(self, items, indent=0, start=1):
        for i, it in enumerate(items):
            par = self._par(f"{_clean(str(start + i))}) {it}", size=10.5, space_after=3)
            par.paragraph_format.right_indent = Cm(0.35)

    def h3_bullets(self, title, items, indent=3):
        self.h3(title)
        self.bullets(items)

    def h3_numbered(self, title, items, indent=0):
        self.h3(title)
        self.numbered(items)

    def h2_bullets(self, title, items, indent=0):
        self.h2(title)
        self.bullets(items)

    def h2_numbered(self, title, items, indent=0):
        self.h2(title)
        self.numbered(items)

    # ---------- جعبه‌ها ----------
    def _box(self, text, title):
        color = BOX_COLORS.get(title, TEAL)
        par = self.doc.add_paragraph()
        run = par.add_run(_clean(f"« {title} »  "))
        run.font.size = Pt(10.5)
        run.font.bold = True
        run.font.color.rgb = color
        _run_rtl(run)
        run2 = par.add_run(_clean(text))
        run2.font.size = Pt(10.5)
        run2.font.color.rgb = GRAY
        _run_rtl(run2)
        _rtl(par)
        par.paragraph_format.space_after = Pt(6)
        # قاب ساده دور پاراگراف
        pPr = par._p.get_or_add_pPr()
        borders = OxmlElement("w:pBdr")
        for side in ("top", "bottom", "left", "right"):
            el = OxmlElement(f"w:{side}")
            el.set(qn("w:val"), "single")
            el.set(qn("w:sz"), "6")
            el.set(qn("w:color"), f"{color}")
            borders.append(el)
        pPr.append(borders)

    def note(self, text, title="نکتهٔ مهم"):
        self._box(text, title)

    def key(self, text, title="قانون کلی"):
        self._box(text, title)

    def warn(self, text, title="ممنوعیت"):
        self._box(text, title)

    def memo(self, text, title="حفظی — این را به خاطر بسپار"):
        self._box(text, title)

    def compare(self, text, title="مقایسه"):
        self._box(text, title)

    def exam(self, text, title="مستعد سؤال"):
        self._box(text, title)

    def mnemo(self, text, title="رمز یادسپاری"):
        self._box(text, title)

    def define(self, text, title="تعریف"):
        self._box(text, title)

    def qa(self, question, answer):
        self._par("سؤال: " + question, size=10.5, bold=True, color=NAVY, space_after=1)
        self._par("پاسخ: " + answer, size=10.5, space_after=6)

    def tag_line(self, items, **kw):
        self._par(" | ".join(items), size=10, color=TEAL)

    # ---------- جدول ----------
    def table(self, headers, rows, widths=None, title="", size=None, hsize=None, **kw):
        if title:
            self._par(title, size=10.5, bold=True, color=TEAL, space_after=2)
        tbl = self.doc.add_table(rows=1 + len(rows), cols=len(headers))
        tbl.style = "Table Grid"
        tbl.alignment = WD_TABLE_ALIGNMENT.RIGHT
        # جهت راست‌به‌چپ جدول
        tblPr = tbl._tbl.tblPr
        bidi = OxmlElement("w:bidiVisual")
        tblPr.append(bidi)
        for j, h in enumerate(headers):
            cell = tbl.rows[0].cells[j]
            cell.text = ""
            par = cell.paragraphs[0]
            run = par.add_run(_clean(h))
            run.font.bold = True
            run.font.size = Pt(9.5)
            run.font.color.rgb = NAVY
            _run_rtl(run)
            _rtl(par)
        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                cell = tbl.rows[1 + i].cells[j]
                cell.text = ""
                par = cell.paragraphs[0]
                run = par.add_run(_clean(val))
                run.font.size = Pt(9)
                run.font.color.rgb = GRAY
                _run_rtl(run)
                _rtl(par)
        self.doc.add_paragraph().paragraph_format.space_after = Pt(2)

    def figure(self, path, caption, w=None):
        try:
            from docx.shared import Mm
            par = self.doc.add_paragraph()
            par.alignment = WD_ALIGN_PARAGRAPH.CENTER
            par.add_run().add_picture(path, width=Mm(150))
        except Exception:
            pass
        self._par(caption, size=9.5, bold=True, color=TEAL, space_after=8)

    # ---------- بی‌اثر در DOCX ----------
    def keep(self, h):
        pass

    def ln(self, h=None):
        pass


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    doc = Document()

    # قلم پایه + راست‌به‌چپ پیش‌فرض
    style = doc.styles["Normal"]
    style.font.name = "Vazirmatn"
    style.font.size = Pt(11)
    rpr = style.element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.append(rfonts)
    rfonts.set(qn("w:cs"), "Vazirmatn")

    # ---------- جلد ----------
    logo = os.path.join(ASSETS, "humsyar_logo.jpg")
    if os.path.exists(logo):
        from docx.shared import Mm
        par = doc.add_paragraph()
        par.alignment = WD_ALIGN_PARAGRAPH.CENTER
        par.add_run().add_picture(logo, width=Mm(70))

    j = DocxJozve(doc)
    for text, size, bold, color in [
        ("جزوهٔ شب امتحانی اصول خدمات سلامت", 24, True, NAVY),
        ("بر پایهٔ «برنامه و راهنمای ایمن‌سازی» — مصوب کمیتهٔ کشوری ایمن‌سازی ۱۴۰۳", 12, False, GRAY),
        ("ایمن‌سازی و واکسیناسیون کشوری", 13, True, TEAL),
        ("HumsYar — دستیار هوشمند دانشجویان", 11, True, TEAL),
    ]:
        par = doc.add_paragraph()
        run = par.add_run(_clean(text))
        run.font.size = Pt(size)
        run.font.bold = bold
        run.font.color.rgb = color
        _run_rtl(run)
        par.alignment = WD_ALIGN_PARAGRAPH.CENTER

    j._box("این سند، نسخهٔ قابل‌ویرایش جزوه است؛ نسخهٔ مرجعِ صفحه‌آرایی‌شده، فایل PDF همراه آن است. "
           "جعبه‌های رنگی PDF در اینجا به صورت پاراگراف‌های قاب‌دار با برچسب «نوع جعبه» آمده‌اند.",
           "پیش از شروع")

    # ---------- فصل‌ها ----------
    from content import (ch1_osool, ch2_imen, ch3_barname, ch4_khass, ch5_vaksanha,
                         ch6_bozorgsalan, ch7_safar, ch8_gheyrefaal, ch9_peyvast,
                         ch10_morur)
    for mod in (ch1_osool, ch2_imen, ch3_barname, ch4_khass, ch5_vaksanha,
                ch6_bozorgsalan, ch7_safar, ch8_gheyrefaal, ch9_peyvast, ch10_morur):
        mod.render(j)

    out = os.path.join(OUTDIR, "جزوه-شب-امتحانی-اصول-خدمات-سلامت.docx")
    doc.save(out)
    print("ساخته شد:", out)


if __name__ == "__main__":
    main()
