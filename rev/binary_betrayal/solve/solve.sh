#!/usr/bin/env bash

# Define the ELF binary name
ELF_FILE="Which"

# Step 1: Check if pyinstxtractor is installed
command -v "pyinstxtractor" >/dev/null 2>&1
if [[ $? -eq 1 ]]; then
    echo "[-] This script expects 'pyinstxtractor' to be a standalone executable (or some shell script)."
    echo "[*] The program can be found here: https://github.com/extremecoders-re/pyinstxtractor"
    exit 1
fi

# Step 2: Run pyinstxtractor on the ELF file
echo "[*] Extracting $ELF_FILE using pyinstxtractor..."
pyinstxtractor "./$ELF_FILE"

# Step 3: Locate the extracted .pyc file
EXTRACTED_DIR="${ELF_FILE}_extracted"
PYC_FILE="$EXTRACTED_DIR/Which.pyc"

# Step 4: Check if the .pyc file exists
if [[ -f "$PYC_FILE" ]]; then
    echo "\n[*] Extracted PYC file found: $PYC_FILE"
    
    # Step 5: Print the .pyc content and extract the flag
    FLAG=$(cat "$PYC_FILE" | strings | grep -o 'magpieCTF{Rich_3no')
    
    if [[ -n "$FLAG" ]]; then
        echo "\n MagpieCTF - binary_betrayal : True"
        exit 0
    else
        echo "\n MagpieCTF - binary_betrayal : False."
        exit 1
    fi
else
    echo "\n[-] Extracted PYC file not found."
fi
