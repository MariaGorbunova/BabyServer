#!/usr/bin/env python3
# Maria Gorbunova

# socket server sends data to client

import threading
import socket
import sys
import os

HOST = "localhost"
PORT = 5551


class Server:
    def __init__(self, num):
        threads = []
        for i in range(num):
            self.fromClient = ''
            self.curdir = ''
            t = threading.Thread(target=self.start_socket, args=(PORT + i, num))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()

    def start_socket(self, port, num):
        """ Creates a socket and listen for incoming messages"""
        # The default socket_family is AF_INET, and the default socket_type is SOCK_STREAM
        with socket.socket() as s:
            try:
                s.settimeout(15)
                s.bind((HOST, port))
                print("Server hostname:", HOST, "port:", port)

                s.listen(num)
                (conn, addr) = s.accept()
                # print(conn, addr)
                while True:
                    # (conn, addr) = s.accept()
                    self.fromClient = conn.recv(1024).decode('utf-8')
                    if self.fromClient == 'q':
                        break
                    print("From client:", addr)
                    print("Received:", self.fromClient)
                    mesg = self.menu()
                    print("Sending to client:    ", mesg)
                    conn.send(mesg.encode('utf-8'))
            except socket.timeout:
                print("Server says: TIMED OUT!")
        print(f"Socket on {port} is closed.")

    def menu(self):
        """menu handles user menu options"""
        _menu = {'d': self.currentDir, 'c': self.changeDir, 'l': self.listAll, 'f': self.newFile}
        try:
            # if its not the first time we change dir of the server to where each client is
            if self.fromClient.split(':')[0] != 'd':
                os.chdir(self.fromClient.split(':')[1])
                self.curdir = os.getcwd()
            message = _menu[self.fromClient.split(':')[0]]()
        except KeyError as e:
            message = str(e)
        return self.curdir + ':' + message

    def currentDir(self):
        """option d gets called only in the beginning of the program"""
        self.curdir = os.getcwd()
        return ''

    def changeDir(self):
        """changes directory to the directory picked by user"""
        message = ''
        try:
            os.chdir(self.fromClient.split(':')[2])
            self.curdir = os.getcwd()
            message = "Changed directory"
        except Exception as e:
            message = str(e)
        return message

    def listAll(self):
        """returns a string in a format of a list of files and directories in the curdir"""
        # print('List all files and directories:', self.curdir)
        message = ''
        if os.listdir():
            for i in os.listdir():
                message += ":" + i
        else:
            message = "Empty directory"
        return message

    def newFile(self):
        """creates new file requested by user"""
        print('In server creating a file...')
        message = ''
        if not os.path.exists(self.fromClient.split(':')[2]):
            with open(self.fromClient.split(':')[2], "w") as file:
                # file.write("Lab5")
                message = "File was created"
        else:
            message = "Failed to create the file"
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
    except IndexError as e:
        print(str(e))
        print("Need a command line argument!")
