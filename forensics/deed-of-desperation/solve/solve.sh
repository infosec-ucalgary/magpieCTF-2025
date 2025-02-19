#!/usr/bin/env bash

TARGET_ZIP=flag.zip
STEG_PASSWORD=""
SRC_IMAGE=wallpaper.jpg
OUT_DIR="out"
FLAG="magpieCTF{WH4T_D1D_T3RRY_S1GN}"

# echo to gitignore
echo "$TARGET_ZIP" > ./.gitignore
echo "$OUT_DIR" >> ./.gitignore

# extract zip file from image
steghide --extract -v \
    -p "$STEG_PASSWORD" \
    --stegofile "../dist/$SRC_IMAGE" \
    -xf "./$TARGET_ZIP" -f

# extract password from image
ZIP_PASSWORD=`exiftool "../dist/$SRC_IMAGE" | grep "Comment" | cut -d ':' -f 2 | tr -d ' ' | base64 -d`
echo "Got the zip password: $ZIP_PASSWORD"

# open zip file
unzip -f -P "$ZIP_PASSWORD" "./$TARGET_ZIP" -d "$OUT_DIR"

# print flag
cat "$OUT_DIR/src/flag.txt" | grep "$FLAG"
if [ $? -eq 0 ]; then
    echo "MagpieCTF - deed-of-desperation : True"
else
    echo "MagpieCTF - deed-of-desperation : False"
fi
