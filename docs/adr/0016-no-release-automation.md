# No release automation in this repo

`.github/workflows/release-please.yml` never produced a release or an open pull
request: `gh pr list --state all` matched nothing and `gh release list` was
empty. Its branch `release-please--branches--main` was rewritten on every push to
the trunk and was left behind. This config is installed by copying or pulling
it, so no consumer resolves a tag, and the workflow had nothing to deliver.

The workflow is deleted, and tags are manual: the user creates one by hand when
a fixed snapshot is wanted. Conventional commits stay, because they keep the
history readable. ADR 0008 still stands for the trunk-based branch and commit
shape; only the release step it mentions is gone. Keeping `release-please` with
the action pinned to a SHA and the permissions settled was rejected, because
that fixes the pin and not the missing consumer.

The cost is that no changelog is generated, and tagging depends on the user
remembering. The orphan branch `release-please--branches--main` stays until the
user deletes it, since the agent rules refuse to delete an unmerged branch.
