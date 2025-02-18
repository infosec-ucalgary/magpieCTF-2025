# The Black Market Binary

Author: Dante 

>Difficulty: medium

Flag: `magpieCTF{kr1pt0_bl4ckm4rk3t_d34ls}`

## Backstory

While reviewing the contents of Christina Krypto’s personal laptop, you come across an unusual file buried deep within her research folders.
At first glance, the file appears to be a simple banking application, seemingly designed to enhance security. But the deeper
you dig, the more troubling things become. You find a note hastily scribbled next to the file in a folder labeled “Confidential Projects”:

"Found this running on Christina’s laptop during the demonstration. Looks like a simple bank security test, but there’s encrypted data hidden in the binary.
Is this how she’s been making her real money? I need to crack this before our meeting tomorrow... The encryption is strange, but I’m sure I can break it."

The note is signed with Henry Explo's initials—H.E.. It’s clear that Henry was trying to uncover something buried deep within Krypto's work. But what exactly was he looking for?

## Handouts

- `black_market`

## Solve

1. `xxd` the file and notice it is packed with `upx`.
2. Unpack it with `upx -d`.
3. Play around with the game until you get the hex values of the flag. This step can be done before unpacking as well. You can even find the 
hex values in a rev program.
4. Open the file in ghidra, or another similar program, and find the `scrambleData` function.
5. Reverse the logic and make a script to decrypt the hex values and get the flag. 
