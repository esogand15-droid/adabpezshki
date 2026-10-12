# -*- coding: utf-8 -*-
"""ساخت دو PDF از data/questions.json:
1) Tafsir_Mozooei_Brothers_Question_Bank.pdf — بانک کامل با پاسخ و توضیح
2) Tafsir_Practice_Without_Answers.pdf — نسخهٔ تمرینی بی‌پاسخ + کلید در انتها
A4، راست‌به‌چپ، فونت وزیرمتن، keep-together برای هر سؤال، پاصفحهٔ HumsYar.
"""
import json, os
from fpdf import FPDF

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
REPO = os.path.dirname(ROOT)
FONTS = os.path.join(REPO, "tools", "fonts")

NAVY = (23, 42, 76); TEAL = (0, 128, 128); TEAL_DARK = (0, 96, 100)
TEAL_LIGHT = (224, 242, 241); GOLD = (240, 173, 30); CREAM = (251, 246, 233)
GOLD_TEXT = (110, 84, 20); GRAY = (90, 98, 110); LINE = (205, 215, 220)
INK = (30, 36, 45); GREEN = (30, 126, 52); GREEN_BG = (230, 244, 234)
WHITE = (255, 255, 255)

D = json.load(open(os.path.join(ROOT, "data", "questions.json"), encoding="utf-8"))
QS = D["questions"]
FA = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")
def fa(x): return str(x).translate(FA)
LM = {"new_x": "LMARGIN", "new_y": "NEXT"}


