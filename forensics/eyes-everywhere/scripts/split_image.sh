#!/usr/bin/env bash

# Check if ImageMagick is installed
if ! command -v convert &>/dev/null || ! command -v montage &>/dev/null; then
    echo "This script requires the program: ImageMagick, cannot run."
    exit 1
fi

# check for image and for output dir
if [ $# -ne 2 ]; then
    echo "Usage: $0 <image_file> <out_dir>"
    echo "Example: $0 input.jpg"
    exit 1
fi

# parsing arguments
input_image="$1"
output_dir="$2"

# Check if input file exists
if [ ! -f "$input_image" ]; then
    echo "Error: Input file '$input_image' not found"
    exit 1
fi

# check if the output dir exists
if [ ! -d "$output_dir" ]; then
    mkdir -p "$output_dir"
    echo "Created dir $output_dir"
fi

filename=$(basename -- "$input_image")
extension="${filename##*.}"
filename="${filename%.*}"

# Create output directories
# the 6 images go into $output_dir/set/
# the construction list goes into $output_dir/
image_dir="$output_dir/set"
mkdir -pv "$image_dir"

# Get image dimensions
dimensions=$(identify -format "%wx%h" "$input_image")
width=$(echo $dimensions | cut -d'x' -f1)
height=$(echo $dimensions | cut -d'x' -f2)

# Calculate dimensions for each piece (2x3 grid)
piece_width=$((width / 2))
piece_height=$((height / 3))

# Show dimensions of pieces
echo -e "\nPiece dimensions:"
echo "Width: $piece_width pixels"
echo "Height: $piece_height pixels"

# Split the image into 6 pieces with random filenames
declare -a piece_files=()
for row in {0..2}; do
    for col in {0..1}; do
        x=$((col * piece_width))
        y=$((row * piece_height))

        # Generate random filename
        random_str=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 8 | head -n 1)
        output_file="${image_dir}/${random_str}.${extension}"
        piece_files+=("$output_file")

        convert "$input_image" -crop ${piece_width}x${piece_height}+${x}+${y} "$output_file"
        echo "Created: $output_file"
    done
done

# Save split order to file
printf "%s\n" "${piece_files[@]##*/}" >"${output_dir}/split_order.txt"

# Create montage in separate solve directory
# montage "${piece_files[@]}" -tile 2x3 -geometry +5+5 "${image_dir}/${filename}_montage.${extension}"
# echo -e "\nCreated montage: ${image_dir}/${filename}_montage.${extension}"

echo -e "\nDone! Split images (6) are saved in the '$image_dir' directory"

# Display the order of splits with actual filenames
echo -e "\nSplit order (left to right, top to bottom):"
for file in "${piece_files[@]}"; do
    echo "$(basename "$file")"
done
