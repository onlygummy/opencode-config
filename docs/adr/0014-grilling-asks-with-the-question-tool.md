# Grilling asks with the question tool

The `grilling` skill asked the whole frontier as numbered plain text with a `➡️`
recommendation per question. The user had to type every answer, and the choices
were buried in prose.

Now the skill sends the frontier in one `question` call, one entry per decision,
with two to four options and the recommended one first, marked `(Recommended)`.
`multiple: true` is used only for non-exclusive choices. Each question has a
header, the question text, and a list of options; the user picks an option or
types a custom answer, moves between the questions, and submits all answers at
once ([OpenCode tools](https://opencode.ai/docs/tools/)). Plain text stays the
fallback for open-ended questions whose answers are not enumerable, and for
environments without the tool. No permission change is needed, because the
question tool is enabled by default.

Batching removes typing, the options make the decision space visible, and the
user still has a free-form field. Three alternatives were rejected. Text only
keeps the typing cost and hides the choices. One call per question adds round
trips. Offering options for every question, including open ones, steers the
answer with invented options. The accepted cost is that a recommended option is
a nudge, and a question with a badly guessed option set is worse than a
plain-text question. The fallback rule is what keeps that in check.
