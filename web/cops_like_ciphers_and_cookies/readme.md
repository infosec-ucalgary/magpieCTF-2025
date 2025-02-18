# Cops Like Ciphers and Cookies

Author: Mohammad Hashmi

>Difficulty: \<easy to medium> 

Flag: `magpieCTF{wh3r3_w4s_Jake}`

## Backstory

A glimpse into the NYPD as a new employee. Attackers will get to navigate through their servers to find out the truth about who killed Kristina. This challenge will frame Jake, however, his innocence will be proven later

## Intended Solve
- Explore the home page a little bit and read the texts
- One of the classes has an odd span of text
- Base64 decode that text and you find out there is a hidden.html page
- Upon arriving to the hidden page the user is greeted with a big message
- When they look around they'll see some cookies that are encoded
- These are encoded with a Vigenère Cipher (hardest part of the challenge) where consistency is the key (Hence the reason for the link in the first page)
- Upon decoding they find that it's a cookie for user
- They can encode 'admin' using the same key and once they set that to the value of the cookie and refresh the page they'll find the flag (with some lore)

## Handouts

- IP of the server

## Hints

Hint 1: Remember, consistency is key
Hint 2: The NYPD used to be fans of Vigenère Ciphers but a bad intern encoded something with base64
