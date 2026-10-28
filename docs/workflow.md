# Workflow

Five agents share the work. Each one has a narrow scope and a stopping point.
The permission rules enforce the scope; the prompt describes the job.

## plan

The default agent. It turns a request into requirements, a design, and a work
breakdown. It can edit plan files under `.opencode/plan/` and nothing else. It
dispatches `scribe` to write ADRs, glossary entries, and docs pages. It cannot
edit code, commit, or push.

## build

It writes and refactors code and config. It cannot write `README.md`,
`GLOSSARY.md`, `GLOSSARY-MAP.md`, or anything under `docs/`; a decision that
needs recording goes to `scribe` through a brief. It runs lint only. Tests
belong to `review`. It can stage the index but cannot commit or push.

## review

It verifies a diff in a fresh context. It cannot edit, stage, commit, or push.
It takes a baseline with `git worktree` at a scratch path, not `git stash`,
because a failed stash pop would strand the user's changes. It runs a static
security scan and the `requesting-code-review` pipeline, then writes the commit
message in conventional commit form. The user commits.

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

## Gates

| Gate | Owner | Why |
| --- | --- | --- |
| Review passes | `review` | A commit lands only after the diff has been checked in a fresh context |
| Push approval | user | A local commit can still be fixed; a pushed one is already on the remote |
| Merge | user, on the web | No automated test run gates the PR, so the merge click is the check that the diff was read |
| Branch deletion | user approves, `ship` checks | A deleted remote branch is hard to recover |
| Release tag | user | No release automation runs, so a tag is a deliberate manual act |

## Only scribe writes documents

`plan` and `build` both dispatch `scribe`, so there is one writer for ADRs,
glossary entries, README, and `docs/`. Two writers would drift the format and
race on ADR numbers.

`scribe` starts with no conversation memory, so the caller has to supply a
brief with the target, the decision, the reason, the rejected alternatives, and
the allowed paths. A thin brief produces a guessed document.
