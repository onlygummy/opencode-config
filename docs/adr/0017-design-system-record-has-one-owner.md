# The design system record has one writer

ADR 0012 gives `scribe` the docs tree because two writers drift the format and
race on ADR numbering. The design system record needs one exception: its pages
have a fixed schema and change when UI work changes, while the rest of the docs
tree changes when a decision settles. So `docs/design-system/` belongs to
`design-steward` alone. `scribe` keeps `docs/adr/`, `docs/*.md`, `README.md`, and
`GLOSSARY.md`. A permission rule denies `scribe` inside the design system
subtree, so the split is a rule and not a convention.

Letting `scribe` write the design system too was rejected. The steward then could
not edit a page it had recorded, and every token change would need a brief routed
through an agent that owns a different domain. Shared write access in both
subagents was rejected for the failure ADR 0012 already describes: two writers
drift the format and race on numbering. There is a second reason. `scribe` starts
with no design knowledge, so it cannot hold `tokens.md` as a standard that code
has to follow.

The cost is that one change touching both a token and an ADR needs two subagents.
In exchange each domain keeps one format, and ADR numbering stays single-writer.
