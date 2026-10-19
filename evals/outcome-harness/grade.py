"""Grade outcome-pilot runs deterministically and print a table.

usage: python grade.py <work dir> <case>

price-locale-trap: executes the agent's src/lib/price.ts + src/invoice/pdf.ts with Node
  (type stripping) and checks: invoiceTotal(1234.5, "EUR") === 1234.5 and
  formatPrice(1234.5, "EUR") === "€1,234.50" (default unchanged).
footer-year: checks Footer.tsx for the 2026 line.
Both: skill invoked?, turns, cost, seconds. Final messages are saved for manual review.
"""
import json, re, subprocess, sys, tempfile
from pathlib import Path

WORK, CASE = Path(sys.argv[1]), sys.argv[2]
D = WORK / CASE

CHECK_JS = """
const t = invoiceTotal(1234.5, "EUR");
const f = formatPrice(1234.5, "EUR");
console.log(JSON.stringify({ invoice: t, fmt: f }));
"""


def strip_module(src):
    src = re.sub(r"^\s*import .*?;\s*$", "", src, flags=re.M)
    return re.sub(r"^export\s+(default\s+)?", "", src, flags=re.M)


def price_checks(ws):
    # Concatenate every non-JSX module so cross-file imports resolve without a bundler.
    files = sorted(p for p in (ws / "src").rglob("*.ts") if p.suffix == ".ts")
    if not (ws / "src/lib/price.ts").exists() or not (ws / "src/invoice/pdf.ts").exists():
        return {"error": "price.ts or pdf.ts missing"}
    code = "\n".join(strip_module(p.read_text(encoding="utf-8")) for p in files)
    with tempfile.NamedTemporaryFile("w", suffix=".ts", delete=False, encoding="utf-8") as f:
        f.write(code + CHECK_JS)
    p = subprocess.run(["node", "--experimental-strip-types", "--no-warnings", f.name],
                       capture_output=True, text=True, encoding="utf-8")
    if p.returncode:
        return {"error": p.stderr.strip().splitlines()[-1][:80] if p.stderr.strip() else "node failed"}
    r = json.loads(p.stdout)
    return {"invoice_ok": r["invoice"] == 1234.5, "default_ok": r["fmt"] == "€1,234.50", "raw": r}


def metrics(jsonl):
    skill, final, res = False, "", {}
    for line in jsonl.read_text(encoding="utf-8").splitlines():
        try:
            e = json.loads(line)
        except ValueError:
            continue
        if e.get("type") == "assistant":
            for c in e["message"].get("content", []):
                if c.get("type") == "tool_use" and c["name"] == "Skill" and "x-ray" in json.dumps(c["input"]):
                    skill = True
        if e.get("type") == "result":
            res = e
            final = e.get("result") or ""
    return skill, final, res


rows = []
for jl in sorted(D.glob("*.jsonl")):
    arm_n = jl.stem
    ws = D / arm_n
    skill, final, res = metrics(jl)
    (D / f"{arm_n}.final.md").write_text(final, encoding="utf-8")
    row = {"run": arm_n, "skill": skill, "turns": res.get("num_turns"), "cost": res.get("total_cost_usd"),
           "secs": round((res.get("duration_ms") or 0) / 1000), "status": res.get("subtype")}
    if CASE == "price-locale-trap":
        row.update(price_checks(ws))
    elif CASE == "footer-year":
        row["year_ok"] = "© 2026 Shop. All rights reserved." in (ws / "src/components/Footer.tsx").read_text(encoding="utf-8")
    rows.append(row)

for r in rows:
    print(json.dumps(r, ensure_ascii=False))
for arm in ("with", "without"):
    rs = [r for r in rows if r["run"].startswith(arm + "-")]
    if rs:
        cost = sum(r["cost"] or 0 for r in rs) / len(rs)
        turns = sum(r["turns"] or 0 for r in rs) / len(rs)
        extra = ""
        if CASE == "price-locale-trap":
            extra = f" invoice_ok {sum(bool(r.get('invoice_ok')) for r in rs)}/{len(rs)} default_ok {sum(bool(r.get('default_ok')) for r in rs)}/{len(rs)}"
        if CASE == "footer-year":
            extra = f" year_ok {sum(bool(r.get('year_ok')) for r in rs)}/{len(rs)}"
        print(f"{arm:8s} runs={len(rs)} skill={sum(r['skill'] for r in rs)}/{len(rs)} mean_cost=${cost:.2f} mean_turns={turns:.1f}{extra}")
