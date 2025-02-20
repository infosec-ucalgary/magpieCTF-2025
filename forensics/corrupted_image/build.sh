#!/bin/bash

input_image="src/image.png"
output_folder="build"
output_image="$output_folder/image.png"
zip_file="dist/corrupted_image.zip"

# Create output directory if it doesn't exist
mkdir -p "$output_folder"

# Perform hex edit: Change the first occurrence of 89 to 98
xxd "$input_image" | sed '0,/89/ s/89/98/' | xxd -r > "$output_image"

# Ensure the file was created before proceeding
if [ ! -f "$output_image" ]; then
    echo "Error: Hex-edited image was not created."
    exit 1
fi


# Zip the modified image with the correct structure
zip -rj "$zip_file" "$output_folder"

echo "Hex edit complete. Archive saved as $zip_file"

