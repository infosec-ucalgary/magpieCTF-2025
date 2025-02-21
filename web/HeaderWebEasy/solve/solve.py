#!/usr/bin/env python3
flag="magpieCTF{I_Don't_Und3rstand_Whats_In_H3r_SHt+p_H3ad}"

import requests as re

HOST="localhost"
PORT="8080"
URL="http://"+HOST+":"+PORT
res=re.head(URL)
if flag in res.headers['FLAG']:
    print("MagpieCTF - headers : True")
else:
    print("MagpieCTF - headers : False")
