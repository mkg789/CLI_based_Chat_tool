import socket
import threading

chat_rooms = {'def room1': []}


def room_handel(room_name, client_socket):
    if room_name not in chat_rooms:
        chat_rooms[room_name] = []
    chat_rooms[room_name].append(client_socket)


def message_broadcast(room_name,sender_socket, message):
    if room_name in chat_rooms:
        for client in chat_rooms[room_name]:
            if sender_socket != client:
                try:
                    client.send(message)
                except Exception as e:
                    print(f"Error {e}")
                    chat_rooms[room_name].remove(client)


def handel_clients(client_socket, client_address):
    try:
        print(f"{client_address} is connected")

        promt = "join a chat room or create a chat room"
        sen = "Available chat rooms:\n"
        n = 0
        for i in chat_rooms.keys():
            n += 1
            sen += f"{n}. " + i + ", \n"
        client_socket.send(sen.encode('utf-8'))
        client_socket.send(promt.encode('utf-8'))

        room_name = client_socket.recv(1024).decode('utf-8')
        room_handel(room_name, client_socket)
        while True:

            message = client_socket.recv(1024)
            if not message:
                break
            message_broadcast(room_name,client_socket,message)
    except Exception as e:
        print(f"error {e}")
    finally:
        if room_name in chat_rooms:
            chat_rooms[room_name].remove(client_socket)
        client_socket.close()
        print(f"Disconnected from {client_address}")

# create server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind(('localhost', 9999))
print("server created")

server_socket.listen(5)

while True:
    client_socket, client_address = server_socket.accept()
    handel = threading.Thread(target=handel_clients, args=(client_socket, client_address))
    handel.start()