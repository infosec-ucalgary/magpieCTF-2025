#!/bin/bash
source ./.scripts/constants.sh

CWD=$(pwd)
IMAGES=0
PROGS=0

# setting opts
case "$1" in
    images)
        IMAGES=1
        ;;
    progs)
        PROGS=1
        ;;
    *)
        IMAGES=1
        PROGS=1
        ;;
esac

# building images
if [ $IMAGES -eq 1 ]; then
    for chal in $CHALS; do
        echo "Building image for $chal"
        cd "$CWD/$chal/src"
        docker build . -t "$TAGROOT/$chal:latest"
    done
    cd $CWD
fi

# building progs
if [ $PROGS -eq 1 ]; then
    for chal in $CHALS; do
        echo "Compiling $chal"
        cd "$CWD/$chal/src"
        make debug
    done
    cd $CWD

    # checking the compilation
    check_chals
fi

