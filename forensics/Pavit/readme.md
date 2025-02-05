# CTF Challenge: Mansion-Recovery

## Overview
In this challenge, after Krypto's Mansion Security was compromised, a PCAP file was recovered. The goal is to analyze the PCAP file to uncover the flag related to the event and possibly identify the killer. The challenge requires network forensics, packet analysis, and some manual decoding.

## Challenge Details

- **Difficulty**: Medium
- **Estimated Time to Solve**: 10-20 minutes
- **Tools Required**: 
  - Wireshark
  - Scapy
  - A little brain power
  
## Files Provided
- **mansion-security.pcapng**: The packet capture file containing important network data.


## Challenge Hints
- Some packets are noise and will need to be filtered out.
- A string is hidden within the packets in a IP range.
- Hidden String is splitted into 3 parts and must be combined to get deciphered
- You might have to manually decode the final flag, which will **not** follow a typical flag format (like MAGPIE{flag})—it will be just a string so that its easier to decipher. once u get the string submit it with the flag like this MAGPIE{String u decoded}.
- Understanding network forensics and packet analysis tools like Wireshark is necessary to succeed.


## Tools & Resources

- **Wireshark**: A network protocol analyzer used to inspect packet captures.
- **Scapy**: A Python library used for packet manipulation and analysis.


## Final Note
This challenge will test your ability to filter out noise from the actual data, along with your skills in decoding hidden information within network traffic. Good luck, and happy hunting!
