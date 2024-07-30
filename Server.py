import socket
import threading
import pickle
from Settings import PORT
import time

class Server:
    
    HREADER = 64
    SERVER = socket.gethostbyname(socket.gethostname())
    ADDR = (SERVER, PORT)
    FORMAT = 'utf-8'
    DISCONNECT_MESSAAGE = "!DISCONNECT"


    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(Server.ADDR)

        self.clients = set()
        self.clients_lock = threading.Lock()

    def send_board(self, conn, board):
        pickle_board = pickle.dumps(board)
        board_length = len(pickle_board)
        send_length = str(board_length).encode(Server.FORMAT)
        send_length += b' ' * (Server.HREADER - len(send_length)) 
        conn.sendall(send_length)
        conn.sendall(pickle_board)
    
    def get_board(self, conn):
        board = None
        board_length = conn.recv(Server.HREADER).decode(Server.FORMAT) # block line (wait for message.)
        if board_length:
            board_length = int(board_length)
            board_pickle = conn.recv(board_length)
            board = pickle.loads(board_pickle)
        return board

    def handle_client_board(self, conn, addr):
        print(f"[NEW CONNECTION] {addr} connected")
        connected = True
        while connected:
            board = self.get_board(conn)
            if board == Server.DISCONNECT_MESSAAGE:
                connected = False

            print(f"[{addr}] {board}") 
            for client in self.clients:
                self.send_board(conn=client, board=board)
        
        conn.close() 


    def start(self):

        self.server.listen()
        print(f"[LISTENING] Server is linstening on {Server.SERVER}")

        while True:
            conn, addr = self.server.accept()
            self.clients.add(conn)
            thread = threading.Thread(target=self.handle_client_board, args=(conn, addr))
            thread.start()  # start thread on each client.
            print(f"\n[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

server = Server().start()