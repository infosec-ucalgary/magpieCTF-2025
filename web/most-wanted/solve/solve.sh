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
response=$(curl -s "http://$HOST:$PORT/mcdata/flag.html")

# checking response
echo "$response" | grep -q 'magpieCTF'
if [ $? -eq 0 ]; then
    echo "MagpieCTF - most-wanted : True"
    exit 0
else
    echo "MagpieCTF - most-wanted : False"
    exit 1
fi
