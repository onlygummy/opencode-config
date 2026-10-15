# Build does not run tests, only lint and typecheck

The build agent validates its own edits with lint and typecheck (`eslint`,
`ruff`, `mypy`, `tsc`, `cargo clippy`, `go vet`) and stops there. It does not
run test suites as a default step. Tests belong to the review agent's
pre-commit pipeline, which already runs them against a baseline worktree to
separate new failures from old ones. Keeping the implementer out of that loop
preserves the split: build produces code and quick static feedback, review
verifies behavior with fresh context.

The enforcement is two-layered on purpose. The system prompt carries the
"Verify (lint only)" rule as the primary control, because permission patterns
match the literal command string and a test command wrapped in a script or
alias escapes them. The permission layer is the backstop: an ordered list of
`effect: "ask"` rules for common test runners (pytest, npm/yarn/pnpm/bun test,
vitest, jest, cargo test, go test, dotnet test, deno test, make test) sits
after the broad shell allow so the last match wins.

The effect is `ask`, not `deny`. A deny would make test runs from build
impossible even when the user explicitly wants one; `ask` keeps that escape
hatch while making the default path lint-only. Lint and typecheck need no
explicit allow rules: the existing broad shell allow already covers them and
none of the test patterns match them, so adding them would be a no-op.

The cost is that the test-runner list is not exhaustive by nature. A script
named `check` or `verify` that runs tests internally will pass through
unchallenged. That gap is accepted because the prompt-level rule, not the
pattern list, is the real constraint.
