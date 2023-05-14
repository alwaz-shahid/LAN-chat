import socket
import threading
import os
from cryptography.fernet import Fernet

HOST = '127.0.0.1'  # IP address of the host machine
PORT = 5000  # Port to listen on

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a TCP/IP socket
server.bind((HOST, PORT))  # Bind the socket to a specific address and port
server.listen()  # Listen for incoming connections

clients = []  # List to keep track of connected clients
keys = {}  # Dictionary to keep track of encryption keys for each client


def encrypt_message(message, key):
    """Encrypt a message using a symmetric encryption key."""
    f = Fernet(key)
    encrypted_message = f.encrypt(message.encode())
    return encrypted_message


def decrypt_message(encrypted_message, key):
    """Decrypt an encrypted message using a symmetric encryption key."""
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message).decode()
    return decrypted_message


def broadcast(message, sender):
    """Send a message to all connected clients except the sender."""
    for client in clients:
        if client != sender:
            key = keys[client]
            encrypted_message = encrypt_message(message, key)
            client.sendall(encrypted_message)


def handle_client(client, address):
    """Handle a client connection."""
    print(f"New client connected: {address}")
    clients.append(client)
    key = Fernet.generate_key()
    keys[client] = key
    client.sendall(key)
    while True:
        try:
            encrypted_message = client.recv(1024)
            if encrypted_message:
                message = decrypt_message(encrypted_message, key)
                print(f"Received message: {message}")
                broadcast(message, client)
            else:
                raise Exception('Client disconnected')
        except:
            print(f"Client disconnected: {address}")
            clients.remove(client)
            del keys[client]
            client.close()
            break


while True:
    client, address = server.accept()
    thread = threading.Thread(target=handle_client, args=(client, address))
    thread.start()
