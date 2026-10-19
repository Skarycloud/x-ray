# Contributing to X-RAY

Thanks for helping. X-RAY is early, and the most valuable contributions are **evidence**: host test reports, evaluation tasks, and documented failures.

## Most wanted

1. **Host validation reports.** Follow the checklist in [adapters/README.md](adapters/README.md) on one host and add the results to that host's adapter file (host version, OS, date, what worked, what didn't).
2. **Evaluation tasks.** Build a task matching the format in [evals/README.md](evals/README.md), with hidden acceptance and regression tests and a reference solution that passes both. Include the source and license of any code used.
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

- [ ] Relative links resolve.
- [ ] `SKILL.md` frontmatter still valid; file still concise.
- [ ] Workflow, references, and templates agree with each other.
- [ ] PR description lists checks you ran.

## License

By contributing, you agree that your contributions are licensed under the [MIT License](LICENSE).
