from threading import Lock

class Audit():
    def __init__(self):
        self.is_on = False
        # self.io_lock = Lock()


    def bracket_text(self, text):
        return "<<" + text.upper() + ">>"

    def ingress_listening(self, listening_addr):
        if (self.is_on):
            print(self.bracket_text("listening"))
            print("listening at: " + str(listening_addr))
            print()

    def connection_closed(self, host_addr=None, closing_addr=None):
        if (self.is_on):
            print(self.bracket_text("connection_closed"))
            print("connection to: " + str(host_addr))
            print("closed by: " + str(closing_addr))
            print()



    def data_recieved(self, data):
        if (self.is_on):
            print(self.bracket_text("data recieved"))

            if (type(data) == str):
                print("data recieved: " + data)
            else:
                print("data recieved: " + data.decode("UTF-8"))

            print()

    def recieved_file(self, filename):
        if (self.is_on):
            print(self.bracket_text("data recieved"))

            print("filename: " + filename)

            print()

    def file_written(self, filename):
        if (self.is_on):
            print(self.bracket_text("file written"))
            print("filename: " + filename)
            print()


    def sending_data(self, data):
        if (self.is_on):
            print(self.bracket_text("data sent"))

            if (type(data) == str):
                print("data sent: " + data)
            else:
                print("data sent: " + data.decode("UTF-8"))

            print()

    def aprint(self, _str):
        if (self.is_on):
            print(_str)

    def new_connection(self, connection_addr):
        if (self.is_on):
            print(self.bracket_text("new connection"))
            print("connecting_addr: " + str(connection_addr))
            print()

    def no_addrs_found(self):
        if (self.is_on):
            print(self.bracket_text("parsing error"))
            print("no addresses found when parsing address file")
            print()

    def recieved_file_list(self, file_list):
        if (self.is_on):
            print(self.bracket_text("file list from peer"))
            print("files: " + str(file_list))
            print()
