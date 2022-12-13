# TODO: add "simple" locking for printing files from list...
# TODO: add hashing?

from time import sleep
from Protocol import Protocol
from Client import Client
import pathlib
import sys
import os
import re
from utils import UI_colors,artist,SpinnerThread

class CLI():
# """
# Commmand Line Interfaceused to initalize a P2P network
# Currently implemented: Initialize, Start Network and Connect to Network
# """
    def __init__(self):

        artist.print_art()
        UI_colors.print_violet("\n"+"-"*80,end='\n\n')

        UI_colors.print_blue("To begin, please specify the path of the")
        UI_colors.print_blue("directory you would like to share (It is best")
        UI_colors.print_blue("if this is an empty directory on your computer)"+"\n")

        self.shared_dir = self.get_usr_directory()
        self.listening_addr = self.get_usr_ip_and_port()
        self.init_dir()

        while(True):
            try :
                self.join_or_create_network()
                break
            except ConnectionError or ConnectionRefusedError:
                UI_colors.print_yellow('\n\n Restarting JOIN/CREATE service !')                
        while (1):
            self.list_or_req()

    def get_usr_directory(self):
        is_valid_path = False

        while (not is_valid_path):

            print()
            sys.stdout.write('Shared directory path (q to quit): ')
            sys.stdout.flush()
            usr_selection = input()
            if usr_selection=="q":
                spinner = SpinnerThread.SpinnerThread('Exit application', 'Bye!')
                spinner.start()
                sleep(1)
                spinner.stop()
                sleep(1)
                sys.exit(1)
            usr_path = pathlib.Path(usr_selection)

            if (not usr_path.exists()):
                UI_colors.print_red("\n[ERROR] path does not exist,please provide a valid input")

            elif (not usr_path.is_dir()):
                UI_colors.print_red("\n[ERROR] path is not a directory,please provide a valid input")

            else:
                is_valid_path = True
                UI_colors.print_green("\nInitializing shared dir at: " + str(usr_path.absolute()),end='\n\n')

                return usr_path

    def get_usr_ip_and_port(self):

        UI_colors.print_violet("\n"+"-"*80,end='\n\n')
        UI_colors.print_blue("Please provide an address that others can use")
        UI_colors.print_blue("to access your directory in the form ip:port")
        print()

        listening_addr = self.get_addr("Listening address (q to exit) : ")
        UI_colors.print_green("\nListening at: " + str(listening_addr),end='\n\n')

        return listening_addr

    def join_or_create_network(self):

        UI_colors.print_violet("\n"+"-"*80,end='\n\n')
        UI_colors.print_blue("would you like to join an existing network or create a new network ?\n")
        UI_colors.print_yellow("1: create a new network")
        UI_colors.print_yellow("2: join a network")


        is_valid_input = False
        while (not is_valid_input):

            print()

            sys.stdout.write('(1 or 2 ): ')
            sys.stdout.flush()
            usr_input = input()
            if usr_input=="q":
                spinner = SpinnerThread.SpinnerThread('Exit application', 'Bye!')
                spinner.start()
                sleep(1)
                spinner.stop()
                sleep(1)
                sys.exit(1)

            if (usr_input != "1" and usr_input != "2"):

                UI_colors.print_red("[ERROR] input out of range\n")

            else:
                if (usr_input == "1"):

                    print()
                    spinner = SpinnerThread.SpinnerThread('Creating Netowrk', '')
                    spinner.start()
                    sleep(1)
                    spinner.stop()
                    sleep(1)
                    try:
                        self.handle_start_network()
                        UI_colors.print_green('\nNetwork successfully created!\nOthers can now join using your listening address')
                    except ConnectionError :
                        UI_colors.print_red('Error happned r for restart\n')
                        cmd = input("What to do? > ")
                        if (cmd=="r"):
                            raise ConnectionError()
                        else:
                            spinner = SpinnerThread.SpinnerThread('Exit application', 'Bye!')
                            spinner.start()
                            sleep(1)
                            spinner.stop()
                            sleep(1)
                            sys.exit(1)
                elif (usr_input == "2"):

                    print()
                    UI_colors.print_yellow("Please provide address of a node in the netowrk in the form ip:port\n")
                    new_node_addr = self.get_addr("Address of other network node: ")
                    print()
                    spinner = SpinnerThread.SpinnerThread('Attemping to join the network', '')
                    spinner.start()
                    sleep(1)
                    spinner.stop()
                    sleep(1)
                    try:
                        self.handle_join_network(new_node_addr)
                        UI_colors.print_green('\nAdded to network sucessfully !')
                    except ConnectionRefusedError :
                        UI_colors.print_red('Connection refused!')
                        UI_colors.print_red('Error happned r for restart\n')
                        cmd = input("What to do? > ")
                        if (cmd=="r"):
                            raise ConnectionRefusedError()
                        else:
                            spinner = SpinnerThread.SpinnerThread('Exit application', 'Bye!')
                            spinner.start()
                            sleep(1)
                            spinner.stop()
                            sleep(1)
                            exit(1)

                is_valid_input = True


    def get_addr(self, address_type_string):
        is_valid_addr = False
        while (not is_valid_addr):

            sys.stdout.write(address_type_string)
            sys.stdout.flush()
            usr_input = input()
            if usr_input=="q":
                spinner = SpinnerThread.SpinnerThread('Exit application', 'Bye!')
                spinner.start()
                sleep(1)
                spinner.stop()
                sleep(1)
                exit(1)
            lo_port_re = r"lo:(\d+)"
            ip_port_re = r"(\d+\.\d+\.\d+\.\d+):(\d+)"


            lo_match = re.match(lo_port_re, usr_input)
            match = re.match(ip_port_re, usr_input)


            if (lo_match):

                listen_addr = ("127.0.0.1", int("900" + lo_match.group(1)))
                is_valid_addr = True
                print()

                return listen_addr

            elif (not match):

                UI_colors.print_red("[ERROR] Not a valid addr in form ip:port")


            else:

                listen_addr = (match.group(1), int(match.group(2)))
                is_valid_addr = True
                print()

                return listen_addr

    def list_or_req(self):

        UI_colors.print_violet("\n"+"-"*80,end='\n\n')
        UI_colors.print_yellow("1: list available files in the network")
        UI_colors.print_yellow("2: request a file from the network")


        is_valid_input = False
        while (not is_valid_input):

            print()
            sys.stdout.write('(1 or 2): ')
            sys.stdout.flush()
            usr_input = input()
            print()
            if(usr_input=="q"):
                spinner = SpinnerThread.SpinnerThread('Exit application', 'Bye!')
                spinner.start()
                sleep(1)
                spinner.stop()
                sleep(1)
                exit(1)
            if (usr_input != "1" and usr_input != "2"):

                UI_colors.print_red("[ERROR] input out of range\n")

            else:
                if (usr_input == "1"):

                    print("connecting to nodes for file lists...")

                    self.client_obj.list_files()


                elif (usr_input == "2"):

                    sys.stdout.write('name of file to request: ')
                    sys.stdout.flush()
                    req_file_name = input()
                    self.client_obj.request_file(req_file_name)
                    print()
                    UI_colors.print_green("Successfully downloaded!\n")


                is_valid_input = True


    def init_dir(self):
        addrs_file_path = self.shared_dir.joinpath(".addrs.config")

        if addrs_file_path.exists():
            addrs_file_path.unlink()

        with open(self.shared_dir.joinpath(".addrs.config"), "w") as addrs_file:
            file_content = "0: " + self.listening_addr[0] + " " + str(self.listening_addr[1]) + "\n"
            addrs_file.write(file_content)


    def handle_init_dir(self):
    # """Handles the creation of a meta file that contains information regarding the nodes in
    # the network currently part of the P2P network"""
        dir_path = sys.argv[2]

        if os.path.isdir(dir_path):

            # TODO: add check for writing in ip and port
            listening_ip = sys.argv[3]
            listening_port_str = sys.argv[4]

            if os.path.isfile(os.path.join(dir_path, "addrs.config")):
                os.remove(os.path.join(dir_path, "addrs.config"))

            with open(os.path.join(dir_path, "addrs.config"), 'wb') as temp_file:
                temp_file.write(b"0: ")
                temp_file.write(listening_ip.encode("UTF-8"))
                temp_file.write(b" ")
                temp_file.write(listening_port_str.encode("UTF-8"))
                temp_file.write(b"\n")

        else:
            UI_colors.print_red("[ERROR] Invalid shared_dir provided")


    def handle_start_network(self):
    # """Initializes a shared directory, enabling other peers to connect to a shared directory of files."""
        # cli start_network shared_dir
        self.client_obj = Client(self.shared_dir, self.listening_addr)
        self.client_obj.start_listening_thread()


    def handle_join_network(self, connection_addr):
        # """Connects two nodes in the network to eachother
        # @params: shared directory, connection ip and connection port"""
        #cli connenct_to_network shared_dir conn_ip, conn_port

        connection_addr =  connection_addr

        self.client_obj = Client(self.shared_dir, self.listening_addr)
        self.client_obj.start_listening_thread()

        self.client_obj.join_network(connection_addr)


if __name__ == "__main__":
    cl = CLI()
