#!/usr/bin/env bash

# checking arguments
if [ $# -ne 2 ]; then
    echo "Usage: $0 <hostname> <port>"
    exit 1
fi

# vars
HOST="$1"
PORT="$2"

# hardcoding encrypted cookie info
CNAME="lubvanl-bwvv"
CVALUE="jdwmj"

# request to the server
RESPONSE=$(curl -s -b "$CNAME=$CVALUE" http://$HOST:$PORT/check)

# checking the response
echo "$RESPONSE" | grep -q "magpieCTF"
if [ $? -eq 0 ]; then
    echo "MagpieCTF - cops-like-ciphers-and-cookies : True"
    exit 0
else
    echo "MagpieCTF - cops-like-ciphers-and-cookies : False"
    exit 1
fi
