# Contributing to X-RAY

Thanks for helping. X-RAY is early, and the most valuable contributions are **evidence**: host test reports, evaluation tasks, and documented failures.

## Most wanted

1. **Host validation reports.** Follow the checklist in [adapters/README.md](adapters/README.md) on one host and add the results to that host's adapter file (host version, OS, date, what worked, what didn't).
2. **Eval cases.** Build a case in the [`claude plugin eval` format](evals/README.md#task-set) with outcome and invariant graders, ideally one the baseline fails. Include the source and license of any code used.
3. **Failure reports.** Cases where an agent following X-RAY did something wrong, wasteful, or overly slow. Include the transcript excerpt if you can.
4. **Corrections.** Wrong paths, stale host behavior, broken links, inaccurate citations.

## Guidelines

- Read [AGENTS.md](AGENTS.md). Its rules apply to human contributors too.
- Keep pull requests small and focused on one concern.
- Changes to `SKILL.md` need a reason: an observed failure, an eval result, or an inconsistency. Explain it in the PR.
- Don't add claims of compatibility or effectiveness without linked evidence.
- Paraphrase and cite outside sources; don't paste copyrighted text.
- No new dependencies without discussion in an issue first.

## Before opening a PR

- [ ] `python tools/validate.py .` passes.
- [ ] Workflow, references, and templates agree with each other.
- [ ] PR description lists checks you ran.

## Releasing (maintainers)

1. Bump the version in `skills/x-ray/SKILL.md`, `.claude-plugin/plugin.json`, and `package.json`; add a [CHANGELOG.md](CHANGELOG.md) entry; run `python tools/validate.py .`.
2. Check the npm package contents: `npm pack --dry-run` should list only `bin/cli.js`, `skills/x-ray/`, `LICENSE`, `README.md`, and `package.json`.
3. Publish: `npm login`, then `npm publish`. Tag the release: `git tag v<version> && git push --tags`.

## License

By contributing, you agree that your contributions are licensed under the [MIT License](LICENSE).
