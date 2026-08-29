#!/usr/bin/env bash
# Regenerate the downloadable PDF and EPUB and stage them as tracked artifacts.
#
# These are built here rather than in CI. The PDF needs a LaTeX installation and
# rsvg-convert (for the SVG figures); neither is in the Netlify build image, and
# installing them there would add several minutes to every deploy and, because
# the build script runs under `set -e`, would let a PDF failure block the whole
# site from deploying. The book changes rarely, so the artifacts are built
# locally and committed.
#
# Run this whenever chapter content changes, then commit personality/_downloads.
#
# Requires: a working LaTeX (TinyTeX) and rsvg-convert on PATH.
set -e
cd "$(dirname "$0")/.."
command -v rsvg-convert >/dev/null || { echo "rsvg-convert not found (brew install librsvg)"; exit 1; }
# One pass: rendering a single format clears the others from _book.
quarto render personality
mkdir -p personality/_downloads
cp personality/_book/Personality-Psychology.pdf  personality/_downloads/
cp personality/_book/Personality-Psychology.epub personality/_downloads/
echo "downloads refreshed:"
ls -lh personality/_downloads/ | tail -n +2 | awk '{print "  "$NF"  "$5}'
