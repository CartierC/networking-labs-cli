# Lab 01: DNS Troubleshooting

## Objective
Resolve a domain name to an IP address and verify proper DNS resolution.

## Tools
- nslookup
- dig
- ping
- traceroute

## Steps

### 1 — Resolve DNS 
nslookup google.com

Expected output:
Address: 142.250.x.x

### 2 — Verify Connectivity
ping google.com

Confirm packets return successfully.

### 3 — Check TTL
nslookup -debug google.com

Observe TTL values in response.

### 4 — Validate Local Hosts File

Linux:
cat/etc/hosts

Windows:
C:\Windows\System32\drivers\etc\hosts

Ensure no incorrect domain overrides exist.

## Result

If DNS resolves correctly, the system can convert a domain name into a reachable IP address.
