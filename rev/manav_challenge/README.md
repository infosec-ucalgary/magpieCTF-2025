# Which

Author: Manav

>Difficulty: easy

Flag: `magpieCTF{Rich_3nou9h_7o_$+@y_C1e@n}`

## Backstory

For years, Cyber-Solutions was the gold standard in digital security, the guardian of businesses worldwide. But that was before Krypto arrived. The newcomer didn’t just compete—it dominated, leaving Cyber-Solutions in the dust. Their stock plummeted nearly 50%, their reputation shattered.

And now, scandal.

The CEO of Cyber-Solutions stands accused of something far worse than corporate failure—whispers of shady dealings, hidden transactions, and secrets buried deep in encrypted files. Then came the leak. Data from the CEO’s personal computer, exposed for the world to see.

But is he truly guilty? Or has someone engineered the perfect takedown?

The truth is locked away in the binary. Decode it, and uncover whether the CEO is the mastermind of his own downfall—or the victim of something far more sinister

## Intended Solve

- Running the elf give you the function name to search for in ROT13
- You need to convert the elf to byte code. Use 'pyinstxtractor.py' to get .pyc
- Convert Which.pyc to bytecode using online resources. (ELF - pycdas)
    - You will get the assembly code on your terminal. Either read through it to find the flag
    under the function name, or ask AI to convert the assembly to python code.
- Optionaly, you could open Which.pyc in vim to find the flag

## Handouts

- Which