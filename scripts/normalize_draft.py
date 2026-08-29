"""Apply the mechanical CONVERSION.md repairs to a pandoc draft.

Pandoc output is a starting point, never a finished chapter. This handles the
repairs that recur in every chapter; figures, table ids, cross-references and
prose judgement are still done by hand afterwards.

Usage: normalize_draft.py <draft.md> <out.qmd> --title "..." [--desc "..."]
"""
from __future__ import annotations
import re, sys, argparse

# Character styles Word applies for inline emphasis. Pandoc renders them as
# spans; left alone they read as stray bracketed text (or, for "Heading N Char",
# get mistaken for headings).
EMPHASIS_STYLES = ("Heading 2 Char", "Heading 3 Char", "Heading 4 Char", "Intense Reference")
# Styles that carry no meaning once converted.
DROP_STYLES = ("Hyperlink", "List Paragraph", "apple-converted-space",
               "footnote text", "footnote reference", "Default Paragraph Font")

def shift_headings(s: str) -> str:
    """Word Heading 1 -> '#'; the chapter title YAML is the page <h1>."""
    return re.sub(r"^(#{1,5}) ", lambda m: "#" * (len(m.group(1)) + 1) + " ", s, flags=re.M)

def pull_captions(s: str):
    """Remove caption divs, returning their text in document order.

    Word's SEQ auto-numbering does not survive conversion, so a caption often
    arrives as '. Some text' or '*Figure 1.* Some text'. Both are normalised to
    the bare caption text; Quarto supplies the number.
    """
    caps = []
    def repl(m):
        body = m.group(1)
        body = re.sub(r"</?p>", "", body)
        body = re.sub(r"\[([^\]]*)\]\{custom-style=\"[^\"]*\"\}", r"\1", body)
        body = " ".join(body.split()).strip()
        body = re.sub(r"^\*?Figure\s*\d*\.?\*?\s*", "", body)   # 'Figure 1.' / '*Figure 1.*'
        body = re.sub(r"^\.\s*", "", body)                       # bare leftover '.'
        body = re.sub(r"^\*+|\*+$", "", body).strip()
        if body:
            caps.append(body)
        return "\n<!--FIGURE-CAPTION-->\n"
    s = re.sub(r'::: \{custom-style="caption"\}\n(.*?)\n:::\n', repl, s, flags=re.S)
    return s, caps

def list_paragraphs(s: str) -> str:
    """Word list items arrive as '(N) ::: {custom-style="List Paragraph"}' with
    the item text indented beneath and a closing ':::'. Rebuild them as a
    markdown ordered list."""
    def repl(m):
        num = m.group(1)
        body = " ".join(l.strip() for l in m.group(2).strip().split("\n")
                        if l.strip() and l.strip() != ":::")
        return f"{num}. {body}\n"
    return re.sub(
        r'^\((\d+)\) ::: \{custom-style="List Paragraph"\}\n((?:[ \t]+.*\n)+)',
        repl, s, flags=re.M)


def flatten_footnotes(s: str) -> str:
    """Unwrap ::: {custom-style="footnote text"} blocks inside footnote bodies."""
    s = re.sub(r'^(\s*)::: \{custom-style="footnote text"\}\n', "", s, flags=re.M)
    s = re.sub(r'^\s*\[\]\{custom-style="footnote reference"\}\s*', "", s, flags=re.M)
    # closing ::: that belonged to a footnote div, indented under a [^n]:
    s = re.sub(r"^(\s{2,}):::\s*$\n?", "", s, flags=re.M)
    return s

def spans(s: str) -> str:
    for st in EMPHASIS_STYLES:                       # emphasis, not structure
        s = re.sub(r'\[([^\]]+)\]\{custom-style="%s"\}' % re.escape(st), r"**\1**", s)
    for st in DROP_STYLES:                           # meaningless after conversion
        s = re.sub(r'\[([^\]]*)\]\{custom-style="%s"\}' % re.escape(st), r"\1", s)
    s = re.sub(r'\[([^\]]*)\]\{custom-style="[^"]*"\}', r"\1", s)   # anything left
    s = re.sub(r'^::: \{custom-style="[^"]*"\}\n', "", s, flags=re.M)
    return s

def math(s: str) -> str:
    """Word bolds math for display; that is formatting, not notation.

    Grid-table lines are left untouched. Their columns are aligned by character
    position, so shortening a cell -- dropping a `\\` hard-break marker, or
    collapsing `$$x$$` to `$x$` -- silently breaks the whole table: pandoc stops
    recognising the grid and merges each row into one cell.
    """
    def is_grid(line):
        return line.startswith(("+-", "+=")) or (line.startswith("|") and line.rstrip().endswith("|"))
    out = []
    for line in s.split("\n"):
        out.append(line if is_grid(line) else _math_line(line))
    return "\n".join(out)


