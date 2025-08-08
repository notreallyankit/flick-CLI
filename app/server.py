import socket
import threading
from app.config import TCP_PORT,BUFFER_SIZE

def start_hub():
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind(('0.0.0.0',TCP_PORT))
    server.listen(5)
    print(f"hub listening on port {TCP_PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

def handle_client(conn,addr):
    print(f"[+] connection from {addr}")
    
    filename = conn.recv(BUFFER_SIZE).decode()
    conn.send(b"ACK")

    with open(filename,"wb") as file:
        while True:
            data = conn.recv(BUFFER_SIZE)
            if not data:
                break
            file.write(data)

    print(f"[+] file {filename} received from {addr}")
    conn.close()
    print(f"connection closed: {addr}")