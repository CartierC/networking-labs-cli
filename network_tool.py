import subprocess
import socket


def ping(host):
    print(f"\nPinging {host}\n")
    subprocess.run(["ping", "-c", "4", host])


def traceroute(host):
    print(f"\nTraceroute to {host}\n")
    subprocess.run(["traceroute", host])


def dns_lookup(host):
    print(f"\nDNS Lookup for {host}\n")
    subprocess.run(["nslookup", host])


def port_scan(host):
    print(f"\nScanning common ports on {host}\n")

    ports = [21, 22, 23, 25, 53, 80, 110, 139, 143, 443, 445, 3389]

    for port in ports:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)

        result = s.connect_ex((host, port))

        if result == 0:
            print(f"Port {port}: OPEN")
        else:
            print(f"Port {port}: CLOSED")

        s.close()


def main():
    print("Network CLI Tool")
    print("1 - Ping")
    print("2 - Traceroute")
    print("3 - DNS Lookup")
    print("4 - Port Scan")

    choice = input("\nSelect option: ").strip()
    host = input("Enter host/domain: ").strip()

    if not host:
        print("No host entered.")
        return

    if choice == "1":
        ping(host)
    elif choice == "2":
        traceroute(host)
    elif choice == "3":
        dns_lookup(host)
    elif choice == "4":
        port_scan(host)
    else:
        print("Invalid option")


if __name__ == "__main__":
    main()
