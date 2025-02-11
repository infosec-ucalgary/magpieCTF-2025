# **Kaylined: The Most Wanted**  
**Author:** Ananya

**Difficulty:** Easy  

### **Security Features & Exploit Considerations**  
- **Brute-forcing required** using common wordlists  
- **No direct hints to the hidden page**  
- **Web enumeration necessary**  

---

**Flag:** `magpieCTF{}`  

---

## **Backstory**  
Jake "Kaylined" is one of the most wanted individuals within the Cybercrime Division of the NYPD. He has evaded capture multiple times, leaving behind digital footprints only for the most skilled investigators to trace.  

The one time he was almost caught was during an operation led by **Christina Krypto**, an expert in cybersecurity. While he narrowly escaped, Kaylined has since dedicated himself to **breaking down Krypto’s security achievements**, proving he can surpass her defenses.  

This **WikiHow-style webpage** documents his methods—perhaps even revealing a hidden weakness.  

---

## **Intended Solve**  
- Competitors must **enumerate directories** to discover hidden pages.  
- **Brute-force common paths** (e.g., using `gobuster` or `dirb`) to locate the **secret members-only page**.  
- The **flag is embedded within `flag.html`** in an undisclosed directory.  
- **No explicit hints are given**—only a subtle comment in the source code suggests directory enumeration.  

---

## **Handouts**  
- `src/` (contains HTML, CSS, and other frontend files)  
- `Dockerfile` (for containerized deployment)  

---

## **Other Notes**  
- The challenge is designed to **teach and test web enumeration**.  
- No need for SQL injection, XSS, or advanced exploits—just **good old-fashioned directory brute-forcing**.  
