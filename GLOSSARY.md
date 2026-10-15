# OpenCode agent configuration

This repo configures OpenCode: three primary agents (plan, build, review), the
global permission baseline, and the skills those agents load. The domain is agent
behavior, not application code.

## Language

**Agent**: One named assistant profile: a system prompt, a mode, and a permission
set. This repo defines three. The reviewer runs in a fresh context with no history
of how the code it checks was written.

_Avoid_: assistant, bot

**Permission rule**: One ordered `{action, resource, effect}` triple. Global rules
load first, agent rules append after them, and the last rule that matches wins. A
broad deny belongs before the narrow allow that must beat it.

_Avoid_: permission block, access control entry

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

**Domain doc**: `GLOSSARY.md`, `GLOSSARY-MAP.md`, and files under `docs/adr/`. These
are the only files the plan agent writes outside plan files.

_Avoid_: vault, notes

**Read-only escape**: A command pattern that still lets an agent without `edit`
permission change state, such as `git branch -d` or `git diff --output=<file>`.
An allow written as a wildcard inherits every write form hidden inside it.

_Avoid_: permission bypass, hole

**Residual risk**: A known gap in the permission layer that is accepted and
recorded rather than patched, because a resource pattern matches a whole command
string and cannot express argument-level rules.

_Avoid_: known issue, accepted limitation
