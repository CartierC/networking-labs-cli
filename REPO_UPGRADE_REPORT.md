# Repo Upgrade Report

Repository: `CartierC/networking-labs-cli`
Last updated: 2026-04-30
Branch (current): `feature/tier-3-evidence-pack`

---

## Upgrade History

| Session | Branch | Maturity | Key Work |
|---|---|---|---|
| Session 1 (2026-04-29) | `main` (direct) | → Tier 1.5 | NOC runbook, troubleshooting guide, AWS notes, sample output, README restructure |
| Session 2 (2026-04-30) | `feature/repo-maturity-upgrade` | Tier 1.5 → Tier 2 | Architecture doc, branching strategy, decision log, runbook, CHANGELOG, RELEASE_NOTES, CI upgrade |
| Session 3 (2026-04-30) | `feature/tier-3-evidence-pack` | Tier 2 → Tier 3 | Real local validation, evidence directory, bug found and fixed |

---

## Session 3: Tier 3 Evidence Pack

### Maturity Before / After

| Dimension | Before | After |
|---|---|---|
| **Overall tier** | Tier 2 | Tier 3 |
| Working code | ✅ | ✅ |
| Passing CI | ✅ | ✅ |
| Full docs suite | ✅ | ✅ |
| Real command outputs | ❌ | ✅ |
| Live validation evidence | ❌ | ✅ |
| Entry point actually works | ❌ (bug) | ✅ (fixed) |
| Bug disclosed honestly | ❌ | ✅ |
| evidence/ directory | ❌ | ✅ |
| logs/ directory | ❌ | ✅ |

---

### Files Added (Session 3)

| File | Purpose |
|---|---|
| `evidence/README.md` | Evidence index — what is proved, how it was captured |
| `evidence/validation-summary.md` | Full validation report with real outputs, analysis, bug disclosure |
| `logs/local-validation.log` | Chronological raw log of all commands run with full output |

### Files Modified (Session 3)

| File | Change |
|---|---|
| `setup.py` | Added `py_modules=["main"]` — fixes entry point `ModuleNotFoundError` on clean install |
| `README.md` | Added "Evidence / Validation" section with live result table and bug disclosure |
| `CHANGELOG.md` | Added evidence files and entry point fix to [Unreleased] section |
| `REPO_UPGRADE_REPORT.md` | This file — updated with Session 3 summary |

---

### Commands Run and Results (Session 3)

All commands were run locally in a clean venv. Results are real.

| Command | Result | Notes |
|---|---|---|
| `nmcli --help` | PASS | 6 subcommands |
| `nmcli dns github.com` | PASS | A=140.82.113.3, AAAA, PTR resolved |
| `nmcli dns google.com` | PASS | A=142.251.15.138, AAAA, PTR resolved |
| `nmcli dns cloudflare.com` | PASS | A+AAAA; PTR warning expected on anycast |
| `nmcli dns <invalid host>` | PASS | Graceful error, no crash |
| `nmcli ping 8.8.8.8 --count 4` | PASS | 0.0% loss, avg 20.7ms |
| `nmcli portscan github.com --ports 22 80 443` | PASS | All 3 OPEN |
| `nmcli portscan 8.8.8.8 --ports 53 80 443` | PASS | 53/443 OPEN, 80 CLOSED (correct) |
| `nmcli traceroute 8.8.8.8` | PASS | 13 hops to dns.google |
| `nmcli aws-vpc` | PASS | Graceful NoCredentialsError, exit 0 |
| `nmcli aws-ec2` | PASS | Graceful NoCredentialsError, exit 0 |
| `pytest tests/ -v` | PASS | 5/5 on Python 3.14.3 |
| `flake8 --select=E9,F63,F7,F82` | PASS | 0 errors |
| `bash -n scripts/net-diag.sh` | PASS | Valid syntax |
| `bash scripts/net-diag.sh` | PASS | All 4 checks working |

---

### Bug Found and Fixed (Session 3)

**Bug:** `setup.py` missing `py_modules=["main"]`
**Symptom:** `nmcli dns github.com` → `ModuleNotFoundError: No module named 'main'`
**Root cause:** `find_packages()` discovers only packages (dirs with `__init__.py`). `main.py` is a standalone root-level module — it was not mapped into the editable install's import finder.
**Why CI missed it:** GitHub Actions runs `pytest tests/ -v`, which imports from the `nmcli` package. The `nmcli` entry point script is never invoked in CI. Tests passed; the actual CLI did not work.
**Fix:** Added `py_modules=["main"]` to `setup.py`.
**Lesson:** CI coverage should include an integration smoke test that calls the CLI entry point directly (e.g., `nmcli --help`). Added to next steps.

---

### Remaining Manual Steps

| Step | Priority | Action |
|---|---|---|
| Push branch and open PR | High | `git push -u origin feature/tier-3-evidence-pack` |
| Verify CI passes with setup.py fix | High | Check GitHub Actions after push |
| Add `nmcli --help` smoke test to CI | Medium | Prevents entry point regressions |
| Capture screenshots | Medium | GitHub Actions green, pytest output, CLI in terminal |
| Merge to dev → main | Medium | After CI passes on feature branch |
| Tag v0.1.1 (patch) | Low | For the entry point fix |

---

## Session 2: Tier 2 Upgrade (reference)

### Files Added

| File | Purpose |
|---|---|
| `AUDIT.md` | Maturity audit — what was missing, what was added |
| `CHANGELOG.md` | Versioned history at v0.1.0 |
| `RELEASE_NOTES.md` | v0.1.0 summary, limitations, next goals |
| `docs/architecture.md` | Component map, data flow, module responsibilities |
| `docs/branching-strategy.md` | GitFlow model with naming and PR workflow |
| `docs/decision-log.md` | 5 engineering decision records |
| `docs/runbook.md` | Project-level install, run, test, deploy guide |
| `.github/workflows/ci.yml` | Two-stage CI: flake8 + bash syntax → pytest |

### Files Modified

| File | Change |
|---|---|
| `README.md` | CI badge, expanded structure table, "Why This Matters" section |
| `.github/workflows/test.yml` | Removed — replaced by ci.yml |

---

## Recommended PR (Current Branch)

**Title:**
```
fix+evidence: entry point bug fix and Tier 3 local validation pack
```

**Body:**
```
## What this PR does

Adds real local validation evidence (Tier 3 proof) and fixes a hidden entry
point bug discovered during the evidence run.

## Bug fixed

setup.py was missing `py_modules=["main"]`. The `nmcli` entry point raised
ModuleNotFoundError on a clean `pip install -e .`. CI passed because the test
runner imports the `nmcli` package directly — it never calls the entry point
script. Fixed and documented.

## Evidence added

- `evidence/README.md` — what is proved and how it was captured
- `evidence/validation-summary.md` — full report with real command outputs,
  analysis of correct vs. expected results, honest bug disclosure
- `logs/local-validation.log` — complete chronological run log

## All 15 checks passed locally

DNS / ICMP / port scan / traceroute / AWS error handling / pytest 5/5 /
flake8 0 errors / bash -n / shell script

## Acceptance

- [ ] CI passes after setup.py fix
- [ ] Evidence files contain real outputs (not documentation examples)
- [ ] Bug is disclosed, not hidden
- [ ] No fake evidence created
```
