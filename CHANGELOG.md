# Changelog

All notable changes to `networking-labs-cli` are documented here.

Format: [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) — Added / Changed / Fixed / Security

---

## [Unreleased]

### Added
- `--region` flag for `aws-vpc` and `aws-ec2` subcommands *(planned)*
- `--output json` flag for pipeline-friendly output *(planned)*
- Route table and security group inspection via AWS CLI *(planned)*

---

## [0.1.0] — 2026-04-30

### Added
- `nmcli dns <host>` — DNS A, AAAA, and PTR record lookup via Python stdlib `socket`
- `nmcli ping <host> --count N` — ICMP reachability test via system `ping`
- `nmcli traceroute <host>` — Hop-by-hop route analysis via system `traceroute`
- `nmcli portscan <host> [--ports N ...]` — TCP port scan with 12-port default profile
- `nmcli aws-vpc` — AWS VPC enumeration via `boto3.client("ec2").describe_vpcs()`
- `nmcli aws-ec2` — EC2 instance inventory via `boto3.client("ec2").describe_instances()`
- `nmcli/utils.py` — Host validation and structured logging shared by all core functions
- `tests/test_core.py` — 5 unit tests covering validation, port scan, DNS lookup, and AWS credential error handling
- `.github/workflows/ci.yml` — CI pipeline: Python 3.10, pytest, flake8 (errors-only), bash syntax check
- `scripts/net-diag.sh` — Standalone bash diagnostic script (no Python required)
- `docs/network-support-runbook.md` — NOC L1/L2 escalation runbook with per-symptom workflows
- `docs/troubleshooting-guide.md` — Decision-tree fault isolation for DNS, ICMP, port, traceroute, and AWS
- `docs/aws-networking-notes.md` — VPC, subnet, security group, NACL, EC2, and boto3 reference
- `docs/architecture.md` — Component map, data flow, module responsibilities, design decisions
- `docs/branching-strategy.md` — GitFlow-based branch model with naming conventions and PR workflow
- `docs/decision-log.md` — Engineering decision records (5 decisions at v0.1.0)
- `docs/runbook.md` — Project-level operations runbook: install, run, test, deploy, troubleshoot
- `labs/01-dns-troubleshooting.md` — Step-by-step DNS triage lab walkthrough
- `labs/02-network-connectivity.md` — Full connectivity lab with port, ping, and traceroute exercises
- `sample-output/` — 5 captured CLI output examples covering all subcommands
- `AUDIT.md` — Repo maturity audit (Tier 1.5 → Tier 2)
- `RELEASE_NOTES.md` — v0.1.0 release summary
- `REPO_UPGRADE_REPORT.md` — Full record of all repo improvements

### Fixed
- CI pipeline was failing due to outdated `actions/checkout` and `actions/setup-python` versions — updated to `@v4` and `@v5`
- `setup.py` was missing `setuptools` import — added explicit import to fix `pip install -e .` in CI

---

## Pre-release history (commits before v0.1.0)

| Commit | Change |
|---|---|
| `dff71f8` | Initial README with project description |
| `60c873f` | `setup.py` for package entry point |
| `f6173ea` | `nmcli/__init__.py` with version and author |
| `640d639` | DNS propagation formatting fix |
| `3987481` | GitHub Actions updated to latest versions |
| `e5572a2` | Initial CI workflow |
| `eb07f50` | Fix missing `setuptools` import in `setup.py` |
| `b3252c0` | Merge PR #1 (`fix-setup-import` → `main`) |
| `740f483` | Recruiter-ready documentation upgrade |
