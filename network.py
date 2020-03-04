# connect to th server via socket
import socket
import pickle  #conv buts to object  : serial obj


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = '192.168.43.73'  # same ip of the server in server.py
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()


    def get_p(self):
        return self.p

    def connect(self): # we will ge a string if the player id

        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data)) # send string to the server
            return pickle.loads(self.client.recv(2048)) # receive object
        except socket.error as e:
            print(str(e))


