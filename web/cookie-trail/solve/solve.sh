#!/usr/bin/env bash

# checking arguments
if [ $# -ne 2 ]; then
    echo "Usage: $0 <hostname> <port>"
    exit 1
fi

# vars
HOST="$1"
PORT="$2"

# request to the server
RESPONSE=$(curl -s -b "name=10" http://$HOST:$PORT/check)

# checking the response
echo "$RESPONSE" | grep -q "magpieCTF"
if [ $? -eq 0 ]; then
    echo "MagpieCTF - cookie-trail : True"
    exit 0
else
    echo "MagpieCTF - cookie-trail : False"
    exit 1
fi
