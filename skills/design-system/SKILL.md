---
name: design-system
description: "Read, record, and maintain a project's design system: tokens, typography, color, spacing, components, motion, accessibility, and UX voice, stored under docs/design-system/. Use when asked to understand an existing design system, bootstrap a record for a project that has none, update a recorded page, or check whether code still matches the record."
---

# Design system record

A design system record is the written form of the decisions a project already makes about
its interface: which values exist, which components exist, and which rules apply when
adding more. It lives at `docs/design-system/` in the repo that owns the UI, next to the
code that justifies it.

Two subagents use this skill. `design-surveyor` reads and reports. `design-steward`
writes and maintains. Neither invents a value that no file supports.

## Token authority

`tokens.md` is the standard. Code follows it, not the other way round.

The first bootstrap is the exception. There is nothing to follow yet, so you extract the
values from the code and write them down. Once that page exists, it leads.

When code and `tokens.md` disagree, do not pick a side silently. Classify the gap under
"Drift" below and report it. A deliberate change updates the record first and the code
second. An accidental change fixes the code.

## Read order

1. `INDEX.md` says which pages exist. Read it first, always.
2. `tokens.md` before any page that quotes a value.
3. Only the component rows for the components the task touches. Do not read the whole
   inventory to change one button.
4. `content-voice.md` when the task involves user-facing text.

## Pages

| Page | Holds |
| --- | --- |
| `INDEX.md` | What exists, where each value family comes from, and the last audit date |
| `tokens.md` | The raw standard: token name, value, source path. No usage advice |
| `typography.md` | Families, scale, weights, line heights, and when each applies |
| `color.md` | Semantic roles, contrast pairs, and the rule for each role |
| `spacing-layout.md` | Spacing scale, grid, breakpoints, container widths |
| `components.md` | One row per exported component: path, props, variants, states, rules |
| `motion.md` | Durations, easing, what may animate, reduced-motion behavior |
| `accessibility.md` | Focus treatment, keyboard behavior, labeling, contrast floor |
| `content-voice.md` | Tone, error and empty-state wording, capitalization rules |

Create a page only when it has content. An empty skeleton is worse than a missing page,
because the next reader cannot tell "none" from "not written yet".

## Audit

`design-surveyor` runs this and writes nothing.

1. Check whether `docs/design-system/` exists and list the pages it holds.
2. Find where values live: token files, theme config, CSS custom properties, a Tailwind
   or equivalent config, a styled-system theme, an exported design file. Name the exact
   paths. If a family has no source, say so.
3. Find components: search the UI layer for exported components. Group them as
   primitives, composed components, and page-level layouts. Record the path of each.
4. Collect accessibility evidence: focus styles, labels and aria attributes, keyboard
   handlers, contrast-bearing roles. Evidence only, no advice.
5. Collect voice evidence: the strings used for errors, empty states, and confirmations.
6. If a record exists, compare it page by page against the code and classify every gap
   as drift.
7. Report in the fixed shape below. Stop there.

### Report shape

```
Record status   missing | partial | present, with paths
Value sources   one line per family, with the source path
Tokens          standard in use, families found, families missing
Components      count by group, then the rows for what the task touches
Accessibility   what the code actually does
Voice           sample strings and where they live
Drift           one line per gap, classified
Gaps            what the record cannot answer yet
```

## Bootstrap

The project has no record, or has one too thin to use.

1. Audit first. Never propose before you have read the code.
2. Say plainly that no record exists, then propose the smallest useful set: the value
   families that are actually in use, the components that actually exist, and the gaps
   that need a decision.
3. Present the proposal in the conversation. Do not write it to a file yet.
4. After the user approves, write `tokens.md` and `INDEX.md` first, then the pages the
   proposal covers.
5. Never import a palette, a type scale, or a component library the project does not use.

## Update

`design-steward` runs this after a brief.

1. Read `INDEX.md` and the target page. Match the headings and table shape that are
   already there. The format in `PAGE-FORMAT.md` is the starting point, not a reason to
   restructure a page someone already wrote.
2. Read the source files the brief names. If the brief asserts a value with no source,
   ask for the source instead of writing it.
3. Write the page: one row per item, relative paths from the repo root, `file:line` when
   a single line decides the value.
4. Update `INDEX.md` when a page is added or removed, and stamp the audit date in ISO
   form.
5. Reply with the paths written and one line per file describing the change.

## Drift

Four classes, four responses. Never collapse them into "mismatch".

| Class | Evidence | Action |
| --- | --- | --- |
| Record stale | Code uses a value consistently and the page lacks it | Steward adds or corrects the row |
| Code off-standard | One file departs from the standard, the rest follow it | Report it. Build fixes the code |
| Deliberate change | The brief or the user says the values changed on purpose | Update the record first, then the code |
| Undecidable | Nothing shows intent either way | Report it and ask. Edit nothing |

## Limits

- No shell and no browser. Read with `read`, `glob`, and `grep`. Do not claim to know
  computed styles, rendered layout, or anything visible only at runtime. Say the record
  covers source, not pixels.
- Do not overwrite a structure the project already has. If the existing record lives
  elsewhere or uses different page names, report it and ask before moving anything.
- English in every file, including the report.
- One record per repo at `docs/design-system/`, even in a monorepo. If two apps need
  different standards, that is a decision for the user, not something to invent.

## Before returning

- [ ] Every value traces to a file path, or is marked `Not defined`
- [ ] No page was created without content
- [ ] `INDEX.md` lists exactly the pages that exist
- [ ] Drift is classified, not merely mentioned
- [ ] Nothing was written outside `docs/design-system/`
- [ ] Paths are exact and relative to the repo root
- [ ] English only, no em dashes

Page skeletons: [PAGE-FORMAT.md](./PAGE-FORMAT.md).
