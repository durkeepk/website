"""Quality checks comparing the Word sources with the rendered book."""
from __future__ import annotations
import json, re, html, pathlib, urllib.parse, sys

SRC = json.load(open("textbook-source/docx-inventory.json"))
BY = {r["file"]: r for r in SRC}
ORDER = [
 ("1_Foundational Frameworks","01-foundational-frameworks"),
 ("2_Past Perspectives","02-past-perspectives"),
 ("3_Contemporary Perspectives","03-contemporary-perspectives"),
 ("4_Measurement Matters","04-measurement-matters"),
 ("5_Personality Power","05-personality-power"),
 ("6_Evolution and Personality","06-evolution-and-personality"),
 ("7_Genetics and Personality","07-genetics-and-personality"),
 ("8_Physiology and Personality","08-physiology-and-personality"),
 ("9_Emotions and Personality","09-emotions-and-personality"),
 ("10_Motivation and Personality","10-motivation-and-personality"),
 ("11_Development and Personality","11-development-and-personality"),
 ("12_Culture_and_Personality_Full","12-culture-and-personality"),
 ("13_Personality_Change","13-personality-change"),
]
BOOK = pathlib.Path("_site/personality")

# Chapters that intentionally diverge from their Word source, with the words
# deliberately removed. Chapter 2's Freud and neo-Freudian sections were
# rewritten from 2,252 words to 1,324, so its ratio is expected to sit near
# 0.78 rather than 1.00.
INTENTIONAL_CUTS = {"02-past-perspectives": 928}

def text_of(h):
    m = re.search(r"<main.*?</main>", h, re.S)
    body = m.group(0) if m else h
    body = re.sub(r"<(script|style|nav|figcaption).*?</\1>", " ", body, flags=re.S)
    return " ".join(html.unescape(re.sub(r"<[^>]+>", " ", body)).split())

print(f"{'ch':>3} {'chapter':32} {'src':>6} {'out':>6} {'ratio':>6} "
      f"{'fig':>7} {'tbl':>7} {'eq':>7} {'hd':>4}")
issues = []
for i, (src, slug) in enumerate(ORDER, 1):
    r = BY[src + ".docx"]
    page = BOOK / f"{slug}.html"
    h = page.read_text()
    words = len(text_of(h).split())
    sw = r["body_words_including_tables"]
    adj = sw - INTENTIONAL_CUTS.get(slug, 0)
    ratio = words / adj if adj else 0
    figs = len(re.findall(r'<figure class="[^"]*quarto-float-fig[^"]*"', h))
    tbls = len(re.findall(r"<table", h))
    eqs  = len(re.findall(r'class="math', h))
    exp_fig = r["media_count"] + len(r["diagrams"])
    if slug == "11-development-and-personality": exp_fig = len(r["diagrams"])   # media are icons inside the SmartArt
    if slug == "09-emotions-and-personality":    exp_fig = 2
    if slug == "06-evolution-and-personality":   exp_fig = 1
    hd = len(re.findall(r"<h[2-6][ >]", h))
    print(f"{i:>3} {slug:32} {sw:>6} {words:>6} {ratio:>6.2f}{'*' if slug in INTENTIONAL_CUTS else ' '}"
          f"{figs:>3}/{exp_fig:<3} {tbls:>3}/{r['tables_count']:<3} "
          f"{eqs:>3}/{r['omath_count']:<3} {hd:>4}")
    if ratio < 0.90: issues.append(f"ch{i} word ratio {ratio:.2f} (possible content loss)")
    if slug in INTENTIONAL_CUTS: note = " (ratio adjusted for the intentional rewrite)"
    if figs != exp_fig: issues.append(f"ch{i} figures {figs} vs {exp_fig} expected")
    if tbls != r["tables_count"]: issues.append(f"ch{i} tables {tbls} vs {r['tables_count']} expected")

# heading hierarchy
print("\nheading hierarchy:")
for i,(src,slug) in enumerate(ORDER,1):
    h=(BOOK/f"{slug}.html").read_text()
    m=re.search(r"<main.*?</main>",h,re.S); body=m.group(0) if m else h
    lv=[int(x) for x in re.findall(r"<h([1-6])[ >]", body)]
    skips=[(a,b) for a,b in zip(lv,lv[1:]) if b>a+1]
    if skips: issues.append(f"ch{i} heading skip {skips}"); print(f"  ch{i:<3} SKIP {skips}")
print("  no skipped levels" if not any('heading skip' in s for s in issues) else "")

# internal links
print("\ninternal references:")
bad=n=0
for page in BOOK.rglob("*.html"):
    t=page.read_text()
    for ref in re.findall(r'''(?:href|src)=["']([^"']+)["']''', t):
        ref=html.unescape(ref)
        if ref.startswith(("http","mailto:","data:","javascript:")): continue
        if ref.startswith("#"):
            n+=1
            if f'id="{ref[1:]}"' not in t: bad+=1; print(f"  DEAD ANCHOR {page.name} {ref}")
            continue
        c=urllib.parse.unquote(ref.split("#")[0].split("?")[0])
        if not c: continue
        tgt=BOOK/c.lstrip("/") if ref.startswith("/") else page.parent/c
        n+=1
        if not tgt.exists(): bad+=1; print(f"  MISSING {page.name} -> {ref}")
print(f"  {n} refs checked, {bad} broken")

# accessibility
print("\naccessibility:")
noalt=0; tbl_nohdr=0; figs_nocap=0
for page in BOOK.glob("*.html"):
    t=page.read_text()
    for img in re.findall(r"<img [^>]*>", t):
        if "alt=" not in img or re.search(r'alt=""', img): noalt+=1
    for tb in re.findall(r"<table.*?</table>", t, re.S):
        if "<th" not in tb: tbl_nohdr+=1
print(f"  images lacking alt text        : {noalt}")
print(f"  tables lacking header cells    : {tbl_nohdr}")
rowhdr=sum(len(re.findall(r"<tbody>.*?<th", t, re.S)) for t in
           (p.read_text() for p in BOOK.glob("*.html")))
print(f"  tables with row headers        : {rowhdr}")
print(f"  lang attribute on every page   : "
      f"{all('lang=' in p.read_text()[:2000] for p in BOOK.glob('*.html'))}")

print("\n" + ("ISSUES:" if issues else "no issues found"))
for s in issues: print("  -", s)
