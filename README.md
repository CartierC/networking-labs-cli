# networking-labs-cli

Python network automation CLI for DNS lookup, port checks, connectivity testing, AWS VPC/EC2 concepts, and CI/CD validation.

---

## Purpose

This project demonstrates practical network engineering skills through a working command-line tool. Every command maps directly to a real troubleshooting workflow used in NOC, cloud support, and infrastructure roles.

---

## Target Roles

- Network Support Engineer
- Cloud Support Engineer
- NOC Analyst
- Infrastructure Support / L1/L2 Operations

---

## Skills Demonstrated

| Skill | Where |
|---|---|
| DNS lookup (A, AAAA, PTR records) | `nmcli/core.py` → `dns_lookup()` |
| TCP port scanning (open/closed audit) | `nmcli/core.py` → `port_scan()` |
| ICMP connectivity testing | `nmcli/core.py` → `ping()` |
| Route path analysis | `nmcli/core.py` → `traceroute()` |
| AWS VPC enumeration via boto3 | `nmcli/aws.py` → `get_vpc_info()` |
| AWS EC2 instance inventory | `nmcli/aws.py` → `get_ec2_instances()` |
| Python CLI with argparse | `main.py` |
| Unit testing with pytest | `tests/test_core.py` — 5/5 passing |
| CI/CD pipeline validation | `.github/workflows/test.yml` |
| Input validation and error handling | `nmcli/utils.py` → `validate_host()` |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10+ |
| AWS SDK | boto3 / botocore |
| CLI Framework | argparse |
| Testing | pytest |
| CI/CD | GitHub Actions (ubuntu-latest) |
| Packaging | setuptools + pip |

---

## Project Structure

```
networking-labs-cli/
├── main.py                        # CLI entry point — 6 subcommands
├── nmcli/
│   ├── core.py                    # ping, traceroute, dns_lookup, port_scan
│   ├── aws.py                     # get_vpc_info, get_ec2_instances (boto3)
│   └── utils.py                   # validate_host, logging config
├── tests/
│   └── test_core.py               # 5 unit tests — all passing
├── labs/
│   ├── 01-dns-troubleshooting.md  # DNS triage runbook
│   └── 02-network-connectivity.md # Full connectivity lab walkthrough
├── docs/
│   └── network-support-runbook.md # NOC-style escalation runbook
├── sample-output/
│   └── network-check-output.txt   # Real CLI output examples
├── scripts/
│   └── net-diag.sh                # Shell diagnostic helper
├── .github/workflows/
│   └── test.yml                   # CI pipeline — runs pytest on every push
├── requirements.txt
└── setup.py
```

---

## How to Run

```bash
# Set up environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .

# Run the CLI
nmcli dns google.com
nmcli ping 8.8.8.8 --count 4
nmcli portscan github.com --ports 22 80 443
nmcli traceroute cloudflare.com

# AWS commands (requires: aws configure)
nmcli aws-vpc
nmcli aws-ec2

# Run tests
python3 -m pytest tests/ -v
```

---

## Sample Output

**DNS Lookup**
```
$ nmcli dns github.com
  A        → 140.82.114.4
  AAAA     → (not available)
  PTR      → lb-140-82-114-4-sea.github.com
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

**Ping / Connectivity**
```
$ nmcli ping 8.8.8.8 --count 4
PING 8.8.8.8: 56 data bytes
64 bytes from 8.8.8.8: icmp_seq=0 ttl=118 time=11.2 ms
64 bytes from 8.8.8.8: icmp_seq=1 ttl=118 time=10.8 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=118 time=11.5 ms
64 bytes from 8.8.8.8: icmp_seq=3 ttl=118 time=10.9 ms

--- 8.8.8.8 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss
```

**AWS VPC**
```
$ nmcli aws-vpc
VPC ID                 CIDR                 DEFAULT    STATE
-----------------------------------------------------------------
vpc-0abc1234def56789   10.0.0.0/16          False      available
vpc-0default000000000  172.31.0.0/16        True       available
```

See [sample-output/network-check-output.txt](sample-output/network-check-output.txt) for the full run.

---

## CI/CD Pipeline

| Run | Trigger | Result |
|---|---|---|
| #1 | Initial workflow push | Failed — misconfigured Actions version |
| #2 | Actions version fix | Failed — missing setuptools import |
| #3 | Autonomous CI repair branch | Passed |
| #4 | Merge to main | Passed |

Root cause of initial failures: outdated Actions versions + missing `setuptools` in `setup.py`. Diagnosed and resolved via Claude Code autonomous repair mode.

Current status: **all pushes to main trigger automated pytest — 5/5 tests pass.**

---

## What This Project Proves

- Can write a modular Python CLI from scratch using argparse and socket libraries
- Understands DNS record types (A, AAAA, PTR) and how to query them programmatically
- Knows TCP connectivity state — port scan logic uses `connect_ex()` to detect open/closed ports
- Familiar with AWS SDK (boto3): can enumerate VPCs, describe EC2 instances, handle `NoCredentialsError`
- Can write and maintain pytest test suites, including mocking AWS SDK calls
- Can read, debug, and fix broken GitHub Actions CI pipelines
- Applies structured logging and input validation to CLI tools

---

## Next Improvements

- Add `--region` flag to AWS commands
- Add SNMP polling module
- Add JSON/CSV output format option
- Add route table and security group inspection
- Integrate with AWS CloudWatch for metric queries

---

## Recruiter Note

Every command in this tool maps to a task performed daily in network support and cloud operations roles: checking if a DNS record resolved correctly after a change, auditing which ports are exposed on a server, verifying ICMP reachability, and inventorying AWS infrastructure. The CI pipeline ensures nothing is broken before it ships. The test suite validates behavior without requiring a live network or AWS account.

AWS Cloud Practitioner in progress.

---

**Author:** Carter | [github.com/CartierC](https://github.com/CartierC)
