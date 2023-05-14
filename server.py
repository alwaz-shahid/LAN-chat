import socket
import threading

HOST = '127.0.0.1'  # IP address of the host machine
PORT = 5000  # Port to listen on

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a TCP/IP socket
server.bind((HOST, PORT))  # Bind the socket to a specific address and port
server.listen()  # Listen for incoming connections

clients = []  # List to keep track of connected clients

def broadcast(message, sender):
    """Send a message to all connected clients except the sender."""
    for client in clients:
        if client != sender:
            client.sendall(message)

def handle_client(client, address):
    """Handle a client connection."""
    print(f"New client connected: {address}")
    clients.append(client)
    while True:
        try:
            message = client.recv(1024)
            if message:
                print(f"Received message: {message.decode()}")
                broadcast(message, client)
            else:
                raise Exception('Client disconnected')
        except:
            print(f"Client disconnected: {address}")
            clients.remove(client)
            client.close()
            break

while True:
    client, address = server.accept()
    thread = threading.Thread(target=handle_client, args=(client, address))
    thread.start()
