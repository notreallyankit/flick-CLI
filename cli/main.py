import typer
from app import client,server,discovery

app = typer.Typer()

@app.command()
def flickserver(discover : bool= False):
    """Start the hub to receive messages"""
    
    print("[SERVER] Starting file hub...")
    server.start_hub()

@app.command()
def flick():
    """Discover devices and send a file to a selected device."""
    print(f"scanning for available devices:")
    devices = discovery.discover_devices()

    if not devices:
        print(f"No devices found. Make sure server is running.")
        raise typer.Exit()
    
    print(f"\n Available devices:")
    for idx, ip in enumerate(devices,start = 1):
        print(f"{idx}. {ip}")

    choice = typer.prompt("Enter the number of the device to send the file to")
    try:
        choice_idx = int(choice) - 1
        if choice_idx < 0 or choice_idx >= len(devices):
            raise ValueError
    except ValueError:
        print("[ERROR] Invalid choice.")
        raise typer.Exit()
    
    host = devices[choice_idx]
    print(f"[CLIENT] Sending file to {host}...")
    client.send_file(host)