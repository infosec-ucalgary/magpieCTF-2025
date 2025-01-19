#!/bin/bash
source ./.scripts/constants.sh
source ./.scripts/assert.sh

# This automagically updates & configures the challenges' Makefiles.
# Dockerfiles, and .gitignores

function check_canary() {
    # check for stack canary function
    readelf -s "$1/src/$1" | grep -Eq "__stack_chk"
    echo "$?"
}

function check_pie() {
    # check for stack canary function
    readelf -h "$1/src/$1" 2>/dev/null | grep "Type:" | grep -q "DYN"
    echo "$?"
}

for chal in $CHALS; do
    if [[ $chal != *"$1"* ]]; then
        continue
    fi

    # updating the docker file
    cp ./base.Dockerfile "$chal/src/Dockerfile"
    sed -i "s/BINARY_NAME/$chal/g" "$chal/src/Dockerfile"

    # updating the makefile
    cp ./base.mk "$chal/src/Makefile"
    sed -i "s/BINARY_NAME/$chal/g" "$chal/src/Makefile"
    echo "$chal*" >"$chal/src/.gitignore"

    # building challenges in debug
    cd "$chal/src"
    make clean
    make debug
    cd - 1>&2 2>/dev/null
done

# setup
which readelf 1>/dev/null 2>/dev/null
if [[ $? -ne 0 ]]; then
    echo "readelf isn't on the path, cannot verify stack canaries."
    exit 1
fi

# checking challenges for canaries
assert_eq $(check_canary printf1) 0 "printf1 should have a canary"
assert_eq $(check_canary printf2) 0 "printf2 should have a canary"
assert_not_eq $(check_canary overflow1) 0 "overflow1 shouldn't have a canary"
assert_not_eq $(check_canary overflow2) 0 "overflow2 shouldn't have a canary"
assert_not_eq $(check_canary ret2libc1) 0 "ret2libc1 shouldn't have a canary"
assert_eq $(check_canary ret2libc2) 0 "ret2libc2 should have a canary"

# checking aslr
assert_eq $(check_pie printf1) 0 "printf1 should have ASLR"
assert_eq $(check_pie printf2) 0 "printf2 should have ASLR"
assert_not_eq $(check_pie overflow1) 0 "overflow1 shouldn't have ASLR"
assert_eq $(check_pie overflow2) 0 "overflow2 should have ASLR"
assert_eq $(check_pie ret2libc1) 0 "ret2libc1 should have ASLR"
assert_eq $(check_pie ret2libc2) 0 "ret2libc2 should have ASLR"
