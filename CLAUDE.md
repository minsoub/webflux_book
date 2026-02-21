# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Korean-language technical book: **Spring Boot + WebFlux + JPA (MongoDB)**. Static site generator that converts Markdown source files into navigable HTML pages.

## Build & Conversion

```bash
# Convert all markdown to HTML (generates index.html + contents/*.html)
python3 convert.py
```

**Dependencies:** Python 3 + `markdown` + `pymdown-extensions`
```bash
pip3 install --break-system-packages markdown pymdown-extensions
```

## Architecture

```
parts/              # Source markdown (authoritative content)
  ch01.md~ch21.md   # Individual chapters
  part1.md~part7.md  # Part-level merged files (cat of chapters)
  appendix_a~d.md   # Appendices
contents/           # Generated HTML output (do not edit directly)
css/style.css       # Shared stylesheet
convert.py          # Markdown → HTML converter
list.md             # Table of contents outline
index.html          # Generated TOC page linking to contents/
books.md            # Full book merged file (all parts concatenated)
```

### Content Pipeline

1. **Edit** markdown in `parts/ch*.md` or `parts/appendix_*.md`
2. **Merge parts** by concatenating chapter files: `cat parts/ch01.md parts/ch02.md ... > parts/partN.md`
3. **Merge full book**: `cat parts/part1.md ... parts/part7.md parts/appendix_*.md > books.md`
4. **Generate HTML**: `python3 convert.py` — reads `parts/*.md`, writes `contents/*.html` + `index.html`

### convert.py Key Structure

- `NAV_ORDER`: Ordered list of `(file_id, title)` tuples defining chapter reading sequence and navigation links
- `PART_FILES`: Part-level merged file definitions
- `build_index_html()`: Generates TOC page with hardcoded chapter/section structure — must be updated manually when adding chapters
- `make_nav()`: Creates prev/next navigation bar based on position in `NAV_ORDER`
- Uses markdown extensions: `TableExtension`, `FencedCodeExtension`, `TocExtension`, `pymdownx.superfences`

### Adding a New Chapter

1. Create `parts/chNN.md`
2. Add entry to `NAV_ORDER` list in `convert.py`
3. Add chapter details to `build_index_html()` parts/chapters data structure
4. Update `list.md` table of contents
5. Re-merge the relevant `partN.md` and `books.md`
6. Run `python3 convert.py`

## Content Conventions

- Written in Korean with English technical terms in parentheses: "배압(Backpressure)"
- Each chapter: 500–800 lines of markdown
- Chapters include: explanations, Java code examples, comparison tables, tip/warning blockquotes
- Code blocks use fenced syntax with language identifiers (```java, ```yaml, ```bash, etc.)
