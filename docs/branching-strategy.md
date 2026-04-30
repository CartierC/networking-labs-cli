# Branching Strategy — networking-labs-cli

## Branch Model

This repo uses a simplified GitFlow model with four branch types. Direct commits to `main` are avoided — all changes enter through pull requests with at least one CI pass.

```
main
 └── dev
      └── feature/*, hotfix/*, release/*
```

---

## Branch Definitions

### `main`
- **Role:** Stable, production-ready code
- **Who merges here:** Only from `dev` (via PR) or `hotfix/*` (via PR)
- **CI required:** Yes — all tests, lint, and shell checks must pass
- **Direct commits:** Never

### `dev`
- **Role:** Integration branch — staging area for the next release
- **Who merges here:** Feature branches via PR
- **CI required:** Yes
- **Direct commits:** Avoided; minor doc fixes acceptable

### `feature/*`
- **Role:** Short-lived branch for a single feature or improvement
- **Branched from:** `dev`
- **Merges back to:** `dev`
- **Naming examples:**
  - `feature/json-output-flag`
  - `feature/region-flag-aws`
  - `feature/snmp-module`
  - `feature/repo-maturity-upgrade`
- **Lifecycle:** Create → implement → open PR to `dev` → merge → delete

### `hotfix/*`
- **Role:** Urgent fix branched directly from `main` when a production issue cannot wait for the next `dev` cycle
- **Branched from:** `main`
- **Merges back to:** `main` AND `dev` (to keep `dev` in sync)
- **Naming examples:**
  - `hotfix/fix-dns-crash-on-empty-host`
  - `hotfix/boto3-credential-error-unhandled`
- **Lifecycle:** Create → fix → open PR to `main` → merge → cherry-pick or merge into `dev` → delete

### `release/*` (optional)
- **Role:** Release preparation — version bumps, final changelog edits, last-minute stabilization
- **Branched from:** `dev`
- **Merges back to:** `main` AND `dev`
- **Naming examples:**
  - `release/v0.2.0`
  - `release/v1.0.0`
- **When to use:** Only when releasing a named version with a formal changelog and release notes

---

## Pull Request Workflow

### Feature → dev

```
1. git checkout dev && git pull origin dev
2. git checkout -b feature/<name>
3. Implement changes
4. git push -u origin feature/<name>
5. Open PR: feature/<name> → dev
6. CI must pass (tests + lint + shell check)
7. Merge PR (squash or merge commit)
8. Delete feature branch
```

### dev → main (release)

```
1. Confirm all feature PRs for the release are merged to dev
2. Update CHANGELOG.md and RELEASE_NOTES.md on dev
3. Open PR: dev → main
4. CI must pass
5. Merge PR
6. Tag the release: git tag v0.X.0 && git push origin v0.X.0
```

### hotfix → main

```
1. git checkout main && git pull origin main
2. git checkout -b hotfix/<description>
3. Fix the issue
4. git push -u origin hotfix/<description>
5. Open PR: hotfix/<description> → main
6. After merge, also merge or cherry-pick the fix into dev
7. Delete hotfix branch
```

---

## Merge Process

| Source | Target | Method | Notes |
|---|---|---|---|
| `feature/*` | `dev` | Merge commit or squash | Prefer squash for single-commit features |
| `dev` | `main` | Merge commit | Preserves dev history |
| `hotfix/*` | `main` | Merge commit | Then sync to `dev` |
| `release/*` | `main` | Merge commit | Then sync to `dev` |

---

## Cleanup Process

- Delete feature and hotfix branches immediately after merge
- Never force-push to `main` or `dev`
- Keep `dev` within a few commits of `main` — drift creates messy merges

```bash
# Delete a merged branch locally and on remote
git branch -d feature/<name>
git push origin --delete feature/<name>
```

---

## Why Not Commit Directly to Main

- Bypasses CI — a broken commit reaches the stable branch without validation
- No code review opportunity — issues are caught later (or not at all)
- Harder to revert — a direct commit on main requires `git revert` or `reset`, both of which can disrupt collaborators
- Breaks the audit trail — PR history documents why changes were made, not just what changed

Even for solo projects: the habit of opening a PR, letting CI run, then merging trains the workflow that production teams require.
