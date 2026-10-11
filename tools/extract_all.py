import os, re, olefile
from pdfminer.high_level import extract_text as pdf_text
from pptx import Presentation

SRC = "extracted"; OUT = "text"
os.makedirs(OUT, exist_ok=True)

def ppt_binary_text(path):
    """Extract text records (TextCharsAtom 0x0FA0, TextBytesAtom 0x0FA8) from legacy .ppt"""
    ole = olefile.OleFileIO(path)
    data = ole.openstream('PowerPoint Document').read()
    out, i = [], 0
    while i + 8 <= len(data):
        ver_inst = int.from_bytes(data[i:i+2], 'little')
        rectype = int.from_bytes(data[i+2:i+4], 'little')
        reclen = int.from_bytes(data[i+4:i+8], 'little')
        if rectype == 0x0FA0:  # UTF-16LE
            out.append(data[i+8:i+8+reclen].decode('utf-16-le', 'ignore'))
            i += 8 + reclen
        elif rectype == 0x0FA8:  # ANSI/cp1256
            out.append(data[i+8:i+8+reclen].decode('cp1256', 'ignore'))
            i += 8 + reclen
        elif (ver_inst & 0x0F) == 0x0F:  # container record, descend
            i += 8
        else:
            i += 8 + reclen
    return "\n".join(out)

def pptx_text(path):
    prs = Presentation(path)
    chunks = []
    for idx, slide in enumerate(prs.slides, 1):
        chunks.append(f"\n===== SLIDE {idx} =====")
        for shape in slide.shapes:
            if shape.has_text_frame:
                for para in shape.text_frame.paragraphs:
                    t = "".join(r.text for r in para.runs).strip()
                    if t: chunks.append(t)
            if shape.has_table if hasattr(shape, 'has_table') else False:
                for row in shape.table.rows:
                    chunks.append(" | ".join(c.text for c in row.cells))
    return "\n".join(chunks)

for f in sorted(os.listdir(SRC)):
    p = os.path.join(SRC, f)
    base = re.sub(r'[^\w\u0600-\u06FF-]+', '_', os.path.splitext(f)[0])
    try:
        if f.endswith('.pdf'): txt = pdf_text(p)
        elif f.endswith('.pptx'): txt = pptx_text(p)
        elif f.endswith('.ppt'): txt = ppt_binary_text(p)
        else: continue
        txt = re.sub(r'\n{3,}', '\n\n', txt)
        with open(f"{OUT}/{base}.txt", 'w') as fh: fh.write(txt)
        print(f"{f}: {len(txt)} chars")
    except Exception as e:
        print(f"{f}: FAILED {e}")
