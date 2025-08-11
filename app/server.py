import socket
import threading
import os
from app.config import TCP_PORT, BUFFER_SIZE
from app.file_operations import receive_files

def start_hub():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', TCP_PORT))
    server.listen(5)
    print(f"Hub listening on port {TCP_PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

def handle_client(conn,addr):
    receive_files(conn,addr)