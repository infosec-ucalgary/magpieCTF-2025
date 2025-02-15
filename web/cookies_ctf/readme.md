# Cookie Trail

Author: Yazeed Badr

>Difficulty: easy

Flag: `magpieCTF{christina_exposed_spider}`

## Backstory

You’ll be trying to uncover the truth behind the mysterious hacker known as Spider and the involvement of Christina. By interacting with the web application, you’ll follow a trail of clues hidden within cookies and pages. The deeper you investigate, the more you’ll unravel the hidden secrets of the case. 

## Intended Solve

1. Explore the homepage and read the provided hints and the form that triggers the search query

2. Submit the "casefile" query via the form, which causes the server to set a name cookie

3. Inspect the cookies to determine the state of the investigation

4. Interact with the /check endpoint using different name values in the cookie to uncover different pieces of the story

## Handouts

- `app.py`
- `Templates/index.html`
- `Templates/check.html`
- `docker-compose.yml`
- `solve_cookiesctf.sh`
