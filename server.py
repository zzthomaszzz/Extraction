import socket
import threading
import pickle
import random
from time import sleep

from player import *

MAX_PLAYER = 6

#Client data
currently_active_player = []
all_player_location = {}
all_player_character = {}
all_player_projectile = {}
all_player_health = {}

team_progress = {"1": 0, "2": 0}

#Team Data

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
            if response is not None:
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
        case "capture":
            team_progress[data[1]] += 1
            return None
        case "team progress":
            for key in team_progress:
                if team_progress[key] > 100:
                    return key
            return team_progress
        case "all player health":
            all_player_health[_id] = data[1]
            return all_player_health
        case "all player projectile":
            all_player_projectile[_id] = [data[1], data[2]]
            return all_player_projectile
        case "all active player":
            return currently_active_player
        case "all player character":
            return all_player_character
        case "initialize":
            match data[2]:
                case 1:
                    location = [0,0]
                case 2:
                    location = [1247, 767]
                case _:
                    location = [0, 0]
            match data[1]:
                case "mage":
                    all_player_character[_id] = "mage"
                    player = Mage(_id, location)
                case "soldier":
                    all_player_character[_id] = "soldier"
                    player = Soldier(_id, location)
                case "alien":
                    all_player_character[_id] = "alien"
                    player = Alien(_id, location)
                case _:
                    all_player_character[_id] = "default"
                    player = Player(_id, location)
            return player
        case "all location":
            all_player_location[_id] = [data[1], data[2]]
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
        if len(currently_active_player) < 6:
            client_id = random.randint(100, 200)
            if client_id in currently_active_player:
                continue
            client_socket, addr = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, addr, client_id))
            client_thread.daemon = True
            client_thread.start()
        else:
            sleep(1)

if __name__ == "__main__":
    start_server()