def _math_line(s: str) -> str:
    s = re.sub(r"\\mathbf\{([^{}]*)\}", r"\1", s)
    s = re.sub(r"\\mathbf\s*", "", s)
    s = s.replace(r"\ $", "$").replace(r"\ ", " ")
    s = re.sub(r"\$\$([^$\n]+)\$\$", r"$\1$", s)     # display math inside a table cell
    s = re.sub(r"\$\s+([^$]*?)\s+\$", r"$\1$", s)   # trim inside the delimiters only
    return s

def captions_for_tables(s: str) -> str:
    """'`: . Caption`' -> '`: Caption`'; Quarto numbers it."""
    s = re.sub(r"^:\s*\.\s*", ": ", s, flags=re.M)
    s = re.sub(r"^:\s*Table\s*\d+\.\s*", ": ", s, flags=re.M)
    return s

TYPOS = [
    (r"\bCogntive\b", "Cognitive"), (r"\bmylenation\b", "myelination"),
    (r"\bNeurotrasnmitter\b", "Neurotransmitter"), (r"\bneurotrasnmitter\b", "neurotransmitter"),
    (r"\bpotenial\b", "potential"), (r"\bVemon\b", "Vernon"),
    (r"\bthe the\b", "the"), (r"\ba a\b", "a"), (r"\bof of\b", "of"),
    (r"\bis is\b", "is"), (r"\bto to\b", "to"), (r"\band and\b", "and"),
    (r"\bthat that\b", "that"), (r"\bin in\b", "in"),
    (r"\bFor we example\b", "For example"),
    (r"\bpsychologial\b", "psychological"), (r"\bindivdual\b", "individual"),
    (r"\benviornment\b", "environment"), (r"\bbehaviour?al\b", "behavioral"),
    (r"\bseperate\b", "separate"), (r"\boccured\b", "occurred"),
    (r"\bteh\b", "the"), (r"\brelationsihp\b", "relationship"),
]

def typos(s: str):
    fixed = []
    for pat, rep in TYPOS:
        s, n = re.subn(pat, rep, s)
        if n:
            fixed.append((pat.strip("\\b"), rep, n))
    return s, fixed

def terminology(s: str):
    """'module' -> 'chapter' only where it plainly means a textbook chapter."""
    pats = [
        (r"\b([Tt])his module\b", r"\1his chapter"),
        (r"\b([Ii])n this module\b", r"\1n this chapter"),
        (r"\b([Tt])he last module\b", r"\1he last chapter"),
        (r"\b([Tt])he previous module\b", r"\1he previous chapter"),
        (r"\b([Pp])revious modules\b", r"\1revious chapters"),
        (r"\b([Ll])ater modules\b", r"\1ater chapters"),
        (r"\b([Ee])arlier modules\b", r"\1arlier chapters"),
        (r"\b([Tt])he next module\b", r"\1he next chapter"),
        (r"\bmodule on\b", "chapter on"),
        (r"\b([Tt])hroughout the modules\b", r"\1hroughout the chapters"),
        (r"\bupcoming modules\b", "upcoming chapters"),
    ]
    n_total = 0
    for pat, rep in pats:
        s, n = re.subn(pat, rep, s); n_total += n
    return s, n_total

def cleanup(s: str) -> str:
    s = s.replace("\\'", "'").replace('\\"', '"')
    s = re.sub(r"^:::\s*$\n?", "", s, flags=re.M)          # orphaned fences
    s = re.sub(r"\n{3,}", "\n\n", s)
    s = re.sub(r"[ \t]+$", "", s, flags=re.M)
    return s.strip() + "\n"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src"); ap.add_argument("out")
    ap.add_argument("--title", required=True); ap.add_argument("--desc", default="")
    a = ap.parse_args()
    s = open(a.src).read()

    s = shift_headings(s)
    s, caps = pull_captions(s)
    s = list_paragraphs(s)
    s = flatten_footnotes(s)
    s = spans(s)
    s = math(s)
    s = captions_for_tables(s)
    s, fixed = typos(s)
    s, nterm = terminology(s)
    s = cleanup(s)

    yaml = f'---\ntitle: "{a.title}"\n'
    if a.desc:
        yaml += f'description: "{a.desc}"\n'
    yaml += "---\n\n"
    open(a.out, "w").write(yaml + s)

    print(f"  {a.out}")
    print(f"    captions recovered : {len(caps)}")
    for c in caps:
        print(f"      - {c[:76]}")
    print(f"    module->chapter    : {nterm}")
    if fixed:
        print(f"    typos fixed        : " + ", ".join(f"{p}->{r}({n})" for p, r, n in fixed))

if __name__ == "__main__":
    main()
