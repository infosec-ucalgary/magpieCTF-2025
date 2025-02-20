# cookie-trail

Author: Yazeed Badr

>Difficulty: easy

Flag: `magpieCTF{chr15t1n@_3xp0$3d_$p1d3r}`

## Backstory

You’ll be trying to uncover the truth behind the mysterious hacker known as Spider and the involvement of Christina.
By interacting with the web application, you’ll follow a trail of clues hidden within cookies and pages.
The deeper you investigate, the more you’ll unravel the hidden secrets of the case.

## Intended Solve

1. Submit some random text (using the form) so that the `/search` endpoint gives you a cookie `name=-1`
2. Realize that `name` is actually bound to an integer on the backend
3. Increment the value of `name` to `10` and obtain the flag

## Handouts

- IP of the website
