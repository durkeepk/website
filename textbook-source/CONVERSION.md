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
