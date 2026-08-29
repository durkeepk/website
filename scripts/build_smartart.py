"""Rebuild the Word SmartArt diagrams as accessible SVG.

Pandoc drops SmartArt silently. Label text is recovered from word/diagrams/
data*.xml (see textbook-source/docx-inventory.json) and the layout is taken
from the LibreOffice page renders of the original documents. Wording and
structure follow the source; only the palette is restyled to match the book.

Text is real <text>, never paths, so it is selectable and screen-readable.
No information is carried by colour alone -- every element is labelled.
"""
from __future__ import annotations
import html, pathlib, textwrap

OUT = pathlib.Path("personality/images")
FONT = ("'Source Sans Pro', -apple-system, 'Segoe UI', Roboto, "
        "Helvetica, Arial, sans-serif")
INK, PARENT, CHILD, LINE = "#ffffff", "#0a5c51", "#177a6b", "#8fc7bd"


def wrap(text, width):
    return textwrap.wrap(text, width) or [""]


def tspans(lines, x, y0, lh):
    return "".join(
        f'<tspan x="{x}" y="{y0 + i * lh:.1f}">{html.escape(l)}</tspan>'
        for i, l in enumerate(lines))


def svg(w, h, title, desc, body, slug):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'role="img" aria-labelledby="{slug}-t {slug}-d" width="{w}" height="{h}">\n'
            f'  <title id="{slug}-t">{html.escape(title)}</title>\n'
            f'  <desc id="{slug}-d">{html.escape(desc)}</desc>\n'
            f'  <g font-family="{FONT}" text-anchor="middle">\n{body}  </g>\n</svg>\n')


def box(x, y, w, h, label, fill, fs=15, chars=None, rx=6):
    chars = chars or max(6, int(w / (fs * 0.52)))
    lines = wrap(label, chars)
    lh = fs * 1.22
    y0 = y + h / 2 - (len(lines) - 1) * lh / 2 + fs * 0.35
    return (f'    <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"/>\n'
            f'    <text font-size="{fs}" font-weight="600" fill="{INK}">'
            f'{tspans(lines, x + w / 2, y0, lh)}</text>\n')


def tree(groups, title, desc, slug, bw=150, bh=58, gap=14, colgap=54):
    """Parent box above its children, joined by a bracket."""
    widths = [max(1, len(g[1])) * (bw + gap) - gap for g in groups]
    W = sum(widths) + colgap * (len(groups) - 1) + 40
    H = 200
    b, x = "", 20
    for (parent, kids), gw in zip(groups, widths):
        cx = x + gw / 2
        b += box(cx - bw / 2, 20, bw, bh, parent, PARENT)
        kx = x
        b += (f'    <path d="M {cx} 78 V 96" stroke="{LINE}" stroke-width="2" fill="none"/>\n')
        firstc = kx + bw / 2
        lastc = kx + (len(kids) - 1) * (bw + gap) + bw / 2
        b += (f'    <path d="M {firstc} 96 H {lastc}" stroke="{LINE}" stroke-width="2" fill="none"/>\n')
        for k in kids:
            kcx = kx + bw / 2
            b += f'    <path d="M {kcx} 96 V 116" stroke="{LINE}" stroke-width="2" fill="none"/>\n'
            b += box(kx, 116, bw, bh + 6, k, CHILD, fs=14)
            kx += bw + gap
        x += gw + colgap
    return svg(int(W), H, title, desc, b, slug)


