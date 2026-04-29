# Screenshots

This directory is reserved for terminal screenshots demonstrating the CLI in action.

## Planned screenshots

| File | Command | Shows |
|---|---|---|
| `dns-lookup.png` | `nmcli dns github.com` | A record, PTR record resolution |
| `port-scan.png` | `nmcli portscan github.com --ports 22 80 443` | Open/closed port table |
| `ping-test.png` | `nmcli ping 8.8.8.8 --count 4` | 0% packet loss output |
| `traceroute.png` | `nmcli traceroute cloudflare.com` | Hop-by-hop path |
| `aws-vpc.png` | `nmcli aws-vpc` | VPC ID, CIDR, state table |
| `ci-passing.png` | GitHub Actions run | Green CI badge + pytest output |

## To capture a screenshot (macOS)

```bash
# Run the command in a clean terminal window, then:
# Cmd + Shift + 4 → select the terminal area
# File saves to Desktop as Screenshot-<date>.png
# Move to this directory and rename
```

## Text-based output

For a full text-based output sample, see [sample-output/network-check-output.txt](../sample-output/network-check-output.txt).
