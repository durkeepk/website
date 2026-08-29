#!/usr/bin/env bash
# Build the whole site: main website first, then the textbook copied in.
# Rendering the main site clears _site/personality, so order matters and the
# book is copied afterwards rather than written directly into _site.
set -e
quarto render
quarto render personality --to html
rm -rf _site/personality
cp -R personality/_book _site/personality
# The PDF and EPUB are built separately by scripts/build-downloads.sh and
# committed, because CI has no LaTeX. Copy them in so the download menu works.
cp personality/_downloads/*.pdf personality/_downloads/*.epub _site/personality/
echo "built: _site (site) + _site/personality (book, incl. PDF/EPUB)"
