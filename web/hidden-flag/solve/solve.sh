#!/usr/bin/env bash

# checking arguments
if [ $# -ne 2 ]; then
    echo "Usage: $0 <hostname> <port>"
    exit 1
fi

# vars
HOST="$1"
PORT="$2"

# querying server
response=$(curl -s "http://$HOST:$PORT")
base64_data=$(echo "$response" | grep -o 'class="hidden-flag">[^<]*' | cut -d'>' -f2)
flag=$(echo "$base64_data" | base64 -d)

echo "$flag" | grep "magpieCTF{\$p1d3r_W4\$_H3r3}"
if [ $? -eq 0 ]; then
    echo "MagpieCTF - hidden-flag : True"
    exit 0
else
    echo "MagpieCTF - hidden-flag : False"
    exit 1
fi
