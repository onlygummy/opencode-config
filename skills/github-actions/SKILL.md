---
name: github-actions
description: "Decide, write, and review GitHub Actions workflows: whether a workflow earns its place, least-privilege permissions, pinned actions, safe triggers, and script injection. Use when adding or changing a file under .github/workflows/, or when deciding whether CI or release automation is needed."
---

# GitHub Actions

Three moments, three jobs. Do not skip the decision and start with YAML.

## Decide (plan)

A workflow earns its place when all four are true:

1. The failure it catches is plausible in this repo.
2. Someone fixes it when it goes red.
3. It finishes in a few minutes.
4. The trigger and the owner are clear.

Skip it when:

- There is no test or validation script to run yet.
- No one consumes the artifact or the tag.
- It needs broad write permissions or a secret it does not have to have.
- A manual step is rare enough that automation costs more than it saves.

One workflow, one purpose. CI, release, deploy, and scheduled checks are
separate files.

For CI, start with the smallest check that would have caught a real bug. A repo
with no tests should get a validation script first, not a test matrix.

## Author (build)

- Triggers: name the branches and the paths. A workflow that runs on every push
  to every branch wastes time and money.
- Permissions: start from `permissions: contents: read` and add only what the
  job needs. Read the action's README for the list it requires instead of
  guessing from its name; release-please, for example, asks for `contents`,
  `issues`, and `pull-requests` write.
- Actions: pin third-party actions to a full commit SHA. A floating major tag
  moves under you.
- Secrets: never inline them, never echo them, and remember secrets are not
  available to pull requests from forks.
- Untrusted input: never interpolate `${{ github.event.* }}` or a branch name
  directly into `run:`. Put the value in `env:` and read the variable in the
  shell.
- Concurrency: add `concurrency` when the same ref can queue twice.
- Caching: only when a dependency install is slow enough to matter.
- Validate the YAML before committing. `actionlint` is the tool when installed.

## Review (review)

Any workflow change gets a security pass beyond the normal diff review:

1. Script injection: an expression inside `run:` that comes from an event field
   (title, body, branch, ref) is a blocker.
2. `pull_request_target`: allowed only when the job never checks out and runs
   fork code.
3. Third-party actions: check the owner and the pin. A tag is weaker than a SHA.
4. Permissions: compare the declared block to the job. Write access that the
   task does not need is a finding.
5. Secrets: no new secret reference without a reason, and no secret printed.
6. Triggers: `workflow_dispatch` and `schedule` are cheaper than `push` on
   every branch.
7. Release bots: a PR opened with `GITHUB_TOKEN` does not trigger other
   workflows, so a chained workflow will not run. Say so when it matters.

Blocking follows the normal review rules: an injection path or an excessive
permission blocks; pinning advice for a first-party action is a suggestion.

## Files in this repo

- `.github/workflows/check-config.yml` validates the agent and skill config on
  every pull request and on a push to the trunk.
- A skill may keep its own workflow under `skills/<id>/.github/`. It does not
  run unless the repo copies it to the root `.github/`.
