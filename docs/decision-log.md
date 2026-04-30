# Decision Log — networking-labs-cli

Architecture and design decisions recorded with rationale. Used to explain choices that aren't obvious from the code.

---

## 2026-04-30 — Use stdlib socket instead of dnspython for DNS lookups

**Decision:** DNS resolution implemented via Python's `socket.gethostbyname()` and `socket.gethostbyaddr()` rather than the `dnspython` third-party library.

**Reason:** The tool is designed to run in restricted support environments (EC2 instances, jumpboxes, minimal VMs) where installing additional packages may require approval or internet access. `socket` is always available and requires no extra installation.

**Tradeoff:** `dnspython` would support direct queries to specific resolvers (e.g., `dig @8.8.8.8`), DNSSEC validation, and raw record types (MX, TXT, NS). The stdlib approach delegates to the system resolver, which is the correct behavior for replicating how applications experience DNS — the same resolver the application would use.

**Impact:** Simpler dependency tree, wider compatibility. The limitation (no resolver override) is documented as a future improvement.

---

## 2026-04-30 — Use subprocess for ping and traceroute instead of raw sockets

**Decision:** `ping` and `traceroute` are implemented by calling system tools via `subprocess.run()` rather than implementing ICMP from scratch using raw sockets.

**Reason:** Raw ICMP sockets require root/administrator privileges on most systems. The tool is intended to run as a standard user in support and dev environments. System `ping` and `traceroute` tools handle ICMP correctly, including TTL logic, sequence numbers, and platform-specific behavior.

**Tradeoff:** The tool depends on `ping` and `traceroute` being installed on the host OS. On macOS the flags differ slightly from Linux (e.g., `ping -c` works on both, but `traceroute` vs `tracepath` varies). A future improvement could detect the OS and adjust flags accordingly.

**Impact:** Correct ICMP behavior without elevated privileges. The subprocess dependency is constrained to two functions and is easy to swap in the future.

---

## 2026-04-30 — Return structured data from all core functions in addition to printing

**Decision:** Functions in `core.py` and `aws.py` print formatted output to stdout AND return structured data (`dict` or `list`). They do not return `None`.

**Reason:** Unit tests need to assert on function output without parsing stdout. Returning structured data makes the test layer clean and decoupled from display formatting. It also enables a future `--output json` flag without changing the core logic — the dispatcher in `main.py` would call the function and format the return value instead of letting the function print directly.

**Tradeoff:** Functions have two responsibilities (compute + display). Ideally, display would be fully separated into a presenter layer. This is acceptable for the current scope; the `--output json` improvement would be the natural forcing function to refactor the display layer.

**Impact:** All 5 unit tests assert on return values, not on captured stdout. Functions remain reusable if the tool is imported as a library.

---

## 2026-04-30 — CI workflow validates both Python and shell code

**Decision:** The CI pipeline (`ci.yml`) runs three validation steps: pytest (correctness), flake8 (Python errors), and bash syntax check for `scripts/net-diag.sh`.

**Reason:** The repo contains both Python (the main CLI tool) and Bash (the diagnostic shell script). Both should be validated on every push. A broken shell script is easy to miss if only Python is tested.

**Tradeoff:** `flake8` is scoped to error-class checks only (`E9,F63,F7,F82`) — syntax errors, undefined names, and invalid escape sequences — rather than full PEP 8 style. Full style linting would flag existing code (line length, import ordering) and require a formatting cleanup pass. The priority is catching real errors, not enforcing style, so style rules are deferred.

**Impact:** CI catches Python syntax errors and undefined names before they reach `main`. The shell script is validated with `bash -n` (syntax-only, no execution) — no side effects during CI.

---

## 2025-XX-XX — boto3 credential errors handled at function level, not at CLI level

**Decision:** `NoCredentialsError` and `ClientError` are caught inside `nmcli/aws.py` functions. The CLI does not check for AWS credentials before dispatching to AWS subcommands.

**Reason:** Checking credentials at the CLI level would require importing boto3 and running a test API call before the user runs their intended command — adding latency and complexity. Handling at the function level means the error is caught exactly where it occurs, logged clearly, and the function returns an empty list. The user sees a useful log message (`"AWS credentials not configured. Run: aws configure"`) and the CLI exits cleanly.

**Tradeoff:** No pre-flight credential check means the user only discovers credential issues at runtime. This is the standard behavior for AWS CLI tools and SDKs.

**Impact:** Test `test_get_vpc_info_no_credentials` validates this path using `unittest.mock` — confirms the function handles the error without crashing and returns `[]`.
