#!/bin/bash
source ./.scripts/constants.sh

CWD=$(pwd)
IMAGES=0
PROGS=0
CHECK=1

# setting opts
case "$1" in
im*)
    IMAGES=1
    ;;
pr*)
    PROGS=1
    ;;
ch*)
    CHECK=1
    ;;
*)
    IMAGES=1
    PROGS=1
    CHECK=1
    ;;
esac

# checking for nsjail
docker image ls | grep nsjail
if [[ $? -ne 0 ]]; then
    # pulling and building nsjail
    if [[ ! -d "./nsjail" ]]; then
        echo "Docker image 'nsjailcontainer' wasn't found, pulling from github."
        git clone https://github.com/google/nsjail.git nsjail
    fi

    # building the image
    cd nsjail
    docker build -t nsjailcontainer .
fi

# building images
if [ $IMAGES -eq 1 ]; then
    for chal in $CHALS; do
        # setup
        echo "Building image for $chal"
        cd "$CWD/$chal/src"

        # building the intermediate image with all the build shit
        docker build . -t "$TAGROOT-$chal:build" --target build

        # building the production image
        docker build . -t "$TAGROOT-$chal:latest"
    done
    cd $CWD
fi

# building progs (requires containers be built)
if [ $PROGS -eq 1 ]; then
    mkdir -p "$CWD/dist/"
    for chal in $CHALS; do
        # checking if image exists
        docker image ls | grep "$TAGROOT-$chal" | grep build 1>&2 2>/dev/null
        if [[ $? -ne 0 ]]; then
            echo "Cannot extract $chal from $TAGROOT-$chal:build, because it does not exist."
            continue
        fi

        # exporting the image to a tar archive
        docker export "$(docker create "$TAGROOT-$chal:build")" --output /tmp/image.tar

        # copying out the challenges
        tar -xvf /tmp/image.tar -C "$CWD/dist/" "ctf/$chal" --strip-components=1
        tar -xvf /tmp/image.tar -C "$CWD/dist/" "ctf/$chal.sha1.sig" --strip-components=1
        tar -xvf /tmp/image.tar -C "$CWD/$chal/src/" "ctf/$chal.debug" --strip-components=1
    done
    cd $CWD

    # clean up
    rm -rf "/tmp/image.tar"
fi

# checking the challenge flags
if [ $CHECK -eq 1 ]; then
    check_chals
fi
