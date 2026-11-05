# Workflow

Six agents share the work. Each one has a narrow scope and a stopping point.
The permission rules enforce the scope; the prompt describes the job.

## plan

The default agent. It turns a request into requirements, a design, and a work
breakdown. It can edit plan files under `.opencode/plan/` and nothing else. It
dispatches `scribe` to write ADRs, glossary entries, and docs pages. It cannot
edit code, commit, or push.

## build

It writes and refactors code and config. Before the first edit it dispatches
`branch-keeper` to cut the short-lived branch. When the subagent is denied,
unavailable, or the user asks for the branch inline, it cuts the branch itself
with `git switch -c <type/slug>` after the same four checks and the same three
stops. It edits only after the branch exists. It cannot write `README.md`,
`GLOSSARY.md`, `GLOSSARY-MAP.md`, or anything under `docs/`; a decision that
needs recording goes to `scribe` through a brief. It runs lint only. Tests belong
to `review`. It stages and commits one change on the short-lived branch, and it
still cannot push. After the commit it dispatches `review` with the branch and
the full SHA. A failed verdict sends it back to fix, amend, and dispatch `review`
again; it stops after two failed rounds. It holds no edit rule for the verdict
artifact, and the edit and write tools are denied for it; a shell write remains
a recorded residual risk.

## branch-keeper

A subagent, launched by `build`, and by `ship` on a clean tree. It cuts the
short-lived branch from the trunk before the first edit, or stops and names the
condition that blocked it: a different branch already checked out, a dirty
trunk, or a branch name that exists. It is no longer the only owner of branch
creation: `build` holds the same `git switch*` allow and repeats the guard in its
own prompt, so the two lists change together. It edits nothing and holds one git
write, `git switch -c*`, plus `cd *` so it can set the repo as the shell's
working directory; `git -C` is still not allowed. The rest is state reads. It
never force-switches or reuses a name.

Every agent now opens its system prompt by naming its own id, so a handoff names
the right tab and a subagent never offers to switch to another agent.

## review

It verifies the commits against the trunk in a fresh context. `build` dispatches
it after the commit, and the user can still switch to its tab. A dispatched run
starts in a child session with no caller history, so the isolation is the same.
It cannot edit code, stage, commit, or push. The baseline is the merge base with
the trunk. A `git worktree` at a scratch path is used only while the tree is
still dirty, because `git stash` would strand the user's changes if the pop
failed. It runs a static security scan and the `requesting-code-review` pipeline,
then cross-checks the commit message against the diff instead of writing it.

Its one write is the verdict artifact at `.opencode/review/<branch>.json`, with
`/` in the branch name replaced by `-`. The file holds the verdict, the full
commit SHA, the branch, and the finding count, plus a reason when the verdict is
`skipped`. The directory is gitignored. `build` holds no edit rule for the file
and the edit and write tools are denied; a shell write is a recorded residual
risk, so the artifact is a record that a review ran, not a proof. On a docs-only
change it skips the deep pipeline and records `skipped`, under the same path
rule the `ship` section defines.

## ship

It reads the trunk from `origin/HEAD`, pushes the commit `build` wrote, and
opens the PR on the short-lived branch that `build` or `branch-keeper` cut. It
commits only when the tree arrives uncommitted. A fallback branch is cut
only when the work was never branched: through `branch-keeper` when the tree is
clean, or by `ship` itself when the reviewed change is still in the tree and the
subagent's dirty-trunk check would refuse it. Before any push it reads the verdict
artifact and refuses unless the verdict is `passed`, the finding count is `0`,
the commit equals `HEAD`, and the branch equals the checked-out branch. A
docs-only change is exempt only when the path list is non-empty and every
changed path is under `docs/` or is one of `README.md`, `GLOSSARY.md`, or
`GLOSSARY-MAP.md`. `agents/` and `skills/` are never exempt, because their
Markdown carries permissions and agent instructions, and an empty path list is
not docs-only. On an exempt change it pushes without the artifact and says so.
When it had to write the commit itself, it stops and asks for a review of that
commit. After you merge, it verifies the PR state, deletes the merged branch
after approval, and pulls the trunk.

It deletes only when all four checks pass:

- `gh pr view <number> --json state,headRefName,baseRefName,mergeCommit` returns
  MERGED, the head branch is the branch to delete, and the base branch is the
  trunk.
- `git fetch origin` ran, so remote refs are current.
- `git branch -r --list origin/<branch>` lists the branch, so the delete has a
  target. An already-deleted branch is a no-op, not an error.
- The branch is not the trunk, and the working tree is clean.

If a check fails, it stops and names the check. It cannot merge, force push,
amend, rebase, delete a local branch, or create a release. The local branch stays
after the remote one is deleted.

## scribe

A subagent, launched by `plan` or `build`. It writes ADRs, glossary entries,
`README.md`, and pages under `docs/`. It loads `docs-writing` for README and docs
pages, and `domain-modeling` for ADRs. It has no shell and cannot dispatch other
subagents.

## Gates

| Gate | Owner | Why |
| --- | --- | --- |
| Review passes | `review`, dispatched by `build` | The diff is checked in a fresh context after the commit, and the verdict artifact gates the push; a failed verdict sends the work back to `build` |
| Merge | user, on the web | No automated test run gates the PR, so the merge click is the check that the diff was read |
| Branch deletion | user approves, `ship` checks | A deleted remote branch is hard to recover |
| Release | user | `release-please` reads conventional commits and opens the release PR; no one creates tags by hand |

## Only scribe writes documents

`plan` and `build` both dispatch `scribe`, so there is one writer for ADRs,
glossary entries, README, and `docs/`. Two writers would drift the format and
race on ADR numbers.

`scribe` starts with no conversation memory, so the caller has to supply a
brief with the target, the decision, the reason, the rejected alternatives, and
the allowed paths. A thin brief produces a guessed document.
