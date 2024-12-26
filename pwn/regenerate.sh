#!/bin/sh

# This automagically updates & configures the challenges' Makefiles.
# Dockerfiles, and .gitignores

CHALS=$(echo printf{1..4} stack{1..3})

for chal in $CHALS; do
    cp -uv ./base.Dockerfile "$chal/src/Dockerfile"
    cp -uv ./base.Makefile "$chal/src/Makefile"
    sed -i "s/BINARY_NAME/$chal/g" "$chal/src/Makefile"
    sed -i "s/BINARY_NAME/$chal/g" "$chal/src/Dockerfile"
    echo "$chal" > "$chal/src/.gitignore"
done
