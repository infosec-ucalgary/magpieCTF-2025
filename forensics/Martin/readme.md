# s3cr3ts pl4ns

>Difficulty: intermediate 

## Category
Forensics

## Backstory:
"Terry’s activity has been traced to having sent messages to various people within Krypto’s company, effectively having her spied on."

## Intended Solve:
The flag is located inside the image that is inside a zip file.

The intended method to solve:
   1. Find the TLS certification.
   2. Decrypt all the packets.
   3. Extract the zip file.
   4. Find the packets that contain different headers from the rest.
   5. Get the password for the zip file.
   6. Analyze the image inside the zip file.
   7. Get the flag.
## Challenge Flag  
`magpieCTF{KryPt0_h4s_b3en_F0und_x9130401}`



