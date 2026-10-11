# -*- coding: utf-8 -*-
"""
سازندهٔ «جزوهٔ تفسیر موضوعی قرآن — ویژه‌ی برادران» | HumsYar
بر پایهٔ تفسیر نور (محسن قرائتی) — فقط از منابع موجود در مخزن.
خروجی: tafsir/output/جزوه-تفسیر-موضوعی-قرآن.pdf
"""
import os
import sys

from fpdf import FPDF
from fpdf.enums import XPos, YPos

HERE = os.path.dirname(os.path.abspath(__file__))
TAFSIR = os.path.dirname(HERE)                 # tafsir/
ROOT = os.path.dirname(TAFSIR)                 # repo root
FONTS_Q = os.path.join(HERE, "fonts")          # tafsir/tools/fonts
FONTS_V = os.path.join(ROOT, "tools", "fonts") # Vazirmatn
ASSETS = os.path.join(ROOT, "tools", "assets")
OUTDIR = os.path.join(TAFSIR, "output")
OUT = os.path.join(OUTDIR, "جزوه-تفسیر-موضوعی-قرآن.pdf")

sys.path.insert(0, TAFSIR)

# ---------- پالت HumsYar ----------
NAVY = (23, 42, 76)
COVER_BG = (0, 1, 19)
TEAL = (0, 128, 128)
TEAL_DARK = (0, 96, 100)
TEAL_BRIGHT = (0, 210, 220)
TEAL_LIGHT = (224, 242, 241)
BLUE_LIGHT = (232, 240, 250)
BLUE_DARK = (30, 62, 110)
# طلایی/کرم — فقط برای بلوک آیه
GOLD = (176, 141, 42)
CREAM = (251, 246, 233)
GOLD_TEXT = (110, 84, 20)
GRAY = (90, 98, 110)
LINE = (205, 215, 220)
WHITE = (255, 255, 255)
RED = (176, 52, 44)
RED_LIGHT = (252, 238, 236)
PURPLE = (94, 70, 130)
PURPLE_LIGHT = (240, 236, 247)
INK = (30, 36, 45)

LH = 7.1
BODY = 10.6
CH_DIGITS = ["۱", "۲", "۳", "۴", "۵", "۶", "۷"]
NUM_DIGITS = ["۱", "۲", "۳", "۴", "۵", "۶", "۷", "۸", "۹", "۱۰", "۱۱", "۱۲", "۱۳",
              "۱۴", "۱۵", "۱۶", "۱۷", "۱۸", "۱۹", "۲۰", "۲۱", "۲۲", "۲۳"]

FA_DIGITS = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")


def fa(n):
    return str(n).translate(FA_DIGITS)


