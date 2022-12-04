from Audit.Audit import Audit
from ClientConnectionThread import ClientConnectionThread

import socket
from threading import Thread

class ListenThread(Thread):
    # """Utilizes TCP to enable the nodes to initialize a listening module"""
    def __init__(self, parent_client, shared_dir_path, listening_addr):
        Thread.__init__(self)
        self.shared_dir_path = shared_dir_path
        self.parent_client = parent_client
        self.listening_addr = listening_addr

        self.listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listening_socket.bind(self.listening_addr)
        self.audit = Audit()


    def run(self):
        self.audit.ingress_listening(self.listening_addr)
        self.listening_socket.listen()

        while (1):
            connection_socket, connection_addr = self.listening_socket.accept()
            self.audit.new_connection(connection_addr)

            new_client_connection_thread = ClientConnectionThread(self.parent_client ,self.shared_dir_path, connection_socket)
            new_client_connection_thread.start()

            self.parent_client.connections.append(new_client_connection_thread)
