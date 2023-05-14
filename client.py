import socket
import threading

HOST = '127.0.0.1'  # IP address of the host machine
PORT = 5000  # Port to connect to

nickname = input("Enter your nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a TCP/IP socket
client.connect((HOST, PORT))  # Connect to the server

def receive():
    """Receive messages from the server."""
    while True:
        try:
            message = client.recv(1024).decode()
            print(message)
        except:
            print("An error occurred!")
            client.close()
            break

def write():
    """Send messages to the server."""
    while True:
        message = f"{nickname}: {input('')}"
        client.sendall(message.encode())

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