class Jozve(FPDF):
    def __init__(self):
        super().__init__("P", "mm", "A4")
        self.add_font("Vazir", "", os.path.join(FONTS_V, "Vazirmatn-Regular.ttf"))
        self.add_font("Vazir", "B", os.path.join(FONTS_V, "Vazirmatn-Bold.ttf"))
        self.add_font("VazirBlack", "", os.path.join(FONTS_V, "Vazirmatn-Black.ttf"))
        self.add_font("VazirLight", "", os.path.join(FONTS_V, "Vazirmatn-Light.ttf"))
        self.add_font("AQuran", "", os.path.join(FONTS_Q, "AmiriQuran-Regular.ttf"))
        self.add_font("Amiri", "", os.path.join(FONTS_Q, "Amiri-Regular.ttf"))
        self.add_font("Amiri", "B", os.path.join(FONTS_Q, "Amiri-Bold.ttf"))
        self.set_text_shaping(True)
        self.set_margins(15, 17, 15)
        self.set_auto_page_break(True, margin=19)
        self.toc = []
        self.chapter_no = 0

    # ---------- سربرگ / پاصفحه ----------
    def header(self):
        if self.page_no() <= 2:
            return
        self.set_draw_color(*LINE)
        self.set_line_width(0.3)
        self.line(self.l_margin, 12.5, self.w - self.r_margin, 12.5)
        self.set_font("Vazir", "", 8)
        self.set_text_color(*GRAY)
        self.set_xy(self.l_margin, 5.5)
        self.cell(self.epw, 6, "جزوهٔ تفسیر موضوعی قرآن | بر پایهٔ تفسیر نور", align="R")
        self.set_xy(self.l_margin, 5.5)
        self.set_text_color(*TEAL_DARK)
        self.cell(self.epw, 6, "ویژه‌ی برادران", align="L")
        self.set_y(17)

    def footer(self):
        if self.page_no() <= 1:
            return
        self.set_y(-13.5)
        self.set_draw_color(*LINE)
        self.set_line_width(0.3)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.set_font("Vazir", "", 9)
        self.set_text_color(*TEAL_DARK)
        self.set_xy(self.l_margin, -13.5)
        self.cell(self.epw, 9, fa(self.page_no()), align="C")
        self.set_xy(self.l_margin, -13.5)
        self.set_font("Vazir", "B", 9.5)
        self.set_text_color(*NAVY)
        hw = self.get_string_width("Hums")
        self.cell(hw, 9, "Hums", align="L")
        self.set_text_color(*TEAL)
        self.cell(14, 9, "Yar", align="L")
        self.set_xy(self.l_margin, -13.5)
        self.set_font("Vazir", "", 7.5)
        self.set_text_color(*GRAY)
        self.cell(self.epw, 9, "دستیار هوشمند دانشجویان", align="R")

    # ---------- ابزار ----------
    @property
    def eph_avail(self):
        return self.page_break_trigger - self.t_margin

    def need(self, h):
        if self.get_y() + h > self.page_break_trigger:
            self.add_page()

    def keep(self, h):
        self.need(min(h, self.eph_avail - 6))

    def est_list(self, items, indent=0, mw=7.5, size=BODY):
        self.set_font("Vazir", "", size)
        total = 0.0
        for it in items:
            total += self.multi_cell(self.epw - indent - mw, LH, it, align="R",
                                     dry_run=True, output="HEIGHT") + 0.4
        return total + 1

    # ---------- اجزای ساختاری ----------
    def chapter(self, title, subtitle="", num_char=None):
        self.chapter_no += 1
        self.add_page()
        label = num_char or CH_DIGITS[self.chapter_no - 1]
        toc_title = title if num_char else f"فصل {label} — {title}"
        self.toc.append((toc_title, self.page_no()))
        y = self.get_y()
        self.set_fill_color(*NAVY)
        self.rect(self.l_margin, y, self.epw, 17, style="F", round_corners=True, corner_radius=2.5)
        self.set_fill_color(*TEAL_BRIGHT)
        cx = self.w - self.r_margin - 8.5
        self.ellipse(cx - 5.5, y + 3, 11, 11, style="F")
        self.set_font("VazirBlack", "", 13)
        self.set_text_color(*NAVY)
        self.set_xy(cx - 5.5, y + 3)
        self.cell(11, 11, label, align="C")
        self.set_font("VazirBlack", "", 14.5)
        self.set_text_color(*WHITE)
        self.set_xy(self.l_margin, y)
        self.cell(self.epw - 18, 17, title, align="R")
        self.set_y(y + 17)
        if subtitle:
            self.ln(1.5)
            self.set_font("Vazir", "", 9.5)
            self.set_text_color(*GRAY)
            self.cell(self.epw, 6, subtitle, align="R", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(3.5)

    def h2(self, text, keep=0):
        self.need(20 + keep if keep else 20)
        self.ln(2.2)
        y = self.get_y()
        self.set_fill_color(*TEAL)
        self.rect(self.w - self.r_margin - 2.6, y + 1.2, 2.6, 7.6, style="F",
                  round_corners=True, corner_radius=1)
        self.set_font("Vazir", "B", 12.5)
        self.set_text_color(*TEAL_DARK)
        self.set_xy(self.l_margin, y)
        self.cell(self.epw - 5.5, 10, text, align="R", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_draw_color(*LINE)
        self.set_line_width(0.25)
        self.line(self.l_margin, self.get_y() + 0.4, self.w - self.r_margin, self.get_y() + 0.4)
        self.ln(2.4)

    def h3(self, text, keep=0):
        self.keep(14 + keep)
        self.ln(1)
        y = self.get_y()
        self.set_fill_color(*TEAL_DARK)
        self.rect(self.w - self.r_margin - 3.6, y + 2.2, 3.1, 3.1, style="F",
                  round_corners=True, corner_radius=0.7)
        self.set_font("Vazir", "B", 11)
        self.set_text_color(*NAVY)
        self.set_xy(self.l_margin, y)
        self.cell(self.epw - 7, 7.5, text, align="R", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(0.6)

    def p(self, text, size=BODY, bold=False):
        self.set_font("Vazir", "B" if bold else "", size)
        self.set_text_color(*INK)
        self.multi_cell(self.epw, LH, text, align="R", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(1.2)

    def bullet(self, text, indent=0, marker="●", mcolor=TEAL, bold=False, size=BODY):
        self.set_font("Vazir", "B" if bold else "", size)
        mw = 7.5
        h = self.multi_cell(self.epw - indent - mw, LH, text, align="R",
                            dry_run=True, output="HEIGHT")
        self.need(h + 1)
        y0 = self.get_y()
        mx = self.w - self.r_margin - indent - mw
        if marker == "●":
            self.set_fill_color(*mcolor)
            self.ellipse(mx + mw / 2 - 1.1, y0 + LH / 2 - 1.1, 2.2, 2.2, style="F")
        else:
            self.set_text_color(*mcolor)
            self.set_font("Vazir", "B", size)
            self.set_xy(mx, y0)
            self.cell(mw, LH, marker, align="C")
        self.set_font("Vazir", "B" if bold else "", size)
        self.set_text_color(*INK)
        self.set_xy(self.l_margin, y0)
        self.multi_cell(self.epw - indent - mw, LH, text, align="R",
                        new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(0.4)

    def bullets(self, items, indent=0):
        for it in items:
            self.bullet(it, indent=indent)
        self.ln(1)

    def numbered(self, items, indent=0, start=1):
        for i, it in enumerate(items):
            self.bullet(it, indent=indent, marker=NUM_DIGITS[start - 1 + i] + ".", mcolor=TEAL_DARK)
        self.ln(1)

    KEEP_CAP = 52  # بیشینهٔ فضای «یکجا بمان» تا صفحه‌ها کم‌پُر نمانند

    def h3_bullets(self, title, items, indent=3):
        self.h3(title, keep=min(self.est_list(items, indent), self.KEEP_CAP))
        self.bullets(items, indent=indent)

    def h3_numbered(self, title, items, indent=0):
        self.h3(title, keep=min(self.est_list(items, indent), self.KEEP_CAP))
        self.numbered(items, indent=indent)

    def h2_bullets(self, title, items, indent=0):
        self.h2(title, keep=min(self.est_list(items, indent), self.KEEP_CAP))
        self.bullets(items, indent=indent)

    def h2_numbered(self, title, items, indent=0):
        self.h2(title, keep=min(self.est_list(items, indent), self.KEEP_CAP))
        self.numbered(items, indent=indent)

    # ---------- بلوک آیه (تنها جای طلایی/کرم) ----------
    def ayah(self, arabic, translation, ref="", size=15.5):
        # قلم AmiriQuran گلیف «ک» فارسی (U+06A9) را ندارد؛ در متن آیه به كاف عربی
        # (رسم‌الخط مصحف) نگاشت می‌شود — ثبت‌شده در QC_REPORT.
        arabic = arabic.replace("ک", "ك")
        pad = 5
        w = self.epw - 2 * pad - 3
        lh_ar = size * 0.78
        self.set_font("AQuran", "", size)
        h_ar = self.multi_cell(w, lh_ar, arabic, align="C", dry_run=True, output="HEIGHT")
        self.set_font("Vazir", "", 9.6)
        h_tr = self.multi_cell(w, 5.9, translation, align="R", dry_run=True, output="HEIGHT")
        h_ref = 5.5 if ref else 0
        box_h = h_ar + h_tr + h_ref + 2 * pad + 3.5
        self.keep(box_h + 3)
        y0 = self.get_y()
        self.set_fill_color(*CREAM)
        self.rect(self.l_margin, y0, self.epw, box_h, style="F",
                  round_corners=True, corner_radius=2.2)
        self.set_fill_color(*GOLD)
        self.rect(self.w - self.r_margin - 2.8, y0, 2.8, box_h, style="F",
                  round_corners=True, corner_radius=1.4)
        self.set_font("AQuran", "", size)
        self.set_text_color(60, 42, 8)
        self.set_xy(self.l_margin + pad, y0 + pad)
        self.multi_cell(w, lh_ar, arabic, align="C")
        yy = y0 + pad + h_ar + 2
        self.set_draw_color(222, 206, 160)
        self.set_line_width(0.25)
        self.line(self.l_margin + pad + 12, yy, self.w - self.r_margin - pad - 12, yy)
        self.set_font("Vazir", "", 9.6)
        self.set_text_color(*GOLD_TEXT)
        self.set_xy(self.l_margin + pad, yy + 1.5)
        self.multi_cell(w, 5.9, translation, align="R")
        if ref:
            self.set_font("Vazir", "B", 8)
            self.set_text_color(*GOLD)
            self.set_xy(self.l_margin + pad, y0 + box_h - pad - 1.5)
            self.cell(w, 5, ref, align="L")
        self.set_y(y0 + box_h)
        self.ln(3)

    # ---------- جعبه‌های شش‌گانه ----------
    def _box(self, text, title, fill, bar, tcolor, body_color=None, size=9.8):
        self.set_font("Vazir", "", size)
        pad = 4
        w = self.epw - 2 * pad - 4
        th = self.multi_cell(w, 6.2, text, align="R", dry_run=True, output="HEIGHT")
        box_h = th + 2 * pad + 7
        self.keep(box_h + 3)
        y0 = self.get_y()
        self.set_fill_color(*fill)
        self.rect(self.l_margin, y0, self.epw, box_h, style="F",
                  round_corners=True, corner_radius=2)
        self.set_fill_color(*bar)
        self.rect(self.w - self.r_margin - 2.6, y0, 2.6, box_h, style="F",
                  round_corners=True, corner_radius=1.3)
        self.set_font("Vazir", "B", 10)
        self.set_text_color(*tcolor)
        self.set_xy(self.l_margin + pad, y0 + pad - 1.5)
        self.cell(w, 7, "« " + title + " »", align="R")
        self.set_font("Vazir", "", size)
        self.set_text_color(*(body_color or (45, 52, 62)))
        self.set_xy(self.l_margin + pad, y0 + pad + 6)
        self.multi_cell(w, 6.2, text, align="R")
        self.set_y(y0 + box_h)
        self.ln(3)

    def note(self, text, title="نکته"):
        self._box(text, title, TEAL_LIGHT, TEAL, TEAL_DARK)

    def hadith(self, text, title="حدیث"):
        self._box(text, title, BLUE_LIGHT, NAVY, BLUE_DARK)

    def key(self, text, title="پیام کلیدی"):
        self._box(text, title, (236, 244, 244), TEAL_DARK, NAVY)

    def warn(self, text, title="هشدار فهمِ غلط"):
        self._box(text, title, RED_LIGHT, RED, RED)

    def memo(self, text, title="حفظی — این را به خاطر بسپار"):
        self._box(text, title, (238, 241, 248), BLUE_DARK, BLUE_DARK)

    def compare(self, text, title="مقایسه"):
        self._box(text, title, PURPLE_LIGHT, PURPLE, PURPLE)

    def qa(self, question, answer):
        self.set_font("Vazir", "", BODY)
        hq = self.multi_cell(self.epw - 10, LH, question, align="R", dry_run=True, output="HEIGHT")
        ha = self.multi_cell(self.epw - 10, LH, answer, align="R", dry_run=True, output="HEIGHT")
        self.keep(hq + 8)
        self.bullet("پرسش: " + question, marker="؟", mcolor=PURPLE, bold=True)
        self.need(min(ha + 2, self.eph_avail - 6))
        self.bullet("پاسخ: " + answer, marker="◆", mcolor=TEAL_DARK)
        self.ln(0.6)

    def tag_line(self, items, fill=TEAL_LIGHT, tcolor=TEAL_DARK):
        self.set_font("Vazir", "B", 9.5)
        rows, row, x_used = [], [], 0.0
        for it in items:
            tw = self.get_string_width(it) + 7
            if x_used + tw > self.epw and row:
                rows.append(row)
                row, x_used = [], 0.0
            row.append((it, tw))
            x_used += tw + 2.5
        if row:
            rows.append(row)
        total_h = len(rows) * 10 + 1
        self.keep(total_h)
        y = self.get_y()
        for r in rows:
            x_right = self.w - self.r_margin
            for it, tw in r:
                self.set_fill_color(*fill)
                self.rect(x_right - tw, y, tw, 8, style="F",
                          round_corners=True, corner_radius=2.5)
                self.set_text_color(*tcolor)
                self.set_xy(x_right - tw, y)
                self.cell(tw, 8, it, align="C")
                x_right -= tw + 2.5
            y += 10
        self.set_y(y + 1)


# =======================================================================
def build():
    pdf = Jozve()

    # ================= جلد =================
    pdf.add_page()
    pdf.set_fill_color(*COVER_BG)
    pdf.rect(0, 0, pdf.w, pdf.h, style="F")
    pdf.set_fill_color(*TEAL)
    pdf.rect(0, 0, pdf.w, 5, style="F")
    pdf.set_fill_color(*GOLD)
    pdf.rect(0, 5, pdf.w, 1.6, style="F")

    logo = os.path.join(ASSETS, "humsyar_logo.jpg")
    if os.path.exists(logo):
        lw = 92
        pdf.image(logo, x=(pdf.w - lw) / 2, y=18, w=lw)

    pdf.set_y(118)
    pdf.set_font("VazirBlack", "", 29)
    pdf.set_text_color(*WHITE)
    pdf.cell(pdf.epw, 16, "جزوهٔ تفسیر موضوعی قرآن", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Vazir", "B", 14)
    pdf.set_text_color(200, 214, 228)
    pdf.cell(pdf.epw, 11, "بر پایهٔ «تفسیر نور» — حجت‌الاسلام محسن قرائتی", align="C",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(4)

    # نشان «ویژه‌ی برادران»
    pdf.set_font("VazirBlack", "", 13)
    badge = "ویژه‌ی برادران"
    bw = pdf.get_string_width(badge) + 18
    bx = (pdf.w - bw) / 2
    by = pdf.get_y()
    pdf.set_fill_color(*TEAL)
    pdf.rect(bx, by, bw, 11.5, style="F", round_corners=True, corner_radius=5.5)
    pdf.set_text_color(*WHITE)
    pdf.set_xy(bx, by)
    pdf.cell(bw, 11.5, badge, align="C")
    pdf.set_y(by + 18)

    pdf.set_draw_color(*TEAL_BRIGHT)
    pdf.set_line_width(0.6)
    pdf.line(70, pdf.get_y(), pdf.w - 70, pdf.get_y())
    pdf.ln(6)

    pdf.set_font("Vazir", "", 11.5)
    pdf.set_text_color(200, 214, 228)
    for line in [
        "سورهٔ حمد — امّ‌الکتاب و سورهٔ واجب هر نماز",
        "سورهٔ توحید — شناسنامهٔ خداوند",
        "سورهٔ عصر — سرمایهٔ عمر و بازار دنیا",
        "سورهٔ کوثر — خیر کثیر و پاسخ خدا به دشمن",
        "مرور سریع شب امتحان",
    ]:
        pdf.cell(pdf.epw, 8.2, "•  " + line, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # آمار
    pdf.ln(5)
    stats = [("۴", "سوره"), ("۱۷", "آیه"), ("۵", "فصل")]
    sw, gap = 34, 8
    x0 = (pdf.w - 3 * sw - 2 * gap) / 2
    y0 = pdf.get_y()
    for i, (num, lab) in enumerate(stats):
        x = x0 + i * (sw + gap)
        pdf.set_draw_color(*TEAL_BRIGHT)
        pdf.set_line_width(0.4)
        pdf.rect(x, y0, sw, 17, style="D", round_corners=True, corner_radius=2.5)
        pdf.set_font("VazirBlack", "", 14)
        pdf.set_text_color(*TEAL_BRIGHT)
        pdf.set_xy(x, y0 + 1.5)
        pdf.cell(sw, 8, num, align="C")
        pdf.set_font("Vazir", "", 9)
        pdf.set_text_color(200, 214, 228)
        pdf.set_xy(x, y0 + 9)
        pdf.cell(sw, 6, lab, align="C")

    pdf.set_auto_page_break(False, 0)
    pdf.set_y(-36)
    pdf.set_font("VazirBlack", "", 15)
    hums_w = pdf.get_string_width("Hums")
    yar_w = pdf.get_string_width("Yar")
    x0 = (pdf.w - hums_w - yar_w) / 2
    pdf.set_xy(x0, pdf.get_y())
    pdf.set_text_color(*WHITE)
    pdf.cell(hums_w, 9, "Hums")
    pdf.set_text_color(*TEAL_BRIGHT)
    pdf.cell(yar_w, 9, "Yar", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Vazir", "", 9.5)
    pdf.set_text_color(*TEAL_BRIGHT)
    pdf.cell(pdf.epw, 7, "دستیار هوشمند دانشجویان", align="C",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_auto_page_break(True, margin=19)

    # ================= فهرست =================
    pdf.add_page()
    pdf.set_y(20)
    pdf.set_font("VazirBlack", "", 17)
    pdf.set_text_color(*NAVY)
    pdf.cell(pdf.epw, 11, "فهرست مطالب", align="R", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_draw_color(*GOLD)
    pdf.set_line_width(0.8)
    pdf.line(pdf.w - pdf.r_margin - 52, pdf.get_y() + 1, pdf.w - pdf.r_margin, pdf.get_y() + 1)
    pdf.ln(6)
    pdf.toc_placeholder_y = pdf.get_y()
    pdf.ln(58)

    # راهنمای نشانه‌های جزوه
    pdf.set_font("Vazir", "B", 12)
    pdf.set_text_color(*NAVY)
    pdf.cell(pdf.epw, 9, "راهنمای نشانه‌های جزوه", align="R", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(1.5)
    guide = [
        (CREAM, GOLD, "بلوک آیه", "متن عربی آیات با قلم قرآنی (Amiri Quran) + ترجمهٔ منبع — عیناً از تفسیر نور"),
        (TEAL_LIGHT, TEAL, "نکته", "نکته‌های تفسیری ذیل هر آیه"),
        (BLUE_LIGHT, NAVY, "حدیث", "روایات معصومین(ع) نقل‌شده در منبع"),
        ((236, 244, 244), TEAL_DARK, "پیام کلیدی", "جمع‌بندی و چکیدهٔ موضوع"),
        ((238, 241, 248), BLUE_DARK, "حفظی", "اعداد و فهرست‌هایی که باید به خاطر بسپاری"),
        (PURPLE_LIGHT, PURPLE, "مقایسه", "تفاوت‌های مفهومی (واحد/احد، کوثر/تکاثر و…)"),
        (RED_LIGHT, RED, "هشدار فهمِ غلط", "جاهایی که معمولاً اشتباه فهمیده می‌شود"),
    ]
    for fill, bar, name, desc in guide:
        y = pdf.get_y()
        pdf.set_fill_color(*fill)
        pdf.rect(pdf.w - pdf.r_margin - 34, y + 0.7, 34, 7.6, style="F",
                 round_corners=True, corner_radius=2)
        pdf.set_fill_color(*bar)
        pdf.rect(pdf.w - pdf.r_margin - 2.2, y + 0.7, 2.2, 7.6, style="F",
                 round_corners=True, corner_radius=1.1)
        pdf.set_font("Vazir", "B", 8.8)
        pdf.set_text_color(*NAVY)
        pdf.set_xy(pdf.w - pdf.r_margin - 34, y + 0.7)
        pdf.cell(32, 7.6, name, align="C")
        pdf.set_font("Vazir", "", 9)
        pdf.set_text_color(*GRAY)
        pdf.set_xy(pdf.l_margin, y + 0.7)
        pdf.cell(pdf.epw - 38, 7.6, desc, align="R")
        pdf.set_y(y + 9.4)

    pdf.ln(2)
    pdf.note("روش کار این جزوه: متن آیات و همهٔ نکته‌ها، حدیث‌ها و پیام‌ها عیناً از «تفسیر نور» "
             "(منابع بارگذاری‌شده در مخزن) آمده است؛ هیچ مطلبی از حافظه یا منابع بیرونی اضافه نشده. "
             "فهرست‌های شماره‌دار با همان تعداد و ترتیبِ منبع حفظ شده‌اند: سیمای بسم‌اللّه ۱۱ مورد، "
             "درس‌های تربیتی حمد ۱۱ مورد، پیام‌های عصر ۱۲ مورد و پیام‌های کوثر ۲۰ مورد.",
             title="پیش از شروع")

    # ================= فصل‌ها =================
    from content import ch1_hamd, ch2_tohid, ch3_asr, ch4_kowsar, ch5_morur
    ch1_hamd.render(pdf)
    ch2_tohid.render(pdf)
    ch3_asr.render(pdf)
    ch4_kowsar.render(pdf)
    ch5_morur.render(pdf)

    return pdf


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    pdf = build()
    toc = list(pdf.toc)

    pdf2 = build()
    pdf2.page = 2
    pdf2.set_y(pdf2.toc_placeholder_y)
    for title, pageno in toc:
        pdf2.set_font("Vazir", "", 10.5)
        pdf2.set_text_color(*NAVY)
        yy = pdf2.get_y()
        pdf2.set_xy(pdf2.l_margin, yy)
        pdf2.cell(14, 9, fa(pageno), align="L")
        pdf2.set_xy(pdf2.l_margin + 16, yy)
        pdf2.cell(pdf2.epw - 16, 9, title, align="R")
        pdf2.ln(9.6)
    pdf2.page = pdf2.pages_count

    pdf2.output(OUT)
    print("ساخته شد:", OUT, "—", pdf2.pages_count, "صفحه")


if __name__ == "__main__":
    main()
