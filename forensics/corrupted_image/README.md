# Corrupted image

Author: Alex Aghajanov

>Difficulty: easy

Flag: `magpieCTF{h3x-3d!t-fix}`

## Description

The given image will not open properly, even though it is a standard .png file! Your job is to extract the information from the image.

## Hints

- *Are you sure it's a PNG file?* (the magic bytes are malformed.)

## Solution

- The starting file is a png file named "image.png".
- however a photo editor won't be able to open it because the starting header has a typo.
- the header should be "89 50 4E 47 0D 0A 1A 0A" however, instead it reads "98 50 4E 47 0D 0A 1A 0A".
- So the user has to open the image in a hex editor and make this change.
- Then when they save it, it should open afterwards.
- The image will be a qr code, when scanned will reveal the flag.

## Handouts

- `image.zip`
