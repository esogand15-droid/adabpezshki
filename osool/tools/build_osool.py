# -*- coding: utf-8 -*-
"""
سازندهٔ «جزوهٔ شب امتحانی اصول خدمات سلامت» | HumsYar
بر پایهٔ «برنامه و راهنمای ایمن‌سازی — مصوب کمیتهٔ کشوری ایمن‌سازی ۱۴۰۳»
(منبع: اصول خدمات/Immunization Guide line-Final-1403.pdf)
خروجی: osool/output/جزوه-شب-امتحانی-اصول-خدمات-سلامت.pdf
"""
import os
import re
import sys

from fpdf import FPDF
from fpdf.enums import XPos, YPos

HERE = os.path.dirname(os.path.abspath(__file__))
OSOOL = os.path.dirname(HERE)                  # osool/
ROOT = os.path.dirname(OSOOL)                  # repo root
FONTS_V = os.path.join(ROOT, "tools", "fonts")  # Vazirmatn
ASSETS = os.path.join(HERE, "assets")
OUTDIR = os.path.join(OSOOL, "output")
OUT = os.path.join(OUTDIR, "جزوه-شب-امتحانی-اصول-خدمات-سلامت.pdf")

sys.path.insert(0, OSOOL)

# ---------- پالت HumsYar ----------
NAVY = (23, 42, 76)
COVER_BG = (0, 1, 19)
TEAL = (0, 128, 128)
TEAL_DARK = (0, 96, 100)
TEAL_BRIGHT = (0, 210, 220)
TEAL_LIGHT = (224, 242, 241)
BLUE_LIGHT = (232, 240, 250)
BLUE_DARK = (30, 62, 110)
# سبز سلامت — رنگ تأکیدی اختصاصی این جزوه (هم‌خانواده با پالت HumsYar)
GREEN = (36, 196, 160)
GREEN_DARK = (18, 122, 98)
GREEN_LIGHT = (228, 246, 240)
GOLD = (240, 173, 30)
CREAM = (251, 246, 233)
GOLD_TEXT = (110, 84, 20)
ORANGE = (214, 112, 20)
ORANGE_LIGHT = (255, 241, 226)
GRAY = (90, 98, 110)
LINE = (205, 215, 220)
WHITE = (255, 255, 255)
RED = (176, 52, 44)
RED_LIGHT = (252, 238, 236)
PURPLE = (94, 70, 130)
PURPLE_LIGHT = (240, 236, 247)
INK = (30, 36, 45)

LH = 6.9
BODY = 10.3
CH_DIGITS = ["۱", "۲", "۳", "۴", "۵", "۶", "۷", "۸", "۹", "۱۰", "۱۱", "۱۲"]
NUM_DIGITS = ["۱", "۲", "۳", "۴", "۵", "۶", "۷", "۸", "۹", "۱۰", "۱۱", "۱۲", "۱۳",
              "۱۴", "۱۵", "۱۶", "۱۷", "۱۸", "۱۹", "۲۰", "۲۱", "۲۲", "۲۳", "۲۴", "۲۵"]

FA_DIGITS = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")
# حذف حرکات عربی از متن فارسی (قلم وزیرمتن با علائم ترکیبی، واژه را می‌شکند)
MARKS = re.compile("[\u064B-\u0652\u0670]")


def fa(n):
    return str(n).translate(FA_DIGITS)


