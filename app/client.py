import socket
import os
from app.config import TCP_PORT, BUFFER_SIZE

def send_file(host: str, filepath: str):
    if not os.path.exists(filepath):
        print("[ERROR] File does not exist.")
        return
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, TCP_PORT))

    filename = os.path.basename(filepath)
    filesize = os.path.getsize(filepath)

    # Send metadata: filename|filesize
    client.send(f"{filename}|{filesize}".encode())
    ack = client.recv(BUFFER_SIZE)

    with open(filepath, "rb") as file:
        while True:
            chunk = file.read(BUFFER_SIZE)
            if not chunk:
                break
            client.sendall(chunk)  # send inside the loop

    print(f"[+] File '{filename}' ({filesize} bytes) sent successfully!")
    client.close()
