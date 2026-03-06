#!/bin/bash

echo "===== NETWORK DIAGNOSTIC REPORT ====="

echo ""
echo "1. Connectivity Test"
ping -c 3 google.com

echo ""
echo "2. DNS Resolution"
nslookup github.com

echo ""
echo "3. Port Connectivity Check"
nc -zv google.com 80
nc -zv google.com 443

echo ""
echo "4. Route Trace"
traceroute google.com

echo ""
echo "===== END REPORT ====="