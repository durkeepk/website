# Word → Quarto conversion notes

Established while converting Module 10 (`10_Motivation and Personality.docx`).
These are the rules to apply to the remaining modules.

## Source rules

- `textbook-source/word/*.docx` are **immutable originals**. Never edit or
  overwrite them; re-export from Word into this folder if a source changes.
- `12_Culture_and_Personality_Full.docx` is the canonical Module 12.
  `12_Culture.docx` is a shorter earlier draft, kept for provenance only.

## Extraction command

```bash
pandoc "textbook-source/word/NN_Name.docx" \
  -f docx+styles -t markdown-simple_tables-multiline_tables+pipe_tables \
  --wrap=none --extract-media=/tmp/conv -o /tmp/conv/NN.md
```

Pandoc output is a **starting point, never the finished chapter**. Every item
below needed hand repair in Module 10.

## Repairs that were needed every time

| Pandoc output | Fix |
|---|---|
| Word `Heading 1` → `#` | Shift all headings down one level (`#`→`##`) — the chapter `title:` is the page `<h1>` |
| `::: {custom-style="caption"}` paragraphs | Delete; move the text into the figure/table caption |
| `[term]{custom-style="Heading 3 Char"}` | A character style used for emphasis, not a heading. Convert to `**strong**` |
| Table caption emitted as `: .` | Word's `SEQ` auto-numbering does not survive. Re-add caption text; let Quarto number |
| Image glued to the following paragraph | Split into its own block with `{#fig-... fig-alt="..."}` |
| Footnote wrapped in `custom-style` divs | Flatten to a plain `[^1]:` footnote |
| `\'` escapes (`one\'s`) | Replace with a plain apostrophe |
| Bold starting mid-number (`.**17\***`) | Word formatting slip. Bold the whole value: `**.17\***` |

## Figures

1. Prefer the raster embedded in the `.docx` (`word/media/`), extracted with
   `--extract-media`, renamed `NN-descriptive-name.ext`.
2. **SmartArt does not extract.** Pandoc silently emits nothing. Check for
   `word/diagrams/data*.xml` in the `.docx` — if present, that figure is
   missing from the conversion and must be handled deliberately. The label text
   can be recovered from `<a:t>` elements in `data*.xml`.
3. Diagrams rebuilt as hand-authored SVG live in `personality/images/`. Keep
   them editable text, not binary, and reuse the existing palette.

Every figure needs a caption, `fig-alt`, and a `#fig-` id. Alt text should
convey the figure's content, not merely name it.

## Tables

- Use markdown pipe tables with the native caption syntax, which produces a
  real table Quarto can cross-reference:

  ```
  | A | B |
  |:--|:--|
  | 1 | 2 |

  : Caption text {#tbl-some-id}
  ```

- `personality/row-headers.lua` promotes the first column of every table to
  row headers (`<th>`), so screen readers announce row context. Opt a table out
  with `{.no-row-headers}`.
- Do not simplify a table to make it convert. Flag it instead.

## Citations

Citations in the Word sources are **plain text** — no Word citation fields, no
Zotero/Mendeley field codes, no bibliography database. References are typed
manually at the end of each module.

For now they are preserved verbatim under a `## References` heading. Do not
invent citation keys, DOIs, or metadata. See the report for what a real
`.bib` migration would require.

## Checks before calling a chapter done

- Heading hierarchy has no skipped levels.
- Every figure has alt text; every table has a caption and header cells.
- All `@fig-`/`@tbl-` cross-references resolve.
- Word count is close to the original (large drops mean content was lost).
- Typos and grammatical slips in the original are **preserved**, not corrected.

---

# Lessons from converting the remaining twelve chapters

The Chapter 10 prototype established the shape of the work. Converting the rest
surfaced these additional rules.

## Run the inventory first, always

`scripts/inventory_docx.py` reads the `.docx` XML directly and reports what
pandoc will and will not carry across. Run it before converting anything:

```bash
./.venv/bin/python scripts/inventory_docx.py "textbook-source/word/"*.docx \
  > textbook-source/docx-inventory.json
```

It needs `lxml` (it uses lxml-only XPath such as `count()`), which the macOS
system Python lacks — hence the gitignored `.venv`.

## SmartArt is everywhere, and pandoc drops all of it

Nine SmartArt diagrams across six chapters (1, 4, 8, 9, 10, 11). Pandoc emits
**nothing** for them — no warning, no placeholder. The only reliable detection
is `word/diagrams/data*.xml` inside the archive, which the inventory reports.

