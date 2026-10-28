# A VCS subagent owns commit and push, the human owns merge

Before this, no agent could write history. `build` allows shell wholesale and
then denies `git *`, `review` holds no `edit` permission and only drafts a
commit message, and the user ran `git commit` by hand after reading it. That
split existed because the reviewer sees the code in a fresh session and its
verdict never reaches `build`, so anything that lets `build` commit would let
unreviewed work land.

The `vcs` agent keeps that split and adds the missing step. It is a `subagent`
with its own permission set, holding `git add`, `git commit`, `git push`, and
the `gh pr` commands. `build` still cannot commit. The difference is that the
user invokes `vcs` deliberately, with `@vcs`, after the work is done. Nothing
in the ordinary coding loop can write history by accident.

Two alternatives were rejected. Giving `build` commit rights collapses the
gate described above. Making `review` commit fails for the reason recorded in
ADR 0001: a reviewer that fixes or lands its own findings is not a reviewer.

Merge stays human. This repo has no CI yet, so an agent merge would be the only
check on the change. A merge on the web costs one click and forces the diff to
be on screen, which is precisely the check that replaces the missing pipeline.
The same reasoning blocks force push, rebase, `commit --amend`, branch deletion,
and release creation: they are denied rather than left to the prompt.

Push is `ask`, not `allow`. Writing a commit is local and reversible, so the
agent may do it unattended. A push is the first action the rest of the world
can see, so the user approves each one.

The cost is real. A subagent needs its own copy of the read-only git rules,
which will drift from the copies in `plan` and `review` unless someone keeps
them in step. The agent also cannot unstage a file, because `git restore` and
`git reset` are not in its allowlist; a mistaken stage therefore ends the run
instead of being repaired. That is the intended trade: stopping costs a minute,
a wrong commit on a shared branch costs a history rewrite that this agent is
forbidden to perform.
