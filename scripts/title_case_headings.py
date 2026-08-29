"""Normalise section headings to title case.

Word headings mixed sentence case and title case, sometimes within one chapter,
and character-level styling left slips like "BRains" and "intra-sexual".
Acronyms, proper nouns and deliberate notation are protected.
"""
from __future__ import annotations
import re, sys, pathlib

# words left lowercase unless first or last, or following a colon
MINOR = {"a","an","the","and","but","or","nor","for","yet","so","as","at","by",
         "in","of","on","to","via","off","per","from","into","onto","over",
         "with","than","upon","versus","vs.","vs"}

# tokens reproduced exactly: acronyms, proper nouns, notation
PROTECT = {
 "GWAS","HEXACO","DNA","RNA","SNP","SNPs","MBTI","IRV","IRVs","fMRI","EEG","MEG",
 "IQ","CC","BY","MZ","DZ","5-HTTLPR","COMT","MAOA","#@%!","(?)","(GWAS)",
 "Tinbergen's","Darwin's","Freud's","Maslow's","Mischel's","Allport's","Cattell's",
 "Falconer's","Horney's","Jung's","Adler's","Hofstede's","McCrae","Costa","Goldberg",
 "Neo-Freudians","Neo-Freudian","Tsimane","Big","Five","Little","Six","Likert",
 "Alfred","Adler:","Karen","Horney:","Carl","Jung:","Walter","Freud","Jung","Adler",
 "Horney","Erikson","Rogers","Skinner","Pavlov","Bandura","Piaget","Mischel",
 "Hofstede","Allport","Cattell","Ashton","Lee","WEIRD",
}

def cap(word: str) -> str:
    if not word:
        return word
    # keep anything that already carries internal capitals or is protected
    if word in PROTECT or (any(c.isupper() for c in word[1:]) and word.upper() == word):
        return word
    if any(c.isupper() for c in word[1:]):
        return word
    lead = re.match(r"^\W*", word).group(0)
    tail = re.search(r"\W*$", word).group(0)
    core = word[len(lead): len(word) - len(tail) if tail else None]
    if not core:
        return word
    if "-" in core:                       # hyphenated compound
        parts = core.split("-")
        core = "-".join(p if p in PROTECT else
                        (p[:1].upper() + p[1:] if p.lower() not in MINOR or i == 0 else p.lower())
                        for i, p in enumerate(parts))
    else:
        core = core[:1].upper() + core[1:]
    return lead + core + tail

def title_case(text: str) -> str:
    words = text.split(" ")
    out, force_next = [], True
    for i, w in enumerate(words):
        bare = re.sub(r"^\W+|\W+$", "", w).lower()
        last = (i == len(words) - 1)
        if w in PROTECT:
            out.append(w)
        elif force_next or last or bare not in MINOR:
            out.append(cap(w))
        else:
            # already-capitalised proper nouns keep their case
            out.append(w if any(c.isupper() for c in w[1:]) else w.lower())
        force_next = w.endswith(":") or w.endswith("?") or w.endswith("!")
    return " ".join(out)

if __name__ == "__main__":
    apply = "--apply" in sys.argv
    for p in sorted(pathlib.Path("personality").glob("*.qmd")):
        lines = p.read_text().split("\n")
        changed = []
        for i, l in enumerate(lines):
            m = re.match(r"^(#{2,6})(\s+)(.*)$", l)
            if not m:
                continue
            hashes, _, txt = m.groups()
            new = title_case(txt.strip())
            if new != txt or m.group(2) != " ":
                lines[i] = f"{hashes} {new}"
                if new != txt.strip():
                    changed.append((txt, new))
        if changed:
            print(f"--- {p.stem} ---")
            for a, b in changed:
                print(f"    {a}\n  → {b}")
        if apply:
            p.write_text("\n".join(lines))
