#!/usr/bin/env bash

# Check dependencies
if ! command -v steghide &>/dev/null; then
    echo "This script requires the program: steghide, cannot run."
    exit 1
fi

# check for image and for output dir
if [ $# -ne 1 ]; then
    echo "Usage: $0 <zip_of_images>"
    echo "Example: $0 security_footage.zip"
    exit 1
fi

# mapping arguments
zip_file="$1"

# checking arguments
if [ ! -f "$zip_file" ]; then
    echo "Error: File '$zip_file' not found."
    exit 1
fi

# vars
image_dir="image_set"
order_file="split_order.txt"
noise_file="flag_noise.txt"
temp_dir=$(mktemp -d)

# ignoring shit
cat .gitignore | grep "$image_dir"
if [ $? -ne 0 ]; then
    echo "$image_dir" >> .gitignore
fi
cat .gitignore | grep "\*.txt"
if [ $? -ne 0 ]; then
    echo "*.txt" >> .gitignore
fi

# checking for supporting files
if [ ! -f "$order_file" ]; then
    echo "Error: Order file '$order_file' not found, cannot solve programmatically."
    exit 1
fi

if [ ! -f "$noise_file" ]; then
    echo "Error: Noise file '$noise_file' not found, cannot solve programmatically."
    exit 1
fi

# unpacking the zip
unzip -f "$zip_file" -d "./$image_dir"

# Read the order file
mapfile -t file_order <"$order_file"

echo "Reconstructing message from ${#file_order[@]} pieces..."

# File paths for processing stages
combined_noisy="combined_noisy.txt"
cleaned_base64="cleaned_base64.txt"
final_output="reconstructed_message.txt"

# Extract text from each image in order
for index in "${!file_order[@]}"; do
    filename="${file_order[$index]}"
    image_path="$image_dir/$filename"
    temp_file="$temp_dir/piece_$((index + 1)).txt"

    if [ ! -f "$image_path" ]; then
        echo "Error: Missing image '$filename' at position $((index + 1))"
        exit 1
    fi

    echo "Extracting from $filename..."
    if steghide extract -sf "$image_path" -xf "$temp_file" -p "" -q; then
        echo "Successfully extracted piece $((index + 1))"
    else
        echo "Failed to extract from $filename"
        exit 1
    fi
done

# Processing pipeline
echo -e "\nProcessing extracted data:"
echo "1. Combining pieces..."
cat "$temp_dir"/piece_*.txt | tr -d '\n' >"$combined_noisy"

echo "2. Removing noise patterns..."
sed -E 's/\$[^$]*\$//g' "$combined_noisy" >"$cleaned_base64"

echo "3. Base64 decoding..."
if base64 -d "$cleaned_base64" >"$final_output" 2>/dev/null; then
    echo "4. Successfully decoded final message!"
else
    echo "Error: Decoding failed - invalid base64 or remaining noise"
    echo "Debug files:"
    echo "- Combined noisy text: $combined_noisy"
    echo "- Cleaned base64 text: $cleaned_base64"
    exit 1
fi

# Cleanup temp files
rm -rf "$temp_dir"

# Display results
echo -e "\nFinal reconstruction saved to: $final_output\n"
