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
pushes only after approval, and opens the PR. It ends with a handoff: merge on
the web, delete the branch there, then pull the trunk. It cannot merge, force
push, amend, rebase, delete a branch, or create a release.

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
| Release | user | `release-please` reads conventional commits and opens the release PR; no one creates tags by hand |

## Only scribe writes documents

`plan` and `build` both dispatch `scribe`, so there is one writer for ADRs,
glossary entries, README, and `docs/`. Two writers would drift the format and
race on ADR numbers.

`scribe` starts with no conversation memory, so the caller has to supply a
brief with the target, the decision, the reason, the rejected alternatives, and
the allowed paths. A thin brief produces a guessed document.