class PDF(FPDF):
    def __init__(self, title):
        super().__init__("P", "mm", "A4")
        self.title_fa = title
        self.set_margins(16, 20, 16)
        self.set_auto_page_break(True, margin=20)
        self.add_font("Vazir", "", os.path.join(FONTS, "Vazirmatn-Regular.ttf"))
        self.add_font("Vazir", "B", os.path.join(FONTS, "Vazirmatn-Bold.ttf"))
        self.add_font("VazirL", "", os.path.join(FONTS, "Vazirmatn-Light.ttf"))
        self.set_text_shaping(True)
        self.in_cover = False

    def header(self):
        if self.in_cover: return
        self.set_fill_color(*GOLD); self.rect(0, 0, 210, 2.2, "F")
        self.set_y(6); self.set_font("VazirL", "", 8.2); self.set_text_color(*GRAY)
        self.cell(0, 5, self.title_fa, align="R")
        self.set_y(20)

    def footer(self):
        if self.in_cover or self.page_no() == 1: return
        self.set_y(-14)
        self.set_draw_color(*LINE); self.set_line_width(.2)
        self.line(16, self.get_y(), 194, self.get_y())
        self.set_font("Vazir", "B", 8.5); self.set_text_color(*TEAL_DARK)
        self.cell(0, 8, "HumsYar", align="C")
        self.set_font("VazirL", "", 8); self.set_text_color(*GRAY)
        self.set_y(-14); self.cell(0, 8, fa(self.page_no()), align="L")

    def need(self, h):
        if self.get_y() + h > self.h - 22: self.add_page()

    def lines_of(self, w, h, text):
        return len(self.multi_cell(w, h, text, align="R", dry_run=True, output="LINES"))

    # ---------- اجزا ----------
    def cover(self, subtitle):
        self.in_cover = True
        self.add_page()
        self.set_fill_color(*NAVY); self.rect(0, 0, 210, 297, "F")
        self.set_fill_color(*GOLD); self.rect(0, 58, 210, 2.4, "F"); self.rect(0, 118, 210, 1.2, "F")
        self.set_y(68); self.set_font("Vazir", "B", 23); self.set_text_color(*WHITE)
        self.multi_cell(0, 13, "بانک سؤالات تستی\nتفسیر موضوعی قرآن کریم", align="C", **LM)
        self.set_font("Vazir", "", 13); self.set_text_color(*GOLD)
        self.ln(3); self.multi_cell(0, 9, subtitle, align="C", **LM)
        self.set_font("VazirL", "", 10.5); self.set_text_color(220, 228, 240)
        self.ln(4)
        self.multi_cell(0, 7.5,
            "محدودهٔ جزوهٔ ویژهٔ برادران: سوره‌های حمد، توحید، عصر و کوثر\n"
            "منبع سؤالات: نمونه سوالات تستی کتاب تفسیر موضوعی قرآن کریم (۲۷۰ سؤال)\n"
            "سؤالات منطبق بر محدودهٔ جزوه: " + fa(len(QS)) + " سؤال — سورهٔ حمد",
            align="C", **LM)
        self.set_y(-40); self.set_font("Vazir", "B", 13); self.set_text_color(*GOLD)
        self.cell(0, 8, "HumsYar", align="C")
        self.in_cover = False

    def h1(self, text):
        self.need(18)
        self.set_fill_color(*NAVY); self.set_text_color(*WHITE)
        self.set_font("Vazir", "B", 12.5)
        self.cell(0, 10.5, "  " + text + "  ", align="R", fill=True, **LM)
        self.ln(3)

    def h2(self, text):
        self.need(14)
        self.set_fill_color(*TEAL); self.set_text_color(*WHITE)
        self.set_font("Vazir", "B", 10.5)
        self.cell(0, 8.5, "  " + text + "  ", align="R", fill=True, **LM)
        self.ln(2.5)

    def para(self, text, size=9.8):
        self.set_font("Vazir", "", size); self.set_text_color(*INK)
        self.multi_cell(0, 6.8, text, align="R", **LM)

    def note_box(self, text, title=None):
        self.set_font("Vazir", "", 9.3)
        x, w = self.l_margin, self.epw
        n = self.lines_of(w - 8, 6, text)
        h = n * 6 + 6 + (6.5 if title else 0)
        self.need(h + 3)
        y = self.get_y()
        self.set_fill_color(*CREAM); self.rect(x, y, w, h, "F")
        self.set_fill_color(*GOLD); self.rect(x + w - 1.6, y, 1.6, h, "F")
        cy = y + 3
        if title:
            self.set_xy(x + 4, cy); self.set_font("Vazir", "B", 9.5)
            self.set_text_color(*GOLD_TEXT)
            self.cell(w - 8, 6, title, align="R"); cy += 6.5
        self.set_xy(x + 4, cy); self.set_font("Vazir", "", 9.3)
        self.set_text_color(*GOLD_TEXT)
        self.multi_cell(w - 8, 6, text, align="R", **LM)
        self.set_y(y + h + 3)

    def exp_box(self, q):
        e = q["explanation"]
        es = q.get("exam_source") or {}
        es_line = ""
        if es:
            es_line = "\nمنبع آزمون (تفسیر نور): " + es["status"]
            if es.get("evidence"):
                es_line += " — «" + es["evidence"] + "»"
        text = ("دلیل: " + e["reason"] + "\nنکتهٔ جزوه: " + e["booklet_note"] + es_line +
                "\nمنبع: " + e["source"] + " · اعتبارسنجی: " + q["validation"])
        self.set_font("Vazir", "", 8.8)
        x, w = self.l_margin, self.epw
        n = self.lines_of(w - 9, 5.6, text)
        h = n * 5.6 + 5
        self.need(h + 2)
        y = self.get_y()
        self.set_fill_color(*TEAL_LIGHT); self.rect(x, y, w, h, "F")
        self.set_fill_color(*TEAL); self.rect(x + w - 1.4, y, 1.4, h, "F")
        self.set_xy(x + 4, y + 2.5); self.set_text_color(*TEAL_DARK)
        self.multi_cell(w - 9, 5.6, text, align="R", **LM)
        self.set_y(y + h + 1.5)

    def question(self, q, num, with_answer=True):
        qw = self.epw
        # برآورد ارتفاع برای keep-together
        est = 10
        self.set_font("Vazir", "B", 10.2)
        est += self.lines_of(qw, 6.6, q["question"]) * 6.6
        self.set_font("Vazir", "", 9.6)
        for o in q["options"]:
            est += self.lines_of(qw - 14, 6.2, o["key"] + ") " + o["text"]) * 6.2 + 1.2
        if with_answer:
            e = q["explanation"]
            self.set_font("Vazir", "", 8.8)
            es = q.get("exam_source") or {}
            es_line = ("\nمنبع آزمون: " + es.get("status", "") + " " + es.get("evidence", "")) if es else ""
            est += self.lines_of(qw - 9, 5.6,
                "دلیل: " + e["reason"] + "\nنکتهٔ جزوه: " + e["booklet_note"] + es_line +
                "\nمنبع: " + e["source"]) * 5.6 + 14
        self.need(min(est + 6, 230))

        # سربرگ سؤال: شماره (راست) + برچسب‌ها (چپ)
        y0 = self.get_y()
        tags = ("قطعی A" if q["category"] == "A" else "مفهومی B") + " · " + q["difficulty"]
        self.set_font("VazirL", "", 8); self.set_text_color(*GRAY)
        self.cell(0, 7, tags, align="L")
        self.set_xy(self.l_margin, y0)
        self.set_font("Vazir", "B", 10.2); self.set_text_color(*TEAL_DARK)
        self.cell(0, 7, "سؤال " + fa(num), align="R", **LM)
        self.set_font("Vazir", "B", 10.2); self.set_text_color(*INK)
        self.multi_cell(0, 6.6, q["question"], align="R", **LM)
        self.ln(1)
        for o in q["options"]:
            txt = o["key"] + ") " + o["text"]
            correct = with_answer and o["key"] == q["answer"]
            if correct:
                self.set_font("Vazir", "B", 9.6)
                n = self.lines_of(qw - 14, 6.2, txt + "  ٭")
                yy = self.get_y()
                self.set_fill_color(*GREEN_BG)
                self.rect(self.l_margin + 2, yy, qw - 4, n * 6.2 + 1, "F")
                self.set_xy(self.l_margin + 3, yy + .5)
                self.set_text_color(*GREEN)
                self.multi_cell(qw - 14, 6.2, txt + "  ٭", align="R", **LM)
                self.ln(.7)
            else:
                self.set_x(self.l_margin + 3)
                self.set_font("Vazir", "", 9.6); self.set_text_color(*INK)
                self.multi_cell(qw - 14, 6.2, txt, align="R", **LM)
                self.ln(.6)
        if with_answer:
            self.ln(1)
            self.exp_box(q)
        self.ln(2.5)
        self.set_draw_color(*LINE); self.set_line_width(.15)
        self.line(self.l_margin, self.get_y(), self.l_margin + self.epw, self.get_y())
        self.ln(3)


