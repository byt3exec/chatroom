import socket
import threading
import sys

nickname = input('Choose a nickname: ')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client.connect(('1.1.1.1', 55555))
except socket.error as e:
    print(f"Failed to connect to the server: {e}")
    sys.exit()

def receive():
    """Handles receiving of messages."""
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except Exception as e:
            print(f"An error occurred: {e}")
            client.close()
            break

def write():
    """Handles sending of messages."""
    while True:
        message = f'{nickname}: {input("")}'
        try:
            client.send(message.encode('ascii'))
        except Exception as e:
            print(f"Failed to send message: {e}")
            client.close()
            break

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()