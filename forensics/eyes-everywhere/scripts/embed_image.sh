#!/usr/bin/env bash

# checking for steghide
if ! command -v steghide &>/dev/null; then
    echo "This script requires the program: steghide, cannot run."
    exit 1
fi

# check for image and for output dir
if [ $# -ne 4 ]; then
    echo "Usage: $0 <image_montage_folder> <reconstruction_list> <flag_noise> <output_dir>"
    echo "Example: $0 input.jpg"
    exit 1
fi

# parsing arguments
image_dir="$1"
order_file="$2"
flag_noise="$3"
output_dir="$4"

# validating arguments
if [ ! -d "$image_dir" ]; then
    echo "Error: Directory '$image_dir' does not exist."
    exit 1
fi

if [ ! -f "$order_file" ]; then
    echo "Error: Order file '$order_file' not found."
    exit 1
fi

if [ ! -f "$flag_noise" ]; then
    echo "Error: Flag noise '$flag_noise' not found."
    exit 1
fi

if [ ! -d "$output_dir" ]; then
    echo "Creating $output_dir."
    mkdir -p "$output_dir"
fi

# load in flag noise
mapfile -t texts <"$flag_noise"

# Create a temporary directory for text files
temp_dir=$(mktemp -d)

# Read the split order from file
mapfile -t ordered_files <"$order_file"

# Verify array lengths match
if [ ${#ordered_files[@]} -ne ${#texts[@]} ]; then
    echo "Error: Number of images (${#ordered_files[@]}) doesn't match number of text pieces (${#texts[@]})"
    echo "${ordered_files[@]}"
    echo "${texts[@]}"
    exit 1
fi

# Process files in original split order
for index in "${!ordered_files[@]}"; do
    filename="${ordered_files[$index]}"
    old_image="$image_dir/$filename"
    new_image="$output_dir/$filename"
    text="${texts[$index]}"

    # Validate image exists
    if [ ! -f "$old_image" ]; then
        echo "Warning: Image '$filename' not found, skipping index $index"
        continue
    fi

    # Create temporary text file
    text_file="$temp_dir/text_$((index + 1)).txt"
    echo "$text" >"$text_file"

    # Embed metadata
    echo "Processing $filename (piece $((index + 1)) of ${#ordered_files[@]})..."
    if steghide embed -cf "$old_image" -ef "$text_file" -sf "$new_image" -p "" -q; then
        echo "Successfully embedded data into $filename"
    else
        echo "Failed to embed data into $filename"
    fi
    echo "-------------------"
done

# Cleanup
rm -rf "$temp_dir"
echo "Processing complete. Results in: $output_dir"
