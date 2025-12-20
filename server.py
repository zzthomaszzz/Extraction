import socket
import threading
import pickle
import random
from time import sleep

from player import *

MAX_PLAYER = 6

#Client data
current_players = []
all_player_location = {}
all_player_character = {}
all_player_projectile = {}
all_player_health = {}

team_progress = {"1": 0, "2": 0}
team_1 = []
team_2 = []

GAME_START = False

#Team Data

def handle_client(client, address, _id):
    print(f"Accepted connection from {address}, id: {_id}")
    #
    current_players.append(_id)

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
    current_players.remove(_id)
    if _id in all_player_character:
        del all_player_character[_id]
    if _id in all_player_location:
        del all_player_location[_id]
    if _id in all_player_health:
        del all_player_health[_id]
    if _id in all_player_projectile:
        del all_player_projectile[_id]
    if _id in team_1:
        team_1.remove(_id)
    if _id in team_2:
        team_2.remove(_id)

def process_data(data, _id):
    match data[0]:
        case "capture":
            team_progress[data[1]] += 1
            return None
        case "team_choice progress":
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
            return current_players
        case "all player character":
            return all_player_character
        case "character choice":
            all_player_character[_id] = data[1]
        case "team choice":
            choice = data[1]
            if choice == 1 and _id not in team_1:
                team_1.append(_id)
                if _id in team_2:
                    team_2.remove(_id)
            if choice == 2 and _id not in team_2:
                team_2.append(_id)
                if _id in team_1:
                    team_1.remove(_id)
        case "team 1":
            return team_1
        case "team 2":
            return team_2
        case "initialize":
            return _id
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
        if len(current_players) < 6 and not GAME_START:
            available_id = [1, 2, 3, 4, 5, 6]
            for _id in available_id:
                if _id in current_players:
                    available_id.remove(_id)
            client_id = random.choice(available_id)
            client_socket, addr = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, addr, client_id))
            client_thread.daemon = True
            client_thread.start()
        else:
            sleep(1)

if __name__ == "__main__":
    start_server()