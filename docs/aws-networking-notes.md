# AWS Networking Notes

Reference for VPC, EC2, and network concepts used in this CLI tool and relevant to cloud support roles.

---

## VPC — Virtual Private Cloud

A VPC is a logically isolated section of the AWS cloud where you launch resources. It behaves like a private data center network inside AWS.

### Key VPC Components

| Component | Purpose |
|---|---|
| VPC | Isolated network boundary — defines the IP space |
| Subnet | Subdivision of the VPC (public or private) |
| Internet Gateway | Allows traffic between a VPC and the public internet |
| Route Table | Controls where traffic is directed within the VPC |
| NACL | Network ACL — stateless firewall at the subnet level |
| Security Group | Stateful firewall at the instance level |

### CIDR Notation

VPCs are defined by a CIDR block — the range of IP addresses available inside the VPC.

```
10.0.0.0/16    → 65,536 IP addresses (typical VPC range)
10.0.1.0/24   → 256 IP addresses (typical subnet range)
172.31.0.0/16  → default VPC range AWS assigns automatically
```

The `/16`, `/24` notation is the **prefix length** — it controls how many addresses are in the range. Smaller number = larger range.

### Public vs. Private Subnets

| Type | Has route to IGW | Has public IP | Use case |
|---|---|---|---|
| Public subnet | Yes | Optional | Web servers, load balancers, bastion hosts |
| Private subnet | No | No | Databases, app servers, internal services |

### How This CLI Uses VPC Data

```python
# nmcli/aws.py → get_vpc_info()
ec2 = boto3.client("ec2", region_name=region)
vpcs = ec2.describe_vpcs()["Vpcs"]
```

Output shows: VPC ID, CIDR block, whether it is the default VPC, and state.

---

## EC2 — Elastic Compute Cloud

EC2 instances are virtual machines running inside a VPC subnet.

### Instance States

| State | Meaning |
|---|---|
| `pending` | Starting up — not yet reachable |
| `running` | Active — should be reachable on open ports |
| `stopping` | Shutting down — will stop billing for compute |
| `stopped` | Off — storage still billed, no compute charge |
| `terminated` | Permanently deleted |

### Public vs. Private IPs on EC2

- **Public IP:** Assigned if instance is in a public subnet with "auto-assign public IP" enabled. Released when instance stops.
- **Elastic IP (EIP):** Static public IP that persists across stop/start cycles.
- **Private IP:** Always assigned. Used for internal VPC communication.

### How This CLI Uses EC2 Data

```python
# nmcli/aws.py → get_ec2_instances()
ec2 = boto3.client("ec2", region_name=region)
reservations = ec2.describe_instances()["Reservations"]
```

Output shows: Instance ID, instance type, state, and public IP.

---

## Security Groups

Security groups are **stateful** firewalls attached to EC2 instances (and other resources).

- **Stateful** means: if you allow inbound port 443, the response traffic is automatically allowed out — no separate outbound rule needed.
- Rules are **allow-only** — you cannot write a deny rule in a security group.
- Default behavior: all inbound **denied**, all outbound **allowed**.

### Common Security Group Patterns

```
Inbound rule: Port 443, Source 0.0.0.0/0   → HTTPS open to the world
Inbound rule: Port 22, Source 203.0.113.5/32  → SSH restricted to one IP
Inbound rule: Port 3306, Source sg-xxxxxxxx   → MySQL open only to app SG
```

### Diagnosing with This CLI

If `nmcli portscan <ec2-public-ip> --ports 22 443` shows a port as CLOSED, the most common causes in order:
1. Security group does not have an inbound rule for that port
2. NACL is blocking (check both inbound AND outbound — NACLs are stateless)
3. The application is not listening on that port
4. The instance is in a private subnet — no public IP routable

---

## NACLs vs. Security Groups

| Feature | NACL | Security Group |
|---|---|---|
| Applied at | Subnet level | Instance level |
| Stateful? | No — must allow both directions | Yes — responses auto-allowed |
| Rule type | Allow and Deny | Allow only |
| Rule order | Processed in number order | All rules evaluated |
| Default | Allow all | Deny all inbound |

**Key diagnostic point:** If traffic passes the security group but is still blocked, check the NACL. NACLs require explicit outbound allow rules for response traffic (ephemeral ports 1024-65535).

---

## boto3 Authentication

The AWS commands in this CLI use boto3, which follows the standard AWS credential chain:

```
1. Environment variables (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
2. AWS credentials file (~/.aws/credentials)
3. AWS config file (~/.aws/config)
4. IAM role (if running on EC2 or Lambda)
```

To set up locally:
```bash
aws configure
# Enter: Access Key ID, Secret Access Key, default region, output format
```

Error handling in this CLI:
```python
except NoCredentialsError:
    logger.error("AWS credentials not configured. Run: aws configure")
    return []
```

---

## Regions

AWS organizes infrastructure into geographic regions. Commands in this CLI default to `us-east-1` (N. Virginia).

```bash
# To query a different region, the code accepts a region parameter:
get_vpc_info(region="us-west-2")
```

Common regions:
- `us-east-1` — N. Virginia (most services launch here first)
- `us-west-2` — Oregon
- `eu-west-1` — Ireland
- `ap-southeast-1` — Singapore

---

## AWS Cloud Practitioner in Progress

These notes reflect concepts covered in the AWS Cloud Practitioner (CLF-C02) curriculum, applied to practical network support tasks.
