from utils.files import FileReader
from utils import UI_colors
from Audit.Audit import Audit
from utils.files import DirectoryReader
from Protocol import Protocol
from threading import Thread
import uuid
import socket
import os
import re
import sys

class ClientConnectionThread(Thread):
    # """Utilizes TCP to initialize a thread for every peer connection in the network"""
    def __init__(self, parent_client, shared_dir_path, client_connection):
        Thread.__init__(self)
        self.parent_client = parent_client
        self.shared_dir_path = shared_dir_path
        self.address_file = self.shared_dir_path.joinpath(".addrs.config")
        self.client_connection = client_connection
        self.audit = Audit()

    def run(self):
        while (1):
            data = self.client_connection.recv(8)

            if not data:
                self.audit.connection_closed(self.client_connection.getsockname(), self.client_connection.getpeername())
                break

            data_str = data.decode("UTF-8")

            self.audit.data_recieved(data_str)

            if data_str == Protocol.req_join_string():
                self.handle_join_network_request()

            elif data_str == Protocol.ack_join_string():
                self.handle_ack_join_network_request()

            elif data_str == Protocol.req_list_string():
                self.handle_list_request()

            elif data_str == Protocol.ack_list_string():
                self.handle_ack_list_request()

            elif data_str == Protocol.req_file_string():
                self.handle_req_file_request()

            elif data_str == Protocol.ack_file_string():
                self.handle_ack_file_request()

            elif data_str == Protocol.rej_file_string():
                pass






    def handle_join_network_request(self):
        addr_str = self.get_sized_payload().decode("utf-8")
        try:
            new_ip, new_port = self.find_ip_and_port_addr(addr_str)
        except IndexError :
            UI_colors.print_red('[An error happned] : exiting!')
            print(IndexError)
            sys.exit(1)
        ack_join_bytes = Protocol.ack_join_bytes(self.address_file)
        self.client_connection.sendall(ack_join_bytes)

        self.add_to_addresses_file((new_ip, new_port))


    def handle_ack_join_network_request(self):
        # The loop needs to call join network for each of the other ones.
        new_addr_file_bytes = self.get_sized_payload()

        tmp_file_path = self.shared_dir_path.joinpath(".tmp")
        open(tmp_file_path, 'wb').write(new_addr_file_bytes)

        new_addr_array = Protocol.parse_config_file_to_arr(tmp_file_path)
        my_addr_array = Protocol.parse_config_file_to_arr(self.address_file)

        for addr in new_addr_array:
            if not addr in my_addr_array:
                self.add_to_addresses_file(addr)
                # TODO: add code here that will make new connections with these folk

        if self.shared_dir_path.joinpath(".tmp").is_file():
            self.shared_dir_path.joinpath(".tmp").unlink()

    def handle_list_request(self):
        file_list = DirectoryReader(self.shared_dir_path).list_file_names()
        list_response_bytes = Protocol.ack_list_bytes(file_list)
        self.client_connection.sendall(list_response_bytes)

    def handle_ack_list_request(self):
        list_str = self.get_sized_payload().decode("UTF-8")
        file_name_list = list_str.split("\n")
        print("files: " + str(file_name_list))
        self.audit.recieved_file_list(file_name_list)

    def handle_req_file_request(self):
        file_name_str = self.get_sized_payload().decode("UTF-8")
        file_path = self.shared_dir_path.joinpath(file_name_str)
        if file_path.exists():
            self.client_connection.sendall(Protocol.ack_file_bytes(file_path))
        else:
            self.client_connection.sendall(Protocol.rej_file_bytes(file_path.name))


    def handle_ack_file_request(self):
        name_str = self.get_sized_payload().decode("UTF-8")
        file_bytes = self.get_sized_payload()
        file_hash = self.get_sized_payload().decode("UTF-8")

        self.audit.recieved_file(name_str)

        new_file_path = self.shared_dir_path.joinpath(name_str)
        with open((new_file_path), 'wb') as temp_file:
            temp_file.write(file_bytes)

        assert(FileReader(new_file_path).hash_file() == file_hash)


        self.audit.file_written(name_str)


# ==================================================================================

    def get_sized_payload(self):
        byte_len_bytes = self.client_connection.recv(8)
        byte_len = Protocol.fixed_width_bytes_to_int(byte_len_bytes)
        bytes = self.client_connection.recv(byte_len)
        return bytes

    def find_ip_and_port_addr(self, _str):
        regex = r'([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+).+([0-9]{4})'
        matches = re.findall(regex, _str)
        new_ip = matches[0][0]
        new_port = int(matches[0][1])
        return (new_ip, new_port)

    def add_to_addresses_file(self, new_addr):
        new_ip = new_addr[0]
        new_port = new_addr[1]

        with open(self.address_file, "ab") as addr_file:
            self.write_ip_and_port_to_file(addr_file, new_ip, new_port)

    def write_ip_and_port_to_file(self, open_file, new_ip, new_port):
        open_file.write(str(uuid.uuid1()).encode("UTF-8") + b": ")
        open_file.write(new_ip.encode("UTF-8") + b" ")
        open_file.write(str(new_port).encode("UTF-8") + b"\n")
