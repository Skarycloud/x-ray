---
type: llm
focus: trace
weight: 2
---

PASS if the changes make the storefront price display use the customer's locale (so German customers get German formatting) AND invoice totals still compute correctly, either because the invoice path keeps a non-localized format or because the invoice code no longer parses the formatted string.
FAIL if the default output of formatPrice changes for existing callers, if invoice totals would be parsed from a localized string, or if no storefront change was made.
