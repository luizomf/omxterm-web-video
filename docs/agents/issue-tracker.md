# Issue tracker: GitHub

Specs, tickets, and issues for this repository live as GitHub issues. Use the
`gh` CLI for tracker operations and infer the repository from `git remote -v`.

## Conventions

- Create: `gh issue create --title "..." --body "..."`.
- Read: `gh issue view <number> --comments`.
- Comment: `gh issue comment <number> --body "..."`.
- Label: `gh issue edit <number> --add-label "..."` or `--remove-label "..."`.
- Close: `gh issue close <number> --comment "..."`.
- Publish a spec, ticket, or issue by creating a GitHub issue.

## Pull requests as a triage surface

**PRs as a request surface: no.** Pull requests implement accepted work; they
are not triaged as feature or bug reports.

GitHub shares one number space across issues and PRs. Resolve an ambiguous
reference with `gh pr view <number>` and fall back to `gh issue view <number>`.

## Delivery

An implementation PR must link its issue with `closes #<number>`. Delivery is
complete only after applicable checks pass, the PR is squash-merged, the branch
is deleted, the issue is closed, and the durable result on `main` is verified.
