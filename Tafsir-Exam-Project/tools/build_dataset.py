# -*- coding: utf-8 -*-
"""ساخت data/questions.json و reports/excluded_questions.csv از:
- /tmp/bank_raw.json (استخراج کامل ۲۷۰ سؤال منبع — خروجی tools/extract_source.py)
- curated_hamd.py (۳۰ سؤال پذیرفته‌شدهٔ درس نهم با توضیح و ارجاع)
+ کنترل کیفی: تطبیق کلید هر سؤال پذیرفته‌شده با پاسخنامهٔ منبع.
"""
import json, csv, os, sys, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from curated_hamd import QUESTIONS

raw = json.load(open("/tmp/bank_raw.json", encoding="utf-8"))
lessons, keys = raw["lessons"], raw["keys"]

ORD = ["اول", "دوم", "سوم", "چهارم", "پنجم", "ششم", "هفتم", "هشتم", "نهم"]
TOPIC = {
    "اول": "شناخت قرآن کریم", "دوم": "انس با قرآن", "سوم": "سیمای خدا در قرآن (صفات الهی)",
    "چهارم": "اهداف آفرینش", "پنجم": "علم و ارزش انسان در قرآن", "ششم": "بهداشت روان در قرآن",
    "هفتم": "حقوق در قرآن", "هشتم": "تکالیف در قرآن", "نهم": "سورهٔ حمد",
}
NUM = {n: i + 1 for i, n in enumerate(ORD)}

# ---- QC: تطبیق کلیدها و متن سؤالات پذیرفته‌شده با منبع ----
src9 = {it["n"]: it for it in lessons["نهم"]}
key9 = {int(k): v for k, v in keys["نهم"].items()}
errors = []
for q in QUESTIONS:
    n = q["source_qnum"]
    if q["answer"] != key9[n]:
        errors.append(f"کلید سؤال {n}: curated={q['answer']} منبع={key9[n]}")
    if len(q["options"]) != 4:
        errors.append(f"سؤال {n}: تعداد گزینه‌ها {len(q['options'])}")
    if q["source_page"] != src9[n]["page"]:
        errors.append(f"سؤال {n}: صفحهٔ منبع {q['source_page']} != {src9[n]['page']}")
if errors:
    print("\n".join(errors)); sys.exit(1)

# ---- excluded_questions.csv (درس‌های ۱ تا ۸ → دسته C) ----
os.makedirs(os.path.join(ROOT, "reports"), exist_ok=True)
csv_path = os.path.join(ROOT, "reports", "excluded_questions.csv")
n_excluded = 0
with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(["ردیف", "درس", "موضوع درس در منبع", "شمارهٔ سؤال", "صفحهٔ منبع",
                "متن سؤال (خلاصه)", "کلید پاسخنامهٔ منبع", "دسته", "علت حذف"])
    row = 0
    for name in ORD[:8]:
        for it in sorted(lessons[name], key=lambda x: x["n"]):
            row += 1; n_excluded += 1
            k = keys[name].get(str(it["n"]), keys[name].get(it["n"], ""))
            note = "" if k else " (کلید این سؤال در پاسخنامهٔ منبع نیامده است)"
            w.writerow([row, f"درس {NUM[name]}", TOPIC[name], it["n"], it["page"],
                        it["q"][:120], k or "—", "C",
                        f"موضوع سؤال «{TOPIC[name]}» از فصل‌های کتاب تفسیر موضوعی قرآن کریم است و در جزوهٔ برادران "
                        f"(محدودهٔ چهار سورهٔ حمد، توحید، عصر و کوثر) مطرح نشده است.{note}"])

# ---- questions.json ----
accepted = QUESTIONS
nA = sum(1 for q in accepted if q["category"] == "A")
nB = sum(1 for q in accepted if q["category"] == "B")
data = {
    "meta": {
        "title": "بانک سؤالات تفسیر موضوعی قرآن — ویژهٔ برادران",
        "version": "1.0",
        "generated": str(datetime.date.today()),
        "source": "Tafsir (2).pdf — نمونه سوالات تستی کتاب تفسیر موضوعی قرآن کریم (۲۷۰ سؤال، ۹ درس)",
        "booklet": "جزوهٔ تفسیر موضوعی قرآن (ویژهٔ برادران) — بر اساس تفسیر نور",
        "scope": ["حمد", "توحید", "عصر", "کوثر"],
        "counts": {
            "source_total": 270, "accepted": len(accepted), "accepted_A": nA,
            "accepted_B": nB, "excluded_C": n_excluded, "duplicates": 0, "fabricated": 0,
        },
        "suras": [
            {"name": "حمد", "count": len(accepted), "note": ""},
            {"name": "توحید", "count": 0, "note": "در منبع Tafsir (2).pdf هیچ سؤالی دربارهٔ سورهٔ توحید وجود ندارد."},
            {"name": "عصر", "count": 0, "note": "در منبع Tafsir (2).pdf هیچ سؤالی دربارهٔ سورهٔ عصر وجود ندارد."},
            {"name": "کوثر", "count": 0, "note": "در منبع Tafsir (2).pdf هیچ سؤالی دربارهٔ سورهٔ کوثر وجود ندارد."},
        ],
    },
    "questions": accepted,
}
os.makedirs(os.path.join(ROOT, "data"), exist_ok=True)
with open(os.path.join(ROOT, "data", "questions.json"), "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=1)

total = len(accepted) + n_excluded
print(f"OK — پذیرفته: {len(accepted)} (A={nA}, B={nB}) | حذف‌شده C: {n_excluded} | جمع: {total} / منبع: 270")
assert total == 270
