#!/bin/bash

# Check if PyInstaller is installed
if ! command -v pyinstaller &> /dev/null
then
    echo "PyInstaller is not installed. Installing now..."
    pip install pyinstaller
fi

# Run PyInstaller
pyinstaller --onefile src/Which.py
mv /path/to/Which dist/Which

# Notify user
echo "Build complete. Executable is in the dist directory."