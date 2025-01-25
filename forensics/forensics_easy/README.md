# Forensics Challenges
## Category: Forensics
### Author: Ayesha Saeed (Ay.s)

## Description
Uncover the secrets hidden within the image and find the flag.


## Hints
1. Check the metadata of the image for useful information.
2. The paraphrase is empty.
3. Look for anything encoded that might need decoding.
4. Use a tool designed for extracting hidden data from images.


## Solution
Run the following lines:
- ```steghide extract -sf image_og.jpg```
- Leave paraphrase empty
- Decode password using Base64 (result -> my_secret_password)
- ```unzip -P my_secret_password flag.zip```
- ```cat flag.txt```


## Flag
magpieCTF{this_is_the_flag}
