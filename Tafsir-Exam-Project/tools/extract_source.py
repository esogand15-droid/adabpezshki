# -*- coding: utf-8 -*-
"""استخراج کامل ۲۷۰ سؤال و پاسخنامه از «Tafsir (2).pdf» (ریشهٔ مخزن) → /tmp/bank_raw.json
نکته: متن استخراجی pdfium دارای آرتیفکت لام‌الف است (مثلاً «سواالت»)؛ متن سؤالات پذیرفته‌شده
به‌صورت دستی در curated_hamd.py پاک‌سازی شده است."""
import re, json, os
import pypdfium2 as pdfium

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
pdf_path = [os.path.join(ROOT, f) for f in os.listdir(ROOT) if f.startswith("Tafsir") and f.endswith(".pdf")][0]
doc = pdfium.PdfDocument(pdf_path)
t = "".join(f"===== PAGE {i+1} =====\n{doc[i].get_textpage().get_text_bounded()}\n" for i in range(len(doc)))
t = t.replace("\r", "")

body = t[t.find("===== PAGE 2 ====="):]
ans_start = body.find("پاسخنامه ها")
marks = [(m.start(), m.group(1)) for m in re.finditer(r"سواالت درس (\S+):", body) if m.start() < ans_start]
bounds = [(nm, p, (marks[k+1][0] if k+1 < len(marks) else ans_start)) for k, (p, nm) in enumerate(marks)]
pages = [(m.start(), int(m.group(1))) for m in re.finditer(r"===== PAGE (\d+) =====", body)]

def pageof(pos):
    last = 1
    for p, n in pages:
        if p <= pos: last = n
        else: break
    return last

lessons = {}
for name, pos, end in bounds:
    seg = body[pos:end]
    sc = re.sub(r"===== PAGE \d+ =====", "", seg)
    sc = re.sub(r"\n\s*\d+\s*\n", "\n", sc)
    qs = re.split(r"\n\s*[-=]?\s*(\d{1,2})\s*[-=]?\s*(?=[^\d\s(])", sc)
    items = []
    for k in range(1, len(qs), 2):
        num, b = int(qs[k]), qs[k+1]
        parts = re.split(r"\n\s*(الف|ب|ج|د)\s*\(", b)
        qtext = parts[0].strip().replace("\n", " ")
        opts = {parts[m]: parts[m+1].strip().replace("\n", " ") for m in range(1, len(parts), 2)}
        items.append({"n": num, "q": qtext, "opts": opts, "page": pageof(pos + seg.find(qtext[:20]))})
    lessons[name] = items

ORD = ["اول","دوم","سوم","چهارم","پنجم","ششم","هفتم","هشتم","نهم"]
keys, aseg = {}, body[ans_start:]
for name in ORD:
    m = re.search(rf"پاسخنامه درس {name}\s*:?\s*\n(.*?)(?=پاسخنامه درس|\Z)", aseg, re.S)
    ans = {}
    for mm in re.finditer(r"-\s*(\d+)\s*(الف|ب|ج|د)|(الف|ب|ج|د)\s*-\s*(\d+)", m.group(1)):
        g = mm.groups()
        ans[int(g[0] or g[3])] = g[1] or g[2]
    keys[name] = ans

json.dump({"lessons": lessons, "keys": keys}, open("/tmp/bank_raw.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("total:", sum(len(v) for v in lessons.values()),
      "| keys:", {n: len(keys[n]) for n in ORD})
