# Ship may unstage and read origin/HEAD

The `ship` prompt asked for two commands its allowlist did not permit. Rule 4
reads the trunk with `git symbolic-ref refs/remotes/origin/HEAD`, and rule 5
splits a mixed diff by taking paths back out of the index. Both were denied on
the first real run, so the agent guessed the trunk from `git branch -r` and
shipped one commit covering two changes, which is the outcome rule 5 exists to
prevent.

The unstage allow is `git reset -- <path>`, not `git restore --staged`. Both
touch only the index, but `git restore` accepts flags after `--staged`, and the
short form `-W` reaches the worktree without matching a deny written for
`--worktree`. After `--`, git reads every word as a pathspec, so the allowed
form has no flag surface at all. `git reset --hard` stays denied.

The read allow is the exact command `git symbolic-ref refs/remotes/origin/HEAD`,
backed by a deny for the two-argument form. The wildcard allow tried first also
permitted `git symbolic-ref HEAD refs/heads/x`, which writes `.git/HEAD` and
moves where the next commit lands.

Consequence: the agent can empty the index by itself. `git add` puts it back,
and file content stays out of reach.
