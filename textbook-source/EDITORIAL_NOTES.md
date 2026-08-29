# Editorial notes

Matters that need the author's judgement. Obvious typos corrected during
conversion are **not** listed here — see `CONVERSION.md` for the fixes applied
mechanically. Everything below was left as found in the Word sources.

## Licence — settled

The book is released under **CC BY-NC 4.0** (Attribution-NonCommercial 4.0
International). You retain copyright and may separately sell the book, license
a commercial edition, or grant a publisher commercial rights.

**Chapter 1's** Word file carries a CC-BY-NC footer; the other twelve sources
carry only a page number. (An earlier version of this note said every source
carried the footer; that was wrong.) Pandoc drops headers and footers, so it
never reaches the rendered book — but Chapter 1's source document and any
copies already given to students still show it, which now happens to agree with
the book's licence.

Chapter 2's OER source was checked directly and is **CC BY 4.0** — no
NonCommercial, no ShareAlike — not the non-commercial licence the source
document described. See `LICENSE_AUDIT.md`. The chapter's attribution note has
been corrected accordingly. This is no longer a blocker.

## Unexplained notation in tables

Several tables use notation that is never defined:

- **Chapter 10, Table 10.1** (fundamental motives × Big Five). Values carry an
  asterisk, and some are bold. There is no legend for either. The bolding is
  *almost* systematic — bold marks |r| ≥ .10 in 46 of 50 cells — with four
  exceptions: `-.08*` is bold though below the threshold, and `.12*`, `.23*`
  and `.19*` are not bold though above it. Both the convention and the four
  exceptions need confirming; the table then needs a note explaining the
  asterisk and the bolding.
- **Chapter 7, Table 7.1** (heritability estimates). No note explains the
  source or the range of estimates given.

Bolding was preserved wherever it appeared systematic. In Chapter 4 the bolded
cells are the convergent-validity diagonal and the prose says so explicitly, so
that bolding is clearly meaningful.

## Chapter 6 has no reference list

Chapter 6 (Evolution and Personality) cites work in the text but ends without a
References section. Every other chapter has one. Either the list was never
written or it was lost before the file reached this conversion.

## Chapter 4's title footnote

The footnote crediting the chapter's name ("shamelessly borrowed from…") was
attached to the chapter title in Word. Quarto takes the title from YAML, where
a footnote marker cannot live, so it is now attached to the first paragraph
instead. Move it if you would rather it sat elsewhere.

## Spelling and style inconsistencies left alone

These are internal inconsistencies rather than clear errors, so they were not
changed:

- **Chapter 2** uses both `humorism` (3×) and `humourism` (2×), plus
  `humourous` (1×) — American and British spellings mixed in one chapter.
- **Chapter 7** uses both `non-shared` (23×) and `nonshared` (3×).
- **Chapter 5** uses `synthetize`, a rare variant of `synthesize`.

## Chapter 1's numbered algorithm

The six-step algorithm for pessimism lost its step numbering in Word: step (5)
had no number of its own and its text sat inside step (4)'s block. The steps
have been renumbered 1–6 in reading order. Worth checking that the intended
step boundaries match.

## SmartArt wording carried over verbatim

The rebuilt Chapter 8 diagram reproduces the source labels, in which four words
were misspelled: *mylenation*, *Neurotrasnmitter*, *nearons* and
*accidentially*. These were corrected in the rebuilt figure
(*myelination*, *Neurotransmitter*, *neurons*, *accidentally*). Flagged here
because the correction is to a figure rather than to prose.

## Heading structure

Two chapters skipped a heading level in the source and were adjusted so the
hierarchy is continuous:

- **Chapter 5**: "Aside: prediction versus (causal) explanation" was a level-4
  heading directly under a level-2; it is now level 3.
- **Chapter 8**: "brain structure" and "Brain Activity" were level-5 headings
  under a level-3; they are now level 4.

