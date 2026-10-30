# The record owns the design tokens

`docs/design-system/tokens.md` is the token standard, and code follows it. The
first bootstrap is the exception: nothing exists to follow yet, so values are
extracted from the code and written down, and after that the record leads. When
code and the record disagree, the gap is classified as record stale, code
off-standard, or a deliberate change, and the class decides who fixes it. A
deliberate change updates the record first and the code second.

The reason is that a reader, an agent, and a reviewer all need one place to look
up a value. A record that mirrors code rots without anyone noticing, because the
copy is only checked when someone happens to open it. A record that leads gets
checked by whoever changes a token.

Two alternatives were rejected. Code as the source of truth makes the record a
snapshot nobody maintains, and every audit degenerates into a copy job. A
duplicate `tokens.json` beside the page is a second copy to synchronize and a
file format nobody opens when reading the system.

The bootstrap is the exception, so it has to extract the values completely. A
half-extracted record leads wrongly from the day it is written.
