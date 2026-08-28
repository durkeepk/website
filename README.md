# pdurkee.com

Personal academic website for Patrick Durkee, built with
[Quarto](https://quarto.org) and deployed to Netlify at
<https://www.pdurkee.com>.

## How it works

```
edit .qmd  →  git commit  →  git push origin master  →  Netlify renders  →  live
```

Netlify renders the Quarto source itself. `netlify.toml` downloads a pinned
Quarto release and runs `quarto render`; the generated `_site/` directory is
**not** committed.

Quarto's documented `@quarto/netlify-plugin-quarto` was tried first and does
not work — it was last published in 2022 and fails resolving releases through
the GitHub API (`HttpError: Not Found`). The explicit download in
`netlify.toml` does the same job deterministically. To upgrade Quarto, bump
`QUARTO_VERSION` in `netlify.toml` and install the matching version locally.

Netlify servers cannot execute R, Python, or Julia. The site is therefore
plain Quarto Markdown with no executable code chunks. If a page ever needs
computation, add `execute: freeze: auto` to `_quarto.yml`, render locally, and
commit the resulting `_freeze/` directory.

## Layout

| Path | What it is |
|---|---|
| `_quarto.yml` | Site config: navbar, theme, metadata |
| `index.qmd` | Home / About |
| `research.qmd` | Publication list |
| `cv.qmd` | CV page (links and embeds the PDF) |
| `styles.scss` / `dark.scss` | Custom theme, layered over Quarto's `cosmo` |
| `images/` | Profile photo and favicon |
| `files/cv/` | Published CV PDFs — `/files/cv/cv.pdf` is a long-standing public URL |
| `files/pubs/` | Publication PDFs — `/files/pubs/*.pdf` are long-standing public URLs |
| `_cv-source/` | CV **source**. Leading `_` means Quarto ignores it, so it is never published |
| `netlify.toml` | Build command (pinned Quarto), legacy-URL redirects, security headers |

## Conventions

PDF links open in a new tab so readers land in the browser's PDF viewer and
can download from there if they want. Nothing on the site forces a download.
When adding a publication, append `{target="_blank"}` to the link:

```markdown
[Title of the paper](files/pubs/Example2026.pdf){target="_blank"}
```

## Working on the site

```bash
quarto preview     # live-reloading local preview
quarto render      # build into _site/
```

Then commit and push to `master`; Netlify does the rest.

## The CV is a separate workflow

The CV is **not** a Quarto document. It is R Markdown → Pandoc → LaTeX, and it
is built by hand, not by the website build.

- `_cv-source/cv.Rmd` — the main CV; produces the published `files/cv/cv.pdf`
- `_cv-source/2page.Rmd` — abbreviated 2-page CV (produced `files/cv/Durkee-shortCV.pdf`)
- `_cv-source/rap-latex-cv.tex` — the Pandoc LaTeX template both use
- `_cv-source/short_cv.Rmd`, `_cv-source/teaching_focused_cv.Rmd` — older variants

To rebuild the published CV:

```r
rmarkdown::render("_cv-source/cv.Rmd", output_file = "cv.pdf")
```

then move the PDF to `files/cv/cv.pdf`, commit, and push. Requires TinyTeX (or
another LaTeX install). `cv.Rmd` contains no R code chunks — only an inline
`` `r format(Sys.time(), '%B, %Y')` `` for the date — so knitr is doing very
little work here.

## History

Before August 2026 this site was built with Hugo + blogdown + the Wowchemy
"Academic" theme. That version is preserved in git history at the tag
`pre-quarto-rebuild`.