def grid(items, cols, title, desc, slug, bw=176, bh=92, gap=12, fs=13):
    rows = (len(items) + cols - 1) // cols
    W = cols * (bw + gap) - gap + 32
    H = rows * (bh + gap) - gap + 32
    b = ""
    for i, lab in enumerate(items):
        x = 16 + (i % cols) * (bw + gap)
        y = 16 + (i // cols) * (bh + gap)
        b += box(x, y, bw, bh, lab, PARENT if i % 2 == 0 else CHILD, fs=fs)
    return svg(W, H, title, desc, b, slug)


def steps(items, title, desc, slug, bw=300, bh=52, dx=46, dy=62):
    W = bw + dx * (len(items) - 1) + 40
    H = dy * (len(items) - 1) + bh + 40
    shades = ["#0a5c51", "#137062", "#1f8a79"]
    b = ""
    for i, lab in enumerate(items):
        x, y = 20 + i * dx, 20 + i * dy
        b += box(x, y, bw, bh, lab, shades[min(i, len(shades) - 1)], fs=16)
        if i < len(items) - 1:
            ax = x + bw - 26
            b += (f'    <path d="M {ax} {y + bh} l 13 0 l -13 16 l -13 -16 z" '
                  f'fill="{LINE}"/>\n')
    return svg(W, H, title, desc, b, slug)


def statement_pairs(pairs, title, desc, slug, cw=300, fs=14):
    """Two statements side by side -- the Chapter 11 layout.

    The Word original placed a decorative pictogram above each statement. Those
    icons carried no information (the text says everything) and their rights
    were unclear, so they were removed. Each statement now sits in a panel in
    the same palette as the book's other diagrams, so the figure still reads as
    a deliberate diagram rather than stray text.
    """
    wrapped = [wrap(label, 30) for _, label in pairs]
    lines_max = max(len(w) for w in wrapped)
    lh = fs * 1.45
    ph = lines_max * lh + 44
    W, H = cw * len(pairs) + 40, int(ph + 40)
    b = ""
    for i, ((_, _label), lines) in enumerate(zip(pairs, wrapped)):
        x = 20 + i * cw
        b += (f'    <rect x="{x + 8}" y="20" width="{cw - 16}" height="{ph:.0f}" '
              f'rx="8" fill="{PARENT if i % 2 == 0 else CHILD}"/>\n')
        y0 = 20 + ph / 2 - (len(lines) - 1) * lh / 2 + fs * 0.35
        b += (f'    <text font-size="{fs}" font-weight="500" fill="{INK}">'
              f'{tspans(lines, x + cw / 2, y0, lh)}</text>\n')
    return svg(W, H, title, desc, b, slug)


def write(name, content):
    (OUT / name).write_text(content)
    print(f"  {name}  ({len(content)} bytes)")


# --- Chapter 1 -------------------------------------------------------------
write("01-tinbergen-questions.svg", tree(
    [("Ultimate", ["Phylogeny", "Function"]),
     ("Proximate", ["Ontogeny", "Mechanism"])],
    "Tinbergen's four questions",
    "Two hierarchies. Ultimate divides into Phylogeny and Function. "
    "Proximate divides into Ontogeny and Mechanism.",
    "tinbergen"))

write("01-marr-levels.svg", steps(
    ["Computational Level", "Algorithmic Level", "Implementational Level"],
    "Marr's three levels of analysis",
    "Three descending levels: Computational, then Algorithmic, then "
    "Implementational.",
    "marr"))

# --- Chapter 4 -------------------------------------------------------------
write("04-validity-types.svg", tree(
    [("Subjective Assessments", ["Face Validity", "Content Validity"]),
     ("Empirical Assessments",
      ["Predictive Validity", "Concurrent Validity", "Discriminant Validity"])],
    "Types of validity",
    "Subjective assessments comprise face validity and content validity. "
    "Empirical assessments comprise predictive, concurrent and discriminant "
    "validity.",
    "validity"))

# --- Chapter 8 -------------------------------------------------------------
write("08-neuronal-sources.svg", grid([
    "The speed of action potential (myelination)",
    "Amount of neurotransmitters released",
    "Number of receptors available to take up neurotransmitters",
    "Efficiency of postsynaptic receptor uptake",
    "Enzymes available to get rid of excess neurotransmitters",
    "Efficiency of reuptake from presynaptic dendrite",
    "Neurotransmitter production (having more or less)",
    "Size of synaptic cleft (space between neurons)",
    "Synaptic fluid viscosity",
    "Number of close postsynaptic neurons that may accidentally pick up floating neurotransmitters",
    "Size or number of vesicles",
    "…",
], 4,
    "Potential sources of individual differences in neuronal communication",
    "Twelve boxes listing sources of variation in neuronal communication and "
    "computation, the last left open as an ellipsis.",
    "neuronal"))

# --- Chapter 9 -------------------------------------------------------------
write("09-emotion-responses.svg", grid([
    "Goals and motivations", "Information-gathering", "Attention",
    "Concept construal", "Perception", "Memory", "Physiology", "Communication",
], 4,
    "Examples of responses that could be coordinated by emotions",
    "Eight response types: goals and motivations, information-gathering, "
    "attention, concept construal, perception, memory, physiology, "
    "communication.",
    "emoresp", bh=72))

# --- Chapter 11 ------------------------------------------------------------
write("11-cumulative-continuity.svg", statement_pairs([
    (None,
     "Rank order of personality traits becomes more stable throughout development"),
    (None,
     "People who are relatively higher in a trait tend to stay higher, even though people change"),
], "Summary of the cumulative continuity principle",
    "Two points: rank order of traits becomes more stable through development; "
    "people relatively higher in a trait tend to stay higher even as people change.",
    "cumcont"))

write("11-maturation-principle.svg", statement_pairs([
    (None,
     "There is consistency in the average changes in trait levels during development"),
    (None,
     "Most people become more conscientious, agreeable, and emotionally stable with age"),
], "Summary of the personality maturation principle",
    "Two points: average changes in trait levels are consistent during "
    "development; most people become more conscientious, agreeable and "
    "emotionally stable with age.",
    "matur"))
