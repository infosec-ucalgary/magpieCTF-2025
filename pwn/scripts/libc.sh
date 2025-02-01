#!/bin/bash
source ./scripts/constants.sh

CWD=$(pwd)
prog=ret2libc1

# checking if image exists
docker image ls | grep "$TAGROOT-$prog" | grep latest 1>&2 2>/dev/null
if [[ $? -ne 0 ]]; then
    echo "Cannot extract $prog from $TAGROOT-$prog:latest, because it does not exist."
fi

# exporting the image to a tar archive
docker export "$(docker create "$TAGROOT-$prog:latest")" --output /tmp/image.tar

# copy out libc and the linker
tar -xvf /tmp/image.tar -C "$CWD" "usr/lib/x86_64-linux-gnu/libc.so.6" --strip-components=3
tar -xvf /tmp/image.tar -C "$CWD" "usr/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2" --strip-components=3
