#!/usr/bin/env node
// X-RAY installer. Copies skills/x-ray/ into the skill folders that coding agents read.
// No dependencies. Never touches a folder unless its SKILL.md says `name: x-ray`, or --force.

"use strict";

const fs = require("fs");
const os = require("os");
const path = require("path");

const SKILL_NAME = "x-ray";
const PKG_ROOT = path.resolve(__dirname, "..");
const SOURCE = path.join(PKG_ROOT, "skills", SKILL_NAME);
const VERSION = require(path.join(PKG_ROOT, "package.json")).version;

// Skill folders each agent documents. "agents" (.agents/skills) is read by Codex, Cursor,
// GitHub Copilot, and Gemini CLI, so one copy there serves all four.
const TARGETS = {
  claude: { label: "Claude Code", user: [".claude", "skills"], project: [".claude", "skills"], detect: [".claude"] },
  agents: { label: "Codex, Cursor, Copilot, Gemini CLI (.agents)", user: [".agents", "skills"], project: [".agents", "skills"], detect: [".agents", ".codex", ".cursor", ".copilot", ".gemini"] },
  cursor: { label: "Cursor (.cursor)", user: [".cursor", "skills"], project: [".cursor", "skills"], detect: [] },
  copilot: { label: "GitHub Copilot (.copilot / .github)", user: [".copilot", "skills"], project: [".github", "skills"], detect: [] },
  gemini: { label: "Gemini CLI (.gemini)", user: [".gemini", "skills"], project: [".gemini", "skills"], detect: [] },
};

const HELP = `x-ray-skill ${VERSION}: install the X-RAY skill for AI coding agents

Usage:
  npx x-ray-skill install [options]     Copy the skill into agent skill folders
  npx x-ray-skill uninstall [options]   Remove X-RAY from those folders
  npx x-ray-skill status [options]      Show where X-RAY is installed

Options:
  --agent <list>   Comma-separated: ${Object.keys(TARGETS).join(", ")}, or all.
                   Default: agents detected in your home folder (Claude Code -> claude;
                   Codex, Cursor, Copilot, or Gemini CLI -> agents).
  --project        Use the current project's folders instead of your home folder
  --force          Replace an existing folder named x-ray even if it isn't X-RAY
  --dry-run        Print what would happen; change nothing
  -h, --help       Show this help
  -v, --version    Show the version
`;

function parseArgs(argv) {
  const opts = { cmd: null, agents: null, project: false, force: false, dryRun: false };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "-h" || a === "--help") opts.cmd = "help";
    else if (a === "-v" || a === "--version") opts.cmd = "version";
    else if (a === "--project") opts.project = true;
    else if (a === "--force") opts.force = true;
    else if (a === "--dry-run") opts.dryRun = true;
    else if (a === "--agent" || a === "--agents") opts.agents = (argv[++i] || "").split(",").map((s) => s.trim()).filter(Boolean);
    else if (a.startsWith("--agent=")) opts.agents = a.slice(8).split(",").map((s) => s.trim()).filter(Boolean);
    else if (!a.startsWith("-") && !opts.cmd) opts.cmd = a;
    else fail(`Unknown option: ${a}\n\n${HELP}`);
  }
  return opts;
}

function fail(msg) {
  process.stderr.write(msg.endsWith("\n") ? msg : msg + "\n");
  process.exit(1);
}

function resolveAgents(opts, home) {
  if (opts.agents && opts.agents.length) {
    if (opts.agents.includes("all")) return Object.keys(TARGETS);
    for (const a of opts.agents) if (!TARGETS[a]) fail(`Unknown agent "${a}". Choose from: ${Object.keys(TARGETS).join(", ")}, all`);
    return [...new Set(opts.agents)];
  }
  const found = Object.keys(TARGETS).filter((k) => TARGETS[k].detect.some((d) => fs.existsSync(path.join(home, d))));
  if (!found.length) fail("No coding agent detected in your home folder. Pick one with --agent (for example --agent claude).");
  return found;
}

function destFor(key, opts, home) {
  const t = TARGETS[key];
  const base = opts.project ? process.cwd() : home;
  return path.join(base, ...(opts.project ? t.project : t.user), SKILL_NAME);
}

function isXray(dir) {
  try {
    const head = fs.readFileSync(path.join(dir, "SKILL.md"), "utf8").slice(0, 400);
    return /^name:\s*x-ray\s*$/m.test(head);
  } catch {
    return false;
  }
}

function installedVersion(dir) {
  try {
    const m = fs.readFileSync(path.join(dir, "SKILL.md"), "utf8").match(/^\s+version:\s*"?([^"\n]+)"?/m);
    return m ? m[1] : "unknown";
  } catch {
    return null;
  }
}

function install(keys, opts, home) {
  if (!fs.existsSync(path.join(SOURCE, "SKILL.md"))) fail(`Skill source missing: ${SOURCE}`);
  let changed = 0;
  for (const key of keys) {
    const dest = destFor(key, opts, home);
    const exists = fs.existsSync(dest);
    if (exists && !isXray(dest) && !opts.force) {
      console.log(`skip     ${TARGETS[key].label}: ${dest} exists and isn't X-RAY (use --force to replace it)`);
      continue;
    }
    const verb = exists ? `update ${installedVersion(dest)} -> ${VERSION}` : `install ${VERSION}`;
    console.log(`${opts.dryRun ? "would " : ""}${verb}  ${TARGETS[key].label}: ${dest}`);
    if (opts.dryRun) continue;
    if (exists) fs.rmSync(dest, { recursive: true, force: true });
    fs.mkdirSync(path.dirname(dest), { recursive: true });
    fs.cpSync(SOURCE, dest, { recursive: true });
    changed++;
  }
  if (!opts.dryRun && changed) {
    console.log("\nDone. Restart your agent (or reload skills) so it picks up X-RAY.");
    console.log("Claude Code users can install it as a plugin instead: /plugin marketplace add Skarycloud/x-ray");
  }
}

function uninstall(keys, opts, home) {
  for (const key of keys) {
    const dest = destFor(key, opts, home);
    if (!fs.existsSync(dest)) continue;
    if (!isXray(dest) && !opts.force) {
      console.log(`skip     ${dest} isn't X-RAY; left alone`);
      continue;
    }
    console.log(`${opts.dryRun ? "would remove" : "remove"}  ${TARGETS[key].label}: ${dest}`);
    if (!opts.dryRun) fs.rmSync(dest, { recursive: true, force: true });
  }
}

function status(opts, home) {
  for (const key of Object.keys(TARGETS)) {
    const dest = destFor(key, opts, home);
    const v = fs.existsSync(dest) ? (isXray(dest) ? installedVersion(dest) : "a different skill") : null;
    console.log(`${(v || "-").padEnd(18)} ${TARGETS[key].label}: ${dest}`);
  }
}

function main() {
  const opts = parseArgs(process.argv.slice(2));
  const home = os.homedir();
  switch (opts.cmd) {
    case "install":
      return install(resolveAgents(opts, home), opts, home);
    case "uninstall":
      return uninstall(opts.agents ? resolveAgents(opts, home) : Object.keys(TARGETS), opts, home);
    case "status":
      return status(opts, home);
    case "version":
      return console.log(VERSION);
    case "help":
    case null:
      return console.log(HELP);
    default:
      fail(`Unknown command: ${opts.cmd}\n\n${HELP}`);
  }
}

main();
