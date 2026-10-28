# A scribe subagent writes the docs

`build` could not record a decision without switching tabs to `plan`. Plan-only
ownership of the docs tree forced that switch mid-implementation, and letting
`plan` and `build` both write had its own failure: two writers drifted the
format and raced on ADR numbering.

So a `scribe` subagent is the only writer of ADRs, glossary entries, `README.md`,
and pages under `docs/`. Both `plan` and `build` dispatch it with a brief. One
writer gives one format and one numbering sequence, and neither caller has to
leave its session to record what it just decided.

Three alternatives were rejected. Plan-only ownership forces a tab switch.
Shared write access in `plan` and `build` means two writers and numbering races.
A per-agent docs prompt with no shared writer drifts the format. The costs are
one extra session per batch, and the caller must supply a brief, because a
subagent starts with no conversation memory. A thin brief produces a guessed
document.
