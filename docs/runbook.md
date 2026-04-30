# Project Runbook — networking-labs-cli

Operations guide for installing, running, testing, and maintaining this tool. For NOC-level usage (how to use the tool to diagnose network issues), see [network-support-runbook.md](network-support-runbook.md).

---

## Prerequisites

| Requirement | Version | Notes |
|---|---|---|
| Python | 3.10+ | `python3 --version` |
| pip | Any | Comes with Python |
| boto3 / botocore | >=1.34.0 | Installed via `requirements.txt` |
| AWS CLI config | Optional | Required only for `aws-vpc` and `aws-ec2` commands |
| ping / traceroute | System tool | Pre-installed on Linux and macOS |

---

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/CartierC/networking-labs-cli.git
cd networking-labs-cli

# 2. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate          # macOS/Linux
# venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Install the package in editable mode
pip install -e .

# 5. Verify the CLI is installed
nmcli --help
```

Expected output from `nmcli --help`:
```
usage: nmcli [-h] {ping,traceroute,dns,portscan,aws-vpc,aws-ec2} ...

Network Automation CLI — production-grade diagnostics & AWS integration
```

---

## Running the Tool

### Core network commands

```bash
# DNS record lookup (A, AAAA, PTR)
nmcli dns google.com

# ICMP ping
nmcli ping 8.8.8.8 --count 4

# Port scan (default: 12 common ports)
nmcli portscan github.com

# Port scan (specific ports)
nmcli portscan github.com --ports 22 80 443

# Traceroute
nmcli traceroute cloudflare.com
```

### AWS commands (requires `aws configure`)

```bash
# List VPCs in us-east-1
nmcli aws-vpc

# List EC2 instances in us-east-1
nmcli aws-ec2
```

If AWS credentials are not configured, the command will log an error and exit cleanly — no crash.

### Shell diagnostic script (no Python required)

```bash
chmod +x scripts/net-diag.sh
./scripts/net-diag.sh
```

Runs ping, nslookup, nc (netcat), and traceroute to google.com. Useful as a baseline connectivity check before running the Python CLI.

---

## Verifying the Tool Works

### Run the test suite

```bash
python3 -m pytest tests/ -v
```

Expected output:
```
tests/test_core.py::test_validate_host_valid            PASSED
tests/test_core.py::test_validate_host_invalid          PASSED
tests/test_core.py::test_port_scan_returns_dict         PASSED
tests/test_core.py::test_dns_lookup_returns_dict        PASSED
tests/test_core.py::test_get_vpc_info_no_credentials    PASSED

5 passed in X.XXs
```

### Run Python syntax validation

```bash
python3 -m compileall nmcli/ main.py -q
```

No output = no syntax errors.

### Run flake8 (errors only)

```bash
pip install flake8
flake8 nmcli/ main.py --max-line-length=100 --select=E9,F63,F7,F82
```

No output = no errors detected.

### Validate shell script syntax

```bash
bash -n scripts/net-diag.sh
```

No output = valid bash syntax.

---

## Updating Dependencies

```bash
# Update a specific package
pip install --upgrade boto3

# Regenerate requirements.txt after updates
pip freeze | grep -E "boto3|botocore" > requirements.txt
```

---

## Deploying a Change

```bash
# 1. Create a feature branch from dev
git checkout dev && git pull origin dev
git checkout -b feature/<description>

# 2. Make changes, run tests locally
python3 -m pytest tests/ -v

# 3. Push and open a PR to dev
git push -u origin feature/<description>
# Open PR on GitHub: feature/<description> → dev

# 4. CI will run automatically on push
# Verify: GitHub Actions tab → ci.yml → all steps green

# 5. After PR is merged to dev, open PR: dev → main
```

See [branching-strategy.md](branching-strategy.md) for the full branch workflow.

---

## Troubleshooting Common Setup Issues

### `nmcli: command not found` after `pip install -e .`

The virtual environment is not activated.

```bash
source venv/bin/activate
nmcli --help
```

Or the editable install did not register the entry point. Reinstall:

```bash
pip install -e . --force-reinstall
```

### `ModuleNotFoundError: No module named 'boto3'`

Dependencies not installed:

```bash
pip install -r requirements.txt
```

### `AWS credentials not configured`

Run `aws configure` and enter your Access Key ID, Secret Access Key, and default region. Or, if running on an EC2 instance, attach an IAM role with `ec2:DescribeVpcs` and `ec2:DescribeInstances` permissions.

### `ping: command not found` or `traceroute: command not found`

Install the system tools:

```bash
# Ubuntu/Debian
sudo apt-get install -y iputils-ping traceroute

# macOS (usually pre-installed)
brew install inetutils
```

### Tests fail with `socket.gaierror` on `test_validate_host_invalid`

This test confirms that an invalid hostname fails resolution. If your network has a DNS resolver that returns a catch-all IP for invalid domains (common with ISP DNS), this test may fail. Use a network with a standards-compliant DNS resolver, or run tests in CI where the resolver returns NXDOMAIN correctly.

---

## Expected CI Behavior

On every push or PR to `main` or `dev`, the CI pipeline (`ci.yml`) runs:

1. **Checkout** — fetches the branch
2. **Setup Python 3.10** — installs the runtime
3. **Install dependencies** — installs boto3, botocore, pytest, flake8
4. **Lint** — `flake8 nmcli/ main.py --select=E9,F63,F7,F82`
5. **Shell check** — `bash -n scripts/net-diag.sh`
6. **Run tests** — `pytest tests/ -v`

All steps must pass for the CI badge to show green.
