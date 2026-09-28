# Book release validation — 2026-09-28

Issue #23 publishes the existing reviewed learning package as a static book.

- `python scripts/build_book.py`: twelve pages plus the index alias, search index,
  24 original illustrations, and five teaching archives generated successfully.
- `python scripts/check_book.py`: all internal page/asset links, HTML fragments,
  expected per-page illustration pairs, alternative text, duplicate IDs, relative
  project URLs, search destinations and archive member safety pass.
- Negative build evidence: validation failed while illustrations were still missing;
  it passed only after all 24 expected assets were generated and copied.
- All four public source snapshots were extracted to independent temporary folders.
  Each executed `python -m calculator --history <temporary CSV> --command 'add 2 3'`
  against its own `src` and returned 5. No original history file was used.
- `ruff check .` and `git diff --check` pass.
- Calculator regression suite: 109 tests pass; statement coverage 98.31%.
  One upstream Starlette/httpx deprecation warning remains. This is not a test failure.
- In-app browser: desktop hero and navigation inspected; search for `observer`
  returned four relevant pages; an unknown term returned no results. Empty-result
  guidance was improved to suggest broader terms.
- Browser: mark page complete changed progress to 1/11; reloading preserved it;
  reset returned it to 0/11. Code-copy button reported success.
- At 390 × 844, the hero, mobile chapter menu and vocabulary tables were inspected.
  Both home and glossary had document width equal to viewport width (390 px).
  Tables scroll within their reading region. Temporary viewport override was reset.
- No browser error or warning logs during the exercised flows.
- All generated illustrations visually reviewed for a consistent Mira character,
  palette, recognizable face and page-appropriate scene.

These checks do not establish universal browser compatibility, full accessibility
conformance or classroom effectiveness. The prior Safari compatibility limitation and
pending learner pilot remain explicit in the teaching materials.

## Published evidence

- Live book: https://kaw393939.github.io/python-calculator/
- Pages deployment succeeded: https://github.com/kaw393939/python-calculator/actions/runs/36492803825
- Calculator CI passed on Python 3.11, 3.12, 3.13 and 3.14:
  https://github.com/kaw393939/python-calculator/actions/runs/36492803720
- All 48 published HTML, image, CSS/JS, index and download resources returned HTTP 200.
- Live browser verified the welcome page and `observer` search (four matching pages).
- [Published welcome screenshot](live-preview.png).

Publishing implementation is in commits `0e4a18c`, `d6d599a` and `f38f23f`, each linked
to issue #23. The original `is218-oop-calculator` repository was not modified.
