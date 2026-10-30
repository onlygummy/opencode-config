# Page format

Fixed shapes so a reader who learns one page can read the next without relearning the
layout. Every file is English, headings are sentence case and start at H2, and one item
gets one row.

Two markers, used consistently:

- `Not defined` means you checked and the project has no value or no rule for it.
- A path means the claim is traceable. A claim with no path is a guess and does not
  belong in the record.

## INDEX.md

```markdown
# Design system

One sentence saying what this record covers and which app it describes.

Audited: YYYY-MM-DD, against BRANCH_OR_COMMIT.

## Pages

| Page | Covers | Updated |
| --- | --- | --- |
| [tokens.md](./tokens.md) | Raw token standard | YYYY-MM-DD |

## Value sources

| Family | Source | Notes |
| --- | --- | --- |
| Color | `src/styles/tokens.css` | CSS custom properties |

## Reading order

Two or three lines naming which page to open for the three most common tasks.
```

## tokens.md

```markdown
# Tokens

The raw standard. Values only, no usage advice, because that lives on the topical pages.

## Color

| Token | Value | Source | Defined |
| --- | --- | --- | --- |
| `--color-accent` | `#b74aff` | `src/styles/tokens.css:12` | yes |

## Spacing

| Token | Value | Source | Defined |
| --- | --- | --- | --- |

## Typography

| Token | Value | Source | Defined |
| --- | --- | --- | --- |

## Radius and border

## Elevation

## Rules

- The rule that decides when a new token may be added, and who approves it.
```

## color.md

```markdown
# Color

## Roles

| Role | Token | Use for | Avoid |
| --- | --- | --- | --- |

## Contrast pairs

| Foreground | Background | Ratio | Verified by |
| --- | --- | --- | --- |

## Rules

- One line per rule. State the rule, not the reasoning behind it.
```

## typography.md

```markdown
# Typography

## Families

| Family | Token | Fallback stack | Source |
| --- | --- | --- | --- |

## Scale

| Name | Size | Line height | Weight | Use for |
| --- | --- | --- | --- | --- |

## Rules
```

## spacing-layout.md

```markdown
# Spacing and layout

## Scale

| Token | Value | Use for |
| --- | --- | --- |

## Grid

## Breakpoints

| Name | Min width | What changes |
| --- | --- | --- |

## Containers

| Name | Max width | Used on |
| --- | --- | --- |
```

## components.md

```markdown
# Components

One sentence naming the UI layer and the convention for adding a component.

## Inventory

| Component | Path | Props | Variants | States | Use when | Avoid when |
| --- | --- | --- | --- | --- | --- | --- |
| Button | `src/ui/Button.tsx` | `variant`, `size`, `disabled` | primary, ghost | default, hover, active, disabled, focus | ... | ... |

## Composition rules

- What may wrap what, and which component owns spacing.
```

`Path` is relative to the repo root. List every component the UI layer exports, not only
the ones already documented elsewhere. A component with no states gets `Not defined`.

## motion.md

```markdown
# Motion

## Durations

| Token | Value | Use for |
| --- | --- | --- |

## Easing

## What may animate

## Reduced motion

- How the project responds to `prefers-reduced-motion`.
```

## accessibility.md

```markdown
# Accessibility

## Focus

- The focus treatment, with the token or class that produces it.

## Keyboard

| Component | Keys | Behavior |
| --- | --- | --- |

## Labels

- How visible labels and accessible names are supplied.

## Contrast floor

- The minimum ratio the project holds itself to, and where it is checked.
```

## content-voice.md

```markdown
# Content and voice

## Tone

## Error messages

| Situation | Wording | Path |
| --- | --- | --- |

## Empty states

## Confirmations

## Capitalization

## Words to avoid

| Avoid | Use instead | Why |
| --- | --- | --- |
```

Sample strings come from the code, quoted exactly, with the path they live in. Do not
invent a better sentence and present it as the project standard.

## Length

A page over roughly 120 lines usually covers two topics. Split it and link from
`INDEX.md`.
