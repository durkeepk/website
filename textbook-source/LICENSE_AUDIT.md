# License audit

Prepared before any public release under **CC BY 4.0**.

Two distinct categories are kept separate throughout:

1. **The author's own text, tables and diagrams.** Patrick Durkee owns these and
   can license them however he chooses, including CC BY 4.0.
2. **Third-party material incorporated into the book.** The original license
   still governs it. Relicensing the book does not relicense this material, and
   an incompatible third-party license cannot be overridden by the book's own.

Nothing here is a legal opinion. Items marked **unclear** need the author's
confirmation, and in two cases probably a rights-holder's.

---

## Blocking issue

### Chapter 2 — Freud and the neo-Freudians section

The Word source states, at the end of its reference list:

> The sections on Freud and the neo-Freudians a largely reproduced with minor
> changes from associated units of the Open Educational Resources available at
> https://oercommons.org/courseware/unit/8482. The units are published with a
> creative commons license allowing reproduction for **non-commercial purposes**,
> but no authors are listed, so it is not clear how to give a proper citation.

That disclosure survived conversion and is reader-facing. Measured against the
converted chapter, the "Freud and the Neo-Freudians" section is **2,295 words —
56% of Chapter 2's body text**.

This is incompatible with a CC BY 4.0 release of the book as a whole:

- CC BY 4.0 explicitly permits commercial use; an NC license explicitly forbids
  it. A downstream user who relies on the book's CC BY notice would be misled
  about more than half of Chapter 2.
- The chapter page currently carries a "CC BY 4.0" footer while its own text
  says this material is non-commercial-only. The book would be making two
  contradictory claims on the same page.
- The source has **no named authors**, so even correct attribution is difficult,
  and the author says so himself.

This needs resolving before release. It is not something conversion can fix.

---

## Figures

| Ch | Figure | Source / attribution | Rights status | CC BY 4.0 compatible? | Action needed |
|---:|:--|:--|:--|:--|:--|
| 1 | 1.1 Tinbergen's four questions | Author's SmartArt; depicts Tinbergen's framework | Author's own diagram; the framework itself is an idea, not protected expression | Yes | None |
| 1 | 1.2 Marr's three levels | Author's SmartArt; depicts Marr's framework | Author's own diagram | Yes | None |
| 4 | 4.1 Types of validity | Author's SmartArt | Author's own | Yes | None |
| 6 | 6.1 Psychological mechanism | Author's image, no attribution given | Presumed author-created | Presumed yes | Confirm the author drew it |
| 8 | 8.1 Sources of neuronal variation | Author's SmartArt | Author's own | Yes | None |
| 9 | 9.1 Emotions as mechanisms | Same base image as 6.1, no attribution | Presumed author-created | Presumed yes | Confirm the author drew it |
| 9 | 9.2 Responses coordinated by emotions | Author's SmartArt | Author's own | Yes | None |
| 10 | 10.1 Pulley system | **Explicitly labelled public domain** in the caption, with a link to Internet Archive Book Images on Flickr | Public domain | Yes | None; keep the caption's link |
| 10 | 10.2 Maslow's hierarchy | Author's SmartArt; depicts Maslow's model | Author's own diagram of a published model | Yes | None |
| 10 | 10.3 Revised fundamental motives | Author's SmartArt; depicts Kenrick et al. (2010) | Author's own diagram; the underlying figure in Kenrick et al. is separately copyrighted but is not reproduced here | Yes | Consider citing Kenrick et al. in the caption |
| 11 | 11.1 Cumulative continuity | Author's SmartArt **containing stock pictogram icons** | See note below | **Unclear** | Confirm icon rights, or drop the icons |
| 11 | 11.2 Maturation principle | Author's SmartArt **containing stock pictogram icons** | See note below | **Unclear** | Confirm icon rights, or drop the icons |
| 13 | 13.1 Personality change framework | No attribution; prose calls it "one way to think about this process" | Presumed author-created; chapter cites Hudson (2021) and Hudson et al. (2021) nearby | Presumed yes | Confirm it is not adapted from a published figure |

### Note on the Chapter 11 icons