def intro(pdf, practice=False):
    pdf.add_page()
    pdf.h1("دربارهٔ این مجموعه")
    m = D["meta"]; c = m["counts"]
    pdf.para(
        "این مجموعه حاصل بررسی تک‌تک " + fa(c["source_total"]) + " سؤال فایل «Tafsir (2).pdf» و تطبیق آن‌ها با "
        "جزوهٔ تفسیر موضوعی قرآن (ویژهٔ برادران — محدودهٔ سوره‌های حمد، توحید، عصر و کوثر) است. "
        "از کل سؤالات منبع، " + fa(c["accepted"]) + " سؤال (درس نهم — سورهٔ حمد) در محدودهٔ جزوه قرار داشت: "
        + fa(c["accepted_A"]) + " سؤال «قطعی» (A؛ مستند مستقیم به جزوه) و " + fa(c["accepted_B"]) +
        " سؤال «مفهومی» (B؛ مرتبط با سورهٔ حمد با تکیه بر پاسخنامهٔ منبع). " + fa(c["excluded_C"]) +
        " سؤال دیگر به فصل‌های کتاب تفسیر موضوعی قرآن کریم مربوط بود و خارج از محدودهٔ جزوه است "
        "(فهرست کامل در excluded_questions.csv).")
    pdf.ln(2)
    pdf.note_box("در منبع سؤالات، هیچ سؤالی دربارهٔ سوره‌های توحید، عصر و کوثر وجود ندارد؛ طبق قاعدهٔ "
                 "پروژه هیچ سؤالی ساخته نشده است. برای این سه سوره به خود جزوه مراجعه کنید.",
                 title="پوشش سوره‌ها")
    if practice:
        pdf.note_box("این نسخهٔ تمرینی بدون پاسخ است؛ کلید همهٔ سؤالات در جدول پایانی آمده است.",
                     title="راهنمای استفاده")


