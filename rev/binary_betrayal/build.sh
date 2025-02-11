#!/bin/bash

# Check if PyInstaller is installed
if ! command -v pyinstaller &> /dev/null
then
    echo "PyInstaller is not installed. Installing now..."
    pip install pyinstaller
fi

# Run PyInstaller
pyinstaller --onefile src/Which.py
mv dist/Which rev/dist/Which

sha1sum rev/dist/Which > rev/dist/Which.sha1.sig

# Notify user
echo "Build complete. Executable is in the dist directory."