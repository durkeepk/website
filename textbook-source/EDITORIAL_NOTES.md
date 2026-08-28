# Editorial notes

Matters that need the author's judgement. Obvious typos corrected during
conversion are **not** listed here — see `CONVERSION.md` for the fixes applied
mechanically. Everything below was left as found in the Word sources.

## Licence discrepancy — needs a decision

Every page of every Word source carries a **CC-BY-NC** footer. The book is
being published under **CC BY 4.0**, which drops the NonCommercial restriction.
As the copyright holder you can relicense freely, but the source documents and
any copies already distributed to students still say NC. Worth deciding whether
to re-export the Word files so the two agree.

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

## Mobile header overflows slightly

Every page scrolls about 13px horizontally on a 375px-wide viewport. The cause
is Quarto's own fixed mobile header, not the book's content, and it predates
this review. Table 12.1 is not involved — it scrolls within its own container,
as wide tables should. Left alone as a framework matter.
