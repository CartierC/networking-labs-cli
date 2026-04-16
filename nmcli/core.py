import subprocess
import socket
import logging
from nmcli.utils import validate_host, logger

COMMON_PORTS = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
    53: "DNS", 80: "HTTP", 443: "HTTPS", 3306: "MySQL",
    3389: "RDP", 5432: "PostgreSQL", 6379: "Redis", 8080: "HTTP-Alt"
}


def ping(host: str, count: int = 4) -> bool:
    if not validate_host(host):
        return False
    logger.info(f"Pinging {host} ({count} packets)")
    result = subprocess.run(
        ["ping", "-c", str(count), host],
        capture_output=True, text=True
    )
    print(result.stdout)
    if result.returncode != 0:
        logger.warning(f"Ping failed for {host}")
    return result.returncode == 0


def traceroute(host: str) -> bool:
    if not validate_host(host):
        return False
    logger.info(f"Running traceroute to {host}")
    result = subprocess.run(
        ["traceroute", host],
        capture_output=True, text=True
    )
    print(result.stdout)
    return result.returncode == 0


def dns_lookup(host: str) -> dict:
    logger.info(f"Resolving DNS for {host}")
    results = {}
    try:
        ipv4 = socket.gethostbyname(host)
        results["A"] = ipv4

        addr_info = socket.getaddrinfo(host, None, socket.AF_INET6)
        if addr_info:
            results["AAAA"] = addr_info[0][4][0]

        hostname, aliases, _ = socket.gethostbyaddr(ipv4)
        results["PTR"] = hostname
        results["aliases"] = aliases

    except socket.herror as e:
        logger.warning(f"Reverse DNS failed: {e}")
    except socket.gaierror as e:
        logger.error(f"DNS resolution failed: {e}")

    for record_type, value in results.items():
        print(f"  {record_type:8} → {value}")
    return results


def port_scan(host: str, ports: list = None, timeout: float = 1.0) -> dict:
    if not validate_host(host):
        return {}
    
    scan_ports = ports or list(COMMON_PORTS.keys())
    results = {"open": [], "closed": []}
    
    logger.info(f"Scanning {len(scan_ports)} ports on {host}")
    print(f"\n{'PORT':<8} {'SERVICE':<16} {'STATUS'}")
    print("-" * 35)

    for port in scan_ports:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        status = s.connect_ex((host, port))
        s.close()

        service = COMMON_PORTS.get(port, "Unknown")
        if status == 0:
            results["open"].append(port)
            print(f"{port:<8} {service:<16} \033[92mOPEN\033[0m")
        else:
            results["closed"].append(port)
            print(f"{port:<8} {service:<16} CLOSED")

    print(f"\nSummary: {len(results['open'])} open, {len(results['closed'])} closed")
    return results
