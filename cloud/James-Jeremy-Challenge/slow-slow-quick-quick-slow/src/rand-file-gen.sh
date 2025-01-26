#!/bin/bash

SEED="tall-oaks-from-tiny-acorns-grow"

# size in MB
SIZE_MB=100
SIZE_BYTES=$((SIZE_MB * 1024 * 1024))

# Generate random string
awk -v seed="$SEED" -v size="$SIZE_BYTES" '
BEGIN {
  # we want a deterministic generator
  srand(seed);
  chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
  while (size > 0) {
    # get a random index into the chars
    n = int(length(chars) * rand());
    # get the character at that index
    randomChar = substr(chars, n+1, 1);
    # print the character
    printf randomChar;
    # track the size
    size -= 1;
  }
}'
