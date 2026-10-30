# Design system agents

`design-surveyor` and `design-steward` keep the design system record under
`docs/design-system/` accurate. This page explains the split, the flow inside
`build`, and the limits of both agents.

## Why two agents

Reading and writing need different scopes. A survey runs often and changes
nothing, so dispatch it whenever the record is in doubt. A write touches one
subtree and needs a narrow allow. The reader holds no edit permission, so its
report cannot change what it describes.

One agent with both abilities would have to stay read-only through its prompt.
Permissions, not instructions, keep the survey safe.

## Inside build

`build` is the only caller of either agent.

1. Read `docs/design-system/INDEX.md` before editing UI. `plan` also reads it
   directly when a plan involves UI, and dispatches neither agent.
2. If the record is missing or does not cover the area, dispatch
   `design-surveyor`. It returns the report shape from the skill: value sources,
   tokens, components, accessibility, voice, drift, and gaps.
3. Make the UI change.
4. After a change that alters tokens or components, dispatch `design-steward`
   once per change set with a brief that names the source of each value.

A change that only uses existing tokens and components does not need the steward.

## What a record holds

The record has one page per value family, and `INDEX.md` lists them. Each page
holds values and the path they come from, not usage advice.

- `INDEX.md`: what exists, where each family comes from, the last audit date
- `tokens.md`: token name, value, source path
- `typography.md`, `color.md`, `spacing-layout.md`: the values and the rule for
  each role
- `components.md`: one row per exported component
- `motion.md`, `accessibility.md`, `content-voice.md`: the behavior the code
  already has

This page does not repeat the schema. The page shapes, read order, audit steps,
and drift classes live in
[the design-system skill](../skills/design-system/SKILL.md).

## Tokens lead after bootstrap

`docs/design-system/tokens.md` is the standard, and code follows it. When the two
disagree, the steward classifies the gap instead of picking a side: record stale,
code off-standard, deliberate change, or undecidable.

The first bootstrap is the exception. There is nothing to follow yet, so the
values are extracted from the code and written down. After that first page
exists, the record leads. See
[ADR 0018](adr/0018-the-record-owns-the-design-tokens.md).

## Boundary with scribe

`scribe` is the only writer of ADRs, glossary entries, `README.md`, and pages
under `docs/`, except `docs/design-system/`, which `design-steward` owns.
`scribe` is denied inside that subtree, so exactly one agent writes each file.
See [ADR 0017](adr/0017-design-system-record-has-one-owner.md).

A change to the design record goes to the steward. A change to the page that
explains the record, like this one, goes to `scribe`.

## Limits

- Neither agent has a shell or a browser. Both read with `read`, `glob`, and
  `grep`, so the record covers source, not rendered output. It cannot report
  computed styles or rendered layout.
- The steward's edit allow is a path pattern, not a structural rule. It can
  rewrite any file under `docs/design-system/`, including a record that already
  exists. A path containing `..` is denied explicitly, but a symlink placed
  inside the subtree cannot be caught by a path pattern, so the prompt rule and
  the brief remain the real control. Its prompt forbids restructuring an
  existing record, so it matches the headings and tables the project already
  has.

## Next steps

- [docs/workflow.md](workflow.md): where both agents sit in the full loop.
