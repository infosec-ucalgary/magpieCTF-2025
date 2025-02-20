# most-wanted

Author: totoclick

>Difficulty: Easy

Flag: `magpieCTF{k@yl1n3d_1s_w@nt3d}`

## Backstory

Jake "Kaylined" is one of the most wanted individuals within the Cybercrime Division of the NYPD. He has evaded capture multiple times, leaving behind digital footprints only for the most skilled investigators to trace.  

The one time he was almost caught was during an operation led by Christina Krypto, an expert in cybersecurity. While he narrowly escaped, Kaylined has since dedicated himself to breaking down Krypto’s security achievements, proving he can surpass her defenses.  

This WikiHow-style webpage documents his methods—perhaps even revealing a hidden weakness.  

## Intended Solve  

- Hacker must look at `robots.txt` to find `mcdata/flag.txt`
- Go to `host/mcdata/flag.txt` and get the flag

## Handouts

- the IP address of the server

## Other Notes

- The challenge is designed to teach and test web enumeration.  
- No need for SQL injection, XSS, or advanced exploits—just good old-fashioned directory brute-forcing.  

## Security Features & Exploit Considerations

- Brute-forcing required using common wordlists  
- No direct hints to the hidden page  
- Web enumeration necessary
