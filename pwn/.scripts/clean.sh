#!/bin/bash

source ./.scripts/constants.sh

CWD=$(pwd)

## cleanup
# delete dist dir
rm -rfv dist

# remove challenges
for chal in $CHALS; do
    rm "$CWD/$chal/src/$chal"
    echo "Deleted $chal"
done

# removing images
docker image ls | grep "$TAGROOT" | sed -e 's/\s\+/ /g' | cut -d " " -f 3 | xargs docker image rm
docker image prune

