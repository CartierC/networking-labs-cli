# networking-labs-cli

> Production-grade network diagnostics and AWS infrastructure automation CLI built with Python, boto3, and argparse.

## What This Project Demonstrates

- Python CLI architecture with modular package structure
- AWS SDK integration via boto3
- Custom networking module (nmcli) for diagnostics
- GitHub Actions CI/CD pipeline with automated testing
- Autonomous CI repair via Claude Code (diagnosed and fixed broken pipeline end-to-end)
- pytest test suite (5/5 passing)

## Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3 |
| AWS SDK | boto3 |
| Testing | pytest |
| CI/CD | GitHub Actions |
| Packaging | setuptools |
| AI Tooling | Claude Code (autonomous mode) |

## Tools Demonstrated

- ping, traceroute, nslookup
- Port scanning
- Linux/macOS network diagnostics
- AWS infrastructure automation

## CI/CD Pipeline

| Run | Trigger | Status |
|-----|---------|--------|
| #1 | Initial workflow | ❌ Failed |
| #2 | Actions version update | ❌ Failed |
| #3 | Autonomous fix branch | ✅ Passed |
| #4 | Merge to main | ✅ Passed |

Root cause diagnosed and resolved via Claude Code autonomous repair mode.

## Run Locally

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 -m pytest tests/
```

## Author

Carter | [](https://github.com/CartierC)
