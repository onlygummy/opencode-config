# Baseline comparison uses a git worktree, not a stash

The review pipeline needs the repo's test and lint state before a change, so it can
tell new failures from old ones. The upstream `requesting-code-review` skill gets
that baseline by stashing the working tree, running the tests, then popping the
stash back. This setup does not use that. The reviewer checks out `HEAD` into a
scratch directory with `git worktree add`, runs the tests there, and removes the
worktree afterward.

The reason is that the reviewer has no `edit` permission. If a stash pop fails,
the user's uncommitted work is stranded in the stash and the agent assigned to
review it cannot get it out. A worktree never touches the working tree, so that
failure mode does not exist. The reviewer also has to be able to clean up after
itself: `git worktree remove` and `git worktree prune` stay allowed even though
`git stash`, `git add`, `git commit`, and `git push` are denied.

The trade-off is that the worktree needs a scratch path and leaves `.git/worktrees`
metadata behind if cleanup is skipped, which is why the skill lists leftover
worktrees as a pitfall. If `git worktree add` fails, for example mid-rebase, the
skill skips the baseline comparison and says so rather than falling back to a
stash.
