#!/usr/bin/env bash
# Build the whole site: main website first, then the textbook copied in.
# Rendering the main site clears _site/personality, so order matters and the
# book is copied afterwards rather than written directly into _site.
set -e
quarto render
quarto render personality
rm -rf _site/personality
cp -R personality/_book _site/personality
echo "built: _site (site) + _site/personality (book)"
