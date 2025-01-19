# magpieCTF 2025 CTF Challenge  
**Author:** Mcveigth Ojeda  

# Challenge name:  
**"Eyes Everywhere"**  

## Description:  
A security breach at a surveillance facility has left behind fragmented and corrupted images from a camera feed. Can you piece together the images, uncover hidden messages, and decode the final flag?  

## Difficulty:  
Medium  / TBD?

## Category:  
Forensics, Steganography  

## Outline:  
1. **Challenge Setup:**  
   - Players are provided with a zip file containing multiple fragmented images labeled sequentially (e.g., `camera_1.jpg`, `camera_2.jpg`).    

2. **Task Flow:**  
   1. **Image Reconstruction:**  
      - Players must identify which fragments correspond to each "camera feed" and piece them together to form a complete image.  

   2. **Steganography Analysis:**  
      - Players may use `steghide` to extract embedded text files from the images.  
      - These text files contain fragments of the flag in an encrypted or encoded format.  

   3. **Noise Removal and Decoding:**  
      - Some of the extracted text files are obscured with random characters or noise.  
      - Players must clean or filter the data to reveal meaningful portions of the flag.  
      - Instructions for decryption or decoding may be partially hidden in the noise.  

3. **Flag Assembly:**  
   - After cleaning the text file fragments, players assemble them in the correct order and decode it to retrieve the complete flag.  