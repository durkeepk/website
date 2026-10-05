#!/usr/bin/env bash
# Build the whole site: main website first, then the textbook copied in.
# Rendering the main site clears _site/personality, so order matters and the
# book is copied afterwards rather than written directly into _site.
set -e

# Publish a freshly knitted CV. rmarkdown writes cv.pdf next to its source in
# _cv-source/, but the site serves files/cv/cv.pdf, so the two drift apart
# silently unless the build copies it across. Must run before `quarto render`,
# which copies files/ into _site/.
#
# Deliberately not mirrored in netlify.toml: _cv-source/cv.pdf is a local build
# artifact that never exists in CI, so CI serves the committed files/cv/cv.pdf.
# -nt is false when the left-hand file is missing, so both tests are no-ops on
# a machine that has never knitted the CV.
if [ _cv-source/cv.pdf -nt files/cv/cv.pdf ]; then
    cp _cv-source/cv.pdf files/cv/cv.pdf
    echo "cv: published newly knitted _cv-source/cv.pdf"
fi
if [ _cv-source/cv.Rmd -nt files/cv/cv.pdf ]; then
    echo "cv: WARNING - _cv-source/cv.Rmd is newer than the published PDF."
    echo "cv:           Re-knit cv.Rmd, or your CV edits will not go live."
fi

quarto render
quarto render personality --to html
rm -rf _site/personality
cp -R personality/_book _site/personality
# The PDF and EPUB are built separately by scripts/build-downloads.sh and
# committed, because CI has no LaTeX. Copy them in so the download menu works.
cp personality/_downloads/*.pdf personality/_downloads/*.epub _site/personality/
echo "built: _site (site) + _site/personality (book, incl. PDF/EPUB)"