The two Chapter 11 diagrams embed four monochrome pictogram icons (an abacus, a
zigzag, an elevator, a staircase) that came from the SmartArt in the Word file.
They carry no metadata identifying a library, but they are consistent with
Microsoft Office's built-in icon set.

Microsoft's terms generally permit using Office stock content inside documents
you create; they do not clearly permit redistributing that content as part of a
work licensed CC BY 4.0, which grants downstream users the right to extract and
reuse any component.

Mitigating factor: the icons are **decorative only**. They are marked
`aria-hidden="true"`, and the accompanying text carries the entire meaning of
both figures. Removing them would cost nothing substantive.

---

## Tables

| Ch | Table | Source / attribution | Rights status | CC BY 4.0 compatible? | Action needed |
|---:|:--|:--|:--|:--|:--|
| 4 | 4.1 Test-retest reliability | "reproduced from Gnambs (2014)" | Third-party data, attributed | Likely — data are facts, but the selection is reproduced | Confirm reuse; consider "adapted from" |
| 4 | 4.2 Inter-item reliability | The author's own in-class test data | Author's own | Yes | None |
| 4 | 4.3 Self- and peer-rated correlations | The author's own data, 112 students | Author's own | Yes | Confirm students consented to data reuse |
| 4 | 4.4 Traits and reported behaviors | "reproduced from Buss & Botwin (1989)" | Third-party data, attributed | Likely | Confirm reuse |
| 4 | 4.5 HEXACO / Big Five correlations | "reproduced from Lee & Ashton (2004)" | Third-party data, attributed | Likely | Confirm reuse |
| 7 | 7.1 Heritability estimates | "Big Five data from Jang et al. 1996; Honesty-Humility data from Lewis & Bates 2014" | Third-party values, assembled and selected by the author | Likely | None beyond the existing note |
| 9 | 9.1 Adaptive problems, cues, solutions | No source given; illustrative examples | Presumed author-written | Presumed yes | None |
| 10 | 10.1 Motives and Big Five correlations | Caption says "from Neel et al. (2016)" | Third-party data, attributed | Likely | Confirm reuse |
| 10 | 10.2 Fundamental motives questionnaire items | **No attribution on the table.** Items appear to be from the Fundamental Motives Inventory (Neel et al., 2016), cited elsewhere in the chapter | Third-party **expressive text**, not data — a stronger copyright question than a table of numbers | **Unclear** | Attribute the scale explicitly; confirm the items may be reproduced |
| 12 | 12.1 Hofstede's six dimensions | Dimension names are Hofstede's; the descriptions read as the author's own paraphrase | Presumed author-written summary | Presumed yes | Consider citing Hofstede & Bond (1984), already cited in the text |

---

## Reader-facing license statements

| Where | Says | Assessment |
|:--|:--|:--|
| Landing page | CC BY 4.0, with link | Correct for the author's own material |
| Every page footer | "CC BY 4.0" | Correct except on Chapter 2, where it contradicts that chapter's own disclosure |
| Chapter 2 body | Third-party OER is non-commercial only | Accurate, and correctly describes the third party's license, not the book's — but it conflicts with the footer on the same page |
| Chapter 1 Word footer | "CC-BY-NC" | **Did not survive conversion.** Pandoc drops headers and footers, so no stray NC claim reaches the rendered book |

Only Chapter 1's Word file carries the CC-BY-NC footer; the other twelve
sources carry only a page number. (An earlier note in `EDITORIAL_NOTES.md`
said every source carried it — that was wrong and has been corrected.)

---

## Summary

- **1 blocking item**: Chapter 2's NC-licensed OER material, 56% of that chapter.
- **2 unclear items**: the Chapter 11 stock icons, and the Chapter 10
  questionnaire items.
- **3 to confirm with the author**: whether he drew Figures 6.1/9.1 and 13.1,
  and whether the Chapter 4 student data may be published.
- **5 third-party data tables** reproduced with attribution — normal practice
  for an OER, but worth a deliberate decision rather than an assumption.
- Everything else is the author's own work and can be released under CC BY 4.0.
