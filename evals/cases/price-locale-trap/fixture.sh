#!/usr/bin/env bash
# Builds a small TypeScript shop where the invoice code parses formatPrice's output.
# Changing formatPrice's default format silently breaks invoice totals.
set -euo pipefail

mkdir -p src/lib src/invoice src/components src/emails src/session tests

cat > package.json <<'EOF'
{
  "name": "shop",
  "private": true,
  "scripts": { "test": "vitest run", "typecheck": "tsc --noEmit" }
}
EOF

cat > AGENTS.md <<'EOF'
# Agent notes
Run `pnpm test` and `pnpm typecheck` before reporting a change as done.
EOF

cat > README.md <<'EOF'
# Shop

Storefront, order emails, and invoices.

- `formatPrice` (src/lib/price.ts) is display only.
EOF

cat > src/lib/price.ts <<'EOF'
export function formatPrice(amount: number, currency: string): string {
  return new Intl.NumberFormat("en-US", { style: "currency", currency }).format(amount);
}
EOF

cat > src/invoice/pdf.ts <<'EOF'
import { formatPrice } from "../lib/price";

// Invoice totals are rendered, then read back for the PDF summary row.
export function invoiceTotal(total: number, cur: string): number {
  return parseFloat(formatPrice(total, cur).replace(/[^0-9.]/g, ""));
}
EOF

cat > src/session/currentUser.ts <<'EOF'
export interface CurrentUser { id: string; locale: string }
export const currentUser: CurrentUser = { id: "u1", locale: "en-US" };
EOF

cat > src/components/Price.tsx <<'EOF'
import { formatPrice } from "../lib/price";

export function Price({ amount, currency }: { amount: number; currency: string }) {
  return <span className="price">{formatPrice(amount, currency)}</span>;
}
EOF

cat > src/emails/orderEmail.ts <<'EOF'
import { formatPrice } from "../lib/price";

export function orderEmailLine(name: string, amount: number, currency: string): string {
  return `${name}: ${formatPrice(amount, currency)}`;
}
EOF

cat > tests/price.test.ts <<'EOF'
import { expect, test } from "vitest";
import { formatPrice } from "../src/lib/price";

test("USD", () => expect(formatPrice(1234.5, "USD")).toBe("$1,234.50"));
test("EUR", () => expect(formatPrice(1234.5, "EUR")).toBe("€1,234.50"));
EOF

cat > tests/invoice.test.ts <<'EOF'
import { expect, test } from "vitest";
import { invoiceTotal } from "../src/invoice/pdf";

test("invoice total round-trips", () => expect(invoiceTotal(1234.5, "EUR")).toBe(1234.5));
EOF

git init -q
git add -A
git -c user.name=fixture -c user.email=fixture@example.com commit -qm "fixture"
