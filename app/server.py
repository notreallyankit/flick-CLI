import socket
import threading
import os
from app.config import TCP_PORT, BUFFER_SIZE

def start_hub():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', TCP_PORT))
    server.listen(5)
    print(f"Hub listening on port {TCP_PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

def handle_client(conn, addr):
    print(f"[+] Connection from {addr}")
    
    # Receive metadata
    meta_data = conn.recv(BUFFER_SIZE).decode()
    try:
        filename, filesize = meta_data.split("|")
        filesize = int(filesize)
    except ValueError:
        print("[ERROR] Invalid metadata.")
        conn.close()
        return

    conn.send(b"ACK")  # acknowledge metadata

    base_filename = os.path.basename(filename)
    save_path = os.path.join(os.getcwd(), base_filename)

    received_bytes = 0
    with open(save_path, "wb") as file:
        while received_bytes < filesize:
            data = conn.recv(BUFFER_SIZE)
            if not data:
                break
            file.write(data)
            received_bytes += len(data)

    print(f"[+] File '{base_filename}' received ({received_bytes}/{filesize} bytes) from {addr}")
    # conn.close()
    