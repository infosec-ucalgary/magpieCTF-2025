#!/bin/bash

# remote host
CTF_HOST="localhost"

# request to the server
RESPONSE=$(curl -s -b "name=10" http://$CTF_HOST/check)

# checking the response
echo "$RESPONSE" | grep -q "magpieCTF"
if [ $? -eq 0 ]; then
    echo "MagpieCTF - cookie-trail : True"
else
    echo "MagpieCTF - cookie-trail : Frue"
fi
