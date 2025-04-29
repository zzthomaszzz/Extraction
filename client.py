import socket
import pickle

class Client:

    def __init__(self, host="192.168.88.14", port=5000):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))

    def disconnect(self):
        self.client_socket.close()

    def send(self, data):
        self.client_socket.send(pickle.dumps(data))
        response = self.client_socket.recv(1024)
        return pickle.loads(response)

    def send_init(self,data):
        self.client_socket.send(pickle.dumps(data))