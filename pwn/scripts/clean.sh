#!/usr/bin/env bash

source ./scripts/constants.sh

CWD=$(pwd)

## cleanup

# remove challenges
for chal in $CHALS; do
    cd "$CWD/$chal/src/"
    make clean
    cd -
    echo "Deleted $chal"
done

# going back to the starting dir
cd "$CWD"

# removing images
docker image ls | grep "<none>" | sed -e 's/\s\+/ /g' | cut -d " " -f 3 | xargs docker image rm
docker image ls | grep "$TAGROOT" | sed -e 's/\s\+/ /g' | cut -d " " -f 3 | xargs docker image rm
docker image prune
