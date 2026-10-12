# -*- coding: utf-8 -*-
"""تزریق data/questions.json در قالب → index.html (تک‌فایل، آفلاین)."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from sanitize_public import public_data
data = public_data(json.load(open(os.path.join(ROOT, "data", "questions.json"), encoding="utf-8")))
tpl = open(os.path.join(HERE, "template.html"), encoding="utf-8").read()
payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
assert "/*__DATA__*/" in tpl
out = tpl.replace("/*__DATA__*/", payload)
open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(out)
print("index.html:", len(out), "bytes")
