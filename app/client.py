import socket
import os
from app.config import TCP_PORT,BUFFER_SIZE

def send_file(host : str,filepath : str):
    if not os.path.exists(filepath):
        print("[ERROR] File does not exist.")
        return
    
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect((host,TCP_PORT))

    filename = os.path.basename(filepath)
    client.send(filename.encode())
    ack = client.recv(BUFFER_SIZE)

    with open(filepath,"rb") as file:
        while True:
            chunk = file.read(BUFFER_SIZE)
            if not chunk:
                break
        client.send(chunk)

    print(f"[+] file {filename} sent succesfully!")
    client.close()
