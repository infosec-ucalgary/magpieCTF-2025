#!/bin/bash
source ./scripts/constants.sh

CWD=$(pwd)
IMAGES=0
PROGS=0
CHECK=1

# setting opts
while getopts "ipc" o; do
    case "${o}" in
    i*)
        IMAGES=1
        ;;
    p*)
        PROGS=1
        ;;
    c*)
        CHECK=1
        ;;
    *) ;;
    esac
done

# if there are no flags
if [[ $OPTIND -eq 1 ]]; then
    IMAGES=1
    PROGS=1
    CHECK=1
fi

# shifting
shift $((OPTIND - 1))

# targets
TARGETS=("$CHALS")
[[ -n "$@" ]] && TARGETS="$@"
#echo "all: $TARGETS IMAGES=$IMAGES PROGS=$PROGS CHECK=$CHECK"

function build_image() {
    # vars
    local prog="$1"

    # setup
    cd "$CWD/$prog/src"

    # building the intermediate image with all the build shit
    docker build . -t "$TAGROOT-$prog:build" --target build --build-arg MAKEROOT="$CWD"

    # building the production image
    docker build . -t "$TAGROOT-$prog:latest" --build-arg MAKEROOT="$CWD"

    # exit out
    cd -
}

function get_program() {
    # vars
    local prog="$1"

    # checking if image exists
    docker image ls | grep "$TAGROOT-$prog" | grep build 1>&2 2>/dev/null
    if [[ $? -ne 0 ]]; then
        echo "Cannot extract $prog from $TAGROOT-$prog:build, because it does not exist."
    fi

    # exporting the image to a tar archive
    docker export "$(docker create "$TAGROOT-$prog:build")" --output /tmp/image.tar

    # copying out the proglenges
    mkdir -p "$CWD/$prog/dist/"
    tar -xvf /tmp/image.tar -C "$CWD/$prog/dist/" "ctf/$prog" --strip-components=1
    tar -xvf /tmp/image.tar -C "$CWD/$prog/dist/" "ctf/$prog.sha1.sig" --strip-components=1
    tar -xvf /tmp/image.tar -C "$CWD/$prog/src/" "ctf/$prog.debug" --strip-components=1

    # clean up
    rm -rf "/tmp/image.tar"
}

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
    # logging
    echo "Image targets: $TARGETS"

    # building
    for chal in $TARGETS; do
        echo "Building image: $chal"
        build_image $chal
    done
    cd $CWD
fi

# building chals (requires containers be built)
if [ $PROGS -eq 1 ]; then
    # logging
    echo "Program targets: $TARGETS"

    # extracting
    for chal in $TARGETS; do
        echo "Extracing program: $chal"
        get_program $chal
    done
    cd $CWD
fi

# checking the challenge flags
if [ $CHECK -eq 1 ]; then
    check_chals
fi