Chapter 8's headings also contained obvious slips that were corrected:
*BRains*, *actIvity*, *conlcusions*.

## Chapter 11's flat structure

Chapter 11 is the shortest chapter (about 1,800 words) and has only five
headings, none below level 3. That is how the source reads; no structure was
invented. It may simply warrant more development.

## References are still plain text

No bibliography database exists — citations are typed by hand. 103 reference
entries across 12 chapters, with no duplicates between chapters. A proper
BibTeX migration is deliberately out of scope for now, and no DOIs, citation
keys or publication metadata have been invented.

---

# Found during the contents and table review

## Two headings look unfinished in the Word source

Both are faithful conversions — the text is incomplete in the originals, so
completing them would mean inventing words:

- **Chapter 1**, heading 2: "Ultimate versus Proximate and Tinbergen's Four".
  It reads as though a noun is missing (Questions?).
- **Chapter 2**, heading 4: "Carl Jung: Archetypes, Attitudes," ended with a
  comma in the source, suggesting a third item was intended. The stray comma
  has been removed; the possibly-missing item has not been supplied.

## Chapter titles differ from the Word document titles

Two chapters carry a different title in the source document than the name used
in the book. The book follows the chapter list you specified:

| Book | Word document title |
|:--|:--|
| Past Perspectives | Past Perspectives on Personality |
| Development and Personality | Personality Development |

Worth confirming which you want to appear in the finished book.

## Headings were normalised to title case

Section headings in the sources mixed sentence case and title case, sometimes
within a single chapter, and character-level styling had left slips such as
"BRains", "actIvity", "intra-sexual" and "Neo-freudians". All headings are now
title case, with acronyms (GWAS, HEXACO), proper nouns and deliberate notation
("What the #@%! Is a Psychological Mechanism?") preserved. Chapter 2's
"humourous humorism" became "Humorous Humorism" — *humourous* is a misspelling
in British and American English alike; the wordplay is unchanged.

## Mobile header overflows slightly — confirmed, and left alone

Pages scroll a little horizontally on a 375px-wide viewport: about 13px on a
text-only chapter, 2px on Chapter 12. Measured directly in the browser at that
width, the diagnosis holds:

- The `<main>` content fits the viewport (right edge 348px of 375px).
- Table 12.1 scrolls inside its own container, and that container fits.
- Every element inside `<main>` that exceeds the viewport is a descendant of
  that scroll container, which is exactly how a wide table should behave.
- The only genuine offenders sit outside `<main>`: Quarto's own
  `header.headroom.fixed-top`, `nav.quarto-secondary-nav`, and
  `div.quarto-sidebar-collapse-item`.

This is framework chrome, not book content, and it is cosmetic. Deliberately
not patched — a CSS override targeting Quarto's internal header classes would
be brittle across Quarto upgrades for a few pixels of gain.


---

# Found during the Chapter 2 rewrite

## Chapter 2's psychodynamic sections were rewritten

The Freud and neo-Freudian sections were rewritten in fresh prose, from 2,252
words to roughly 1,300. Concepts retained: unconscious motivation, id/ego/
superego and the conflict between them, defense mechanisms, the psychosexual
stages and fixation, the Oedipus complex, Freud's evidentiary problem, and
Adler's, Horney's and Jung's departures from him. The five separate stage
subsections were collapsed into one compact treatment.

Chapter 10 refers back to this material — Freud on libido, Horney on belonging
and security, Adler on superiority — and all three claims are preserved.

## An orphan citation — resolved

Chapter 2 previously cited **Jung & Kerenyi (1963)** with no matching entry in
its reference list, inherited from the source material. The sentence it
supported also misattributed *penis envy* to Jung. That sentence has been
corrected — Jung coined the term *Electra complex*, which Freud never adopted;
penis envy is Freud's own concept — and the revised sentence makes a plain
attributional claim that needs no citation at this level. The citation was
removed rather than completed, so no bibliographic details were invented.
