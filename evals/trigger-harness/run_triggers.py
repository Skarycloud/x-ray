"""Run X-RAY trigger queries headlessly and record whether the skill loaded.

usage: python run_triggers.py <queries_md> <fixtures_dir> <results_dir> [runs] [workers]
Read-only: only Read, Grep, Glob, Skill are allowed; everything else is denied.
"""
import json, re, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

QUERIES, FIX, RES = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
RUNS = int(sys.argv[4]) if len(sys.argv) > 4 else 1
WORKERS = int(sys.argv[5]) if len(sys.argv) > 5 else 4
RES.mkdir(parents=True, exist_ok=True)

rows = re.findall(r"^\| ([TN]\d+) \| (.+?) \|", QUERIES.read_text(encoding="utf-8"), re.M)
queries = [(qid, q.strip()) for qid, q in rows]
assert len(queries) == 20, len(queries)

CLAUDE = "claude.cmd" if sys.platform == "win32" else "claude"


def run(job):
    cond, qid, q, n = job
    out = RES / f"{cond}__{qid}__{n}.jsonl"
    if out.exists() and out.stat().st_size > 0:
        return job
    cmd = [CLAUDE, "-p", q, "--output-format", "stream-json", "--verbose",
           "--permission-mode", "dontAsk", "--allowedTools", "Read Grep Glob Skill",
           "--max-turns", "3", "--no-session-persistence"]
    t = time.time()
    p = subprocess.run(cmd, cwd=FIX / cond, stdin=subprocess.DEVNULL, capture_output=True, text=True, encoding="utf-8", timeout=600)
    out.write_text(p.stdout, encoding="utf-8")
    (RES / f"{cond}__{qid}__{n}.err").write_text(f"rc={p.returncode} secs={time.time()-t:.0f}\n{p.stderr}", encoding="utf-8")
    return job


jobs = [(c, qid, q, n) for n in range(1, RUNS + 1) for qid, q in queries for c in ["skill-only", "skill-plus-pointer"]]
with ThreadPoolExecutor(WORKERS) as ex:
    for i, j in enumerate(ex.map(run, jobs), 1):
        print(f"{i}/{len(jobs)} done: {j[0]} {j[1]} run{j[3]}", flush=True)
