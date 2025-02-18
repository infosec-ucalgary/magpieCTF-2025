#!/bin/bash
source ./scripts/assert.sh

CHALS=$(echo printf{1..2} overflow{1..2} ret2libc{1..2})
TAGROOT="magpiesctf2025/pwn"

function check_canary() {
    # check for stack canary function
    readelf -s "$1" | grep -Eq "__stack_chk"
    echo "$?"
}

function check_pie() {
    # check for stack canary function
    readelf -h "$1" 2>/dev/null | grep "Type:" | grep -q "DYN"
    echo "$?"
}

function check_chals() {
    # setup
    which readelf 1>/dev/null 2>/dev/null
    if [[ $? -ne 0 ]]; then
        echo "readelf isn't on the path, cannot verify challenge functionality."
        return
    fi

    # checking challenges for canaries
    assert_eq $(check_canary printf1/dist/printf1) 0 "printf1 should have a canary"
    assert_eq $(check_canary printf2/dist/printf2) 0 "printf2 should have a canary"
    assert_not_eq $(check_canary overflow1/dist/overflow1) 0 "overflow1 shouldn't have a canary"
    assert_not_eq $(check_canary overflow2/dist/overflow2) 0 "overflow2 shouldn't have a canary"
    assert_not_eq $(check_canary ret2libc1/dist/ret2libc1) 0 "ret2libc1 shouldn't have a canary"
    assert_eq $(check_canary ret2libc2/dist/ret2libc2) 0 "ret2libc2 should have a canary"

    # checking aslr
    assert_eq $(check_pie printf1/dist/printf1) 0 "printf1 should have ASLR"
    assert_eq $(check_pie printf2/dist/printf2) 0 "printf2 should have ASLR"
    assert_not_eq $(check_pie overflow1/dist/overflow1) 0 "overflow1 shouldn't have ASLR"
    assert_eq $(check_pie overflow2/dist/overflow2) 0 "overflow2 should have ASLR"
    assert_not_eq $(check_pie ret2libc1/dist/ret2libc1) 0 "ret2libc1 shouldn't have ASLR"
    assert_eq $(check_pie ret2libc2/dist/ret2libc2) 0 "ret2libc2 should have ASLR"
}
