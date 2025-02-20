# Cops Like Ciphers and Cookies

Author: Mohammad Hashmi, obliviousturnip

>Difficulty: easy to medium

Flag: `magpieCTF{wh3r3_w4s_Jake}`

## Backstory

A glimpse into the NYPD as a new employee.
Attackers will get to navigate through their servers to find out the truth about who killed Kristina.
This challenge will frame Jake, however, his innocence will be proven later.

## Intended Solve

This is the intended solve of the challenge:

- Explore the homepage and find a specific `<li>` element with a base64 encoded string which says "We need someone to fix /login, it's been broken for far too long."
- The hacker goes to `/login`
- The following hints are given to the hacker from this new page:
  - there's a meta tag that says *vigenere* in base64
  - the word *admin* is italized
  - it mentions cookies too
- The hacker is supposed to break the vigenere cipher of the cookies, realize what it does, and encrypt *admin* using the obtained key
- The hacker is then supposed to refresh the page to resend the request, after which he is then prompted with the flag

>The key is located in `src/app.js:76`

## Handouts

- IP of the server
