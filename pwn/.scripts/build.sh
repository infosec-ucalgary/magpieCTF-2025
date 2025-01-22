#!/bin/bash
source ./.scripts/constants.sh

CWD=$(pwd)
IMAGES=0
PROGS=0

# setting opts
case "$1" in
    image*)
        IMAGES=1
        ;;
    prog*)
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
        # setup
        echo "Building image for $chal"
        cd "$CWD/$chal/src"

        # building the intermediate image with all the build shit
        docker build . -t "$TAGROOT/$chal:build" --target build

        # building the production image
        docker build . -t "$TAGROOT/$chal:latest"
    done
    cd $CWD
fi

# building progs (requires containers be built)
if [ $PROGS -eq 1 ]; then
    for chal in $CHALS; do
        echo "Compiling $chal"
        cd "$CWD/$chal/src"
        make clean
        make
    done
    cd $CWD

    # checking the compilation
    check_chals
fi
