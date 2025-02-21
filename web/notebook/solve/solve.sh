#!/usr/bin/env bash

# this script acts as a loader for the full python script

# checking arguments
if [ $# -ne 3 ]; then
    echo "Usage: $0 <hostname> <website-port> <ssh-port>"
    exit 1
fi

# vars
HOST="$1"
WEBPORT="$2"
SSHPORT="$3"

VENVNAME="notebook"

# create venv
if [ ! -d "./$VENVNAME" ]; then
    python -m venv "$VENVNAME"
fi

# activate venv
source "./$VENVNAME/bin/activate"
pip install -r requirements.txt

# run the actual solve script
python ./solve.py "$HOST" "$WEBPORT" "$SSHPORT"