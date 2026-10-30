# OpenCode agent configuration

This repo configures OpenCode: four primary agents (plan, build, review, ship),
three subagents (scribe, design-surveyor, design-steward), the global permission
baseline, and the skills those agents load. The domain is agent behavior, not
application code.

## Language

**Agent**: One named assistant profile: a system prompt, a mode, and a permission
set. This repo defines four primary agents and three subagents. The reviewer runs
in a fresh context with no history of how the code it checks was written.

_Avoid_: assistant, bot

**Permission rule**: One ordered `{action, resource, effect}` triple. Global rules
load first, agent rules append after them, and the last rule that matches wins. A
broad deny belongs before the narrow allow that must beat it.

_Avoid_: permission block, access control entry

**Pipeline stage**: One command between pipes or statement separators. The
scanner emits each stage as its own shell resource, so an allow has to cover
every stage of a pipeline. A rule written for the whole line never matches.

_Avoid_: sub-command, pipe part

**Mode**: Where an agent runs. `primary` means it is the main agent of a session
and the user switches to it by tab. `subagent` means a parent agent launches it in
a child session. `all` means either.

_Avoid_: role, type

**Skill**: A Markdown instruction file with an ID derived from its path, loaded on
demand by the `skill` tool. It holds reusable behavior that would bloat every
agent prompt if copied inline. Its `description` decides whether the model sees it.

_Avoid_: plugin, command, helper

**Independent reviewer**: The review agent. It verifies a diff with no shared
context with the implementer and holds no `edit` permission, so it reports issues
instead of fixing them.

_Avoid_: checker, QA bot

**Baseline**: The test and lint failure count a repo already had before a change.
Only failures above the baseline block a commit.

_Avoid_: golden state, reference run

**Frontier**: In a grilling interview, the set of decisions whose prerequisites are
already settled. A question that depends on an unanswered one belongs to a later
round.

_Avoid_: open questions, backlog

**Domain doc**: `GLOSSARY.md`, `GLOSSARY-MAP.md`, and every file under `docs/`,
including `docs/adr/`, except the design system record. The scribe subagent
writes them; no primary agent does, and the design system record has its own
writer.

_Avoid_: vault, notes

**Scribe**: The subagent that writes the docs tree. It owns the format and the
numbering, never the decision, so a caller has to supply a brief.

_Avoid_: docs bot, document writer

**Design system record**: The pages under `docs/design-system/` that state a
project's tokens, components, accessibility rules, and UX voice. Owned by
`design-steward`.

_Avoid_: style guide, design docs

**Surveyor**: The `design-surveyor` subagent. It reads a project and reports what
exists, and holds no write permission.

_Avoid_: auditor, inspector

**Steward**: The `design-steward` subagent. It is the only writer of the design
system record.

_Avoid_: design owner, style keeper

**Design drift**: A disagreement between the record and the code, classified as
record stale, code off-standard, or a deliberate change. The class decides who
fixes it.

_Avoid_: inconsistency, mismatch

**Token authority**: The rule that `docs/design-system/tokens.md` is the standard
and code follows it. Bootstrap extracts from code first because the record does
not exist yet.

_Avoid_: token sync, source of truth

**Usage doc**: `README.md`. It explains how to use the config and is not a place
for design notes; those go under `docs/`.

_Avoid_: guide, manual

**Read-only escape**: A command pattern that still lets an agent without `edit`
permission change state, such as `git branch -d` or `git diff --output=<file>`.
An allow written as a wildcard inherits every write form hidden inside it.

_Avoid_: permission bypass, hole

**Residual risk**: A known gap in the permission layer that is accepted and
recorded rather than patched, because a resource pattern matches a whole command
string and cannot express argument-level rules.

_Avoid_: known issue, accepted limitation

**Trunk**: The branch a repo treats as its mainline. Read it from `origin/HEAD`
rather than assuming `main`, because a repo may keep its trunk on
`development`. Short-lived branches are cut from it and merged back into it.

_Avoid_: main branch, master

**Short-lived branch**: A branch that carries one change and lives hours to a
couple of days before merging into the trunk. The thing it is not is a
long-lived integration branch, which holds unmerged work for weeks.

_Avoid_: dev branch, feature branch

**Ship agent**: The `ship` main agent that owns branch, commit, push, and pull
request. It is a primary agent selected by tab, not a subagent, and it starts
only when the user switches to it deliberately. It holds git and gh permissions
of its own so the other agents stay read-only, and it stops before merge.

_Avoid_: VCS agent, git bot, commit bot

**Commit gate**: The approval point before an action that cannot be undone from
the machine. Here it is push: a local commit can still be fixed, a pushed one
is already on the remote.

_Avoid_: approval step, checkpoint

**Release tag**: A tag the user creates by hand when they want a fixed snapshot
of the config. No workflow creates tags in this repo.

_Avoid_: release PR, version PR
