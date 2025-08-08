import typer
from app import client,server

app = typer.Typer()

@app.command()
def greet():
    print(f"hello there!")

@app.command()
def catch():
    client.get_file()

@app.command()
def flickserver():
    """Start the hub to receive messages"""
    server.start_hub()

@app.command()
def flick(host : str, filepath : str):
    client.send_file(host,filepath)