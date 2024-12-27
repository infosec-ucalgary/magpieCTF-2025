#!/bin/sh
source ./.scripts/constants.sh
docker image ls | grep "$TAGROOT" | sed -e 's/\s\+/ /g' | cut -d " " -f 3 | xargs docker image rm
docker image prune
