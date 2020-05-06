import socket
from user import User
import threading
class Server:

    def __init__(self):
        self.clients = []
        self.nicknames = []
        self.serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("server initializated")
        self.start()
        self.receiving()

    def start(self):
        host = '127.0.0.1'
        port = 777
        self.serv.bind((host, port))
        self.serv.listen(10)
        print('start')
    def receiving(self):
        while True:
            conn, addr = self.serv.accept()
            print(conn)
            print(addr)
            if addr not in self.clients:
                self.meetings(addr, conn)
                self.clients.append(addr)

            else:
                msg = conn.recv(1024)
                print(msg)




    def meetings(self, addr, conn):

        user = User()

        # meetings: name and opponet's name

        nickname = conn.recv(1024)
        nickname = nickname.decode('utf-8')

        print(nickname + ' присоединился')
        msg = 'connected!'
        self.send_to_client(conn, msg)

        self.nicknames.append(nickname)

        opponent = conn.recv(1024)
        opponent = opponent.decode('utf-8')

        user.addr = addr
        user.sock = conn
        user.nick = nickname
        user.opponent = opponent

        print(opponent + ' - имя соперника')

        if opponent in self.nicknames:
            msg = opponent + ' connected'
            self.send_to_client(user.sock, msg)
        else:
            msg = opponent + ' is not here :('
            self.send_to_client(user.sock, msg)

    def print_on_server(self, data):
        print(data.decode('utf-8'))

    def send_to_client(self, client_socket, msg):
        client_socket.send(msg.encode('utf-8'))

if __name__ == '__main__':
    s = Server()