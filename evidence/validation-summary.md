# Validation Summary — networking-labs-cli

**Date:** 2026-04-30
**Environment:** macOS Darwin 25.4.0, Python 3.14.3 (venv)
**Branch:** feature/tier-3-evidence-pack

All results below are from real local command execution. No outputs fabricated.

---

## Overall Result: ALL CHECKS PASSED

| Category | Command | Result | Detail |
|---|---|---|---|
| CLI Entry Point | `nmcli --help` | PASS | 6 subcommands registered |
| DNS | `nmcli dns github.com` | PASS | A=140.82.113.3, AAAA, PTR resolved |
| DNS | `nmcli dns google.com` | PASS | A=142.251.15.138, AAAA, PTR resolved |
| DNS | `nmcli dns cloudflare.com` | PASS | A+AAAA resolved; PTR warning expected (no rDNS on anycast) |
| DNS Error Handling | `nmcli dns <invalid>` | PASS | Graceful logged error, no crash, exit 0 |
| ICMP Ping | `nmcli ping 8.8.8.8 --count 4` | PASS | 0.0% packet loss, avg 20.7ms RTT |
| Port Scan | `nmcli portscan github.com --ports 22 80 443` | PASS | All 3 ports OPEN |
| Port Scan | `nmcli portscan 8.8.8.8 --ports 53 80 443` | PASS | 53/443 OPEN, 80 CLOSED (correct) |
| Traceroute | `nmcli traceroute 8.8.8.8` | PASS | 13-hop path, reaches dns.google |
| AWS (no creds) | `nmcli aws-vpc` | PASS | NoCredentialsError caught, exit 0 |
| AWS (no creds) | `nmcli aws-ec2` | PASS | NoCredentialsError caught, exit 0 |
| Unit Tests | `pytest tests/ -v` | PASS | 5/5 passing |
| Lint | `flake8 --select=E9,F63,F7,F82` | PASS | 0 errors |
| Shell Syntax | `bash -n scripts/net-diag.sh` | PASS | Valid bash syntax |
| Compile Check | `python3 -m compileall` | PASS | No syntax errors |
| Shell Script | `bash scripts/net-diag.sh` | PASS | ping, nslookup, nc, traceroute working |

---

## DNS Evidence

Real resolution results from 2026-04-30:

```
$ nmcli dns github.com
  A        → 140.82.113.3
  AAAA     → ::ffff:140.82.113.3
  PTR      → lb-140-82-113-3-iad.github.com
  aliases  → ['3.113.82.140.in-addr.arpa']

$ nmcli dns google.com
  A        → 142.251.15.138
  AAAA     → 2607:f8b0:4002:c2c::71
  PTR      → yl-in-f138.1e100.net
  aliases  → ['138.15.251.142.in-addr.arpa']

$ nmcli dns cloudflare.com
  A        → 104.16.132.229
  AAAA     → 2606:4700::6810:84e5
  [WARNING] Reverse DNS failed — expected on Cloudflare anycast IPs
```

---

## ICMP Ping Evidence

```
$ nmcli ping 8.8.8.8 --count 4

PING 8.8.8.8 (8.8.8.8): 56 data bytes
64 bytes from 8.8.8.8: icmp_seq=0 ttl=112 time=21.397 ms
64 bytes from 8.8.8.8: icmp_seq=1 ttl=112 time=21.107 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=112 time=23.751 ms
64 bytes from 8.8.8.8: icmp_seq=3 ttl=112 time=16.634 ms

4 packets transmitted, 4 packets received, 0.0% packet loss
round-trip min/avg/max/stddev = 16.634/20.722/23.751/2.573 ms
```

---

## Port Scan Evidence

```
$ nmcli portscan github.com --ports 22 80 443

PORT     SERVICE          STATUS
-----------------------------------
22       SSH              OPEN
80       HTTP             OPEN
443      HTTPS            OPEN
Summary: 3 open, 0 closed

$ nmcli portscan 8.8.8.8 --ports 53 80 443

PORT     SERVICE          STATUS
-----------------------------------
53       DNS              OPEN
80       HTTP             CLOSED
443      HTTPS            OPEN
Summary: 2 open, 1 closed
```

Port 80 closed on 8.8.8.8 is correct — Google's DNS resolver does not serve HTTP. Port 53 (TCP DNS) and 443 (DNS-over-HTTPS) are expected open.

---

## Traceroute Evidence

13-hop path from local machine to Google DNS (8.8.8.8):

```
$ nmcli traceroute 8.8.8.8

 1  sbe1v1k.lan (192.168.1.1)           — local gateway
 2  35.151.157.0 (Spectrum ISP edge)     — ISP handoff
 3  * * *                                — ICMP filtered (normal)
 8  rcr01sghlgaao (Spectrum backbone)    — regional backbone
 9  bbr01atlnga (Atlanta PoP)            — long-haul backbone
10  prr01atlnga (Atlanta peering)        — peering exchange
11  142.250.172.234                      — Google network entry
13  dns.google (8.8.8.8)                 — DESTINATION REACHED
```

Hops with `* * *` are routers that filter ICMP TTL-exceeded messages — this is standard ISP behavior, not a path break. Destination confirmed reached at hop 13.

---

## AWS Error Handling Evidence

```
$ nmcli aws-vpc
[INFO] Fetching VPC data from AWS region: us-east-1
[ERROR] AWS credentials not configured. Run: aws configure
EXIT CODE: 0

$ nmcli aws-ec2
[INFO] Fetching EC2 instances in us-east-1
[ERROR] AWS credentials not configured.
EXIT CODE: 0
```

The tool catches `botocore.exceptions.NoCredentialsError`, logs a user-actionable error message, and exits cleanly with code 0. The unit test `test_get_vpc_info_no_credentials` validates this exact path with `unittest.mock`.

---

## Unit Test Evidence

```
$ python3 -m pytest tests/ -v

platform darwin -- Python 3.14.3, pytest-9.0.3
rootdir: /Users/carter/Projects/Automation/networking-labs-cli

tests/test_core.py::test_validate_host_valid           PASSED   [ 20%]
tests/test_core.py::test_validate_host_invalid         PASSED   [ 40%]
tests/test_core.py::test_port_scan_returns_dict        PASSED   [ 60%]
tests/test_core.py::test_dns_lookup_returns_dict       PASSED   [ 80%]
tests/test_core.py::test_get_vpc_info_no_credentials   PASSED   [100%]

5 passed in 0.08s
```

---

## Bug Found and Fixed

During this evidence run, the `nmcli` CLI entry point failed immediately after `pip install -e .`:

```
$ nmcli dns github.com
Traceback (most recent call last):
  File ".../venv/bin/nmcli", line 3, in <module>
    from main import main
ModuleNotFoundError: No module named 'main'
```

**Root cause:** `setup.py` used `find_packages()` which discovers only packages (directories with `__init__.py`). `main.py` is a standalone root-level module — it was not included in the editable install's import path mapping.

**Fix:** Added `py_modules=["main"]` to `setup.py`. This explicitly registers `main.py` as an installable module.

**Why CI passed despite this bug:** The GitHub Actions workflow runs `pytest tests/ -v` which imports from the `nmcli` package — it never calls the `nmcli` entry point script directly. Tests passed; the CLI itself did not work on a fresh install.

**Impact:** Any user following the README install instructions (`pip install -e .` then `nmcli dns ...`) would hit this error. Fixed and documented.

---

## Full Log

See [../logs/local-validation.log](../logs/local-validation.log) for complete timestamped command output.
