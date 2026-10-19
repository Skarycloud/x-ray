"""Score trigger results: did the session invoke the x-ray skill?

usage: python score.py <results_dir>
"""
import json, sys
from collections import defaultdict
from pathlib import Path

RES = Path(sys.argv[1])
table = defaultdict(dict)
meta = {}
for f in sorted(RES.glob("*.jsonl")):
    cond, qid, n = f.stem.split("__")
    hit, other, tools, err = False, set(), [], None
    for line in f.read_text(encoding="utf-8").splitlines():
        try:
            ev = json.loads(line)
        except ValueError:
            continue
        if ev.get("type") == "system" and ev.get("subtype") == "init":
            meta = {"model": ev.get("model"), "version": ev.get("claude_code_version"),
                    "skills_listed": "x-ray" in json.dumps(ev.get("skills", ev.get("slash_commands", [])))}
        if ev.get("type") == "assistant":
            for c in ev.get("message", {}).get("content", []):
                if c.get("type") == "tool_use":
                    tools.append(c["name"])
                    if c["name"] == "Skill":
                        s = json.dumps(c.get("input", {}))
                        if "x-ray" in s:
                            hit = True
                        else:
                            other.add(c.get("input", {}).get("skill", s))
        if ev.get("type") == "result" and ev.get("is_error"):
            err = ev.get("subtype")
    table[(qid, n)][cond] = ("Y" if hit else "n") + ("!" if err else "") + (f" (other: {','.join(sorted(other))})" if other else "")

print("meta:", meta)
for cond in ["skill-only", "skill-plus-pointer"]:
    for grp in "TN":
        vals = [v[cond] for (q, n), v in table.items() if q.startswith(grp) and cond in v]
        print(f"{cond:20s} {'should' if grp=='T' else 'should-not'}-trigger: {sum(x.startswith('Y') for x in vals)}/{len(vals)} triggered")
print()
print(f"{'query':8s} {'skill-only':30s} skill-plus-pointer")
for (q, n) in sorted(table, key=lambda k: (k[0][0] != 'T', int(k[0][1:]), k[1])):
    v = table[(q, n)]
    print(f"{q:8s} {v.get('skill-only','-'):30s} {v.get('skill-plus-pointer','-')}")
