# Troubleshooting Guide

Structured fault isolation workflows for network and cloud support using this CLI tool.

---

## How to Use This Guide

Each section follows a decision-tree structure:

```
Symptom → First check → What the result means → Next action
```

Start at the symptom. Work top-to-bottom. Stop when you find the fault.

---

## Decision Tree: "Application is not reachable"

```
Application not reachable
│
├─ Step 1: Does DNS resolve?
│   nmcli dns <hostname>
│   ├─ No A record returned → DNS failure (go to DNS section)
│   └─ A record returned → Continue
│
├─ Step 2: Does the host respond to ping?
│   nmcli ping <ip-or-hostname> --count 4
│   ├─ 100% packet loss → Host unreachable or ICMP blocked (go to connectivity section)
│   └─ 0% packet loss → Continue
│
├─ Step 3: Is the required port open?
│   nmcli portscan <host> --ports 80 443
│   ├─ Port CLOSED → Service down or firewall blocking (go to port section)
│   └─ Port OPEN → Application-level issue — check app logs, SSL cert, HTTP response
│
└─ If AWS hosted: check instance state
    nmcli aws-ec2
    ├─ Instance stopped → Start it
    └─ Instance running → Check security group and NACL rules
```

---

## DNS Failure

**Symptom:** `nmcli dns` returns no A record, or application throws a name resolution error.

**Checks in order:**

1. Verify the hostname is spelled correctly.

2. Test with a known-good host to confirm the resolver itself works:
   ```bash
   nmcli dns google.com
   ```
   If this fails too, the local DNS resolver is down — check `/etc/resolv.conf`.

3. If only the target domain fails, check:
   - Was a DNS record recently changed? TTL may not have expired yet.
   - Is the domain registered and not expired?
   - For internal domains: confirm VPN is connected and the correct private DNS resolver is in use.

4. For AWS Route 53:
   - Confirm the hosted zone exists and is public or correctly associated with the VPC.
   - Confirm the A or CNAME record exists and points to the right resource.
   - Wait for TTL to expire after a record change (check the TTL value in the record).

**Resolution confirmed when:** `nmcli dns <hostname>` returns the expected A record.

---

## Host Unreachable — ICMP Failure

**Symptom:** `nmcli ping` shows 100% packet loss.

**Checks in order:**

1. Confirm DNS resolves first — you may be pinging a wrong or non-existent IP.

2. For AWS EC2 instances: ICMP is blocked by default in security groups.
   - Check if an inbound rule for ICMP (type: All ICMP - IPv4) exists.
   - If ICMP is intentionally blocked, skip ping and go directly to port check.

3. Check the instance is running:
   ```bash
   nmcli aws-ec2
   ```
   State should be `running`. If `stopped`, start it via AWS console or CLI.

4. Check NACL rules for the subnet — NACLs block ICMP by default unless explicitly allowed.

5. Run traceroute to see where the path breaks:
   ```bash
   nmcli traceroute <host>
   ```
   The last hop that responds is where to investigate.

**Resolution confirmed when:** `nmcli ping <host> --count 4` returns 0% packet loss, or the port check (next section) confirms the service is reachable even if ICMP is blocked.

---

## Port Closed / Connection Refused

**Symptom:** `nmcli portscan` shows expected port as CLOSED. Application returns "connection refused."

**Checks in order:**

1. Confirm the host resolves and is reachable (Steps 1-2 above).

2. For AWS EC2:
   - Check the security group has an inbound rule allowing the port from your IP (or 0.0.0.0/0 for public services).
   - Check the NACL allows both inbound on the port AND outbound on ephemeral ports (1024-65535).

3. Check whether the service is actually running on the instance:
   ```bash
   # SSH into the instance, then:
   systemctl status nginx        # or apache2, sshd, etc.
   netstat -tlnp | grep <port>   # confirm the process is listening
   ```

4. Check the application is binding to the right interface:
   - `127.0.0.1` means only localhost can connect — must be `0.0.0.0` for external access.
   - Check application config for `bind`, `listen`, or `host` settings.

5. For port 22 (SSH) specifically:
   - Restrict source IP in security group to prevent brute force.
   - Confirm `sshd` is running: `systemctl status sshd`.
   - Confirm the key pair is correct.

**Resolution confirmed when:** `nmcli portscan <host> --ports <port>` shows OPEN.

---

## Route Path Broken — Traceroute Analysis

**Symptom:** Intermittent drops, high latency, or path not reaching the destination.

**How to run:**
```bash
nmcli traceroute <host>
```

**Reading the output:**

```
 1  192.168.1.1       2ms   ← Local gateway — first hop out of your LAN
 2  100.64.0.1        8ms   ← ISP edge router
 3  * * *                   ← Hop filters ICMP — normal, not a problem
 4  * * *                   ← Same
 5  104.16.133.229   10ms   ← Destination responds — path is intact
```

**Asterisks (`* * *`)** mean that router does not return ICMP TTL-exceeded messages. This is common and not an error. If the destination answers, the path works.

**True break:** If traceroute stops at hop N and the destination does not respond:
- Hop N is the last point packets reach.
- The break is between hop N and hop N+1.
- If hop N is in AWS: check route tables, NACLs, or the target instance state.
- If hop N is at the ISP: escalate to the network carrier or wait for recovery.

**High latency at a specific hop:**
- Persistent high latency (>200ms added) at one hop may indicate congestion or a misconfigured route.
- Transient latency spikes are normal — run traceroute multiple times to confirm.

---

## AWS VPC Reachability Issues

**Symptom:** EC2 instance not reachable after a deploy, VPC config unclear.

**Step 1 — Check instance state:**
```bash
nmcli aws-ec2
```
- State = `stopped` → start the instance.
- State = `running`, PUBLIC IP = `N/A` → instance is in a private subnet. Requires bastion host or VPN to reach.

**Step 2 — Check VPC config:**
```bash
nmcli aws-vpc
```
- DEFAULT = `False` → custom VPC. Confirm an Internet Gateway is attached and route table points `0.0.0.0/0` to the IGW.
- CIDR overlap with another VPC → routing conflict if VPC peering is in use.

**Step 3 — Security group checklist:**
- Inbound rule exists for the required port from the correct source.
- Rule is on the correct security group (attached to the right instance or ENI).

**Step 4 — NACL checklist:**
- Inbound rule allows traffic on the required port.
- Outbound rule allows ephemeral ports (1024-65535) for response traffic.
- Rules are evaluated in number order — a lower-numbered DENY overrides a higher-numbered ALLOW.

---

## Escalation Checklist

Before escalating to L2/L3 or opening an AWS support ticket, confirm:

- [ ] `nmcli dns <hostname>` → A record resolves to expected IP
- [ ] `nmcli ping <host>` → 0% packet loss (or ICMP intentionally blocked and port check passes)
- [ ] `nmcli portscan <host> --ports <required>` → expected ports OPEN
- [ ] `nmcli traceroute <host>` → destination reached (no early break)
- [ ] `nmcli aws-ec2` → instance in `running` state
- [ ] `nmcli aws-vpc` → VPC state `available`, no CIDR conflicts
- [ ] Security group: inbound rule allows port from correct source
- [ ] NACL: both inbound and outbound rules allow required traffic
- [ ] Application: service is running and binding to correct interface

**When escalating, include:**
- Output of the above CLI commands
- Instance ID (from `nmcli aws-ec2`)
- VPC ID and subnet ID
- Security group ID and relevant rules
- Exact error message from the application or client
