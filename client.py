from socket import *

host = '127.0.0.1'
port = 777
addr = (host,port)

is_working = True

socket = socket(AF_INET, SOCK_STREAM)
socket.connect(addr)

nickname = input('your name: ')
nickname = nickname.encode('utf-8')
socket.send(nickname)

msg = socket.recv(1024)
print(msg.decode('utf-8'))

opponent = input ('your opponent: ')
opponent =  opponent.encode('utf-8')
socket.send(opponent)

msg = socket.recv(1024)
print(msg.decode('utf-8'))

while is_working:
    data = input('write to server: ')
    data = data.encode('utf-8')
    socket.send(data)
    msg = socket.recv(1024)
    print(msg.decode('utf-8'))




socket.close()
