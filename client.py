import socket
import threading
import time

key = 8194

working = True
join = False

def receiving(name, sock):
    while working:
        try:
            while True:
                data, addr = sock.recvfrom(1024)
                # print(data.decode("utf-8"))

                decrypt = ""
                k = False
                for i in data.decode("utf-8"):
                    if i == ":":
                        k = True
                        decrypt += i
                    elif k == False or i == " ":
                        decrypt += i
                    else:
                        decrypt += chr(ord(i) ^ key)
                print(decrypt)
        except:
            pass
host = socket.gethostbyname(socket.gethostname())
port = 0
server = ('192.168.88.165', 9090)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
s.setblocking(0)

nickname = input('Name: ')

thr = threading.Thread(target = receiving, args = ('RecvThread', s))
thr.start()

while working:
    if join == False:
        s.sendto(("[" + nickname + "] => join chat ").encode("utf-8"), server)
        join = True
    else:
        try:
            message = input()
            crypt = ''
            for i in message:
                crypt += chr(ord(i)^key)
            message = crypt
            if message != "":
                s.sendto(("[" + nickname + "] :: " + message).encode("utf-8"), server)



        except:
            s.sendto(("[" + nickname + "] <= left chat ").encode("utf-8"), server)
            working = False
thr.join()
s.close()

