import os
import hashlib
# """ Library that contains helper functions """

class FileReader():
    # """Library of util functions to handle files being transferred through the network"""
    def __init__(self, filename):
        self.filename = filename
        self.filepath = os.path.abspath(self.filename);

    def get_file_size(self):
    # """Takes in a file name and returns the size in bytes"""
        file_size = os.path.getsize(self.filepath);
        return file_size

    def get_file_bytes(self):
    # """Returns a bytes array of the file that can be sent"""
        byteContent = b""
        with open(self.filepath,'rb') as file:
            byteContent += file.read()
        return byteContent

    def hash_file(self):
        #"""Utilizes hashing to protect the integrity of the files downloaded through our system"""
        #Function taken from: https://stackoverflow.com/questions/22058048/hashing-a-file-in-python
        hash = hashlib.sha256()
        with open(self.filename, 'rb', buffering=0) as f:
            for b in iter(lambda : f.read(128*1024), b''):
                hash.update(b)

        return hash.hexdigest()

    def partitionFile(self, chunkSize):
    #Not yet tested.
    #Function is based on the implementation found at: http://bdurblg.blogspot.com/2011/06/python-split-any-file-binary-to.html
        file = open(self.filepath, 'rb')
        fileData = file.read()
        file.close()
        bytes = len(data)
        chunkNum = bytes/chunkSize
        if (bytes%chunkSize):
            chunckNum = chunkNum + 1

        #Creates a file to track different partitions
        file = ("tracker.txt", "w")
        file.write(self.filepath +','+'chunk,'+str(chunkNum)+','+str(chunkSize))
        file.close()

        chunkNames = []
        for i in range(0, bytes+1, chunkSize):
            fn1 = "chunk%s" % i
            chunkNames.append(fn1)
            file = open(fn1, 'wb')
            file.write(data[i:i+ chunkSize])
            file.close()

    def mergeFiles(self, chunkNum, chunkSize):
        #Not yet tested
        #Function is based on the implementation found at: http://bdurblg.blogspot.com/2011/06/python-split-any-file-binary-to.html
        for j in range(0,chunkNum):
            chunkNum=i * chunkSize
            chunkName = self.filename+'%s'%chunkNum
            file = open(chunkName, 'rb')
            dataList.append(f.read())
            file.close()
            file = open(self.filename, 'wb')
            for data in dataList:
                file.write(data)
                file.close()

class DirectoryReader():
    # """Helper library to handle the directories linked to the P2P network"""
    def __init__(self, shared_dir):
        self.shared_dir = shared_dir

    def list_file_names(self):
        file_NameList = os.listdir(self.shared_dir)
        return file_NameList
