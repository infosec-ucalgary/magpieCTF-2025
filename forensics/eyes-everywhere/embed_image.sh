#!/bin/bash
# Check if steghide is installed
if ! command -v steghide &>/dev/null; then
    echo "Installing steghide..."
    sudo apt-get update && sudo apt-get install -y steghide
    
    # Verify installation
    if ! command -v steghide &>/dev/null; then
        echo "Error: steghide installation failed. Please install manually:"
        echo "sudo apt-get install steghide"
        exit 1
    fi
fi

# Array of text pieces to embed (in original split order)
texts=(
    'bWFncGllQ1R$<$Ge0Ix$Y$SU5EbkVTNV$9'
    '$8hc180X1$Q$BSSVY0N2VfTWE$!$3dDN$H'
    '$SXzgzdHd$2$FM25fQV$L$9QRVIkb25fYU'
    '5EX3RIRV8$z$zWUU1X1dpN0h$J$fd$c$0$'
    '4$hJY0hf$V$d$#$E$!$hleV93M3JFX0Jvc'
    'k59'
)

# Directory containing images
image_dir="security_footage_set"
order_file="solve/split_order.txt"

# Create a temporary directory for text files
temp_dir=$(mktemp -d)

# Validate environment
if [ ! -d "$image_dir" ]; then
    echo "Error: Directory '$image_dir' does not exist."
    exit 1
fi

if [ ! -f "$order_file" ]; then
    echo "Error: Order file '$order_file' not found."
    exit 1
fi

# Read the split order from file
mapfile -t ordered_files < "$order_file"

# Verify array lengths match
if [ ${#ordered_files[@]} -ne ${#texts[@]} ]; then
    echo "Error: Number of images (${#ordered_files[@]}) doesn't match number of text pieces (${#texts[@]})"
    exit 1
fi

# Process files in original split order
for index in "${!ordered_files[@]}"; do
    filename="${ordered_files[$index]}"
    image_path="$image_dir/$filename"
    text="${texts[$index]}"

    # Validate image exists
    if [ ! -f "$image_path" ]; then
        echo "Warning: Image '$filename' not found, skipping index $index"
        continue
    fi

    # Create temporary text file
    text_file="$temp_dir/text_$((index+1)).txt"
    echo "$text" > "$text_file"

    # Embed metadata
    echo "Processing $filename (piece $((index+1)) of ${#ordered_files[@]})..."
    if steghide embed -cf "$image_path" -ef "$text_file" -p "" -q; then
        echo "Successfully embedded data into $filename"
    else
        echo "Failed to embed data into $filename"
    fi
    echo "-------------------"
done

# Cleanup
rm -rf "$temp_dir"
echo "Processing complete. Results in: $image_dir"