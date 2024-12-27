#!/bin/sh
source ./scripts/constants.sh

# This automagically updates & configures the challenges' Makefiles.
# Dockerfiles, and .gitignores

for chal in $CHALS; do
    cp -uv ./base.Dockerfile "$chal/src/Dockerfile"
    sed -i "s/BINARY_NAME/$chal/g" "$chal/src/Dockerfile"
    # cp -uv ./base.Makefile "$chal/src/Makefile"
    # sed -i "s/BINARY_NAME/$chal/g" "$chal/src/Makefile"
    echo "$chal" > "$chal/src/.gitignore"
done
