#!/bin/bash

source ./scripts/constants.sh
source ./scripts/assert.sh

# This automagically updates & configures the challenges' Makefiles.
# Dockerfiles, and .gitignores

CWD=$(pwd)

# targets
TARGETS=("$CHALS")
[[ -n "$@" ]] && TARGETS="$@"
# echo "all: $TARGETS"

for chal in $TARGETS; do
    # updating the docker file
    cp -vu ./base.Dockerfile "$CWD/$chal/src/Dockerfile"
    sed -i "s/BINARY_NAME/$chal/g" "$CWD/$chal/src/Dockerfile"

    # updating the makefile
    cp -vu ./base.mk "$CWD/$chal/src/Makefile"
    sed -i "s/BINARY_NAME/$chal/g" "$CWD/$chal/src/Makefile"
    
    # update the gitignore
    echo "$chal*" > "$CWD/$chal/src/.gitignore"
    echo "common.h" >> "$CWD/$chal/src/.gitignore"

    # copying the header file
    cp -vu "$CWD/common.h" "$CWD/$chal/src/common.h"

    # logging
    echo "Regenerated files for $chal."
done
