#!/usr/bin/env bash
# Rebuild the student download for the R workshop.
#
# The zip is committed rather than generated during the site build, because
# Netlify's image has no reason to carry a zip toolchain and the contents change
# only when the workshop materials do. Run this after editing anything under
# files/r-workshop/r-workshop-1/, then commit both the files and the zip.
#
# -x excludes the macOS metadata that would otherwise ship to students as a
# stray __MACOSX folder and .DS_Store files.
set -e
cd "$(dirname "$0")/../files/r-workshop"
rm -f r-workshop-1.zip
zip -r -q r-workshop-1.zip r-workshop-1 -x '*.DS_Store' '*__MACOSX*' '*.Rproj.user*'
echo "built: files/r-workshop/r-workshop-1.zip"
unzip -l r-workshop-1.zip | awk '/----/{f=!f; next} f && NF {print "  "$4"  "$1" bytes"}'
