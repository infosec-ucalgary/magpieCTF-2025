#!/bin/sh
source ./.scripts/constants.sh

# This automagically updates & configures the challenges' Makefiles.
# Dockerfiles, and .gitignores

for chal in $CHALS; do
    # updating the docker file
    cp -uv ./base.Dockerfile "$chal/src/Dockerfile"
    sed -i "s/BINARY_NAME/$chal/g" "$chal/src/Dockerfile"

    # updating the makefile
    if [[ $chal != *"stack"* ]]; then
        cp -uv ./base.Makefile "$chal/src/Makefile"
        sed -i "s/BINARY_NAME/$chal/g" "$chal/src/Makefile"
    fi
    echo "$chal" > "$chal/src/.gitignore"

    # building challenges in debug
    cd "$chal/src"
    make clean
    make debug
    cd -
done
