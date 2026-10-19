"""Build two copies of a small fake shop repo for X-RAY trigger tests.

usage: python make_fixture.py <xray_repo> <out_dir>
Creates <out_dir>/skill-only and <out_dir>/skill-plus-pointer.
"""
import shutil, subprocess, sys
from pathlib import Path

XRAY, OUT = Path(sys.argv[1]), Path(sys.argv[2])

FILES = {
    "package.json": '{\n  "name": "shop",\n  "private": true,\n  "scripts": {"test": "vitest run", "typecheck": "tsc --noEmit"}\n}\n',
    "README.md": "# Shop\n\nStorefront and order service.\n\n- `formatPrice` is display only.\n- HTTP retries use exponential backoff.\n",
    "src/lib/price.ts": 'export function formatPrice(amount: number, currency: string): string {\n  return new Intl.NumberFormat("en-US", { style: "currency", currency }).format(amount);\n}\n',
    "src/invoice/pdf.ts": 'import { formatPrice } from "../lib/price";\nexport function invoiceTotal(total: number, cur: string): number {\n  return parseFloat(formatPrice(total, cur).replace(/[^0-9.]/g, ""));\n}\n',
    "src/pricing.ts": "export function applyDiscount(total: number, pct: number): number {\n  return total * (1 - pct / 100);\n}\n",
    "src/payments/stripe.ts": 'export async function charge(amount: number): Promise<string> {\n  if (amount <= 0) throw new Error("invalid amount");\n  return "ch_123";\n}\n',
    "src/payments/retry.ts": "export async function withRetry<T>(fn: () => Promise<T>, tries = 3): Promise<T> {\n  for (let i = 0; ; i++) {\n    try { return await fn(); } catch (e) {\n      if (i >= tries - 1) throw e;\n      await new Promise(r => setTimeout(r, 2000));\n    }\n  }\n}\n",
    "src/routes/orders.ts": 'import { applyDiscount } from "../pricing";\nimport { charge } from "../payments/stripe";\nexport async function createOrder(total: number, discountPct: number) {\n  const amount = applyDiscount(total, discountPct);\n  const id = await charge(amount);\n  return { id, amount };\n}\n',
    "src/auth/session.ts": "export const SESSION_TTL_SECONDS = Number(process.env.SESSION_TTL ?? 30 * 60);\n",
    "src/auth/permissions.ts": 'export type Role = "org_owner" | "team_admin" | "member";\nexport function canDeleteProject(role: Role): boolean {\n  return role === "org_owner";\n}\n',
    "src/users/validateUser.ts": 'import { db } from "../db";\nexport async function validateUser(email: string) {\n  if (!email.includes("@")) throw new Error("bad email");\n  const u = await db.users.find(email);\n  return u ?? db.users.create({ email });\n}\n',
    "src/db.ts": "export const db: any = {};\n",
    "src/models/user.ts": "export interface User { id: string; email: string; fullname: string }\n",
    "src/components/Nav.tsx": "export function Nav() { return <nav className=\"nav\">...</nav>; }\n",
    "src/components/Footer.tsx": "export function Footer() { return <footer>(c) 2025 Shop</footer>; }\n",
    "src/pages/Dashboard.tsx": 'import { Nav } from "../components/Nav";\nexport const Dashboard = () => <Nav />;\n',
    "src/pages/Settings.tsx": 'import { Nav } from "../components/Nav";\nexport const Settings = () => <Nav />;\n',
    "src/flags.ts": 'export const flags = { new_checkout: true };\n',
    "src/errors.ts": 'export const MSG = { cartEmpty: "Your cart is empty" };\n',
}

POINTER = """## Changing existing code
Before editing existing code, explore the relevant files first. Then use the `x-ray` skill:
size the change by what it could break, check claims against the code, and report only
what you actually verified. Skip it for trivial edits where nothing else can break.
"""

SKILL_PARTS = ["SKILL.md", "LICENSE", "references", "templates"]  # inside skills/x-ray/

for cond in ["skill-only", "skill-plus-pointer"]:
    root = OUT / cond
    if root.exists():
        shutil.rmtree(root)
    for rel, text in FILES.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
    dest = root / ".claude" / "skills" / "x-ray"
    dest.mkdir(parents=True)
    for part in SKILL_PARTS:
        src = XRAY / "skills" / "x-ray" / part
        (shutil.copytree if src.is_dir() else shutil.copy)(src, dest / part)
    if cond == "skill-plus-pointer":
        (root / "CLAUDE.md").write_text(POINTER, encoding="utf-8")
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    subprocess.run(["git", "add", "-A"], cwd=root, check=True)
    subprocess.run(["git", "-c", "user.name=fixture", "-c", "user.email=f@x", "commit", "-qm", "fixture"], cwd=root, check=True)
    print("built", root)