class Jozve(FPDF):
    def __init__(self):
        super().__init__("P", "mm", "A4")
        self.add_font("Vazir", "", os.path.join(FONTS_V, "Vazirmatn-Regular.ttf"))
        self.add_font("Vazir", "B", os.path.join(FONTS_V, "Vazirmatn-Bold.ttf"))
        self.add_font("VazirBlack", "", os.path.join(FONTS_V, "Vazirmatn-Black.ttf"))
        self.add_font("VazirLight", "", os.path.join(FONTS_V, "Vazirmatn-Light.ttf"))
        self.set_text_shaping(True)
        self.set_margins(15, 17, 15)
        self.set_auto_page_break(True, margin=19)
        self.toc = []
        self.chapter_no = 0

    # همهٔ متن جزوه با وزیرمتن است؛ حرکات ترکیبی سراسری حذف می‌شوند
    # و اگر متن فارسی با نویسهٔ لاتین شروع شود، RLM اول آن می‌نشیند تا جهت پایه RTL بماند
    @staticmethod
    def _fix(text):
        text = MARKS.sub("", text)
        if text and re.match(r"[A-Za-z0-9(\[]", text.lstrip()) and \
                any("\u0600" <= c <= "\u06FF" for c in text):
            text = "\u200F" + text
        return text

    def cell(self, w=None, h=None, text="", *a, **kw):
        return super().cell(w, h, self._fix(text), *a, **kw)

    def multi_cell(self, w, h=None, text="", *a, **kw):
        return super().multi_cell(w, h, self._fix(text), *a, **kw)

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
        self.cell(self.epw, 6, "جزوهٔ شب امتحانی اصول خدمات سلامت", align="R")
        self.set_xy(self.l_margin, 5.5)
        self.set_text_color(*GREEN_DARK)
        self.cell(self.epw, 6, "ایمن‌سازی کشوری ۱۴۰۳", align="L")
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
        self.set_fill_color(*GREEN)
        cx = self.w - self.r_margin - 8.5
        self.ellipse(cx - 5.5, y + 3, 11, 11, style="F")
        self.set_font("VazirBlack", "", 12 if (num_char and len(num_char) > 1) or self.chapter_no > 9 else 13)
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

    # --- تیتر معلق ---
    _pending = None

    def h2(self, text, keep=0):
        self._pending = ("h2", text, keep)

    def h3(self, text, keep=0):
        self._pending = ("h3", text, keep)

    def _anchor(self, first_h):
        if self._pending:
            kind, text, keep = self._pending
            self._pending = None
            head_h = 20 if kind == "h2" else 14
            self.need(min(head_h + max(keep, first_h), self.eph_avail - 6))
            if kind == "h2":
                self._draw_h2(text)
            else:
                self._draw_h3(text)
            self.need(min(first_h, self.eph_avail - 6))
        else:
            self.need(min(first_h, self.eph_avail - 6))

    def _draw_h2(self, text):
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

    def _draw_h3(self, text):
        self.ln(1)
        y = self.get_y()
        self.set_fill_color(*GREEN)
        self.rect(self.w - self.r_margin - 3.6, y + 2.2, 3.1, 3.1, style="F",
                  round_corners=True, corner_radius=0.7)
        self.set_font("Vazir", "B", 11)
        self.set_text_color(*NAVY)
        self.set_xy(self.l_margin, y)
        self.cell(self.epw - 7, 7.5, text, align="R", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(0.6)

    def p(self, text, size=BODY, bold=False):
        self.set_font("Vazir", "B" if bold else "", size)
        th = self.multi_cell(self.epw, LH, text, align="R", dry_run=True, output="HEIGHT")
        self._anchor(min(th + 1, 34))
        self.set_font("Vazir", "B" if bold else "", size)
        self.set_text_color(*INK)
        self.multi_cell(self.epw, LH, text, align="R", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(1.2)

    def bullet(self, text, indent=0, marker="●", mcolor=TEAL, bold=False, size=BODY):
        self.set_font("Vazir", "B" if bold else "", size)
        mw = 7.5
        h = self.multi_cell(self.epw - indent - mw, LH, text, align="R",
                            dry_run=True, output="HEIGHT")
        self._anchor(h + 1)
        self.set_font("Vazir", "B" if bold else "", size)
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

    KEEP_CAP = 52

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

    # ---------- جعبه‌ها ----------
    def _box(self, text, title, fill, bar, tcolor, body_color=None, size=9.8):
        self.set_font("Vazir", "", size)
        pad = 4
        w = self.epw - 2 * pad - 4
        th = self.multi_cell(w, 6.2, text, align="R", dry_run=True, output="HEIGHT")
        box_h = th + 2 * pad + 7
        self._anchor(box_h + 3)
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

    def note(self, text, title="نکتهٔ مهم"):
        self._box(text, title, (255, 248, 229), GOLD, GOLD_TEXT)

    def key(self, text, title="قانون کلی"):
        self._box(text, title, (236, 244, 244), TEAL_DARK, NAVY)

    def warn(self, text, title="ممنوعیت"):
        self._box(text, title, RED_LIGHT, RED, RED)

    def memo(self, text, title="حفظی — این را به خاطر بسپار"):
        self._box(text, title, (238, 241, 248), BLUE_DARK, BLUE_DARK)

    def compare(self, text, title="مقایسه"):
        self._box(text, title, PURPLE_LIGHT, PURPLE, PURPLE)

    def exam(self, text, title="مستعد سؤال"):
        self._box(text, title, ORANGE_LIGHT, ORANGE, ORANGE)

    def mnemo(self, text, title="رمز یادسپاری"):
        self._box(text, title, GREEN_LIGHT, GREEN_DARK, GREEN_DARK)

    def define(self, text, title="تعریف"):
        self._box(text, title, BLUE_LIGHT, TEAL, BLUE_DARK)

    def qa(self, question, answer):
        self.set_font("Vazir", "", BODY)
        hq = self.multi_cell(self.epw - 10, LH, question, align="R", dry_run=True, output="HEIGHT")
        ha = self.multi_cell(self.epw - 10, LH, answer, align="R", dry_run=True, output="HEIGHT")
        self._anchor(hq + min(ha, 24) + 9)
        self.bullet("پرسش: " + question, marker="؟", mcolor=PURPLE, bold=True)
        self.need(min(ha + 2, self.eph_avail - 6))
        self.bullet("پاسخ: " + answer, marker="●", mcolor=TEAL_DARK)
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
        self._anchor(total_h)
        self.set_font("Vazir", "B", 9.5)
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

    # ---------- جدول RTL ----------
    def table(self, headers, rows, widths=None, title="", size=8.6, hsize=9.2,
              header_fill=NAVY, min_rh=7.5):
        """جدول راست‌به‌چپ: ستون نخست در منتهاالیه راست. widths نسبی است."""
        n = len(headers)
        widths = widths or [1] * n
        tot = float(sum(widths))
        ws = [self.epw * w / tot for w in widths]
        pad_x, pad_y = 1.6, 1.3
        lh = size * 0.52

        def row_h(cells, s, bold):
            self.set_font("Vazir", "B" if bold else "", s)
            h = 0.0
            for c, w in zip(cells, ws):
                hh = self.multi_cell(w - 2 * pad_x, lh, str(c), align="C",
                                     dry_run=True, output="HEIGHT")
                h = max(h, hh)
            return max(h + 2 * pad_y, min_rh)

        def draw_row(cells, s, bold, fill, tcolor, h):
            y0 = self.get_y()
            x_right = self.w - self.r_margin
            self.set_draw_color(*LINE)
            self.set_line_width(0.22)
            for c, w in zip(cells, ws):
                x = x_right - w
                self.set_fill_color(*fill)
                self.rect(x, y0, w, h, style="FD")
                self.set_font("Vazir", "B" if bold else "", s)
                self.set_text_color(*tcolor)
                ch = self.multi_cell(w - 2 * pad_x, lh, str(c), align="C",
                                     dry_run=True, output="HEIGHT")
                self.set_xy(x + pad_x, y0 + (h - ch) / 2)
                self.multi_cell(w - 2 * pad_x, lh, str(c), align="C")
                x_right = x
            self.set_y(y0 + h)

        hh = row_h(headers, hsize, True)
        first_rh = row_h(rows[0], size, False) if rows else 0
        title_h = 8 if title else 0
        self._anchor(min(title_h + hh + first_rh + 4, self.eph_avail - 6))

        def draw_title_header():
            if title:
                self.set_font("Vazir", "B", 9.6)
                self.set_text_color(*GREEN_DARK)
                self.cell(self.epw, 7, title, align="R",
                          new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                self.ln(0.6)
            draw_row(headers, hsize, True, header_fill, WHITE, hh)

        draw_title_header()
        zebra = False
        for cells in rows:
            rh = row_h(cells, size, False)
            if self.get_y() + rh > self.page_break_trigger:
                self.add_page()
                draw_row(headers, hsize, True, header_fill, WHITE, hh)
            draw_row(cells, size, False, (247, 250, 252) if zebra else WHITE, INK, rh)
            zebra = not zebra
        self.ln(3)

    # ---------- تصویر با شرح ----------
    def figure(self, path, caption, w=None):
        from PIL import Image
        img = Image.open(path)
        iw, ih = img.size
        w = w or self.epw * 0.86
        h = w * ih / iw
        self._anchor(min(h + 12, self.eph_avail - 6))
        x = (self.w - w) / 2
        y0 = self.get_y()
        self.image(path, x=x, y=y0, w=w)
        self.set_y(y0 + h + 1)
        self.set_font("Vazir", "B", 8.8)
        self.set_text_color(*GRAY)
        self.cell(self.epw, 6, caption, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(2)


# =======================================================================
def build():
    pdf = Jozve()

    # ================= جلد =================
    pdf.add_page()
    pdf.set_fill_color(*COVER_BG)
    pdf.rect(0, 0, pdf.w, pdf.h, style="F")
    pdf.set_fill_color(*TEAL)
    pdf.rect(0, 0, pdf.w, 5, style="F")
    pdf.set_fill_color(*GREEN)
    pdf.rect(0, 5, pdf.w, 1.6, style="F")

    logo = os.path.join(ASSETS, "humsyar_logo.jpg")
    if os.path.exists(logo):
        lw = 88
        pdf.image(logo, x=(pdf.w - lw) / 2, y=16, w=lw)

    pdf.set_y(110)
    pdf.set_font("VazirBlack", "", 28)
    pdf.set_text_color(*WHITE)
    pdf.cell(pdf.epw, 15, "جزوهٔ شب امتحانی اصول خدمات سلامت", align="C",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Vazir", "B", 13)
    pdf.set_text_color(200, 214, 228)
    pdf.cell(pdf.epw, 10, "بر پایهٔ «برنامه و راهنمای ایمن‌سازی» — مصوب کمیتهٔ کشوری ایمن‌سازی ۱۴۰۳",
             align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(4)

    pdf.set_font("VazirBlack", "", 13)
    badge = "ایمن‌سازی و واکسیناسیون کشوری"
    bw = pdf.get_string_width(badge) + 18
    bx = (pdf.w - bw) / 2
    by = pdf.get_y()
    pdf.set_fill_color(*GREEN_DARK)
    pdf.rect(bx, by, bw, 11.5, style="F", round_corners=True, corner_radius=5.5)
    pdf.set_text_color(*WHITE)
    pdf.set_xy(bx, by)
    pdf.cell(bw, 11.5, badge, align="C")
    pdf.set_y(by + 18)

    pdf.set_draw_color(*TEAL_BRIGHT)
    pdf.set_line_width(0.6)
    pdf.line(70, pdf.get_y(), pdf.w - 70, pdf.get_y())
    pdf.ln(6)

    pdf.set_font("Vazir", "", 11)
    pdf.set_text_color(200, 214, 228)
    for line in [
        "اصول کلی واکسیناسیون، زنجیرهٔ سرما و آنافیلاکسی",
        "برنامهٔ ایمن‌سازی کشوری و جدول‌های تأخیری",
        "گروه‌های خاص و نکات کاربردی ۱۱ واکسن",
        "بزرگسالان، سفر و ایمن‌سازی غیرفعال",
        "پیوست‌ها + مرور سریع شب امتحان",
    ]:
        pdf.cell(pdf.epw, 8, "•  " + line, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.ln(5)
    stats = [("۸", "فصل + ۲ پیوست"), ("۲۴", "جدول منبع"), ("۱۰۶", "صفحهٔ منبع")]
    sw, gap = 40, 8
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
        pdf.set_font("Vazir", "", 8.6)
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
    pdf.set_y(18)
    pdf.set_font("VazirBlack", "", 17)
    pdf.set_text_color(*NAVY)
    pdf.cell(pdf.epw, 11, "فهرست مطالب", align="R", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_draw_color(*GREEN)
    pdf.set_line_width(0.8)
    pdf.line(pdf.w - pdf.r_margin - 52, pdf.get_y() + 1, pdf.w - pdf.r_margin, pdf.get_y() + 1)
    pdf.ln(5)
    pdf.toc_placeholder_y = pdf.get_y()
    pdf.ln(104)

    # راهنمای نشانه‌های جزوه
    pdf.set_font("Vazir", "B", 12)
    pdf.set_text_color(*NAVY)
    pdf.cell(pdf.epw, 9, "راهنمای نشانه‌های جزوه", align="R", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(1.5)
    guide = [
        (BLUE_LIGHT, TEAL, "تعریف", "تعریف‌های رسمی منبع که عین عبارتشان مهم است"),
        ((255, 248, 229), GOLD, "نکتهٔ مهم", "جزئیات مهم و استثناهایی که نباید از قلم بیفتد"),
        ((236, 244, 244), TEAL_DARK, "قانون کلی", "جمع‌بندی و قاعدهٔ عملی هر مبحث"),
        ((238, 241, 248), BLUE_DARK, "حفظی", "اعداد، فاصله‌ها و فهرست‌هایی که باید به خاطر بسپاری"),
        (PURPLE_LIGHT, PURPLE, "مقایسه", "تفاوت‌های دوبه‌دو (غش/آنافیلاکسی، کنژوگه/پلی‌ساکاریدی و…)"),
        (RED_LIGHT, RED, "ممنوعیت", "موارد منع مصرف و خطاهای پرتکرار"),
        (ORANGE_LIGHT, ORANGE, "مستعد سؤال", "نقطه‌هایی که معمولاً محل طرح سؤال‌اند"),
        (GREEN_LIGHT, GREEN_DARK, "رمز یادسپاری", "ترفند ذهنی برای حفظ سریع‌تر"),
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
    pdf.note("این جزوه تمام فصل‌های «برنامه و راهنمای ایمن‌سازی ۱۴۰۳» را به ترتیب خود منبع پوشش می‌دهد: "
             "متن‌ها، جدول‌ها، اعداد و استثناها از همان منبع بازنویسی و فشرده شده‌اند و شمارهٔ جدول‌های منبع "
             "(جدول ۱ تا ۲۴) کنار هر جدول آمده است تا در صورت نیاز بتوانی به اصل آن مراجعه کنی. "
             "جعبه‌های رنگی فقط ابزار مرور سریع‌اند؛ متن اصلی هر مبحث را هم حتماً یک‌بار بخوان.",
             title="پیش از شروع")

    # ================= فصل‌ها =================
    from content import (ch1_osool, ch2_imen, ch3_barname, ch4_khass, ch5_vaksanha,
                         ch6_bozorgsalan, ch7_safar, ch8_gheyrefaal, ch9_peyvast,
                         ch10_morur)
    ch1_osool.render(pdf)
    ch2_imen.render(pdf)
    ch3_barname.render(pdf)
    ch4_khass.render(pdf)
    ch5_vaksanha.render(pdf)
    ch6_bozorgsalan.render(pdf)
    ch7_safar.render(pdf)
    ch8_gheyrefaal.render(pdf)
    ch9_peyvast.render(pdf)
    ch10_morur.render(pdf)

    return pdf


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    pdf = build()
    toc = list(pdf.toc)

    pdf2 = build()
    pdf2.page = 2
    pdf2.set_y(pdf2.toc_placeholder_y)
    for title, pageno in toc:
        pdf2.set_font("Vazir", "", 10.2)
        pdf2.set_text_color(*NAVY)
        yy = pdf2.get_y()
        pdf2.set_xy(pdf2.l_margin, yy)
        pdf2.cell(14, 8.6, fa(pageno), align="L")
        pdf2.set_xy(pdf2.l_margin + 16, yy)
        pdf2.cell(pdf2.epw - 16, 8.6, title, align="R")
        pdf2.ln(9.0)
    pdf2.page = pdf2.pages_count

    pdf2.output(OUT)
    print("ساخته شد:", OUT, "—", pdf2.pages_count, "صفحه")


if __name__ == "__main__":
    main()
