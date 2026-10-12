# -*- coding: utf-8 -*-
"""پاک‌سازی نسخهٔ عمومی: حذف هر ردپایی از منبع سؤالات (Tafsir (2).pdf)،
پاسخنامهٔ منبع و منابع آزمون از داده‌ای که وارد index.html و PDFها می‌شود.
نسخهٔ کامل با ردیابی، در data/questions.json و reports/ باقی می‌ماند.
"""
import copy

# عبارت‌هایی که در متن دلیل/نکته منبع را لو می‌دهند
_TEXT_FIXES = [
    ("بر اساس منبع سؤالات، ", ""),
    ("طبق منبع سؤالات، ", ""),
    ("طبق پاسخنامهٔ منبع، ", ""),
    ("در منبع سؤالات و تفاسیر مشهورند", "در تفاسیر مشهورند"),
    ("منبع آزمون (تفسیر نور): ", "همچنین در تفاسیر آمده است: "),
    ("؛ هم‌سو با درخواست دائمی «اهدنا الصراط المستقیم»", " و با درخواست دائمی «اهدنا الصراط المستقیم» هم‌سوست"),
]

_DROP_Q_KEYS = ["validation", "review_flag", "exam_source", "source_qnum", "source_page"]


def _fix(t):
    for a, b in _TEXT_FIXES:
        t = t.replace(a, b)
    return t


def public_data(d):
    d = copy.deepcopy(d)
    m = d["meta"]
    m.pop("source", None)
    m.pop("counts", None)
    m["title"] = "بانک سؤالات تفسیر موضوعی قرآن — ویژهٔ برادران"
    m["booklet"] = "جزوهٔ تفسیر موضوعی قرآن (ویژهٔ برادران)"
    for s in m.get("suras", []):
        if s["count"] == 0:
            s["note"] = ("برای این سوره فعلاً سؤالی در بانک موجود نیست؛ برای مرور به جزوهٔ "
                         "تفسیر موضوعی (ویژهٔ برادران) مراجعه کنید.")
    for q in d["questions"]:
        for k in _DROP_Q_KEYS:
            q.pop(k, None)
        e = q["explanation"]
        e.pop("source", None)
        e["reason"] = _fix(e["reason"])
        e["booklet_note"] = _fix(e["booklet_note"])
    return d
