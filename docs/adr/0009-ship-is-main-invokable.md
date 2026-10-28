# Ship is a main agent, not an @mention subagent

The agent that writes history started as a subagent reached with `@vcs`. ADR
0007 chose that shape so the commit step could not happen by accident: a
subagent runs only when a parent session dispatches it, and nothing in the
ordinary coding loop does that. The cost showed up in daily use. A subagent
opens a child session with no memory of the conversation, so it rebuilds the
reason for the change by reading the diff, which is the one thing a commit
message should not do. The user also had to remember a mention syntax, and
`build` needed a `subagent` allow that existed for this single agent and
nothing else.

It is now a primary agent named `ship`. Switching to it with `tab` gives it the
conversation the commit body is supposed to describe, and it removes the
mention syntax and the extra permission rule from `build`. The gate is
unchanged in substance but moves: it used to be "type the mention", now it is
"switch the agent". Both are deliberate, and neither happens during a normal
coding turn. The default agent stays `plan`, so a fresh session never starts in
`ship`.

Keeping `mode: all` was the other option, which would have preserved `@vcs`
alongside the tab. It was rejected because two entry points need two permission
stories for one capability, and the mention path was the one nobody needed. The
`edit` deny and the `push: ask` gate still carry the safety of the change.
Nothing about merge, force push, `rebase`, `commit --amend`, branch deletion, or
release creation changes; those stay denied per ADR 0007.

The name changed with the mode. `vcs` names the tool, `ship` names the state the
user is trying to reach, and the tab list shows the finished action rather than
the machinery. The rename covers the agent file, its description, the glossary
term, and the `build` permission that referenced it by name. ADR 0007 keeps its
old wording because it records what was true when it was written; this record
supersedes only its invocation model.

Cost: muscle memory for `@vcs` now fails with an unresolved mention, and any
note outside this repo that quotes the old command needs a manual edit.
