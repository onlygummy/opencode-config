# Plan files live in the project

A plan file is written to `<location>/.opencode/plan/`, inside the project being
planned, not to `~/.opencode/plan`. The `plan` agent creates the directory when
it is missing. The edit allow stays `*.opencode/plan/*`, which covers both the
project-relative path and the absolute one. Plans stay out of git through the
rule `**/.opencode/plan/`, and `review` is the agent that checks it.

The reason is that a plan describes one project, so it belongs next to that
project. A plan kept in the home directory disappears from view the moment the
project is opened elsewhere, and two plan directories compete for the same name.
Ignoring the subtree keeps a session artefact out of history without hiding
`.opencode/`, which holds real project configuration. The leading `**/` carries
weight: a gitignore pattern with a slash in it is anchored to the file that
holds it, so `.opencode/plan/` alone matches only at the repo root and would
miss a plan written from a monorepo subpackage.

Three alternatives were rejected. Keeping `~/.opencode/plan` as the single
location separates the plan from the code it describes and leaves two candidate
directories. Letting `build` append the ignore line itself writes to a file the
user may want to control, and leaves a diff in every project that never asked
for one. Putting plans under `docs/plans/` uses a permanent tree owned by
`scribe`, while a plan expires when the work ends.

`review` runs the check in the user's working tree, not the baseline worktree. A
staged plan file blocks the verdict, because it would enter history. A directory
that exists without an ignore rule warns without blocking, and the warning names
the line to add. `build` never stages a plan file and does not edit
`.gitignore`; the user picks the mechanism, which may be `.gitignore` or
`.git/info/exclude`. `ship` already refuses to commit anything `.gitignore`
covers, and plan files are on its non-negotiable list.

OpenCode's shipped Plan mode injects a fixed instruction that names
`~/.opencode/plan`. A test on 2026-10-30 showed that the text does not change
when the repo's permission rule changes, so the config cannot move it. The
project path wins anyway: `plan` writes to `<location>/.opencode/plan/` and
falls back to the runtime path only when it cannot write the project path, then
states in the plan which path it used. Writing a plan anywhere else stays
forbidden. The permission rule covers both paths, because `*` spans `/` in
`*.opencode/plan/*`.

Two alternatives were rejected. Following the runtime instruction first would
restore the behaviour this ADR replaces and leave the plan outside the project
it describes. Renaming the agent id to avoid the injected text would touch
`default_agent`, the README table, the docs, and this ADR, and it is unproven
that the injection is keyed to the agent id.
