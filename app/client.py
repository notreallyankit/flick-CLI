import socket
import os
from app.config import TCP_PORT, BUFFER_SIZE
from app.file_operations import send_file_interactive

def send_file(host: str):
    send_file_interactive(host)