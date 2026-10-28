# OpenCode config

This repo is a personal OpenCode configuration, installed at `~/.config/opencode`
(`%USERPROFILE%\.config\opencode` on Windows). It defines four primary agents,
one docs subagent, a global permission baseline, and the skills those agents
load.

## Install

Put the repo at `~/.config/opencode`. On Windows that is
`%USERPROFILE%\.config\opencode`.

Restart OpenCode after you change an agent file. Sessions start in `plan`.
Switch agents with `tab`.

## Agents

| Agent | Use it for | Can edit |
| --- | --- | --- |
| plan | Requirements, design, and work breakdown; the default agent | Plan files under `.opencode/plan/` |
| build | Writing and refactoring code and config | Code and config, but not `README.md`, `GLOSSARY.md`, `GLOSSARY-MAP.md`, or `docs/` |
| review | Pre-commit verification and the commit message | Nothing |
| ship | Branch, commit, push, and pull request | Nothing; it writes git and `gh` state only |
| scribe | ADRs, glossary entries, README, and pages under `docs/` | `README.md`, `GLOSSARY.md`, `GLOSSARY-MAP.md`, and `docs/` |

## The loop

1. `plan` clarifies the request and records decisions through `scribe`.
2. `build` implements the change and runs lint.
3. `review` verifies the diff and writes the commit message.
4. `ship` commits, pushes after approval, and opens the PR, then hands off the
   merge.
5. You merge on the web. `ship` verifies the merge, deletes the remote branch
   after approval, and pulls the trunk.

## Human gates

1. `review` must pass before a commit.
2. Push asks for approval every time. `ship` cannot push without it.
3. You merge the PR on the web. Merge is never automated.

## Skills

| Skill | When it runs |
| --- | --- |
| grilling | You want a plan or decision stress-tested, or use a grill phrase |
| grill-with-docs | A grilling round should also write ADRs and glossary entries |
| domain-modeling | A term or decision needs recording in `GLOSSARY.md` or `docs/adr/` |
| git-workflow | `ship` starts a branch, commit, push, or PR |
| requesting-code-review | `review` verifies a diff before commit |
| docs-writing | `scribe` writes or edits a README or a page under `docs/` |
| github-actions | A workflow is added, changed, or reviewed |
| humanizer | Prose is drafted or reviewed |
| powerapps-canvas-yaml-generator | You need Power Apps canvas app YAML |
| report | You want to report an OpenCode bug |

## Docs

- [GLOSSARY.md](GLOSSARY.md): terms used in this repo
- [docs/adr/](docs/adr/): decisions, numbered in sequence
- [docs/workflow.md](docs/workflow.md): what each agent does and where it stops
- [docs/permissions.md](docs/permissions.md): how the permission rules work
- [docs/contributing.md](docs/contributing.md): adding agents, skills, and docs

Design notes live under `docs/`.
