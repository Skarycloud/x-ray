#!/usr/bin/env bash
# A trivial, isolated copy change. X-RAY should add little or no overhead here.
set -euo pipefail

mkdir -p src/components src/pages

cat > package.json <<'EOF'
{ "name": "site", "private": true, "scripts": { "test": "vitest run" } }
EOF

cat > src/components/Footer.tsx <<'EOF'
export function Footer() {
  return <footer className="footer">© 2025 Shop. All rights reserved.</footer>;
}
EOF

cat > src/pages/Home.tsx <<'EOF'
import { Footer } from "../components/Footer";
export const Home = () => <main><h1>Shop</h1><Footer /></main>;
EOF

git init -q
git add -A
git -c user.name=fixture -c user.email=fixture@example.com commit -qm "fixture"
