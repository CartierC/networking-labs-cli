# Architecture — networking-labs-cli

## System Purpose

`networking-labs-cli` is a Python CLI tool that automates the core diagnostic tasks performed daily in network support, cloud operations, and NOC environments. It replaces manual, one-off shell commands with a structured, testable, and CI-validated tool that can be learned from, extended, and dropped into a support workflow.

---

## Component Map

```
networking-labs-cli/
│
├── main.py                  ← CLI entry point — argparse dispatcher
│
├── nmcli/
│   ├── core.py              ← Network ops: ping, traceroute, dns_lookup, port_scan
│   ├── aws.py               ← AWS ops: get_vpc_info, get_ec2_instances (boto3)
│   └── utils.py             ← Input validation, logging config
│
├── tests/
│   └── test_core.py         ← pytest unit tests — mock-based, CI-safe
│
├── scripts/
│   └── net-diag.sh          ← Standalone bash diagnostic (no Python required)
│
├── docs/                    ← Operational reference docs
├── labs/                    ← Step-by-step lab walkthroughs
├── sample-output/           ← Captured CLI output examples
└── .github/workflows/
    └── ci.yml               ← CI pipeline: test + lint + shell check
```

---

## Data and Process Flow

```
User CLI Input
      │
      ▼
main.py (argparse)
      │
      ├──── dns / ping / portscan / traceroute
      │           │
      │           ▼
      │       nmcli/core.py
      │       ├── socket (stdlib) — DNS, port checks
      │       ├── subprocess — ping, traceroute system calls
      │       └── nmcli/utils.py — host validation, structured logging
      │
      └──── aws-vpc / aws-ec2
                  │
                  ▼
              nmcli/aws.py
              └── boto3/botocore — AWS EC2 API calls
                  └── Handles: NoCredentialsError, ClientError
```

**Key properties:**
- No external service dependencies for network ops — uses Python stdlib (`socket`, `subprocess`)
- AWS ops require `aws configure` or an IAM role — fail gracefully with logged error, empty return
- All ops return structured data (dicts/lists) in addition to printing output — enables future JSON/CSV output flags
- All inputs pass through `validate_host()` before network calls — prevents subprocess injection via hostname

---

## Module Responsibilities

### `main.py`
- Defines the argparse CLI with 6 subcommands
- Dispatches to the correct module function
- Propagates exit codes: `sys.exit(0)` on success, `sys.exit(1)` on ping failure

### `nmcli/core.py`
- `ping(host, count)` → calls system `ping -c N host`, prints stdout, returns bool
- `traceroute(host)` → calls system `traceroute host`, prints stdout
- `dns_lookup(host)` → resolves A, AAAA, PTR via `socket.gethostbyname`, `getaddrinfo`, `gethostbyaddr`
- `port_scan(host, ports, timeout)` → TCP `connect_ex()` on each port, returns `{"open": [...], "closed": [...]}`
- Uses `COMMON_PORTS` dict (12 services) as default scan target when no ports specified

### `nmcli/aws.py`
- `get_vpc_info(region)` → `ec2.describe_vpcs()` — prints VPC ID, CIDR, default flag, state
- `get_ec2_instances(region)` → `ec2.describe_instances()` — prints instance ID, type, state, public IP
- Both default to `us-east-1`; both handle `NoCredentialsError` and `ClientError` gracefully

### `nmcli/utils.py`
- `validate_host(host)` → `socket.gethostbyname()` as a reachability pre-check; returns bool
- Configures root logger with timestamp + level format (applied once at import)

### `tests/test_core.py`
- 5 unit tests using `pytest` and `unittest.mock`
- No live network dependency — AWS test mocks `boto3.client` to raise `NoCredentialsError`
- DNS and port tests use real network but target stable public hosts (`google.com`, `127.0.0.1`)

---

## Operational Value

| Capability | Real-World Use |
|---|---|
| DNS lookup | Verify Route 53 record propagation after a change |
| Port scan | Audit exposed ports on an EC2 instance before go-live |
| Ping | Confirm ICMP reachability after a VPC routing change |
| Traceroute | Identify where packets drop between subnets or regions |
| VPC inventory | Enumerate VPCs and CIDR blocks for overlap audit |
| EC2 inventory | Check instance states and public IPs during an incident |

---

## Design Decisions

- **stdlib over third-party for networking:** `socket` and `subprocess` require no additional dependencies for core ops — the tool installs cleanly in restricted environments
- **subprocess for ping/traceroute:** Platform system tools handle ICMP correctly, including TTL logic — reimplementing in Python would require raw socket privileges (root)
- **boto3 region defaulting to us-east-1:** Matches the most common AWS default; `--region` flag is the prioritized next improvement
- **Structured return values alongside print output:** Functions return dicts/lists so unit tests can assert on data without parsing stdout; also enables future `--output json` mode

---

## Future Improvements

| Improvement | Value |
|---|---|
| `--region` flag on AWS subcommands | Multi-region inventory and triage |
| `--output json` flag | Pipeline-friendly output; feeds into monitoring tools |
| Route table and security group inspection | Full AWS network path audit from CLI |
| SNMP polling module | Extends tool into network device monitoring |
| CloudWatch metric queries | Adds performance telemetry to connectivity checks |
| `--verbose` flag | Full packet-level logging for deep debugging |
