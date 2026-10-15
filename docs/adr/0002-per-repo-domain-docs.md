# Domain docs live per repo, not in a central vault

An earlier setup kept a single vault at a fixed path: `vault/04 Memory/[project]/glossary.md`,
`vault/.../adr/`, plus folders for best practices, lessons learned, frameworks,
and libraries. `plan.md` hardcoded those paths. Nothing on disk matched them, and
the `domain-modeling` skill was already writing to `GLOSSARY.md` at the repo root
and `docs/adr/`. The prompt and the skill disagreed, and the prompt was wrong.

The vault is gone. `plan.md` now names only the two file kinds it may write,
`GLOSSARY*.md` and `docs/adr/**`, and the `domain-modeling` skill decides where
those go. A single-context repo gets one `GLOSSARY.md` at the root. A multi-context
repo gets a `GLOSSARY-MAP.md` plus one glossary and one `docs/adr/` per bounded
context.

A central vault was attractive because it put every project's decisions in one
place. It lost because the docs belong with the code that justifies them: a
glossary copied out of its repo drifts the moment the code moves, and a reviewer
who has to leave the repo to learn what a term means will not bother. Anyone who
wants the cross-project view can read the glossaries directly.
