# AGENTS.md

Repository map and engineering contract for humans and coding agents working on
the OMXTerm Web video materials.

## Authority and scope

- This file applies repository-wide. A nested `AGENTS.md` may refine it for its
  subtree; the closest applicable file wins.
- The repository documents the video deployment scenario; it is not the
  OMXTerm Web application source. Application behavior belongs in
  `luizomf/omxterm-web`.
- Read `README.md` and the affected script before changing documented or
  operational behavior. Surface conflicts instead of silently choosing one.

## Project map

- `scripts/` contains sanitized, scenario-specific Bash deployment helpers and
  the public configuration example used by the video.
- `diagrams/` contains the editable Excalidraw source shown in the video.
- `demos/` contains the educational Python PTY demonstration.
- Deployment values may cross public Internet, Docker, firewall, ACME, DNS,
  proxy, SSH, and local-secret trust boundaries. Never commit real credentials,
  access tokens, private infrastructure values, `.local.env` files, or ACME
  account material.

## Canonical commands

Run commands from the repository root.

```text
Bootstrap:      N/A; this repository has no dependency installation step
Config check:   ./scripts/setup_omxterm_web --check <trusted-config-file>
Focused test:   bash -n <affected-script>
Test:           bash -n scripts/first_deploy scripts/reset_vps scripts/setup_omxterm_web
Lint:           N/A; no repository linter is configured
Type-check:     N/A; no statically typed build is configured
Format check:   git diff --check
Docs check:     N/A; no documentation checker is configured
Build:          N/A; the repository contains source materials only
```

Do not claim the configuration check passed unless a trusted local config was
available and the command was actually run.

## Mechanical quality gates

- Run `bash -n` for every changed shell script and `git diff --check` for every
  change. Add focused regression coverage when a practical caller-visible seam
  exists; otherwise document the exact manual verification.
- Keep `README.md`, script defaults, usage output, and
  `scripts/setup_omxterm_web.env.example` synchronized.
- Validate security-sensitive deployment changes in a disposable, explicitly
  authorized environment. Record HTTPS, WSS, ACME, forwarded-client-address,
  and rollback evidence when those behaviors are affected.

## Working agreement

- Before editing, inspect the current issue, worktree, applicable instructions,
  relevant files, and Git history. Preserve unrelated work.
- Use GitHub Issues through `gh`. Follow the configured tracker and triage
  mappings in `docs/agents/`.
- Follow this delivery flow: issue -> dedicated branch -> implementation and
  verification -> conventional commit(s) -> PR containing `closes #N` -> wait
  for applicable checks -> `gh pr merge --squash --delete-branch`.
- Do not report a Ticket delivered until its PR is merged, its issue is closed,
  and the durable result on `main` has been verified.
- Keep changes small and cohesive. Code, comments, commits, issues, and PRs are
  written in English. Existing PT-BR educational prose may remain in PT-BR.

## Destructive deployment constraints

- `scripts/first_deploy` resets a remote checkout and invokes
  `scripts/reset_vps`; `scripts/reset_vps` removes host-wide Docker resources.
  Never run either script without explicit authorization for the exact host and
  exact destructive scope.
- Prefer narrow, reversible app/edge operations for upgrades and verification.
  Never weaken firewall, proxy, SSH allowlist, TLS, access-token, Origin, or
  forwarded-address controls to make a demo pass.
- Treat sourced configuration as trusted executable Bash. Do not print or copy
  secrets into logs, issues, PRs, tests, chat, or video artifacts.

## Agent skills

### Issue tracker

Specs, tickets, and issues live in GitHub Issues; external PRs are not a request
surface. See `docs/agents/issue-tracker.md`.

### Triage labels

The repository uses the canonical triage label vocabulary. See
`docs/agents/triage-labels.md`.

### Domain docs

The repository uses a single-context documentation layout. See
`docs/agents/domain.md`.
