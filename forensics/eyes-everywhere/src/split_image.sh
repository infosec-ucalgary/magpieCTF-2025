#!/bin/bash

# Check if an image file was provided
if [ $# -ne 1 ]; then
    echo "Usage: $0 <image_file>"
    echo "Example: $0 input.jpg"
    exit 1
fi

input_image="$1"
filename=$(basename -- "$input_image")
extension="${filename##*.}"
filename="${filename%.*}"

# Check if input file exists
if [ ! -f "$input_image" ]; then
    echo "Error: Input file '$input_image' not found"
    exit 1
fi

# Create output directory
output_dir="${filename}_set"
mkdir -p "$output_dir"

# Get image dimensions
dimensions=$(identify -format "%wx%h" "$input_image")
width=$(echo $dimensions | cut -d'x' -f1)
height=$(echo $dimensions | cut -d'x' -f2)

# Calculate dimensions for each piece
# We'll do a 2x3 grid (6 pieces)
piece_width=$((width/2))
piece_height=$((height/3))

echo "Splitting image into 6 pieces (2x3 grid)..."

# Split the image into 6 pieces with sequential numbering
count=1
declare -a piece_files=()  # Array to store piece filenames in order
for row in {0..2}; do
    for col in {0..1}; do
        x=$((col * piece_width))
        y=$((row * piece_height))
        
        output_file="${output_dir}/camera_${count}.${extension}"
        piece_files+=("$output_file")
        
        convert "$input_image" -crop ${piece_width}x${piece_height}+${x}+${y} "$output_file"
        
        echo "Created: $output_file"
        ((count++))
    done
done

echo "Done! Split images are saved in the '$output_dir' directory"

# Show dimensions of pieces
echo -e "\nPiece dimensions:"
echo "Width: $piece_width pixels"
echo "Height: $piece_height pixels"

# Create montage in numerical order
# The -tile 2x3 ensures the layout matches the original image
montage "${piece_files[@]}" -tile 2x3 -geometry +5+5 "${output_dir}/montage.${extension}"
echo "Created montage: ${output_dir}/montage.${extension}"

# Display the order of splits for reference
echo -e "\nSplit order (left to right, top to bottom):"
for i in {1..6}; do
    echo "camera_${i}.${extension}"
done