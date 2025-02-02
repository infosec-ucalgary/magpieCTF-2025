#!/bin/bash

# Check if ImageMagick is installed
if ! command -v convert &>/dev/null || ! command -v montage &>/dev/null; then
    echo "Installing ImageMagick..."
    sudo apt-get update && sudo apt-get install -y imagemagick
    # Verify installation
    if ! command -v convert &>/dev/null; then
        echo "Error: ImageMagick installation failed. Please install manually."
        exit 1
    fi
fi

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

# Create output directories
output_dir="${filename}_set"
solve_dir="solve"
mkdir -p "$output_dir" "$solve_dir"

# Get image dimensions
dimensions=$(identify -format "%wx%h" "$input_image")
width=$(echo $dimensions | cut -d'x' -f1)
height=$(echo $dimensions | cut -d'x' -f2)

# Calculate dimensions for each piece (2x3 grid)
piece_width=$((width/2))
piece_height=$((height/3))

echo "Splitting image into 6 pieces (2x3 grid)..."

# Split the image into 6 pieces with random filenames
declare -a piece_files=()
for row in {0..2}; do
    for col in {0..1}; do
        x=$((col * piece_width))
        y=$((row * piece_height))
        
        # Generate random filename
        random_str=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 8 | head -n 1)
        output_file="${output_dir}/${random_str}.${extension}"
        piece_files+=("$output_file")
        
        convert "$input_image" -crop ${piece_width}x${piece_height}+${x}+${y} "$output_file"
        echo "Created: $output_file"
    done
done

echo -e "\nDone! Split images are saved in the '$output_dir' directory"

# Show dimensions of pieces
echo -e "\nPiece dimensions:"
echo "Width: $piece_width pixels"
echo "Height: $piece_height pixels"

# Create montage in separate solve directory
montage "${piece_files[@]}" -tile 2x3 -geometry +5+5 "${solve_dir}/${filename}_montage.${extension}"
echo -e "\nCreated montage: ${solve_dir}/${filename}_montage.${extension}"

# Save split order to file
printf "%s\n" "${piece_files[@]##*/}" > "${output_dir}/split_order.txt"

# Display the order of splits with actual filenames
echo -e "\nSplit order (left to right, top to bottom):"
for file in "${piece_files[@]}"; do
    echo "$(basename "$file")"
done