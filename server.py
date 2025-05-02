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
all_player_health = {}

def handle_client(client, address, _id):
    print(f"Accepted connection from {address}, id: {_id}")
    #
    currently_active_player.append(_id)

    # Run once data goes here
    initialize_data = client.recv(2048)
    initialize_reply = process_data(pickle.loads(initialize_data), _id)
    client.sendall(pickle.dumps(initialize_reply))

    try:
        while True:
            data = client.recv(2048)
            if not data:
                break
            response = process_data(pickle.loads(data), _id)
            client.sendall(pickle.dumps(response))
    except Exception as e:
        print(f"Error handling client {address}: {e}")
    finally:
        remove(_id)
        client.close()
        print(f"Connection with {address} closed")

def remove(_id):
    currently_active_player.remove(_id)
    if _id in all_player_character:
        del all_player_character[_id]
    if _id in all_player_location:
        del all_player_location[_id]
    if _id in all_player_health:
        del all_player_health[_id]
    if _id in all_player_projectile:
        del all_player_projectile[_id]

def process_data(data, _id):
    match data[0]:
        case "all player health":
            all_player_health[_id] = data[1]
            return all_player_health
        case "all player projectile":
            all_player_projectile[_id] = data[1]
            return all_player_projectile
        case "all active player":
            return currently_active_player
        case "all player character":
            return all_player_character
        case "initialize":
            match data[1]:
                case "mage":
                    all_player_character[_id] = "mage"
                    player = Mage(_id)
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
            print(all_player_location)
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

    player_id = 0

    print(f"Server listening on {host}:{port}")
    while True:
        client_socket, addr = server_socket.accept()
        client_id = player_id
        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr, client_id))
        client_thread.daemon = True
        client_thread.start()
        player_id += 1

if __name__ == "__main__":
    start_server()