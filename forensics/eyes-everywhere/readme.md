# Eyes Everywhere  

Author: **Mcveigth Ojeda (Gato Matematico)**  

> Difficulty: **Easy/Medium**  

Flag: `magpieCTF{B1INDnES5_!s_4_PRIV47e_Ma7t3R_83twE3n_A_PER$on_aND_tHE_3YE5_Wi7H_wHIcH_tHey_w3rE_BorN}`  

---

## Backstory  
A security breach at a surveillance facility has left behind fragmented and corrupted images from a critical camera feed. Investigators suspect the attackers hid clues within the footage to taunt the facility’s security team. Your task is to reconstruct the corrupted data, uncover hidden messages, and decode the final flag to identify the perpetrators.  

---

## Intended Solve  
1. **Image Reconstruction**:  
   - Players receive a zip file (`surveillance_feed.zip`) containing fragmented images (e.g., `camera_random_1.jpg`). These fragments are parts of a single larger image. When pieced together (manually or via tools like GIMP/Python PIL), the reconstructed image subtly hints at the flag’s theme.  

2. **Steganography Extraction**:  
   - Each image contains embedded data via `steghide` (no password). Extracting from **any single image** reveals a text file with a fragment of the flag encoded in Base64 but obscured by random non-Base64 characters (e.g., `#m?a@gp!i^eCTF{...}`).  

3. **Noise Removal and Decoding**:  
   - Players must filter out characters not allowed in Base64 (e.g., `!@#$%^&*`). Cleaned fragments resemble valid Base64 strings (e.g., `bWFncGllQ1RGe...`).  

4. **Flag Assembly**:  
   - Combine all cleaned Base64 fragments in order and decode to reveal the final flag.  

---

## Handouts  
- `surveillance_feed.zip`: Contains 4–9 fragmented JPEG images (e.g., `camera_random_1.jpg`, `camera_random_2.jpg`).  

---

## Other  
- **Tools Required**: `steghide`, image editors (GIMP), scripting tools (Python for automation).  