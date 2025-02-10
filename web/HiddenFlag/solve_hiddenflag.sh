#!/bin/bash

# Set the base URL
BASE_URL="http://localhost:8080"

# Step 1: Access the home page to get the HTML content
response=$(curl -s "$BASE_URL/")

# Extract the flag
flag=$(echo "$response" | grep -oE 'magpieCTF\{[^}]+\}')

# Print the flag
if [[ -n $flag ]]; then
    echo "[+] Flag found: $flag"
else
    echo "[-] Flag not found. Check the response format."
fi