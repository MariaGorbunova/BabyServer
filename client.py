#!/usr/bin/env python3
# Maria Gorbunova

# socket client receives server response

import socket
import sys

HOST = '127.0.0.1'
# PORT = 5551


class Client:
    def __init__(self, port):
        with socket.socket() as s:
            s.connect((HOST, port))
            print("Client connect to:", HOST, "port:", port)
            validation = {'c': self.changeDir, 'f': self.newFile}

            mesg = 'd'
            s.send(mesg.encode('utf-8'))
            while mesg != 'q':
                fromServer = s.recv(1024).decode('utf-8')
                # if its the first time we get dir or changed dir we need to save this value
                # print the directory and list of returned values
                print("\nReceived from server:")  # , fromServer)
                for serv_resp in fromServer.split(':'):
                    print(serv_resp)

                if mesg.split(':')[0] in list('dclfq'):
                    self.directory = fromServer.split(':')[0]
                    #print("Current directory for client on server: ", self.directory)

                # validate users input
                while mesg not in list('clfq'):
                    print(
                        '\nMenu\nc: change to a new directory \nl: show all subdirectories and files of the current directory tree'
                        '\nf: create a new file in the current directory\nq: quit')
                    mesg = input("Enter message to send or q to quit: ").strip()

                # mesg is user choice+currdir+aditional options
                if mesg != 'q' and mesg != 'd':
                    val = ''
                    if mesg in validation:
                        val = validation[mesg]()
                    mesg += ':' + self.directory + ':' + val
                    #print("In client to server:    ", mesg)
                s.send(mesg.encode('utf-8'))

    def changeDir(self):
        """returns input from the user for a directory"""
        return input("Enter the name of the directory: ")

    def newFile(self):
        """returns input from the user for a newfile"""
        return input("Enter the name of the new file: ")


if __name__ == '__main__':
    try:
        arg = int(sys.argv[1])
        if len(sys.argv) == 2 and len(sys.argv[1]) == 4:
            client = Client(arg)
        else:
            print("Command line argument is not valid!")
    except TypeError as e:
        print(str(e))
        print("Enter an integer!")
    except IndexError as e:
        print(str(e))
        print("Need a command line argument!")
