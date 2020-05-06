import socket
from user import User
import threading
import time
class Server:

    def __init__(self):
        self.is_connected = True
        self.dict = {}  #cловарь имя пользователя - имя сокета
        self.clients = []
        self.nicknames = []
        self.is_new_msg = False

        self.last_msg = "".encode('utf-8')
        self.serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("server initialised")
        self.start()
        self.connecting()
    def start(self):
        host = '127.0.0.1'
        port = 777
        self.serv.bind((host, port))
        self.serv.listen(10)
        print('start')

    def connecting(self):  #подключение новых пользователей
        while self.is_connected:
            conn, addr = self.serv.accept()
            print(conn)
            print(addr)
            if addr not in self.clients:
                self.meetings(addr, conn)
            else:
                conn.close()
                self.is_connected = False

    def sending(self, user):
        while self.is_connected:
            if self.is_new_msg:
                user.opponent_socket.send(self.last_msg)
                self.is_new_msg = False

    def receiving(self, user):
        while self.is_connected:

            self.last_msg = user.sock.recv(1024)
            self.is_new_msg = True
            time.sleep(0.08)
            msg ='delivered at ' + time.ctime() + '  ---->  ' + self.last_msg.decode('utf-8')
            #self.send_to_client(user.sock, 'Me: '+ msg)
            self.print_on_server(('from ' + user.nick+ " to "+ user.nick +' : ' + msg).encode('utf-8'))



    def meetings(self, addr, conn):

        user = User()

        # meetings: name and opponent's name

        nickname = conn.recv(1024)
        nickname = nickname.decode('utf-8')

        print(nickname + ' присоединился')
        msg = 'connected!'
        self.send_to_client(conn, msg)

        self.clients.append(addr)
        self.nicknames.append(nickname)
        self.dict.update({nickname: conn})

        opponent = conn.recv(1024)
        opponent = opponent.decode('utf-8')

        user.addr = addr
        user.sock = conn
        user.nick = nickname
        user.opponent = opponent


        print(opponent + ' - имя соперника участника ' + nickname)

        if opponent in self.nicknames:
            msg = opponent + ' connected'
            self.send_to_client(user.sock, msg)
            #сокет соперника
            msg = self.dict.get(opponent)
            user.opponent_socket = msg
            self.send_to_client(user.sock, msg) #кажется, это не нужно отсылать клиенту, но пусть будет
            self.threads(user)

        else:
            msg = opponent + ' is not here :('
            self.send_to_client(user.sock, msg)

    def threads(self, user):
        thrsend = threading.Thread(target=self.sending, args = (user,))
        thrreceiving = threading.Thread(target=self.receiving, args = (user,))
        thrsend.start()
        thrreceiving.start()

    def print_on_server(self, data):
        print(data.decode('utf-8'))

    def send_to_client(self, client_socket, msg):
        client_socket.send(str(msg).encode('utf-8'))

if __name__ == '__main__':
    s = Server()