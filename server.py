import threading
import socket
import sys

HOST = '1.1.1.1'
PORT = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    server.bind((HOST, PORT))
    server.listen()
    print("Server is listening...")
except socket.error as e:
    print(f"Socket error: {e}")
    sys.exit()

clients = []
nicknames = []

def broadcast(message):
    """Send a message to all connected clients."""
    for client in clients:
        try:
            client.send(message)
        except socket.error as e:
            print(f"Error sending message: {e}")

def handle(client):
    """Handle messages from clients."""
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except Exception as e:
            print(f"Error handling message: {e}")
            disconnect_client(client)
            break

def disconnect_client(client):
    """Disconnect a client gracefully."""
    try:
        index = clients.index(client)
        nickname = nicknames[index]
        print(f"{nickname} has left the chat.")
        broadcast(f"{nickname} left the chat.".encode('ascii'))
        nicknames.remove(nickname)
        clients.remove(client)
        client.close()
    except ValueError as e:
        print(f"Error removing client: {e}")

def receive():
    """Accept new connections."""
    while True:
        try:
            client, address = server.accept()
            print(f"Connected with {str(address)}")

            client.send('NICK'.encode('ascii'))
            nickname = client.recv(1024).decode('ascii')
            nicknames.append(nickname)
            clients.append(client)

            print(f"Nickname of the client is {nickname}")
            broadcast(f"{nickname} joined the chat.".encode('ascii'))
            client.send("Connected to the server.".encode('ascii'))

            thread = threading.Thread(target=handle, args=(client,))
            thread.start()
        except Exception as e:
            print(f"Error accepting connections: {e}")
            continue

receive()
