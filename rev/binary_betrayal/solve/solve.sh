#!/bin/bash

# Define the ELF binary name
ELF_FILE="Which"

# Step 1: Check if pyinstxtractor is installed
if ! [[ -f "pyinstxtractor.py" ]]; then
    echo "[-] Error: pyinstxtractor.py not found!"
    echo "[*] Please download it from: https://github.com/extremecoders-re/pyinstxtractor"
    exit 1
fi

# Step 2: Run pyinstxtractor on the ELF file
echo "[*] Extracting $ELF_FILE using pyinstxtractor..."
python3 pyinstxtractor.py "$ELF_FILE"

# Step 3: Locate the extracted .pyc file
EXTRACTED_DIR="${ELF_FILE}_extracted"
PYC_FILE="$EXTRACTED_DIR/Which.pyc"

# Step 4: Check if the .pyc file exists
if [[ -f "$PYC_FILE" ]]; then
    echo "\n[*] Extracted PYC file found: $PYC_FILE"
    
    # Step 5: Print the .pyc content and extract the flag
    FLAG=$(cat "$PYC_FILE" | strings | grep -o 'magpieCTF{[^}]*}')
    
    if [[ -n "$FLAG" ]]; then
        echo "\n MagpieCTF - binary_betrayal : True"
    else
        echo "\n MagpieCTF - binary_betrayal : False."
    fi
else
    echo "\n[-] Extracted PYC file not found."
fi
