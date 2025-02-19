# Deed of Desperation

Author: ay.s

>Difficulty: Easy  

Flag: `magpieCTF{WH4T_D1D_T3RRY_S1GN}`  

## Backstory

Cyber-Solutions was once the top name in security, but ever since Krypto arrived, the company has been struggling. Terry claims Krypto is undercutting his prices and stealing customers without making a profit. His quiet frustration has turned into public outrage as he fights to keep his business afloat.

## Intended Solve

The intended solve is as follows:

- use `exiftool` (or `file`) to see that the comment property is a base64 encoded string
- use `steghide --extract` **with no password** to extract the zip file from the image
- decode the base64 string and use that as the password for the zip file
- extract the file contents and get the flag

## Handouts

- wallpaper.jpg

## Other Notes  

1. Form.pdf This file shows evidence of Terry Blue selling off property. It further incriminates him by providing motive.
2. Check the metadata of the image for useful information.
3. The paraphrase is empty.
4. Look for anything encoded that might need decoding.
5. Use a tool designed for extracting hidden data from images.
