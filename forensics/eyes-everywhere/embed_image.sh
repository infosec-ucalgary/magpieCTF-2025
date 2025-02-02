#!/bin/bash

# Array of text pieces to embed
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

# Create a temporary directory for text files
temp_dir=$(mktemp -d)

# Ensure the image directory exists
if [ ! -d "$image_dir" ]; then
    echo "Error: Directory '$image_dir' does not exist."
    exit 1
fi

# Process each text piece
for i in "${!texts[@]}"; do
    image_path="$image_dir/camera_$((i+1)).jpg"
    
    # Check if the image exists
    if [ ! -f "$image_path" ]; then
        echo "Error: Image '$image_path' not found. Skipping."
        continue
    fi

    # Create a temporary file for the current text
    text_file="$temp_dir/text_$((i+1)).txt"
    echo "${texts[$i]}" > "$text_file"

    # Embed the text into the image
    echo "Embedding text into 'camera_$((i+1)).jpg'..."
    if steghide embed -cf "$image_path" -ef "$text_file" -p "" -q; then
        echo "Successfully embedded into 'camera_$((i+1)).jpg'."
    else
        echo "Failed to embed into 'camera_$((i+1)).jpg'."
    fi
    echo "-------------------"
done

# Clean up temporary files
rm -rf "$temp_dir"

echo "All files processed!"
