#!/bin/bash
source ./.scripts/assert.sh

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
    assert_eq $(check_canary dist/printf1) 0 "printf1 should have a canary"
    assert_eq $(check_canary dist/printf2) 0 "printf2 should have a canary"
    assert_not_eq $(check_canary dist/overflow1) 0 "overflow1 shouldn't have a canary"
    assert_not_eq $(check_canary dist/overflow2) 0 "overflow2 shouldn't have a canary"
    assert_not_eq $(check_canary dist/ret2libc1) 0 "ret2libc1 shouldn't have a canary"
    assert_eq $(check_canary dist/ret2libc2) 0 "ret2libc2 should have a canary"
    
    # checking aslr
    assert_eq $(check_pie dist/printf1) 0 "printf1 should have ASLR"
    assert_eq $(check_pie dist/printf2) 0 "printf2 should have ASLR"
    assert_not_eq $(check_pie dist/overflow1) 0 "overflow1 shouldn't have ASLR"
    assert_eq $(check_pie dist/overflow2) 0 "overflow2 should have ASLR"
    assert_not_eq $(check_pie dist/ret2libc1) 0 "ret2libc1 shouldn't have ASLR"
    assert_eq $(check_pie dist/ret2libc2) 0 "ret2libc2 should have ASLR"
}

