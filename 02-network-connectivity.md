# Lab 02 — Network Connectivity Diagnostics

## Objective
Demonstrate production-grade network troubleshooting using a Python CLI tool with AWS integration.

## Environment
- Python 3.10+
- AWS Free Tier account (configured via `aws configure`)
- Linux/macOS terminal

## Commands Executed

### 1. ICMP Connectivity Check
```bash
nmcli ping google.com --count 4
```
**Expected:** 0% packet loss, round-trip time < 50ms to public hosts.

### 2. Route Path Analysis
```bash
nmcli traceroute google.com
```
**Expected:** Full hop-by-hop path showing ISP → backbone → destination.

### 3. DNS Resolution
```bash
nmcli dns github.com
```
**Expected:** A record (IPv4), AAAA record (IPv6), PTR reverse lookup.

### 4. Port Audit
```bash
nmcli portscan github.com --ports 22 80 443
```
**Expected:** SSH (22), HTTP (80), HTTPS (443) all OPEN.

### 5. AWS VPC Inspection
```bash
nmcli aws-vpc
```
**Expected:** Table output showing VPC ID, CIDR block, default status.

### 6. EC2 Instance Inventory
```bash
nmcli aws-ec2
```
**Expected:** Instance ID, type, state, public IP for all running instances.

## Key Concepts Demonstrated
- TCP socket connection state (OPEN/CLOSED)
- DNS record types: A, AAAA, PTR
- ICMP packet behavior and latency
- AWS VPC architecture and CIDR notation
- boto3 SDK authentication via IAM credentials

## Real-World Application
This workflow mirrors L1/L2 network triage used by cloud engineers to:
- Validate connectivity after VPC changes
- Audit exposed ports on EC2 instances
- Confirm DNS propagation after Route 53 updates
