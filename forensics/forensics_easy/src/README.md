# **Deed of Desperation**  

**Difficulty:** Easy  

---

**Flag:** `magpieCTF{WH4T_D1D_T3RRY_S1GN}`  

---


## **Backstory**  
Cyber-Solutions was once the top name in security, but ever since Krypto arrived, the company has been struggling. Terry claims Krypto is undercutting his prices and stealing customers without making a profit. His quiet frustration has turned into public outrage as he fights to keep his business afloat.


---
## **Intended Solve**  Run the following lines:
- ```steghide extract -sf wallpaper.jpg```
- Leave paraphrase empty
- Decode password using Base64 (result -> my_secret_password)
- ```unzip -P my_secret_password flag.zip```
- ```cat flag.txt```
  
---

## **Handouts**  
- wallpaper.jpg image located in `dist/`


---

## **Other Notes**  
1. Check the metadata of the image for useful information.
2. The paraphrase is empty.
3. Look for anything encoded that might need decoding.
4. Use a tool designed for extracting hidden data from images.








  

