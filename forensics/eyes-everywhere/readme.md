# Eyes Everywhere  

Author: **Mcveigth Ojeda (Gato Matematico)**  

> Difficulty: **Easy/Medium**  

Flag: `magpieCTF{B1INDnES5_!s_4_PRIV47e_Ma7t3R_83twE3n_A_PER$on_aND_tHE_3YE5_Wi7H_wHIcH_tHey_w3rE_BorN}`  

---

## Backstory  
Surveillance cameras never lie… or do they? The footage from Christina Krypto’s mansion on the night of her murder has gaps—corrupted frames, missing segments, and unexplained distortions. Someone tampered with the system, but who and why?

The Cybercrime Division recently recovered fragments of a surveillance image, but it's a mess. Your task is to piece it back together, extract any hidden data, and uncover the truth.

Rumors suggest that Jake "Kaylined" might have been up to his usual tricks, but was he really there? Or is someone else pulling the strings?
### Hints:
   - The image is broken into multiple pieces—reconstruct it carefully.
   - Look beyond what’s visible; something might be hiding in the noise.
   - Tools like Steghide and Base64 decoding will be useful.

---

## Intended Solve  
1. **Image Reconstruction**:  
   - Players receive a zip file (`security_footage.zip`) containing fragmented images (e.g., `ZzEjxfAi.jpg`). These fragments are parts of a single larger image. When pieced together (manually or via tools like GIMP/Python PIL), the reconstructed image subtly hints at the flag’s theme.  

2. **Steganography Extraction**:  
   - Each image contains embedded data via `steghide` (no password). Extracting from **any single image** reveals a text file with a fragment of the flag encoded in Base64 but obscured by random non-Base64 characters (e.g., `#m?a@gp!i^eCTF{...}`).  

3. **Noise Removal and Decoding**:  
   - Players must filter out characters not allowed in Base64 (e.g., `!@#$%^&*`). Cleaned fragments resemble valid Base64 strings (e.g., `bWFncGllQ1RGe...`).  

4. **Flag Assembly**:  
   - Combine all cleaned Base64 fragments in order and decode to reveal the final flag.  

---

## Handouts  
- `security_footage.zip`: Contains 4–9 fragmented JPEG images (e.g., `camera_random_1.jpg`, `camera_random_2.jpg`).  

# Challenge Builder Documentation

## Prerequisites
- Python 3.x
- `steghide` installed (`sudo apt-get install steghide`)
- ImageMagick installed (`sudo apt-get install imagemagick`)
- Bash shell environment

## Challenge Construction Workflow

### 1. Prepare Flag Components
```python
# File: split_noise.py

# STEP 1: Set your flag in the 'original' variable
original = "REPLACE_WITH_YOUR_FLAG"  # e.g., "magpieCTF{...}"

# STEP 2: Run the encoding script
python3 split_noise.py
```
**Outputs**: 
- Generated text pieces in console (copy these for next step)
- Base64 encoded flag with random noise added

### 2. Image Preparation
```bash
# STEP 1: Place your source image in the working directory
# Recommended: 2:3 aspect ratio, minimum 1000px width
# Supported formats: JPG, PNG, BMP

# STEP 2: Run the image splitter
./split_image.sh security_footage.jpg

# Output:
# - Creates 'security_footage_set' directory
# - Generates 6 scrambled image pieces
# - Creates 'split_order.txt' mapping file
```

### 3. Embed Flag Pieces
```bash
# File: embed_image.sh

# STEP 1: Update the texts array with your generated pieces
texts=(
    'PIECE_1_HERE'   # From split_noise.py output
    'PIECE_2_HERE'   # Maintain original order
    'PIECE_3_HERE'
    'PIECE_4_HERE'
    'PIECE_5_HERE'
    'PIECE_6_HERE'
)

# STEP 2: Run the embedding script
./embed_image.sh

# Verification:
# Check security_footage_set directory for:
# - Modified timestamps on image files
# - Expected 6 image files present
```

## Full Build Command Sequence
```bash
# 1. Generate flag pieces
python3 split_noise.py

# 2. Split base image
./split_image.sh security_footage.jpg

# 4. Embed pieces into images
./embed_image.sh

# 5. Package challenge
zip -r final_challenge.zip security_footage_set split_order.txt solve.sh
```
---

## Other  
- **Tools Required**: `steghide`, image editors (GIMP), scripting tools (Python or Bash for automation).  