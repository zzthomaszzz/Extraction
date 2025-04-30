import socket
import threading
import pickle
import random
from player import *

player_list = []
client_list = []
projectile_list = []

def handle_client(client, address, _id):
    print(f"Accepted connection from {address}")

    client_list.append(client)
    init = client.recv(1024)
    init_reply = init_pack(pickle.loads(init), _id)
    client.sendall(pickle.dumps(init_reply))

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
        for player in player_list:
            if player.id == _id:
                player_list.remove(player)
        for proj in projectile_list:
            if proj[0] == _id:
                projectile_list.remove(proj)
        if client in client_list:
            client_list.remove(client)

        print(f"Connection with {address} closed")

def init_pack(data, _id):
    if data[0] == "init":
        projectile_list.append([_id, []])
        if data[1] == "soldier":
            player_list.append(Soldier(_id))
            return Soldier(_id)
        elif data[1] == "alien":
            player_list.append(Alien(_id))
            return Alien(_id)
        else:
            player_list.append(Player(_id))
            return Player(_id)

def process_data(data):
    if data[0] == "position":
        for player in player_list:
            if player.id == data[1].id:
                player.rect = data[1].rect
        return player_list
    elif data[0] == "projectile":
        for proj in projectile_list:
            if proj[0] == data[1]:
                proj[1] = data[2]
        return projectile_list
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
        client_id = random.random()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr, client_id))
        client_thread.daemon = True
        client_thread.start()

if __name__ == "__main__":
    start_server()