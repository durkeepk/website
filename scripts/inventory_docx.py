from __future__ import annotations

import json
import re
import sys
import zipfile
from collections import Counter
from pathlib import Path

from lxml import etree

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
A = "http://schemas.openxmlformats.org/drawingml/2006/main"
M = "http://schemas.openxmlformats.org/officeDocument/2006/math"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
NS = {"w": W, "a": A, "m": M, "r": R}


def xml(zf: zipfile.ZipFile, name: str):
    try:
        return etree.fromstring(zf.read(name))
    except KeyError:
        return None


def texts(node):
    if node is None:
        return []
    return node.xpath(".//w:t/text()", namespaces=NS)


def para_text(p):
    return "".join(p.xpath(".//w:t/text() | .//w:tab/text()", namespaces=NS))


def inventory(path: Path):
    with zipfile.ZipFile(path) as zf:
        names = set(zf.namelist())
        doc = xml(zf, "word/document.xml")
        styles = xml(zf, "word/styles.xml")
        style_names = {}
        if styles is not None:
            for st in styles.xpath(".//w:style", namespaces=NS):
                sid = st.get(f"{{{W}}}styleId")
                nm = st.find("w:name", NS)
                style_names[sid] = nm.get(f"{{{W}}}val") if nm is not None else sid

        paragraphs = []
        style_counts = Counter()
        headings = []
        for i, p in enumerate(doc.xpath(".//w:body/w:p", namespaces=NS)):
            text = para_text(p).strip()
            ps = p.find("w:pPr/w:pStyle", NS)
            sid = ps.get(f"{{{W}}}val") if ps is not None else None
            sname = style_names.get(sid, sid or "(none)")
            if text:
                paragraphs.append(text)
                style_counts[sname] += 1
            if text and (re.match(r"(?i)^heading\s*\d+$", sname or "") or re.match(r"(?i)^title$", sname or "")):
                headings.append({"index": i, "style": sname, "text": text})

        tables = []
        for ti, tbl in enumerate(doc.xpath(".//w:body/w:tbl", namespaces=NS)):
            rows = []
            for tr in tbl.xpath("./w:tr", namespaces=NS):
                rows.append([" ".join(t.strip() for t in tc.xpath(".//w:t/text()", namespaces=NS) if t.strip()) for tc in tr.xpath("./w:tc", namespaces=NS)])
            tables.append({"index": ti, "rows": len(rows), "cols_max": max((len(r) for r in rows), default=0), "cells": rows})

        media = sorted(n for n in names if n.startswith("word/media/") and not n.endswith("/"))
        diagram_files = sorted(n for n in names if n.startswith("word/diagrams/") and not n.endswith("/"))
        diagrams = []
        for name in diagram_files:
            if "/data" in name and name.endswith(".xml"):
                root = xml(zf, name)
                labels = [x.strip() for x in root.xpath(".//a:t/text()", namespaces=NS) if x.strip()] if root is not None else []
                diagrams.append({"file": name, "labels": labels})

        foot = xml(zf, "word/footnotes.xml")
        end = xml(zf, "word/endnotes.xml")
        footnotes = []
        endnotes = []
        if foot is not None:
            for n in foot.xpath("./w:footnote", namespaces=NS):
                nid = n.get(f"{{{W}}}id")
                if nid not in {"-1", "0"}:
                    footnotes.append({"id": nid, "text": " ".join(texts(n))})
        if end is not None:
            for n in end.xpath("./w:endnote", namespaces=NS):
                nid = n.get(f"{{{W}}}id")
                if nid not in {"-1", "0"}:
                    endnotes.append({"id": nid, "text": " ".join(texts(n))})

        rels = xml(zf, "word/_rels/document.xml.rels")
        links = []
        if rels is not None:
            for rel in rels:
                typ = rel.get("Type", "")
                if typ.endswith("/hyperlink"):
                    links.append(rel.get("Target"))

        drawings = doc.xpath("count(.//w:drawing)", namespaces=NS)
        picts = doc.xpath("count(.//w:pict)", namespaces=NS)
        omath = doc.xpath("count(.//m:oMath)", namespaces=NS)
        omath_para = doc.xpath("count(.//m:oMathPara)", namespaces=NS)
        fields = [x.strip() for x in doc.xpath(".//w:instrText/text()", namespaces=NS) if x.strip()]
        all_text = "\n".join(paragraphs + ["\t".join(cell for row in t["cells"] for cell in row) for t in tables])
        words = re.findall(r"\b[\w’'-]+\b", all_text, flags=re.UNICODE)

        return {
            "file": path.name,
            "size": path.stat().st_size,
            "body_words_including_tables": len(words),
            "paragraphs": len(paragraphs),
            "heading_count": len(headings),
            "headings": headings,
            "style_counts": dict(style_counts.most_common()),
            "tables_count": len(tables),
            "tables": tables,
            "drawings": int(drawings),
            "legacy_picts": int(picts),
            "media_count": len(media),
            "media": media,
            "diagram_file_count": len(diagram_files),
            "diagram_files": diagram_files,
            "diagrams": diagrams,
            "omath_count": int(omath),
            "omath_para_count": int(omath_para),
            "footnotes": footnotes,
            "endnotes": endnotes,
            "hyperlinks": links,
            "fields": fields,
            "headers": sorted(n for n in names if re.match(r"word/header\d+\.xml$", n)),
            "footers": sorted(n for n in names if re.match(r"word/footer\d+\.xml$", n)),
            "comments": "word/comments.xml" in names,
        }


def main():
    paths = [Path(p) for p in sys.argv[1:]]
    print(json.dumps([inventory(p) for p in paths], indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
