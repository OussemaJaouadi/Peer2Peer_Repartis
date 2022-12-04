from Audit.Audit import Audit
from Protocol import Protocol
from ClientConnectionThread import ClientConnectionThread
from ListenThread import ListenThread
import socket
import os

class Client():
    def __init__(self, shared_dir_path, listening_addr):
    # """Initates a peer node for a P2P network, takes in listening address"""
        self.shared_dir_path = shared_dir_path
        self.addr_config_path = self.shared_dir_path.joinpath(".addrs.config")
        self.listening_addr = listening_addr
        self.connections = []
        self.audit = Audit()

    def start_listening_thread(self):
        self.listening_thread = ListenThread(self, self.shared_dir_path, self.listening_addr)
        self.listening_thread.start()

    def join_network(self, connection_addr):
    # """Protocol utlized for each peer to join a network given one or more nodes initialized in
    # P2P network."""
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(connection_addr)

        self.audit.sending_data(Protocol.req_join_bytes())
        client_socket.sendall(Protocol.req_join_bytes(self.listening_addr))

        new_client_connection_thread = ClientConnectionThread(self, self.shared_dir_path, client_socket)
        new_client_connection_thread.start()

        self.connections.append(new_client_connection_thread)

    def list_files(self):
        addrs_arr = Protocol.parse_config_file_to_arr(self.addr_config_path)
        for addr in addrs_arr:
            if not (addr == self.listening_addr):
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect(addr)

                self.audit.sending_data(Protocol.req_list_bytes())
                client_socket.sendall(Protocol.req_list_bytes())

                new_client_connection_thread = ClientConnectionThread(self, self.shared_dir_path, client_socket)
                new_client_connection_thread.start()

                self.connections.append(new_client_connection_thread)

    def request_file(self, filename):
        addrs_dict = Protocol.parse_config_file(self.shared_dir_path.joinpath(".addrs.config"))

        for key, connection_addr in addrs_dict.items():
            if key != "0":
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect(connection_addr)

                self.audit.sending_data(Protocol.req_file_bytes(filename))
                client_socket.sendall(Protocol.req_file_bytes(filename))

                new_client_connection_thread = ClientConnectionThread(self, self.shared_dir_path, client_socket)
                new_client_connection_thread.start()

                self.connections = [a for a in self.connections if a.is_alive()]
                self.connections.append(new_client_connection_thread)
