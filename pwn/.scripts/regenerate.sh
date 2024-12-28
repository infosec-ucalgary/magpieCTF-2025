#!/bin/sh
source ./.scripts/constants.sh

# This automagically updates & configures the challenges' Makefiles.
# Dockerfiles, and .gitignores

function check_canary {
    # setup
    which readelf 1>/dev/null 2>/dev/null
    if [[ $? -ne 0 ]]; then
        echo "readelf isn't on the path, cannot verify stack canaries."
    fi

    # check for stack canary function
    if readelf -s $1 2> /dev/null | grep " UND " | grep -Eq "__stack_chk_fail|__stack_chk_guard"; then
        return 1
    else
        return 0
    fi
}

function check_pie {
    # setup
    which readelf 1>/dev/null 2>/dev/null
    if [[ $? -ne 0 ]]; then
        echo "readelf isn't on the path, cannot verify stack canaries."
    fi

    # check for stack canary function
    if readelf -h $1 2> /dev/null | grep "Type:" | grep -q "DYN"; then
        return 1
    else
        return 0
    fi
}

for chal in $CHALS; do
    if [[ $chal != *"$1"* ]]; then
        continue
    fi

    # updating the docker file
    cp -uv ./base.Dockerfile "$chal/src/Dockerfile"
    sed -i "s/BINARY_NAME/$chal/g" "$chal/src/Dockerfile"

    # updating the makefile
    cp -uv ./base.Makefile "$chal/src/Makefile"
    sed -i "s/BINARY_NAME/$chal/g" "$chal/src/Makefile"
    echo "$chal" >"$chal/src/.gitignore"

    # building challenges in debug
    cd "$chal/src"
    make clean
    make debug
    cd - 1>&2 2>/dev/null
done

# for stack2
check_canary stack2
if [[ $? -ne 0 ]]; then
    echo "stack2 has a canary, this is incorrect."
fi
check_pie stack2
if [[ $? -ne 0 ]]; then
    echo "stack2 has a canary, this is incorrect."
fi
