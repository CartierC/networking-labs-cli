# Lab 02: Network Connectivity Troubleshooting

## Objective
Determine whether a host can reach external networks and identify where connectivity fails.

## Tools
- ping
- traceroute / tracert
- ipconfig / ifconfig

## Steps

### 1 — Verify Local Network Configuration

Windows:

ipconfig

Linux:

ifconfig

Confirm the system has a valid IP address.

---

### 2 — Test External Connectivity

ping google.com

Expected result:
Packets return successfully.

---

### 3 — Trace the Network Path

Windows:

tracert google.com

Linux:

traceroute google.com

This identifies where packets stop along the route.

---

## Result

Connectivity testing confirms whether the system can communicate with external hosts.