# Per-agent git rules live in the agent file, not the global config

The global `permissions` list in `opencode.jsonc` holds the shared baseline:
reads, globs, greps, web fetches, skills, and a read-only shell block. Git is
the exception. Every git rule an agent needs sits in `agents/<agent>.md`, and
the global list keeps only `git *` as an allow for agents that never override
it.

The reason is ordering. Rules are evaluated in load order and the last match
wins, with agent rules appended after global rules. Both `plan` and `review`
declare `{ "action": "shell", "resource": "*", "effect": "deny" }` in their own
file so shell access is opt-in per command. That deny is evaluated after every
global allow, which means a global shell allow has no effect inside either
agent. Repeating the read-only list in each agent file is the only way to keep
the blanket deny and still grant specific commands. `build` is the opposite
case: it allows shell wholesale and then denies `git *`, so it needs denies
rather than allows, and those denies must not leak into the other two agents.

The same ordering rule creates a second constraint inside one agent file. A
write form of an allowed command has to be denied after the allow that would
otherwise cover it, which is why `git branch -d`, `git tag -a`, and
`git * --output*` sit at the end of the block instead of next to their read
forms.

Two gaps are accepted rather than patched. A resource pattern matches the whole
command string, so `git -C <path> commit` does not match `git commit*`, and an
agent that can reach `git -C` can commit. The baseline worktree recipe therefore
uses `Push-Location` plus plain `git`. The same limitation is why
`--output=<file>` needs its own deny instead of a flag-level rule. Closing
either gap would need argument-aware matching, which the permission layer does
not offer.

This record was written after the rules, from the comments that already
justified them, to replace the `docs/adr/0005` reference that configuration
pointed at while no such file existed.
