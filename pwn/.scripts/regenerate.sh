#!/bin/bash

source ./.scripts/constants.sh
source ./.scripts/assert.sh

# This automagically updates & configures the challenges' Makefiles.
# Dockerfiles, and .gitignores

CWD=$(pwd)
mkdir -p "$CWD/dist"

for chal in $CHALS; do
    if [[ $chal != *"$1"* ]]; then
        continue
    fi

    # updating the docker file
    cp ./base.Dockerfile "$CWD/$chal/src/Dockerfile"
    sed -i "s/BINARY_NAME/$chal/g" "$CWD/$chal/src/Dockerfile"

    # updating the makefile
    cp ./base.mk "$chal/src/Makefile"
    sed -i "s/BINARY_NAME/$chal/g" "$CWD/$chal/src/Makefile"
    
    # update the gitignore
    echo "$chal*" > "$CWD/$chal/src/.gitignore"
    echo "common.h" >> "$CWD/$chal/src/.gitignore"
    echo "Makefile" >> "$CWD/$chal/src/.gitignore"
    echo "Dockerfile" >> "$CWD/$chal/src/.gitignore"

    # copying the header file
    cp "$CWD/common.h" "$CWD/$chal/src/common.h"

    # building challenges
    cd "$CWD/$chal/src"
    make clean
    make
    cd "$CWD" 1>&2 2>/dev/null

    # linking to dist
    ln -sf "$CWD/$chal/src/$chal" "$CWD/dist/$chal"

    # asserting that the flags exist
    if [[ ! -f "$CWD/$chal/src/flag.txt" ]]; then
        echo "$chal is missing its flag, uh oh!"
        exit -99999
    fi

    # linking the flags
    ln -sf "$CWD/$chal/src/flag.txt" "$CWD/$chal/solve/flag.txt"
    if [[ -f "$CWD/$chal/src/flag.root.txt" ]]; then
        ln -sf "$CWD/$chal/src/flag.root.txt" "$CWD/$chal/solve/flag.root.txt"
    fi
done

# checking the compilation
check_chals
