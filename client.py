import socket
import threading
import os
from cryptography.fernet import Fernet

HOST = '127.0.0.1' # IP address of the host machine
PORT = 5000 # Port to connect to

nickname = input("Enter your nickname: ")
key = None

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a TCP/IP socket
client.connect((HOST, PORT)) # Connect to the server

def receive():
    """Receive and decrypt messages from the server."""
    global key
    while True:
        try:
            if key is None:
                # If this is the first message, receive the encryption key
                key = client.recv(1024)
                continue
            encrypted_message = client.recv(1024)
            message = decrypt_message(encrypted_message, key)
            print(message)
        except:
            print("An error occurred!")
            client.close()
            break

def write():
    """Encrypt and send messages to the server."""
    global key
    while True:
        try:
            message = f"{nickname}: {input('')}"
            encrypted_message = encrypt_message(message, key)
            client.sendall(encrypted_message)
        except:
            print("An error occurred!")
            client.close()
            break

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

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
