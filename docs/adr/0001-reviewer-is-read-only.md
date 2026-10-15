# The review agent is read-only and does not commit

`requesting-code-review` v2.1.0 tells the reviewer to run an auto-fix loop (Step 7)
and then `git add -A && git commit` (Step 8). The review agent does neither. Its
permission set denies `edit`, `git add`, and `git commit`, and it runs as a
`primary` agent, so no parent can launch it as a subagent to fix anything either.
There is no path from "the reviewer found an issue" to "the reviewer fixed it"
inside one session, so Step 7 is skipped and Step 8 generates the commit message
only.

Two alternatives were considered. Granting `build` commit permission fails
because `build` and `review` are separate sessions: `build` cannot see the
reviewer's verdict, so it would commit unreviewed code. Making `build` a
subagent so the reviewer could dispatch fixes would let the reviewer approve its
own delegate's work, which defeats the point of the fresh-context review.

The cost is real: after a failed review the user switches to `build`, applies the
fixes, switches back, and reviews again, then runs the commit by hand. That
round-trip buys the guarantee that the reviewer never touches the code it judges.
