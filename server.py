import socket
import threading

class Server:
    clients_list = []
    last_received_message = ""
    def __init__(self):
        self.server_socket = None
        self.create_server()

    def create_server(self):

        self.server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        local_ip = '127.0.0.1'
        local_port = 9090
        print('server started')
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((local_ip, local_port))
        self.server_socket.listen(5)
        self.receive_message_in_a_new_thread()


    def receive_message(self, so):
        while True:
            incoming_buffer = so.recv(1024)
            if not incoming_buffer:
                break
            self.last_received = incoming_buffer.decode('utf-8')
            self.broadcast_to_all_clients(so)

    def broadcast_to_all_clients(self, sender_sockets):
        for client in self.clients_list:
            so, (ip,port) = client
            if so not in sender_sockets:
                so.sendall(self.last_received_message.encode('utf-8'))

    def receive_message_in_a_new_thread(self):
        while True:
            client = so, (ip, port) = self.server_socket.accept()
            self.add_to_clients(client)
            t = threading.Thread(target = self.receive_message(), args = (so,))
            t.start()
    def add_to_clients(self, client):
        if client not in self.clients_list:
            self.clients_list.append(client)

if __name__ == '__main__':
    s = Server()