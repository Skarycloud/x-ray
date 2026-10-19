"""Outcome pilot: run eval cases with and without X-RAY via headless Claude Code.

usage: python run_outcomes.py <x-ray repo> <work dir> <case> [runs] [workers]

Each run: fresh workspace -> case fixture.sh -> `claude -p <prompt>`.
Arm "with" loads the repo as a plugin (--plugin-dir); arm "without" doesn't.
Tools: Read Glob Grep Skill TodoWrite Edit Write. No shell, so no tests can run.
Saves transcript, final diff, and metrics; grade.py scores them.
"""
import json, re, shutil, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

REPO, WORK, CASE = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), sys.argv[3]
RUNS = int(sys.argv[4]) if len(sys.argv) > 4 else 3
WORKERS = int(sys.argv[5]) if len(sys.argv) > 5 else 3
CASE_DIR = REPO / "evals" / "cases" / CASE
CLAUDE = "claude.cmd" if sys.platform == "win32" else "claude"
BASH = shutil.which("bash")

prompt_md = (CASE_DIR / "prompt.md").read_text(encoding="utf-8")
front, body = re.match(r"^---\n(.*?)\n---\n(.*)$", prompt_md, re.S).groups()
prompt = body.strip()
max_turns = re.search(r"max_turns:\s*(\d+)", front).group(1)


def run(job):
    arm, n = job
    ws = WORK / CASE / f"{arm}-{n}"
    out = WORK / CASE / f"{arm}-{n}.jsonl"
    if out.exists() and out.stat().st_size > 0:
        return job
    if ws.exists():
        shutil.rmtree(ws)
    ws.mkdir(parents=True)
    subprocess.run([BASH, str(CASE_DIR / "fixture.sh")], cwd=ws, check=True)
    cmd = [CLAUDE, "-p", prompt, "--output-format", "stream-json", "--verbose",
           "--permission-mode", "dontAsk",
           "--allowedTools", "Read Glob Grep Skill TodoWrite Edit Write",
           "--max-turns", max_turns, "--no-session-persistence"]
    if arm == "with":
        cmd += ["--plugin-dir", str(REPO)]
    t = time.time()
    p = subprocess.run(cmd, cwd=ws, stdin=subprocess.DEVNULL, capture_output=True,
                       text=True, encoding="utf-8", timeout=1800)
    out.write_text(p.stdout, encoding="utf-8")
    diff = subprocess.run(["git", "diff"], cwd=ws, capture_output=True, text=True, encoding="utf-8").stdout
    untracked = subprocess.run(["git", "ls-files", "--others", "--exclude-standard"], cwd=ws,
                               capture_output=True, text=True, encoding="utf-8").stdout
    (WORK / CASE / f"{arm}-{n}.diff").write_text(diff + "\n# untracked:\n" + untracked, encoding="utf-8")
    (WORK / CASE / f"{arm}-{n}.err").write_text(f"rc={p.returncode} secs={time.time()-t:.0f}\n{p.stderr}", encoding="utf-8")
    return job


jobs = [(arm, n) for n in range(1, RUNS + 1) for arm in ("with", "without")]
(WORK / CASE).mkdir(parents=True, exist_ok=True)
with ThreadPoolExecutor(WORKERS) as ex:
    for j in ex.map(run, jobs):
        print("done", CASE, *j, flush=True)