def build_bank():
    pdf = PDF("بانک سؤالات تفسیر موضوعی قرآن — ویژهٔ برادران (با پاسخ و توضیح)")
    pdf.cover("نسخهٔ کامل — با پاسخ تشریحی و ارجاع به جزوه")
    intro(pdf)
    topics = []
    for q in QS:
        if q["topic"] not in topics: topics.append(q["topic"])
    pdf.add_page()
    pdf.h1("سورهٔ حمد — " + fa(len(QS)) + " سؤال به تفکیک مباحث جزوه")
    n = 0
    for t in topics:
        sub = [q for q in QS if q["topic"] == t]
        pdf.h2(t + " — " + fa(len(sub)) + " سؤال")
        for q in sub:
            n += 1
            pdf.question(q, n, with_answer=True)
    out = os.path.join(ROOT, "pdf", "Tafsir_Mozooei_Brothers_Question_Bank.pdf")
    pdf.output(out); print(out, pdf.page_no(), "pages")


def build_practice():
    pdf = PDF("آزمون تمرینی تفسیر موضوعی قرآن — ویژهٔ برادران (بدون پاسخ)")
    pdf.cover("نسخهٔ تمرینی — بدون پاسخ (کلید در پایان)")
    intro(pdf, practice=True)
    pdf.add_page()
    pdf.h1("سؤالات — سورهٔ حمد")
    for i, q in enumerate(QS, 1):
        pdf.question(q, i, with_answer=False)
    pdf.add_page()
    pdf.h1("پاسخنامهٔ کلیدی")
    pdf.set_font("Vazir", "", 9.5)
    cols, rh = 3, 7.5
    rw = pdf.epw / cols
    x0, y0 = pdf.l_margin, pdf.get_y()
    per = (len(QS) + cols - 1) // cols
    for c in range(cols):
        for r in range(per):
            i = c * per + r
            if i >= len(QS): break
            q = QS[i]
            x = x0 + pdf.epw - (c + 1) * rw   # ستون‌ها راست‌به‌چپ
            y = y0 + r * rh
            pdf.set_xy(x, y)
            pdf.set_draw_color(*LINE); pdf.set_line_width(.2)
            pdf.set_text_color(*INK)
            pdf.cell(rw, rh, "سؤال " + fa(i + 1) + ":  گزینهٔ " + q["answer"], align="C", border=1)
    pdf.set_y(y0 + per * rh + 6)
    pdf.note_box("کلیدها مطابق پاسخنامهٔ منبع (Tafsir (2).pdf) و پس از تطبیق با جزوهٔ برادران است. "
                 "توضیح تشریحی هر سؤال در «Tafsir_Mozooei_Brothers_Question_Bank.pdf» آمده است.",
                 title="یادآوری")
    out = os.path.join(ROOT, "pdf", "Tafsir_Practice_Without_Answers.pdf")
    pdf.output(out); print(out, pdf.page_no(), "pages")


if __name__ == "__main__":
    os.makedirs(os.path.join(ROOT, "pdf"), exist_ok=True)
    build_bank(); build_practice()
