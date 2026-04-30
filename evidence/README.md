# Evidence — networking-labs-cli

This directory contains real, locally-executed command outputs that prove the tool works as documented. No outputs were fabricated or copied from documentation.

**Captured:** 2026-04-30 | **Platform:** macOS Darwin 25.4.0 | **Python:** 3.14.3

---

## What Is Proved Here

| Capability | Evidence |
|---|---|
| DNS A, AAAA, PTR resolution | Real queries to github.com, google.com, cloudflare.com |
| DNS error handling | Resolution failure on invalid host — graceful logged error, no crash |
| ICMP connectivity test | Live ping to 8.8.8.8 — 0% loss, 20.7ms avg RTT |
| TCP port scanning | github.com (22/80/443 all OPEN), 8.8.8.8 (53/443 OPEN, 80 CLOSED — correct) |
| Route path analysis | 13-hop traceroute to dns.google (8.8.8.8) — destination reached |
| AWS credential error handling | NoCredentialsError caught, logged, clean exit — no crash |
| Unit test suite | 5/5 pytest tests passing on Python 3.14.3 |
| Python lint | flake8 0 errors on nmcli/ and main.py |
| Shell syntax | bash -n passes on scripts/net-diag.sh |
| Shell diagnostic script | bash net-diag.sh — ping, nslookup, nc, traceroute all working |
| Entry point bug discovery | setup.py missing py_modules=['main'] — found and fixed |

---

## Files in This Directory

| File | Contents |
|---|---|
| [validation-summary.md](validation-summary.md) | Full validation report with all command outputs, analysis, and bug disclosure |

## Related

| File | Contents |
|---|---|
| [../logs/local-validation.log](../logs/local-validation.log) | Chronological raw log of all commands run, with full output and timestamps |

---

## How This Evidence Was Captured

1. Clean venv created: `python3 -m venv venv && source venv/bin/activate`
2. Dependencies installed: `pip install boto3 botocore pytest flake8 && pip install -e .`
3. Each CLI command was run once in a live terminal session
4. Outputs were copied verbatim — no editing of results
5. Failures were documented honestly (entry point bug)

The only environment variable required is a working internet connection. No AWS credentials, no cloud access, no special tooling beyond standard Python and macOS system tools.