Recovery procedure:

1. Take the label text from `<a:t>` elements (already in the inventory JSON).
2. Take the *layout* from a page render of the original — never guess it.
3. Rebuild with `scripts/build_smartart.py` so every diagram shares one visual
   language and real `<text>` (not paths).

Rendering the sources to page images is what makes step 2 possible:

```bash
soffice --headless --convert-to pdf --outdir <dir> "<chapter>.docx"
```

## Caption divs mark where a dropped figure belonged

Even when the image itself is lost, `::: {custom-style="caption"}` survives and
sits at the figure's position. The normalizer replaces each with a
`<!--FIGURE-CAPTION-->` marker, so a dropped figure leaves a visible slot rather
than disappearing silently. Word's `SEQ` numbering does not survive, so captions
arrive as `. Some text` or `*Figure 1.* Some text` — strip the remnant and let
Quarto number.

## EMF figures contain a decodable bitmap

Chapter 13's figure is an EMF that neither pandoc nor LibreOffice would render
(LibreOffice produced a blank area; converting to SVG turned text into paths).
The EMF+ `Object` record holds a plain bitmap that can be read directly:

- EMF+ record header is **12 bytes** (Type, Flags, Size, DataSize).
- `EmfPlusImage` then gives Version, Type (1 = bitmap), then Width, Height,
  Stride, PixelFormat, BitmapType.
- With `BitmapType == 0` the pixels are raw BGRA — read them with
  `Image.frombuffer(..., "raw", "BGRA", stride, 1)`.

Composite onto white afterwards, or transparent regions come out black.

## Media inside a .docx is not necessarily a figure

Chapter 11 has eight media files but only two figures: the images are the
decorative *icons inside* its SmartArt, not standalone graphics. Conversely
Chapters 6 and 9 share one byte-identical image, which Word **crops
differently** in each chapter — Chapter 6 shows only the mechanism, Chapter 9
keeps the "Emotion system" brace. Crop is stored in the drawing properties, not
the media, so compare against the page render before assuming one image means
one figure.

## Word lists arrive as fenced divs

Ordered lists come through as `(N) ::: {custom-style="List Paragraph"}` with the
item text indented beneath and a closing `:::`. Handle these *before* any
generic `:::` cleanup, or the closing fence is stripped first and the list
collapses into one item.

## Bold in a table is often meaningful — check before removing

Arbitrary bolding is usually formatting noise, but not always:

- Chapter 4's bolded cells are exactly the convergent-validity diagonal, and the
  prose says so.
- Chapter 10's bolding tracks |r| ≥ .10 in 46 of 50 cells.

Test the pattern against the data before stripping. Bold that spells something
out is also meaningful: Chapter 3 writes `**E**motionality`, `e**X**traversion`,
`**H**onesty-Humility` to spell HEXACO.

Watch for a body row where *every* cell is bold — that is a header row Word
faked with formatting, and it should become a real header row.

## Equations convert cleanly

All twelve OMML equations (eleven in Chapter 7, one in Chapter 1) became proper
LaTeX with no manual repair. Two cautions:

- Word bolds display math; `\mathbf{h}^{\mathbf{2}}` is formatting, not
  notation. Strip it.
- Display math inside a table cell (`$$…$$`) should be inline `$…$`.
- When trimming whitespace inside `$…$`, only trim *inside* the delimiters.
  Trimming around them silently welds math to adjacent words
  (`reliability$h^{2}$estimates`).

## Footnotes attached to the chapter title are orphaned

Quarto takes the title from YAML, where a footnote marker cannot live, so such a
footnote is defined but never referenced and pandoc warns. Reattach it to a
sensible place in the body and record the move in `EDITORIAL_NOTES.md`.

## "References" is plain text

No chapter styles its reference heading as a heading. Promote the bare line to
`## References` so it appears in the table of contents. Do this *after* any
terminology pass, and never run text substitutions over the reference list —
Chapter 9 cites a paper titled "toward an evolved **module** of fear", which a
naive module→chapter replacement would corrupt.

## Verify, don't assume

`scripts/qa_book.py` compares the rendered book against the inventory: word
counts, figure counts, table counts, equation counts, heading hierarchy, broken
links and accessibility. Word-count ratios should sit near 1.00; anything below
0.90 means content went missing.
