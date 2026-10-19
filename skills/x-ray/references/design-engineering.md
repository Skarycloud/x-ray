# Design engineering

Design quality and functional correctness are both requirements. A UI change that works but breaks the layout at 375px, drops focus styles, or invents a new grey has a defect.

This reference applies when a change touches anything users see or interact with.

## 1. Learn the existing system first

Before writing UI code, find:
- **Tokens**: color, spacing, radius, shadow, font size, z-index, duration/easing. Look in CSS custom properties, Tailwind config, theme files, `tokens.json`.
- **Components**: the existing Button, Input, Dialog, and so on. Use them; don't rebuild them.
- **Patterns**: how similar screens handle layout, loading, empty, and error states.
- **Breakpoints and supported viewports.**
- **Theme modes**: light/dark, high contrast, RTL.

Rule: **don't introduce a raw value when a token exists.** If no token fits, use the nearest one and flag the gap rather than inventing `#6b6f76` or `margin: 13px`.

## 2. Review checklist

### Hierarchy
- [ ] One clear primary action per view or region.
- [ ] Visual weight (size, color, contrast) matches importance.
- [ ] Related items are grouped; unrelated items are separated by space, not just lines.

### Typography
- [ ] Sizes and weights come from the type scale.
- [ ] Body text line length stays readable (roughly 45–80 characters).
- [ ] Long strings, translations, and user content wrap or truncate deliberately (test a long name, a long word, an empty value).

### Spacing and layout
- [ ] Spacing uses the scale; similar elements have identical spacing.
- [ ] Alignment is consistent with neighbors.
- [ ] No horizontal scroll at the narrowest supported width.

### Interaction states
For every interactive element:
- [ ] default, hover (pointer devices only), **focus-visible**, active/pressed, disabled
- [ ] loading (with no layout shift), success, error
- [ ] empty state for lists and data views

### Accessibility
- [ ] Semantic elements (`button` for actions, `a` for navigation, real `label`s).
- [ ] All functionality reachable by keyboard; focus order follows visual order; focus visible.
- [ ] Text contrast meets WCAG 2.2 AA (4.5:1 normal text, 3:1 large text and UI components).
- [ ] Images have meaningful `alt` or `alt=""` if decorative; icon-only buttons have accessible names.
- [ ] Dialogs trap focus, close on Esc, and return focus to the trigger.
- [ ] Touch targets are adequately sized (WCAG 2.2 sets 24×24 CSS px as the AA minimum; 44×44 is a common comfortable target).

### Responsiveness
- [ ] Checked at narrowest supported width (often 320–375px) and a wide desktop width.
- [ ] Content reflows; nothing is clipped or overlapping.
- [ ] Inputs don't trigger unwanted zoom on mobile (font size ≥ 16px on iOS).

## 3. Motion

Animate only when motion helps the user. Typical purposes:
- **Feedback**: confirm an action happened (button press, toast).
- **Orientation**: show where something came from or went (panel slides from its trigger).
- **Continuity**: preserve context across a state change.

Decision rules:
| Situation | Guidance |
| --- | --- |
| Action users repeat many times a day (keyboard shortcut, command palette) | Little or no animation; speed matters more than polish |
| UI responding to user input | Short, roughly 150–250ms; ease-out so it starts fast |
| Elements entering vs exiting | Exits can be faster than entrances |
| Interruptible interactions (drag, toggle spam) | Use transitions or springs that retarget, not fixed keyframes that must finish |
| Properties | Prefer `transform` and `opacity`; avoid animating layout properties (`width`, `top`, `height`) on hot paths |
| Reduced motion | Respect `prefers-reduced-motion`: remove or replace large movement with opacity changes |

Match existing duration and easing tokens when the project has them.

## 4. Verify visually

Code review can't confirm visual correctness. When tooling allows:
1. Run the app or a component story.
2. Inspect the changed view at the viewports listed above, in each theme the product supports.
3. Tab through the changed region with the keyboard.
4. Trigger loading, error, and empty states (mock or throttle if needed).
5. Capture before/after screenshots when the change is visual and the tooling supports it.

If none of this is possible, say so in the report: "Visual result not inspected; verified only by code review."

## Example findings (from a diff review)

```text
- New card uses padding: 18px; spacing scale is 4/8/12/16/24 → use 16 (token --space-4).
- Icon button "×" has no aria-label → add aria-label="Close".
- Hover color added, no :focus-visible style → keyboard users get no indicator.
- Modal fades in over 400ms with ease-in → feels sluggish; use the existing --duration-fast (150ms) ease-out.
- Price column overflows at 375px with 7-digit values → allow wrap or reduce to compact format.
```
