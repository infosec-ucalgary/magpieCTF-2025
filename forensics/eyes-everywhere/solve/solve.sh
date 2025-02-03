#!/bin/bash

# Check dependencies
if ! command -v steghide &>/dev/null; then
    echo "Installing steghide..."
    sudo apt-get update && sudo apt-get install -y steghide
    if ! command -v steghide &>/dev/null; then
        echo "Error: steghide installation failed. Please install manually:"
        echo "sudo apt-get install steghide"
        exit 1
    fi
fi

# Check arguments
if [ $# -ne 2 ]; then
    echo "Usage: $0 <image_directory> <order_file>"
    echo "Example: $0 security_footage_set split_order.txt"
    exit 1
fi

image_dir="$1"
order_file="$2"
temp_dir=$(mktemp -d)

# Validate inputs
if [ ! -d "$image_dir" ]; then
    echo "Error: Image directory '$image_dir' not found"
    exit 1
fi

if [ ! -f "$order_file" ]; then
    echo "Error: Order file '$order_file' not found"
    exit 1
fi

# Read the order file
mapfile -t file_order < "$order_file"

echo "Reconstructing message from ${#file_order[@]} pieces..."

# File paths for processing stages
combined_noisy="combined_noisy.txt"
cleaned_base64="cleaned_base64.txt"
final_output="reconstructed_message.txt"

# Extract text from each image in order
for index in "${!file_order[@]}"; do
    filename="${file_order[$index]}"
    image_path="$image_dir/$filename"
    temp_file="$temp_dir/piece_$((index+1)).txt"
    
    if [ ! -f "$image_path" ]; then
        echo "Error: Missing image '$filename' at position $((index+1))"
        exit 1
    fi

    echo "Extracting from $filename..."
    if steghide extract -sf "$image_path" -xf "$temp_file" -p "" -q; then
        echo "Successfully extracted piece $((index+1))"
    else
        echo "Failed to extract from $filename"
        exit 1
    fi
done

# Processing pipeline
echo -e "\nProcessing extracted data:"
echo "1. Combining pieces..."
cat "$temp_dir"/piece_*.txt | tr -d '\n' > "$combined_noisy"

echo "2. Removing noise patterns..."
sed -E 's/\$[^$]*\$//g' "$combined_noisy" > "$cleaned_base64"

echo "3. Base64 decoding..."
if base64 -d "$cleaned_base64" > "$final_output" 2>/dev/null; then
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
echo -e "\nFinal reconstruction saved to: $final_output"