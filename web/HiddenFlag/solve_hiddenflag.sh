#!/bin/bash


BASE_URL="http://localhost:8080"


response=$(curl -s "$BASE_URL/")


flag=$(echo "$response" | grep -oE 'magpieCTF\{[^}]+\}')


if [[ -n $flag ]]; then
    echo "[+] Flag found: $flag"
else
    echo "[-] Flag not found. Check the response format."
fi