# networking-labs-cli

[![CI](https://github.com/CartierC/networking-labs-cli/actions/workflows/ci.yml/badge.svg)](https://github.com/CartierC/networking-labs-cli/actions/workflows/ci.yml)

> Python network automation CLI for DNS lookup, port checks, connectivity testing, AWS VPC/EC2 concepts, and CI/CD validation.

---

## Purpose

A working Python CLI tool that replicates the core diagnostic commands used daily in network support, cloud operations, and NOC environments. Built to demonstrate hands-on technical skill — every command maps to a real troubleshooting task.

---

## Role Alignment

| Role | What this repo demonstrates |
|---|---|
| Network Support Engineer | DNS lookup, port scanning, ICMP testing, traceroute |
| Cloud Support Engineer | AWS VPC enumeration, EC2 inventory, boto3 SDK |
| NOC Analyst | Structured triage workflows, connectivity checks, runbook docs |
| Infrastructure Support | Python CLI tooling, CI/CD pipeline, test-driven validation |

---

## Skills Demonstrated

| Skill | Implementation |
|---|---|
| DNS lookup (A, AAAA, PTR) | `nmcli/core.py` → `dns_lookup()` |
| TCP port scanning | `nmcli/core.py` → `port_scan()` |
| ICMP connectivity testing | `nmcli/core.py` → `ping()` |
| Route path analysis | `nmcli/core.py` → `traceroute()` |
| AWS VPC enumeration | `nmcli/aws.py` → `get_vpc_info()` |
| AWS EC2 instance inventory | `nmcli/aws.py` → `get_ec2_instances()` |
| Python CLI with argparse | `main.py` — 6 subcommands |
| Input validation + logging | `nmcli/utils.py` → `validate_host()` |
| Unit testing with pytest | `tests/test_core.py` — 5/5 passing |
| CI/CD pipeline | `.github/workflows/test.yml` — runs on every push |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10+ |
| AWS SDK | boto3 / botocore |
| CLI Framework | argparse |
| Networking | socket (stdlib) |
| Testing | pytest |
| CI/CD | GitHub Actions (ubuntu-latest) |
| Packaging | setuptools + pip |

---

## Project Structure

```
networking-labs-cli/
├── main.py                              # CLI entry point — 6 subcommands
├── nmcli/
│   ├── core.py                          # ping, traceroute, dns_lookup, port_scan
│   ├── aws.py                           # get_vpc_info, get_ec2_instances (boto3)
│   └── utils.py                         # validate_host, logging config
├── tests/
│   └── test_core.py                     # 5 unit tests — all passing
├── labs/
│   ├── 01-dns-troubleshooting.md        # Step-by-step DNS triage lab
│   └── 02-network-connectivity.md       # Full connectivity lab walkthrough
├── docs/
│   ├── architecture.md                  # Component map, data flow, design decisions
│   ├── runbook.md                       # Install, run, test, deploy guide
│   ├── branching-strategy.md            # GitFlow branch model and PR workflow
│   ├── decision-log.md                  # Engineering decision records
│   ├── network-support-runbook.md       # NOC L1/L2 escalation runbook
│   ├── troubleshooting-guide.md         # Structured fault isolation guide
│   └── aws-networking-notes.md          # AWS VPC/EC2 networking reference
├── sample-output/
│   ├── dns-lookup-output.txt            # DNS command output example
│   ├── port-check-output.txt            # Port scan output example
│   ├── connectivity-test-output.txt     # Ping + traceroute output example
│   └── ci-validation-output.txt         # pytest CI run output example
├── screenshots/
│   └── README.md                        # Manual screenshot capture guide
├── scripts/
│   └── net-diag.sh                      # Shell diagnostic helper
├── .github/workflows/
│   └── ci.yml                           # CI: lint + shell check + pytest
├── AUDIT.md                             # Repo maturity audit
├── CHANGELOG.md                         # Version history
├── RELEASE_NOTES.md                     # v0.1.0 release summary
├── requirements.txt
└── setup.py
```

---

## How to Run

```bash
# 1. Clone and set up
git clone https://github.com/CartierC/networking-labs-cli.git
cd networking-labs-cli

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
pip install -e .

# 4. Run tests to verify everything works
python3 -m pytest tests/ -v
```

---

## Example Commands

```bash
# DNS lookup — resolves A, AAAA, and PTR records
nmcli dns google.com

# Ping — ICMP reachability test
nmcli ping 8.8.8.8 --count 4

# Port scan — check specific ports
nmcli portscan github.com --ports 22 80 443

# Port scan — scan all common ports
nmcli portscan 192.168.1.1

# Traceroute — hop-by-hop path analysis
nmcli traceroute cloudflare.com

# AWS — list VPCs (requires: aws configure)
nmcli aws-vpc

# AWS — list EC2 instances (requires: aws configure)
nmcli aws-ec2
```

---

## What This Project Proves

- **DNS:** Queries A, AAAA, and PTR records programmatically using Python's `socket` library — same records checked during real DNS propagation validation
- **Port checks:** TCP `connect_ex()` correctly identifies open vs. closed ports — same logic used to audit exposed services on EC2 instances
- **Connectivity:** ICMP ping and traceroute expose packet loss, latency, and broken hops — foundational NOC triage tools
- **AWS SDK:** boto3 integration enumerates VPCs and EC2 instances, handles `NoCredentialsError` gracefully — demonstrates cloud SDK familiarity
- **Testing:** pytest suite validates behavior without a live network or AWS account — mock-based AWS test included
- **CI/CD:** GitHub Actions pipeline runs tests on every push to `main` — pipeline was broken, diagnosed, and repaired end-to-end
- **Documentation:** Runbooks, troubleshooting guides, and lab walkthroughs reflect the documentation habits expected in support roles

---

## Sample Output

**DNS Lookup**
```
$ nmcli dns github.com
  A        → 140.82.114.4
  PTR      → lb-140-82-114-4-sea.github.com
  aliases  → []
```

**Port Scan**
```
$ nmcli portscan github.com --ports 22 80 443
PORT     SERVICE          STATUS
-----------------------------------
22       SSH              OPEN
80       HTTP             OPEN
443      HTTPS            OPEN

Summary: 3 open, 0 closed
```

**Ping**
```
$ nmcli ping 8.8.8.8 --count 4
64 bytes from 8.8.8.8: icmp_seq=0 ttl=118 time=11.2 ms
64 bytes from 8.8.8.8: icmp_seq=1 ttl=118 time=10.8 ms
...
4 packets transmitted, 4 received, 0% packet loss
```

See [sample-output/](sample-output/) for full command output files.

---

## CI / Validation

| Run | Trigger | Result |
|---|---|---|
| #1 | Initial workflow push | Failed — misconfigured Actions version |
| #2 | Actions version fix | Failed — missing setuptools |
| #3 | Autonomous CI repair branch | Passed |
| #4 | Merge to main | Passed |

Root cause: outdated Actions versions + missing `setuptools` in `setup.py`. Diagnosed and resolved using Claude Code autonomous repair mode.

**Current status: all pushes to `main` and `dev` run CI (lint + shell check + pytest). 5/5 tests passing.**

CI now runs in two stages: `validate` (flake8 + bash syntax check) gates the `test` job, so test resources are not consumed on code with syntax errors.

```
tests/test_core.py::test_validate_host_valid            PASSED
tests/test_core.py::test_validate_host_invalid          PASSED
tests/test_core.py::test_port_scan_returns_dict         PASSED
tests/test_core.py::test_dns_lookup_returns_dict        PASSED
tests/test_core.py::test_get_vpc_info_no_credentials    PASSED
```

---

## Next Improvements

- Add `--region` flag to AWS subcommands
- Add JSON and CSV output format option (`--output json`)
- Add route table and security group inspection
- Add SNMP polling module
- Integrate AWS CloudWatch for metric queries
- Add `--verbose` flag with full packet-level logging

---

## Why This Matters in Real IT / Cloud Operations

Network and cloud support roles require fast, repeatable diagnostic workflows. Manual one-off commands (`ping`, `nslookup`, `aws ec2 describe-instances`) are fine for a single host but don't scale across incidents, don't produce consistent output for ticket documentation, and can't be validated in CI.

This tool addresses that:

| Real scenario | How this tool helps |
|---|---|
| "DNS isn't propagating after a Route 53 change" | `nmcli dns <host>` — confirms the A record and PTR are live from the resolver's perspective |
| "Users can't reach the new EC2 instance" | `nmcli portscan <ip> --ports 22 80 443` — confirms which ports are open vs. blocked by security group |
| "Application times out connecting to the DB" | `nmcli portscan <rds-host> --ports 5432 3306` — rules out network as the cause in under 10 seconds |
| "Not sure if ICMP is blocked or if the host is down" | `nmcli ping` followed by `nmcli portscan` — separates ICMP filtering from actual unreachability |
| "Need to audit VPC config before a deployment" | `nmcli aws-vpc && nmcli aws-ec2` — snapshot of current VPC state and instance inventory |

The CI pipeline, branching strategy, decision log, and architecture documentation demonstrate that this isn't just a script — it's built with the process discipline expected in production engineering teams.

---

## Recruiter Note

Every command in this tool performs a real task done daily in network support and cloud operations: verifying DNS resolved after a Route 53 change, auditing which ports are exposed on an EC2 instance, confirming ICMP reachability after a VPC change, inventorying running instances. The CI pipeline ensures no change breaks the tool before it ships. Tests validate behavior without requiring a live environment.

AWS Cloud Practitioner in progress.

---

**Author:** Carter | [github.com/CartierC](https://github.com/CartierC)
