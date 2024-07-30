import socket
import pickle

class Client:

    HREADER = 64
    FORMAT = 'utf-8'
    DISCONNECT_MESSAAGE = "!DISCONNECT"

    def __init__(self, server, port=5001):

        self.server = server
        self.port = port
        self.addr = (self.server, self.port)

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(self.addr)

    def send(self, msg):
        message = msg.encode(Client.FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(Client.FORMAT)
        send_length += b' ' * (Client.HREADER - len(send_length)) 
        self.client.send(send_length)
        self.client.send(message)
        print(self.client.recv(2048))

    def send_board(self, board):

        pickle_board = pickle.dumps(board)
        board_length = len(pickle_board)
        send_length = str(board_length).encode(Client.FORMAT)
        send_length += b' ' * (Client.HREADER - len(send_length)) 
        self.client.send(send_length)
        self.client.send(pickle_board)

        new_pikle_board = self.client.recv(1000000)
        print(pickle.loads(new_pikle_board))

if __name__ == '__main__':
    
    client = Client('172.20.10.4', 5001)
    client.send([1,2,3])
    client.send("aviel2")
    client.send("aviel3")
    input()
    client.send(Client.DISCONNECT_MESSAAGE)