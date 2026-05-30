# CLAUDE.md

Guidance for AI assistants (Claude Code) working in this repository.

## What this repository is

This is a **coursework / homework repository**, not a software project. It holds
written assignment reports (Markdown) and their supporting image assets for
**CS 625 (Data Visualization), Fall 2024**. The author is Kenny Bush (GitHub:
`rkbush12`).

There is **no application code, no build system, no dependencies, and no test
suite.** Do not look for `package.json`, `Makefile`, CI config, linters, etc.;
they do not exist and should not be added unless explicitly requested.

## Repository structure

```
.
├── HW1-report.md        # Homework 1 report (Markdown prose + embedded images)
├── CLAUDE.md            # This file
└── assets/
    └── img/             # Images referenced by the reports
        ├── woodchuck.jpg
        ├── SalesintheEast.png
        ├── penguins1.png
        └── penguins2.png
```

- **Reports** live at the repo root, named `HW<N>-report.md`. Future homework
  should follow the same `HW<N>-report.md` pattern.
- **Images** live in `assets/img/` and are referenced from reports using
  relative paths, e.g. `![A Woodchuck](assets/img/woodchuck.jpg)`.

## Conventions

### Report format
Each report is a single Markdown file with this structure:
- A top-level `#` title (e.g. `# Homework 1: Tool Setup`).
- An identification block: author name, course/term, due date.
- `##` sections grouping related questions (e.g. `## Git, GitHub`, `## Markdown`).
- `###` subsections per question, prefixed with the question label
  (e.g. `### Q1 - URL of GitHub Repo`).
- A `### References` subsection at the end of a section when sources are cited.

### Markdown style
- Use relative paths for images (`assets/img/...`), not absolute URLs.
- Bare URLs are wrapped in angle brackets: `<https://example.com>`.
- Two trailing spaces are used for hard line breaks within reference lists.
- Image filenames avoid spaces (note the prior rename
  `Sales in the East.png` → `SalesintheEast.png`); keep new asset names
  space-free to avoid broken Markdown links.

### Adding assets
- Place new images in `assets/img/`.
- Use descriptive, space-free filenames.
- Reference them with relative paths from the report.

## Working in this repo

- This is primarily a **content** repository. Most tasks are editing prose in a
  report, fixing typos, adjusting Markdown formatting, or adding/linking images.
- Preserve the existing structure and heading conventions when editing.
- When fixing or rephrasing answers, keep the student's voice; do not rewrite
  substance unless asked.
- There is nothing to "run" or "test." Verification means checking that
  Markdown renders correctly and that image links resolve to files that exist
  in `assets/img/`.

## Git workflow

- Default branch: `main`.
- Remote: GitHub repo `rkbush12/rkbush12`.
- Typical workflow is the standard add → commit → push cycle. The commit
  history is mostly small content edits (e.g. "Update HW1-report.md").
- Always `git push -u origin <branch-name>`. Do **not** create pull requests
  unless explicitly asked.
- Commit messages should be short and descriptive of the content change.
