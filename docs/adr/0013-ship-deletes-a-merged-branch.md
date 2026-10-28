# Ship deletes a merged branch after four checks

Branch deletion was fully denied for `ship`, so every merge ended with a manual
step on the web. The colon refspec form, `git push origin :BRANCH`, already fell
under the push ask, so deletion was possible but undocumented. This supersedes
the "delete the branch on the web" step in
[ADR 0011](0011-ship-closes-the-loop.md).

`ship` may now delete a remote branch only after four checks: `gh pr view <number>
--json state,headRefName` returns MERGED and the head branch is the branch to
delete, `git fetch origin` ran so remote refs are current, `git branch -r
--merged origin/<trunk>` lists the branch, and the branch is not the trunk with a
clean working tree. If any check fails, the agent stops and names the check. The
remote delete is `git push origin --delete <branch>`, which still uses the `ask`
effect, so the user approves each deletion. Local deletion stays denied. Windows
matches permission patterns without case, so a rule that allows `git branch -d`
also allows the force form `git branch -D`, and the two cannot be separated. Only
the remote branch is deleted; the local branch stays until the user removes it.
After deleting, `ship` switches to the trunk and runs `git pull --ff-only origin
<trunk>`.

Three alternatives were rejected. Keeping the deny costs a manual step on every
merge. Allowing only branches with a known prefix such as `feat/` or `chore/`
adds no real protection, since naming is free. Allowing deletion without the
checks can lose an unmerged branch. The accepted risk is that the user can still
approve deleting an unmerged branch or the trunk, because a permission pattern
cannot express "this branch only". The four checks are the only argument-level
control available.
