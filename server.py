import socket
import threading
import pickle
import random
from time import sleep

MAX_PLAYER = 6

#Client data

#Contains ID only
current_players = []

#Contains ID:Character name in string
player_characters = {}

data_packet = {"team 1": 0.0, "team 2": 0.0}

ready_status = {}
team_1 = []
team_2 = []

GAME_START = False
SERVER_TICK = 0
#Team Data

def handle_client(client, address, _id):
    print(f"Accepted connection from {address}, id: {_id}")
    #
    current_players.append(_id)
    ready_status[_id] = False

    # Run once data goes here
    initialize_data = client.recv(4096)
    initialize_reply = process_data(pickle.loads(initialize_data), _id)
    client.sendall(pickle.dumps(initialize_reply))

    try:
        while True:
            data = client.recv(4096)
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
    if _id in player_characters:
        del player_characters[_id]
    if _id in team_1:
        team_1.remove(_id)
    if _id in team_2:
        team_2.remove(_id)
    if _id in ready_status:
        del ready_status[_id]

def process_data(data, _id):
    match data[0]:
        case "packet":
            if data[1]["point"] != 0:
                print(data[1]["point"])
                if _id in team_1:
                    data_packet["team 1"] += data[1]["point"]
                    if data_packet["team 1"] < 0:
                        data_packet["team 1"] = 0
                elif _id in team_2:
                    data_packet["team 2"] += data[1]["point"]
                    if data_packet["team 2"] < 0:
                        data_packet["team 2"] = 0
            data_packet[_id] = data[1]
            return data_packet
        case "all active player":
            return current_players
        case "all player character":
            return player_characters
        case "character choice":
            player_characters[_id] = data[1]
        case "team choice":
            choice = data[1]
            if choice == 1 and _id not in team_1 and len(team_1) < 3:
                team_1.append(_id)
                if _id in team_2:
                    team_2.remove(_id)
            if choice == 2 and _id not in team_2 and len(team_2) < 3:
                team_2.append(_id)
                if _id in team_1:
                    team_1.remove(_id)
        case "team 1":
            return team_1
        case "team 2":
            return team_2
        case "ready":
            ready_status[_id] = True
            global GAME_START
            GAME_START = True
            for player in current_players:
                if player in ready_status:
                    if not ready_status[player]:
                        GAME_START = False
        case "ready status":
            return ready_status
        case "game start":
            return GAME_START
        case "initialize":
            return _id
        case _:
            return data

def start_server():
    host = ""
    port = 5000

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    server_socket.settimeout(10)

    print(f"Server listening on {host}:{port}")
    while not GAME_START:
        if len(current_players) < 6:
            available_id = {1, 2, 3, 4, 5, 6}
            taken_id = {0}
            for _id in available_id:
                if _id in current_players:
                    taken_id.add(_id)
            valid_options = available_id - taken_id
            valid_options = list(valid_options)
            client_id = random.choice(valid_options)
            try:
                client_socket, addr = server_socket.accept()
            except socket.timeout:
                continue
            client_thread = threading.Thread(target=handle_client, args=(client_socket, addr, client_id))
            client_thread.start()
        else:
            sleep(1)
    server_socket.close()
    print("Server stopped listening for connection")


if __name__ == "__main__":
    start_server()


