# Short-lived branches off the trunk, no long-lived development branch

The working habit was a long-lived `development` branch, commits and pushes
into it, then a pull request from `development` to `main`. It works, and it is
the GitFlow shape: two branches that both live for months and meet at release
time. The cost shows up as merge debt. Work that sits on `development` diverges
from `main` for as long as the branch exists, so every promotion is a merge
event with its own class of conflicts, and the further the two drift the less
the PR diff tells a reviewer.

Trunk-based development is the alternative, and it is what the published
guidance now recommends for small teams: one mainline, and branches that carry
a single change for hours or a couple of days before merging back. A pull
request is still part of it. The branch being short-lived is the part that
matters, not the absence of PRs.

So the shape is: cut a branch from the trunk, commit, push, open a PR, merge,
delete the branch. One change per branch. The trunk is read from `origin/HEAD`
rather than assumed to be `main`, because repos that must keep `development`
for organisational reasons still exist, and in those repos `development` is the
trunk and `main` is the release line.

Squash merge is the intended merge style, which keeps the trunk linear and
gives `release-please` one conventional commit per change to parse. In a
one-commit PR the squash is a no-op, which is the normal case here. This is a
repository setting and cannot be enforced from configuration, so it is recorded
here as intent rather than as a rule the tooling checks.

Release branches are not part of this. `release-please` tags from the trunk and
`main` stays releasable, so there is no need to cut and harden a branch per
release. If a future deploy pipeline needs a hardened branch, that is a new
decision with its own record.
