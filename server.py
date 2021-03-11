#!/usr/bin/env python3
# Maria Gorbunova

# socket server demo

import threading
import socket
import sys
import os

HOST = "localhost"
PORTS = [5551, 5552, 5553, 5554]


class Server:
    def __init__(self, num):
        threads = []
        for i in range(num):
            self.fromClient = ''
            t = threading.Thread(target=self.start_socket,
                                 args=(PORTS[i],))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()

    def start_socket(self, port):
        """ Creates a socket and listen for incoming messages"""
        # The default socket_family is AF_INET, and the default socket_type is SOCK_STREAM,
        with socket.socket() as s:
            try:
                s.settimeout(15)
                s.bind((HOST, port))
                print("Server hostname:", HOST, "port:", port)

                s.listen()
                (conn, addr) = s.accept()
                while True:
                    self.fromClient = conn.recv(1024).decode('utf-8')
                    if self.fromClient == 'q':
                        break
                    print("From client:", addr)
                    print("Received:", self.fromClient)

                    mesg = self.menu()
                    conn.send(mesg.encode('utf-8'))
            except socket.timeout:
                print("Server says: TIMED OUT!")

        print(f"Socket on {port} is closed.")

    def menu(self):
        _menu = {'d': self.currentDir, 'c': self.changeDir, 'l': self.listAll, 'f': self.newFile}
        try:
            # print(message)
            message = _menu[self.fromClient.split(':')[0]]()
        except KeyError as e:
            message = str(e)
        return message

    def currentDir(self):
        print("In server CurrentDir:" + os.getcwd())
        return os.getcwd()

    def changeDir(self):
        try:
            os.chdir(self.fromClient.split(':')[1])
            message = 'Directory changed to:' + os.getcwd()
        except Exception as e:
            message = str(e)
        return message

    def listAll(self):
        print('List all files and directories: ')
        print(os.getcwd())
        message = os.getcwd()
        if os.listdir():
            for i in os.listdir():
                print(i)
                message += ":" + i
        else:
            message += ":Empty directory"
        return message

    def newFile(self):
        # TODO:  print acknowledgment with the directory name
        message = os.getcwd()
        if not os.path.exists(self.fromClient.split(':')[1]):
            with open(self.fromClient.split(':')[1], "w") as file:
                # file.write("Lab5")
                message += ':File was created'
        else:
            message = 'File already exists'
        return message


if __name__ == '__main__':
    
    try:
        arg = int(sys.argv[1])
        if len(sys.argv) == 2 and arg < 5:
            server = Server(arg)
        else:
            print("Command line argument is not valid!")
    except TypeError as e:
        print(str(e))
        print("Enter an integer!")


