#!/usr/bin/env bash

BUILDDIR="build"
OUTDIR="dist"
SRCDIR="src"
SOLVEDIR="solve"

# legendary logging message
echo "This script sometimes breaks. Too bad!"

# cleanup
rm -rv "$BUILDDIR/"
mkdir -p "$BUILDDIR"

# generate flag pieces
python scripts/split_noise.py "./$BUILDDIR/flag_noise.txt"

# checking that the script worked
if [ ! -f "$BUILDDIR/flag_noise.txt" ]; then
    echo "split_image.sh failed, no such file $BUILDDIR/flag_noise.txt"
    exit 1
fi

# split base image
./scripts/split_image.sh "$SRCDIR/security_footage.jpg" "$BUILDDIR"

# checking that the script worked
if [ ! -f "$BUILDDIR/split_order.txt" ]; then
    echo "split_image.sh failed, no such file $BUILDDIR/split_order.txt"
    exit 1
fi
if [ ! -d "$BUILDDIR/set" ]; then
    echo "split_image.sh failed, no such directory $BUILDDIR/set"
    exit 1
fi

# embed pieces into images
./scripts/embed_image.sh "$BUILDDIR/set" "$BUILDDIR/split_order.txt" "$BUILDDIR/flag_noise.txt" "$BUILDDIR/out"
if [ ! -d "$BUILDDIR/out" ]; then
    echo "split_image.sh failed, no such directory $BUILDDIR/out"
    exit 1
fi

# pack challenge
rm -v "$OUTDIR/security_footage.zip"
zip -rj "$OUTDIR/security_footage.zip" "$BUILDDIR/out"

# generate SHA-1 hash of the zip file {NO IDEA WHY}
sha1sum "$OUTDIR/security_footage.zip" | awk '{print $1}' > "$OUTDIR/security_footage.zip.sha1"

# copying files into solve
cp -vf "$BUILDDIR/split_order.txt" "$SOLVEDIR/split_order.txt"
cp -vf "$BUILDDIR/flag_noise.txt" "$SOLVEDIR/flag_noise.txt"

# logging for the end user 
echo "Build complete. SHA-1 hash generated:"
cat "$OUTDIR/security_footage.zip.sha1"
