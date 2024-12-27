#!/bin/sh
source ./scripts/constants.sh

CWD=$(pwd)

for chal in $CHALS; do
    echo $CWD
    cd "$CWD/$chal/src"
    docker build . -t "$TAGROOT/$chal:latest"
done

cd $CWD
