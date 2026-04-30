# Release Notes

---

## v0.1.0 — 2026-04-30

### What This Release Demonstrates

`networking-labs-cli` v0.1.0 is a fully functional Python CLI tool that automates the core diagnostic tasks performed in network support, cloud operations, and NOC environments. This release establishes the foundation: working code, a passing CI pipeline, a complete documentation suite, and a professional branch workflow.

**Built to prove:** Python CLI development, AWS SDK integration, test-driven validation, CI/CD pipeline ownership, and the documentation discipline expected in support and infrastructure roles.

---

### What Is Included

| Area | What ships in v0.1.0 |
|---|---|
| **CLI tool** | 6 subcommands: `dns`, `ping`, `traceroute`, `portscan`, `aws-vpc`, `aws-ec2` |
| **Tests** | 5 unit tests — all passing; mock-based, CI-safe |
| **CI pipeline** | GitHub Actions — tests + lint + shell syntax check on every push |
| **Docs** | Architecture, runbook, branching strategy, decision log, troubleshooting guide, NOC runbook, AWS notes |
| **Labs** | 2 step-by-step lab walkthroughs (DNS triage, connectivity analysis) |
| **Sample output** | 5 captured CLI output files covering all commands |

---

### Known Limitations

| Limitation | Notes |
|---|---|
| AWS region is hardcoded to `us-east-1` | `--region` flag is the top planned improvement |
| Output format is print-only | No `--output json` or CSV mode; structured data is returned but not exposed via CLI flag |
| `ping` / `traceroute` depend on system tools | Requires `iputils-ping` and `traceroute` on Linux hosts |
| No SNMP or CloudWatch integration | Planned for a future minor release |
| 5 unit tests | Core validation covered; `ping()` and `traceroute()` subprocess calls not yet mocked |
| No authentication for private DNS | Uses system resolver only — no resolver override flag |

---

### CI Status at Release

```
tests/test_core.py::test_validate_host_valid            PASSED
tests/test_core.py::test_validate_host_invalid          PASSED
tests/test_core.py::test_port_scan_returns_dict         PASSED
tests/test_core.py::test_dns_lookup_returns_dict        PASSED
tests/test_core.py::test_get_vpc_info_no_credentials    PASSED

5 passed
```

Lint: `flake8 nmcli/ main.py --select=E9,F63,F7,F82` — 0 errors
Shell: `bash -n scripts/net-diag.sh` — valid syntax

---

### Next Release Goals (v0.2.0)

- `--region` flag for all AWS subcommands
- `--output json` flag for pipeline-friendly output
- Security group inspection: `nmcli aws-sg <instance-id>`
- Expanded test coverage: `ping()` and `traceroute()` subprocess mocking
- Route table and NACL inspection

---

### Installation

```bash
git clone https://github.com/CartierC/networking-labs-cli.git
cd networking-labs-cli
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt && pip install -e .
nmcli --help
```

See [docs/runbook.md](docs/runbook.md) for the full setup and operations guide.
