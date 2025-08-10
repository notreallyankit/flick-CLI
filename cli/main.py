import typer
from app import client,server

app = typer.Typer()

@app.command()
def flickserver():
    """Start the hub to receive messages"""
    server.start_hub()

@app.command()
def flick(host : str, filepath : str):
    """Send a file to the flick server"""
    client.send_file(host,filepath)