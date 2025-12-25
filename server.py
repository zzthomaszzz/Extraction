import socket
import sys
import threading
import pickle
import random

MAX_PLAYER = 6

current_players = []

game_packet = {"team 1": 0.0, "team 2": 0.0}

lobby_packet = {"team 1": [], "team 2": [], "characters": {}, "ready": {}, "start": False}


#Team Data

def handle_client(client, address, _id):
    print(f"Accepted connection from {address}, id: {_id}")
    #
    current_players.append(_id)
    lobby_packet["ready"][_id] = False

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
    if _id in lobby_packet["team 1"]:
        lobby_packet["team 1"].remove(_id)
    if _id in lobby_packet["team 2"]:
        lobby_packet["team 2"].remove(_id)
    if _id in lobby_packet["ready"]:
        del lobby_packet["ready"][_id]
    if _id in lobby_packet["characters"]:
        del lobby_packet["characters"][_id]

def process_data(data, _id):
    match data[0]:
        case "lobby":
            if data[1]["team"] is not None:
                team = data[1]["team"]
                team_1 = lobby_packet["team 1"]
                team_2 = lobby_packet["team 2"]
                if team == 1 and _id not in team_1 and len(team_1) < 3:
                    lobby_packet["team 1"].append(_id)
                    if _id in team_2:
                        lobby_packet["team 2"].remove(_id)
                elif team == 2 and _id not in team_2 and len(team_2) < 3:
                    lobby_packet["team 2"].append(_id)
                    if _id in team_1:
                        lobby_packet["team 1"].remove(_id)
            if data[1]["character"] is not None:
                lobby_packet["characters"][_id] = data[1]["character"]
            if data[1]["ready"]:
                lobby_packet["ready"][_id] = True
                lobby_packet["start"] = True
                for player in current_players:
                    if player in lobby_packet["ready"]:
                        if not lobby_packet["ready"][player]:
                            lobby_packet["start"] = False
            return lobby_packet

        case "packet":
            if data[1]["point"] != 0:
                team_1 = lobby_packet["team 1"]
                team_2 = lobby_packet["team 2"]
                if _id in team_1:
                    game_packet["team 1"] += data[1]["point"]
                    if game_packet["team 1"] < 0:
                        game_packet["team 1"] = 0
                elif _id in team_2:
                    game_packet["team 2"] += data[1]["point"]
                    if game_packet["team 2"] < 0:
                        game_packet["team 2"] = 0
            game_packet[_id] = data[1]
            print(sys.getsizeof(pickle.dumps(game_packet)))
            return game_packet
        case "all active player":
            return current_players
        case "initialize":
            return _id
        case _:
            return data

def get_assignable_id(taken_id_list):
    assignable_id = [1, 2, 3, 4, 5, 6]
    for _id in taken_id_list:
        assignable_id.remove(_id)
    return assignable_id

def start_server():
    host = ""
    port = 5000

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    server_socket.settimeout(10)

    print(f"Server listening on {host}:{port}")
    while not lobby_packet["start"]:
        available_id = get_assignable_id(current_players)
        client_id = random.choice(available_id)
        try:
            client_socket, addr = server_socket.accept()
        except socket.timeout:
            continue
        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr, client_id))
        client_thread.start()
    server_socket.close()
    print("Server stopped listening for connection")


if __name__ == "__main__":
    start_server()


