import socket
import threading

def receive_messages(client_socket):
    try:
        while True:
            message = client_socket.recv(1024)
            if not message:
                break
            print(message.decode('utf-8'))
    except Exception as e:
        print(f"Error receiving messages: {e}")
    finally:
        client_socket.close()

# Create a socket for the client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
server_address = ('localhost', 9999)
client_socket.connect(server_address)

# Start a thread to receive messages from the server
receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
receive_thread.start()

try:
    while True:
        # Send a message to the server
        message = input()
        client_socket.send(message.encode('utf-8'))
except KeyboardInterrupt:
    pass
finally:
    client_socket.close()
