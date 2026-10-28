# Plan decides workflows, build writes them

`release-please.yml` had no owner. It pins the action with a floating `@v4` tag,
and no agent prompt mentioned workflows, so nothing in the repo decided whether
the file should exist or what it was allowed to do.

Now `plan` decides whether a workflow exists and why, and records that decision
as an ADR. `build` writes the YAML following the `github-actions` skill, `review`
runs that skill's Review checklist on a workflow diff, `ship` commits and opens
the PR, and `scribe` writes the ADR and the docs. One exception: `build` may add
a read-only CI check that runs lint or validation without new permissions or
secrets. Anything that adds a permission or a secret goes to `plan` first.

Three alternatives were rejected. A dedicated `ci` agent would add a tab for
work that is rare. Letting `build` decide everything would let permissions creep
in with no one reviewing the reason. Leaving workflows unowned is the state that
produced the file above. The costs are one more skill to maintain, and a `plan`
round trip whenever a workflow needs a new permission.
