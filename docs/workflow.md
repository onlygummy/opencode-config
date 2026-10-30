# Workflow

Seven agents share the work: four primary and three subagents. Each one has a
narrow scope and a stopping point. The permission rules enforce the scope; the
prompt describes the job.

## plan

The default agent. It turns a request into requirements, a design, and a work
breakdown. It writes the plan to `<location>/.opencode/plan/`, inside the project
being planned, and creates the directory when it is missing. When a runtime
instruction names another plan directory, the project path still wins. The agent
writes to the runtime path only if it cannot write the project path, and then
states in the plan which path it used. Plan files are ignored by git. It can
edit files matching `*.opencode/plan/*` and nothing else; the leading `*` covers
both the project-relative path and the absolute one. It cannot edit code,
commit, or push.

It can dispatch three subagents. `scribe` records ADRs, glossary entries, and
docs pages. `explore` and `general` do fact-finding for the grilling interview,
so the interview does not ask the user something the filesystem can answer. It
cannot dispatch `design-surveyor` or `design-steward`; those belong to `build`.

## build

It writes and refactors code and config. It cannot write `README.md`,
`GLOSSARY.md`, `GLOSSARY-MAP.md`, or anything under `docs/`; a decision that
needs recording goes to `scribe` through a brief. It runs lint or typecheck
only. Tests belong to `review`, and a test run needs the user's approval. It can
stage the index but cannot commit or push.

The order matters: the design record follows the settled code, and the docs
handoff comes last.

1. Read the request and the workspace.
2. Change code with diff-shaped edits, not by rewriting the whole file.
3. If the change touches `.github/workflows/`, load the `github-actions` skill
   before editing anything there.
4. Run lint or typecheck. If the change needs a test run to confirm it, ask.
5. If the change touches UI, read `docs/design-system/INDEX.md`. Dispatch
   `design-surveyor` when the record is missing or does not cover the area, and
   dispatch `design-steward` once per change set after the code settles.
6. Record decisions last. Dispatch `scribe` with a brief, once per change set,
   and send only the delta as a shorter brief when `review` sends findings back.
7. Explain the change, then run the `humanizer` skill on the prose.

Standing rules: it never stages anything under `.opencode/plan/`, never adds the
ignore rule itself, and reports an already-tracked plan file instead of removing
it.

One gap is accepted on purpose. A page can end up behind code that `review`
asked to change afterwards, and writing docs early would not close it.

## review

It verifies a diff in a fresh context. It cannot edit, stage, commit, or push.
It takes a baseline with `git worktree` at a scratch path, not `git stash`,
because a failed stash pop would strand the user's changes. It also checks plan
files, in the user's working tree rather than the baseline worktree:
it runs `git status --short` and looks for anything under `.opencode/plan/`. A
staged plan file blocks the verdict. A plan directory that exists without an
ignore rule warns and names the line to add, `**/.opencode/plan/`, without
blocking. It runs a static security scan and the `requesting-code-review`
pipeline, then writes the commit message in conventional commit form. The user
commits.

## ship

It reads the trunk from `origin/HEAD`, creates a short-lived branch, commits,
pushes only after approval, and opens the PR. After you merge, it verifies the
PR state, deletes the merged branch after approval, and pulls the trunk.

It deletes only when all four checks pass:

- `gh pr view <number> --json state,headRefName` returns MERGED, and the head
  branch is the branch to delete.
- `git fetch origin` ran, so remote refs are current.
- `git branch -r --merged origin/<trunk>` lists the branch.
- The branch is not the trunk, and the working tree is clean.

If a check fails, it stops and names the check. It cannot merge, force push,
amend, rebase, delete a local branch, or create a release. The local branch stays
after the remote one is deleted.

## scribe

A subagent, launched by `plan` or `build`. It writes ADRs, glossary entries,
`README.md`, and pages under `docs/`. It loads `docs-writing` for README and docs
pages, and `domain-modeling` for ADRs. It has no shell and cannot dispatch other
subagents.

## design-surveyor

A subagent, launched by `build`. It reads a project and reports what design
values and components exist, then how the code and the record disagree. It has
no edit permission, no shell, and cannot dispatch other subagents. It runs the
audit in the `design-system` skill and writes nothing.

## design-steward

A subagent, launched by `build`. It writes and maintains the design system
record under `docs/design-system/`, the only path it can edit. It has no shell
and cannot dispatch other subagents. It loads `design-system` for the page list,
the update procedure, and the drift classes. It writes only after a brief that
names the source for every value.

## Gates

| Gate | Owner | Why |
| --- | --- | --- |
| Review passes | `review` | A commit lands only after the diff has been checked in a fresh context |
| Push approval | user | A local commit can still be fixed; a pushed one is already on the remote |
| Merge | user, on the web | No automated test run gates the PR, so the merge click is the check that the diff was read |
| Branch deletion | user approves, `ship` checks | A deleted remote branch is hard to recover |
| Release tag | user | No release automation runs, so a tag is a deliberate manual act |

## One writer per document

`scribe` is the only writer of ADRs, glossary entries, `README.md`, and pages
under `docs/`, except the design system record under `docs/design-system/`,
which `design-steward` owns. `scribe` is denied inside that subtree, so exactly
one agent writes each file. Two writers would drift the format and race on ADR
numbers. See
[ADR 0017](adr/0017-design-system-record-has-one-owner.md) for why the design
record is the exception.

`scribe` starts with no conversation memory, so the caller has to supply a
brief with the target, the decision, the reason, the rejected alternatives, and
the allowed paths. A thin brief produces a guessed document.
