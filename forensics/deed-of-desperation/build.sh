TARGET_ZIP=flag.zip
STEG_PASSWORD=""
ZIP_PASSWORD=F0rS4l3!2025
ENCRYPTED=$(base64 <<<"$ZIP_PASSWORD")
SRC_IMAGE=wallpaper.jpg

# creating the dist dir
mkdir -vp ./dist ./build

# zipping everything together
zip -P "$ZIP_PASSWORD" -9 build/flag.zip src/flag.txt src/Form.pdf

# embedding the
steghide --embed -v -e none \
    -p "$STEG_PASSWORD" \
    --stegofile "dist/$SRC_IMAGE" \
    --coverfile "src/$SRC_IMAGE" \
    --embedfile build/flag.zip

# adding the base64 encoded password as a comment
exiftool -Comment="$ENCRYPTED" "dist/$SRC_IMAGE"
