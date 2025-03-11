# \<ShadowWizzards>

Author: *Royce*

>Difficulty: \<easy> 

Flag: `magpieCTF{christinadeath}`

## Backstory
The NYDP seized the computer of Harriette and obtained the etc/shadow file. Unfortunately it appears to be encrypted, and no one at the NYDP has the time to crack it. find the password. 

## Intended Solve
You see Harriette is in the list of users. Grab the hash "$6$cL0SgXQsoQgIbTpy$7bo3q.D2oWI7ikcJCnNdCZA1J5qLxPqsjF88TWikyO.ujwWP1V3mBJcGe1qbV.NkxYAiE/rMpp4iyV6cla1z/.", place the hash inside passwd.txt and use john --wordlist=/usr/share/wordlists/rockyou.txt passwd.txt to crack the hash. Finally use john --show to see the password

## Handouts
- dist/shadow_output.txt
