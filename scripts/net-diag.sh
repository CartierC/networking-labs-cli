#!/bin/bash
echo "--- Connectivity Report ---"
ping -c 3 google.com
echo "--- DNS Resolution ---"
nslookup github.com
echo "--- Port 80/443 Check ---"
nc -zv google.com 80 443
