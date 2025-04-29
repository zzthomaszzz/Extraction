import socket
import threading
import pickle

player_list = []

def handle_client(client, address):
    print(f"Accepted connection from {address}")
    init = client.recv(1024)
    process_data(pickle.loads(init))
    try:
        while True:
            data = client.recv(1024)
            if not data:
                break
            response = process_data(pickle.loads(data))
            client.sendall(pickle.dumps(response))
    except Exception as e:
        print(f"Error handling client {address}: {e}")
    finally:
        client.close()
        print(f"Connection with {address} closed")

def process_data(data):
    if data[0] == "init":
        player_list.append(data[1])
        return True
    elif data[0] == "position":
        for player in player_list:
            if player.name == data[1].name:
                player.rect = data[1].rect
        return player_list
    else:
        return data

def start_server():
    host = ""
    port = 5000

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print(f"Server listening on {host}:{port}")
    while True:
        client_socket, addr = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_thread.daemon = True
        client_thread.start()

if __name__ == "__main__":
    start_server()