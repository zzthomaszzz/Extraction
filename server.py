import socket
import threading
import pickle
import random
from player import *

#Refactoring code
currently_active_player = []
all_player_location = {}
all_player_character = {}
all_player_projectile = {}

def handle_client(client, address, _id):
    print(f"Accepted connection from {address}, id: {_id}")
    #
    currently_active_player.append(_id)

    # Run once data goes here
    initialize_data = client.recv(1024)
    initialize_reply = process_data(pickle.loads(initialize_data), _id)
    client.sendall(pickle.dumps(initialize_reply))

    try:
        while True:
            data = client.recv(1024)
            if not data:
                break
            response = process_data(pickle.loads(data), _id)
            client.sendall(pickle.dumps(response))
    except Exception as e:
        print(f"Error handling client {address}: {e}")
    finally:
        client.close()
        remove(_id)
        print(f"Connection with {address} closed")

def remove(_id):
    currently_active_player.remove(_id)
    if _id in all_player_character:
        del all_player_character[_id]
    if _id in all_player_location:
        del all_player_location[_id]

def process_data(data, _id):
    match data[0]:
        case "all player projectile":
            all_player_projectile[_id] = data[1]
            return all_player_projectile
        case "all active player":
            return currently_active_player
        case "all player character":
            return all_player_character
        case "initialize":
            match data[1]:
                case "soldier":
                    all_player_character[_id] = "soldier"
                    player = Soldier(_id)
                case "alien":
                    all_player_character[_id] = "alien"
                    player = Alien(_id)
                case _:
                    all_player_character[_id] = "default"
                    player = Player(_id)
            return player
        case "all location":
            all_player_location[_id] = data[1]
            return all_player_location
        case _:
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