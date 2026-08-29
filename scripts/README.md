# Conversion scripts

Originally written by the Codex session; preserved and validated here.

- `inventory_docx.py` — structural inventory of Word chapters (headings, styles,
  tables, media, SmartArt in `word/diagrams/`, OMML equations, footnotes,
  endnotes, hyperlinks, fields). Emits JSON. Validated against Chapter 10.
- `make_contact_sheets.py` — page-image contact sheets from the LibreOffice PDF
  renders, used as visual ground truth when checking a conversion.
- `parse_emfplus.py` — inspects EMF+ records; used for the Chapter 13 figure.

These need `lxml`, which the macOS system Python lacks. Use the project venv:

```bash
python3 -m venv .venv && ./.venv/bin/pip install lxml
./.venv/bin/python scripts/inventory_docx.py "textbook-source/word/"*.docx \
  > textbook-source/docx-inventory.json
```
