# The Engineer’s Field Guide

[Read the public book](https://kaw393939.github.io/python-calculator/).

A twelve-page illustrated edition of the reviewed learning package in `docs/learning`.
The calculator runtime remains independent of this static publishing layer. GitHub
Pages serves HTML, CSS, JavaScript, images and selected downloads; it does not run FastAPI.

## Publishing specification — issue #23

Theme: help learners transform AI-generated output into software they understand.
Epic: publish an accessible, engaging book that makes the existing six labs usable.

| Story | Acceptance criteria |
| --- | --- |
| As a new learner, I want an inviting introduction so I know where to begin. | Home has a clear learning promise, guide introduction, six-chapter path and direct start CTA. No fabricated testimonials, urgency, learning results or enrollment counts. |
| As a learner, I want a consistent companion so complex ideas feel approachable. | Mira has a recognizable face, and appears in the hero, sidebar, tip and fact callouts. Every page has two distinct generated illustrations: its own portrait and scene. |
| As a reader, I want navigable lessons so I can learn at my own pace. | Twelve pages expose the six labs, student setup, vocabulary, case study, assessment and instructor guide. Previous/next navigation, a chapter menu, in-page headings, search, copyable code and local reading progress support study. |
| As a student without repository access, I want workshop files so I can perform the labs. | Four historical source snapshots and the current lesson pack are public downloads. Downloaded snapshots can be installed without GitHub authentication. |
| As a maintainer, I want repeatable releases so the public book stays consistent with the lessons. | A push to main builds from Markdown, validates links/fragments/art/downloads, and deploys through GitHub Actions. PRs build and check without publishing. |
| As a mobile or keyboard reader, I want readable pages and usable controls. | Responsive layout, mobile chapter toggle, semantic headings, descriptive image alternatives, skip link, visible focus, native search dialog and reduced-motion support. Navigation and lessons work without JavaScript. |

The publishing extension supersedes the original module's exclusion of a hosted course
site. It does not introduce accounts, payments, grading services, learner analytics or
claims of proven classroom effectiveness.

## Build and serve

From the repository root, using Python 3.11 or newer:

```sh
python -m pip install -r book/requirements.txt
python scripts/build_book.py
python scripts/check_book.py
python -m http.server 8020 --directory _site
```

Open `http://127.0.0.1:8020`. The build requires full Git history: four intentionally
pinned historical revisions are packaged using `git archive`. CI checks out with
`fetch-depth: 0`. `_site` is generated and ignored by Git.

- `pages.json`: page order, source mappings, hero copy, tips and facts.
- `templates/page.html`: shared semantic structure.
- `assets/book.css`, `assets/book.js`: responsive styles and progressive enhancements.
- `assets/images`: 24 original PNGs generated with the built-in image-generation tool.
- `image-prompts.json`: original prompts for the illustrations; home-guide is the visual reference.
- `../scripts/build_book.py`: Markdown rendering, link rewriting and download packaging.
- `../scripts/check_book.py`: checks the actual build output for broken internal links,
  anchors, root-relative paths, missing artwork/alt text, duplicate IDs, search targets,
  and unsafe archive members.
- `../.github/workflows/pages.yml`: separate build and least-privilege Pages deployment jobs.

Changes to lesson content belong in `docs/learning`, not in generated HTML.
Pages uses relative asset and navigation paths so the project URL works correctly.
Search uses a generated JSON index. Reading progress stores only page slugs in the
reader's local browser; storage failures degrade to progress for the current visit.

## Character and editorial direction

Mira is a fictional engineering mentor: warm brown skin, short curly hair, round gold
glasses, teal jacket, cream shirt and a small gold star pin. Editorial illustrations
use teal, ivory and muted gold. The magician archetype is expressed as achievable
transformation: learners turn ideas into working systems through deliberate practice.
Gold sparks are visual metaphors, not claims that engineering is effortless.

The copy applies [Cialdini's influence principles](https://www.influenceatwork.com/7-principles-of-persuasion/)
ethically: useful ungated materials (reciprocity), a small first requirement
(commitment), evidence and an explicit rubric (authority), a welcoming guide
(liking), and shared engineering practice (unity). It deliberately does not invent
social proof or scarcity. Every claim about validation retains the actual limits:
author dry-run completed, learner pilot pending, Safari compatibility unverified.

## Public artifact boundary

The repository stays private; the Pages book and its downloadable teaching code are
public. The workflow uploads only `_site`. Source downloads come from explicit
tracked paths in pinned commits: `src`, `tests`, `examples`, `pyproject.toml`,
`README.md`, `docs`, `.gitignore` and `.github`. Working CSV history, `.env`, virtual
environments and `.git` are not published. The current teaching bundle contains
only `docs/learning`. Adding new download paths requires reviewing their contents.

## Issue audit

Issues #1–22 were already closed when this publishing work began. Their existing
completion evidence was reviewed; the teaching dry-run records remain in
`docs/learning/validation-report.md`. No old issue was closed merely to reduce a count.
Issue #23 tracks this new site and its publishing acceptance evidence.
