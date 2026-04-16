import argparse
import sys
from nmcli import core, aws


def build_parser():
    parser = argparse.ArgumentParser(
        prog="nmcli",
        description="Network Automation CLI — production-grade diagnostics & AWS integration"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # ping
    p = subparsers.add_parser("ping", help="ICMP ping a host")
    p.add_argument("host")
    p.add_argument("--count", type=int, default=4)

    # traceroute
    t = subparsers.add_parser("traceroute", help="Trace route to host")
    t.add_argument("host")

    # dns
    d = subparsers.add_parser("dns", help="DNS record lookup")
    d.add_argument("host")

    # portscan
    ps = subparsers.add_parser("portscan", help="Scan common ports")
    ps.add_argument("host")
    ps.add_argument("--ports", nargs="+", type=int, help="Custom port list")
    ps.add_argument("--timeout", type=float, default=1.0)

    # aws-vpc
    subparsers.add_parser("aws-vpc", help="List AWS VPCs")
    
    # aws-ec2
    subparsers.add_parser("aws-ec2", help="List EC2 instances")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "ping":
        success = core.ping(args.host, args.count)
        sys.exit(0 if success else 1)

    elif args.command == "traceroute":
        core.traceroute(args.host)

    elif args.command == "dns":
        core.dns_lookup(args.host)

    elif args.command == "portscan":
        core.port_scan(args.host, args.ports, args.timeout)

    elif args.command == "aws-vpc":
        aws.get_vpc_info()

    elif args.command == "aws-ec2":
        aws.get_ec2_instances()


if __name__ == "__main__":
    main()
