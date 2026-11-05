# Build dispatches review and ship checks the verdict artifact

`review` is now `mode: all`, so `build` dispatches it as a subagent after the
commit instead of the user switching tabs and relaying findings. A dispatched run
still starts in a child session with no parent history, so the independence that
[ADR 0001](0001-reviewer-is-read-only.md) records is unchanged. `build` already
writes the commit, per [ADR 0020](0020-build-writes-the-commit.md), so the
reviewer checks a committed range and can run right after the commit. `review`
stays read-only for code; its one write is the verdict artifact at
`.opencode/review/<branch>.json`, with `/` in the branch name replaced by `-`.
The artifact holds `verdict` (`passed`, `failed`, or `skipped`), the full `commit`
SHA, the `branch`, and a `findings` count. A `skipped` verdict also carries a
`reason`.

`build` holds no edit rule for that path, and the edit and write tools are denied
for `*.opencode/review/*.json` after its broad allow. `review` holds a narrow
allow after its own broad deny. `build` also holds a broad shell allow, so a
shell write to the path is not blocked. That gap is a recorded residual risk,
not a guarantee: the artifact records that a review ran for that commit and
branch, and it is not a cryptographic proof.

`ship` reads the artifact before any push and refuses unless `verdict` is
`passed`, `findings` is `0`, `commit` equals `git rev-parse HEAD`, and `branch`
equals `git rev-parse --abbrev-ref HEAD`. A docs-only change is exempt only when
the path list from `git diff --name-only <merge-base>...HEAD` is non-empty and
every path is under `docs/` or is one of `README.md`, `GLOSSARY.md`, or
`GLOSSARY-MAP.md`. `agents/` and `skills/` are never exempt, because their
Markdown carries permissions and agent instructions, and an empty range is not
docs-only. A config change (`opencode.jsonc`, `cli.json`, `agents/`) gets the
full pipeline. If `ship` had to write the commit itself, the artifact cannot
match the new commit yet, so it stops and asks for a review of that commit.

Four alternatives were rejected. Letting `build` write the verdict with the edit
tool would remove the tool-level separation, so the record would rest on the
prompt alone. Letting `ship` trust `build`'s report leaves no durable record, and
the report goes stale after an amend. Letting `review` fix or commit its own
findings fails for the reason ADR 0001 records: a reviewer that lands its own
findings is no longer a reviewer. Keeping `review` primary-only keeps the tab
round trip and leaves no record.

An amend changes HEAD, so the artifact has to be regenerated, and `ship` rejects
a stale one rather than accepting it. `build` re-dispatches `review` after an
amend and stops after two failed rounds. The artifact directory is gitignored.
This change adds no auto-merge or auto-delete; those are a later decision.

[ADR 0001](0001-reviewer-is-read-only.md) denies `edit` for `review` and runs it
as a `primary` agent, and
[ADR 0007](0007-vcs-agent-owns-commit-and-push.md) repeats the edit claim. This
ADR amends both: `review` now holds one narrow edit allow for the verdict
artifact and is `mode: all`. ADR 0001 and ADR 0007 stay as written.
