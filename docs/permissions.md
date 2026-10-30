# Permissions

A permission rule is one triple:

```
{ action, resource, effect }
```

`action` is what the agent wants to do, such as `edit`, `read`, `shell`, or
`subagent`. `resource` is a path or a command string. `effect` is `allow`,
`deny`, or `ask`.

Rules are ordered. The global rules in `opencode.jsonc` load first, an agent's
rules append after them, and the last rule that matches wins. A broad deny
belongs before the narrow allow that must beat it. A broad allow belongs before
the narrow deny that must beat it. Order is the whole mechanism, so moving a
line changes behavior.

## Global baseline

| Action | Effect |
| --- | --- |
| `edit` | deny |
| `read` | allow |
| `glob` | allow |
| `grep` | allow |
| `skill` | allow |
| `subagent` | deny |
| `shell` | deny, with a read-only allowlist |
| `webfetch` | allow |

Per-agent git rules live in `agents/<agent>.md`, not in the global list. The
reason is ordering: an agent that denies shell has to re-grant each read-only
command after its own deny. See [ADR 0005](adr/0005-per-agent-git-rules.md).

## Agent scope

| Agent | Edit scope | Shell scope | Subagent scope |
| --- | --- | --- | --- |
| `plan` | Files matching `*.opencode/plan/*` | Read-only git and read-only file commands | `scribe`, `explore`, `general` |
| `build` | Code and config; docs files are denied | Full allow, but `git *` is denied except read forms, `git add`, `git rm`, `git mv`, and `git stash`; test runners ask | `scribe`, `design-surveyor`, `design-steward` |
| `review` | Nothing | Read-only git, test runners, and lint; no `add`, `commit`, or `push` | None |
| `ship` | Nothing | Git write path and `gh pr` read and create; `push` and remote branch deletion ask, merge and force push are denied | None |
| `scribe` | `docs/` except `docs/design-system/`, plus `README.md` | Nothing | None |

## How patterns match

Patterns are globs over the whole normalized path or command string. `*` spans
`/`, so `*docs/*` matches a file at any depth under `docs/`. A pattern with no
leading `*` matches only paths that begin with those characters, which is why a
path outside the project needs the leading wildcard. On Windows, pattern
matching ignores case, so `*README.md` also matches a file named `readme.md`.
Name a template `readme-template.md` when only the README itself should be
protected. A shell rule matches a command string, not a single argument.

Pipelines are checked one stage at a time. Each command between pipes is its own
resource, so an allow has to cover every stage. See
[ADR 0006](adr/0006-read-only-pipeline-allowlist.md).

## Read-only escapes

A wildcard allow can inherit a write form hidden inside it. `git branch*` would
also permit `git branch -d`, so `ship` follows that allow with an explicit deny
for `-d` and `-D`. `git diff --output=<file>` writes a file through a command
that reads as inspection, so `plan`, `review`, and `ship` deny `git * --output*`.

The unstage rule shows the fix. `git restore --staged -W` touches only the
index under `--staged`, but the `-W` flag reaches the worktree without matching
a deny written for `--worktree`. `git reset -- <path>` replaced it: after `--`,
every word is a pathspec, so the allowed form has no flag surface. See
[ADR 0010](adr/0010-ship-can-unstage.md).

## Residual risk

A pattern matches the whole command string, so argument-level rules are not
expressible. `git -C <path> commit` does not match `git commit*`, and an agent
that can reach `git -C` can commit. `--output=<file>` needs its own deny because
a rule cannot say "this flag, in this position". Closing either gap would need
argument-aware matching, which the permission layer does not offer. Both are
accepted and recorded in [ADR 0005](adr/0005-per-agent-git-rules.md).
