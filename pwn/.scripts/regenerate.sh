#!/bin/bash

source ./.scripts/constants.sh
source ./.scripts/assert.sh

# This automagically updates & configures the challenges' Makefiles.
# Dockerfiles, and .gitignores

CWD=$(pwd)

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

    # building challenges in debug
    cd "$CWD/$chal/src"
    make clean
    make debug
    cd "$CWD" 1>&2 2>/dev/null
done

# checking the compilation
check_chals

