# PALETTE'S JOURNAL - CRITICAL LEARNINGS ONLY

## 2026-02-23 - Accessibility of Single-Letter Text Buttons
**Learning:** Text-based toggle buttons like 'B' (Bold) and 'I' (Italic) rely heavily on visual grouping context. Without `aria-label`, screen readers only announce the single letter, which is confusing and lacks semantic meaning.
**Action:** Always add `aria-label` and `aria-pressed` to single-letter or icon-only toggle buttons to ensure they are self-describing for assistive technology.
