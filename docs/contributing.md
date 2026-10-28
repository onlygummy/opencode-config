# Contributing

## Add an agent

Create a Markdown file in `agents/`. The frontmatter holds `description`,
`mode`, `color`, and `permissions`. The body is the system prompt. Add a row for
the agent to the table in `README.md`.

Rules are appended after the global baseline, and the last match wins. Read
[permissions.md](permissions.md) before writing the list.

## Add a skill

Create a folder under `skills/` with a `SKILL.md`. The frontmatter holds `name`
and `description`. The description decides when the model loads the skill, so
state the trigger.

## Write documents

Dispatch `scribe`. It is the only writer of `README.md`, `GLOSSARY.md`,
`GLOSSARY-MAP.md`, and files under `docs/`. `plan` and `build` both reach it.
Scribe loads the `docs-writing` skill for README and docs pages. It fixes the
page types, the page shape, the length limits, and the compaction rules.

The brief needs the target, the decision, the reason, the rejected alternatives,
and the allowed paths. `scribe` starts with no conversation memory, so anything
the brief leaves out is a guess.

ADR numbers are sequential in `docs/adr/`. Take the highest number and add one,
padded to four digits. Glossary entries follow the shape already in
`GLOSSARY.md`, including the `_Avoid_:` line when a term has aliases.

## Workflows

Workflow changes follow the `github-actions` skill. `plan` decides when a
workflow is needed and records it as an ADR. `build` writes the YAML. `review`
checks it for script injection, excessive permissions, and unpinned actions. A
read-only check that adds no permission or secret may be added by `build`
without a new ADR.

CI runs `scripts/check_config.py` on every pull request and on a push to the
trunk. The script parses the frontmatter of every agent and skill, checks
permission triples and effects, checks that skill names match their folder, and
checks that links in `README.md` and `docs/` resolve. Run the same script
locally before asking for review.

## Change flow

1. `plan` settles the requirements and records the decisions.
2. `build` implements the change and runs lint.
3. `review` verifies the diff and writes the commit message.
4. `ship` commits, pushes after approval, and opens the PR.

The user merges on the web, deletes the branch there, and pulls the trunk.

## Commits

Commit messages use conventional commit form. This repo has no release
automation, so no changelog or tag is produced automatically. If you want a fixed
snapshot, create the tag by hand.
