import socket
import threading
import pickle

class Server:
    
    HREADER = 64
    SERVER = socket.gethostbyname(socket.gethostname())
    PORT = 5001
    ADDR = (SERVER, PORT)
    FORMAT = 'utf-8'
    DISCONNECT_MESSAAGE = "!DISCONNECT"


    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(Server.ADDR)
    
    def handle_client(self, conn, addr):
        print(f"[NEW CONNECTION] {addr} connected")
        connected = True
        while connected:
            msg_length = conn.recv(Server.HREADER).decode(Server.FORMAT) # block line (wait for message.)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(Server.FORMAT)
                if msg == Server.DISCONNECT_MESSAAGE:
                    connected = False

                print(f"[{addr}] {msg}") 
                conn.sendall("Msg received".encode(Server.FORMAT))   
        
        conn.close() 

    def handle_client_board(self, conn, addr):
        print(f"[NEW CONNECTION] {addr} connected")
        connected = True
        while connected:
            board_length = conn.recv(Server.HREADER).decode(Server.FORMAT) # block line (wait for message.)
            if board_length:
                board_length = int(board_length)
                board_pickle = conn.recv(board_length)
                board = pickle.loads(board_pickle)
                if board == Server.DISCONNECT_MESSAAGE:
                    connected = False

                print(f"[{addr}] {board}") 
                conn.sendall(board_pickle)
                # conn.sendall("Msg received".encode(Server.FORMAT))   
        
        conn.close() 


    def start(self):

        self.server.listen()
        print(f"[LISTENING] Server is linstening on {Server.SERVER}")

        while True:
            conn, addr = self.server.accept()
            thread = threading.Thread(target=self.handle_client_board, args=(conn, addr))
            thread.start()  # start thread on each client.
            print(f"\n[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

server = Server().start()