# Network Support Runbook

Operations guide for DNS, connectivity, and port triage using the networking-labs-cli tool.

---

## Overview

This runbook covers the five most common L1/L2 escalation paths in cloud and network support:

1. DNS resolution failure
2. Host unreachable / no ICMP response
3. Port closed or connection refused
4. Route path broken (traceroute)
5. AWS VPC/EC2 reachability

Each section includes the symptom, the CLI command to run, how to read the output, and what to do next.

---

## 1. DNS Resolution Failure

**Symptom:** Browser shows "DNS_PROBE_FINISHED_NXDOMAIN" or application throws `socket.gaierror`.

**Command:**
```bash
nmcli dns <hostname>
```

**What to check:**

| Output | Meaning |
|---|---|
| `A → <IP>` present | DNS resolving correctly |
| No output / error logged | Host not resolving — DNS failure |
| `PTR →` missing | Reverse DNS not configured (usually OK for external hosts) |

**Next steps if DNS fails:**
1. Check local resolver: `cat /etc/resolv.conf`
2. Try a public resolver: `nmcli dns <hostname>` (uses system resolver by default)
3. Verify the domain exists: cross-check with a second DNS server (8.8.8.8 or 1.1.1.1)
4. If internal domain: check if the host is on the correct VPN / private subnet
5. If Route 53: confirm the record set exists and TTL has expired since the last change

---

## 2. Host Unreachable — ICMP Test

**Symptom:** Timeout errors, no response from host, application cannot connect.

**Command:**
```bash
nmcli ping <host> --count 4
```

**What to check:**

| Output | Meaning |
|---|---|
| `0% packet loss` | Host is reachable, ICMP allowed |
| `100% packet loss` | Host unreachable or ICMP blocked by firewall/security group |
| High RTT (>200ms) | Network congestion or routing issue |

**Next steps if unreachable:**
1. Confirm DNS resolves first (Step 1)
2. Check AWS security group inbound rules — ICMP may be blocked
3. Check NACL rules for the subnet
4. Try traceroute to see where the path breaks (Step 4)
5. Verify the instance is in a running state: `nmcli aws-ec2`

---

## 3. Port Closed / Connection Refused

**Symptom:** `Connection refused` or service not responding on expected port.

**Command:**
```bash
nmcli portscan <host> --ports 22 80 443
```

**What to check:**

| Output | Meaning |
|---|---|
| `OPEN` | Port is reachable and accepting connections |
| `CLOSED` | Port is not accepting connections — service down or firewall blocking |

**Common port reference:**

| Port | Service | Common issue |
|---|---|---|
| 22 | SSH | Security group blocks 22 inbound |
| 80 | HTTP | Web server not started |
| 443 | HTTPS | TLS cert error or service down |
| 3306 | MySQL | DB not bound to 0.0.0.0 or SG restricts |
| 6379 | Redis | Redis not exposed externally (expected) |

**Next steps if port is closed:**
1. SSH into host and confirm service is running: `systemctl status <service>`
2. Check AWS security group allows inbound on that port from your IP
3. Check NACL: NACLs are stateless and must allow both inbound AND outbound
4. Confirm the application is binding to the correct interface (0.0.0.0 vs 127.0.0.1)

---

## 4. Route Path Analysis — Traceroute

**Symptom:** Intermittent connectivity, high latency, packets dropping mid-path.

**Command:**
```bash
nmcli traceroute <host>
```

**How to read output:**

```
 1  192.168.1.1     2.3 ms    ← local gateway (LAN)
 2  100.64.0.1      8.4 ms    ← ISP edge
 3  72.14.215.165  12.2 ms    ← backbone transit
 4  * * *                     ← hop filtering ICMP (normal)
 5  104.16.133.229 10.4 ms    ← destination
```

**Asterisks (`* * *`)** mean that hop is not returning ICMP responses — not necessarily a break. If the destination responds, the path is working.

**Next steps if path breaks:**
1. Identify the last responding hop — that's where to investigate
2. Check if the destination host is in a private subnet with no public route
3. If hop 1 (gateway) is the problem: local network issue, check router/DHCP
4. If break is mid-path: upstream ISP or routing issue — escalate or wait for recovery

---

## 5. AWS VPC / EC2 Reachability

**Symptom:** EC2 instance not reachable after deploy, VPC configuration unknown.

**Commands:**
```bash
nmcli aws-vpc    # list VPCs and CIDR blocks
nmcli aws-ec2    # list EC2 instances, states, and public IPs
```

**VPC output — what to check:**

| Column | What it means |
|---|---|
| `VPC ID` | The VPC containing the instance |
| `CIDR` | Address range — ensure no overlap with on-prem or peered VPCs |
| `DEFAULT` | True = default VPC (internet gateway attached by default) |
| `STATE` | Should be `available` |

**EC2 output — what to check:**

| Column | What it means |
|---|---|
| `INSTANCE ID` | Unique identifier for AWS support tickets |
| `TYPE` | Instance size — relevant for CPU/memory issues |
| `STATE` | `running` = operational; `stopped` = needs start |
| `PUBLIC IP` | `N/A` if instance has no public IP (private subnet) |

**Next steps:**
1. No public IP → instance is in a private subnet → access via bastion host or VPN
2. State = `stopped` → start via AWS console or `aws ec2 start-instances`
3. CIDR overlap → route conflict → check route tables and VPC peering config
4. Credentials error → run `aws configure` or check IAM role permissions

---

## Escalation Checklist

Before escalating to L2/L3 or opening an AWS support ticket:

- [ ] DNS resolves to the expected IP
- [ ] Host responds to ICMP ping
- [ ] Required ports are OPEN in port scan
- [ ] Traceroute reaches the destination without breaking early
- [ ] EC2 instance is in `running` state
- [ ] Security group allows inbound traffic on required ports
- [ ] NACL allows both inbound and outbound on required ports
- [ ] Instance has a public IP (or bastion access configured for private subnets)

---

## Tool Reference

| Command | What it does |
|---|---|
| `nmcli dns <host>` | Resolve A, AAAA, PTR records |
| `nmcli ping <host> --count N` | ICMP reachability test |
| `nmcli portscan <host> --ports N ...` | TCP port audit |
| `nmcli traceroute <host>` | Hop-by-hop route analysis |
| `nmcli aws-vpc` | List VPCs in us-east-1 |
| `nmcli aws-ec2` | List EC2 instances |
