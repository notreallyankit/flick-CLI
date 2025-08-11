import socket
import os
from app.config import TCP_PORT,BUFFER_SIZE

def send_single_file(client_socket: socket.socket, filepath: str):
    """
    Send a single file over an existing TCP connection.
    """
    filename = os.path.basename(filepath)
    filesize = os.path.getsize(filepath)

    # Send metadata
    client_socket.send(f"{filename}|{filesize}".encode())
    ack = client_socket.recv(BUFFER_SIZE)

    # Send file in chunks
    with open(filepath, "rb") as file:
        while True:
            chunk = file.read(BUFFER_SIZE)
            if not chunk:
                break
            client_socket.sendall(chunk)

    print(f"[+] File '{filename}' ({filesize} bytes) sent successfully!")

def send_file_interactive(host: str):
    """
    Connect to a server and send multiple files interactively.
    Type 'exit' to close the connection.
    """
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, TCP_PORT))
    print(f"[INFO] Connected to {host}:{TCP_PORT}")

    try:
        while True:
            filepath = input("Enter file path to send (or 'exit' to quit): ").strip()

            if filepath.lower() == "exit":
                client.send(b"EXIT")
                print("[INFO] Closing connection...")
                break

            if not os.path.exists(filepath):
                print("[ERROR] File does not exist.")
                continue

            send_single_file(client, filepath)

    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        client.close()
        print("[INFO] Disconnected.")

def receive_files(conn: socket.socket, addr):
    """
    Continuously receive files from a connected client until 'EXIT' is sent.
    """
    while True:
        meta_data = conn.recv(BUFFER_SIZE).decode()

        if not meta_data:
            break  # Client disconnected

        if meta_data.strip().upper() == "EXIT":
            print(f"[INFO] Client {addr} requested to close the connection.")
            break

        try:
            filename, filesize = meta_data.split("|")
            filesize = int(filesize)
        except ValueError:
            print("[ERROR] Invalid metadata format.")
            break

        conn.send(b"ACK")  # Acknowledge metadata

        save_path = os.path.join(os.getcwd(), os.path.basename(filename))
        received_bytes = 0

        with open(save_path, "wb") as file:
            while received_bytes < filesize:
                chunk = conn.recv(BUFFER_SIZE)
                if not chunk:
                    break
                file.write(chunk)
                received_bytes += len(chunk)

        print(f"[+] File '{filename}' received ({received_bytes}/{filesize} bytes) from {addr}")

    conn.close()
    print(f"[INFO] Connection closed: {addr}")