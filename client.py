#!/usr/bin/env python3
# Maria Gorbunova

# socket client demo

import socket

HOST = '127.0.0.1'
PORT = 5551


class Client:
    def __init__(self):
        with socket.socket() as s:
            s.connect((HOST, PORT))
            print("Client connect to:", HOST, "port:", PORT)
            validation = {'c': self.changeDir, 'f': self.newFile}

            mesg = 'd'
            s.send(mesg.encode('utf-8'))
            while mesg != 'q':

                fromServer = s.recv(1024).decode('utf-8')
                print("\nReceived from server:")  # , fromServer)
                for serv_resp in fromServer.split(':'):
                    print(serv_resp)

                mesg = ''
                while mesg not in list('clfq'):
                    print('\nMenu\nc: change to a new directory \nl: show all subdirectories and files of the current directory tree'
                          '\nf: create a new file in the current directory\nq: quit')
                    mesg = input("Enter message to send or q to quit: ").strip()

                if mesg in validation:
                    mesg = validation[mesg]()
                s.send(mesg.encode('utf-8'))

    def changeDir(self):
        return 'c:' + input("Enter the name of the directory: ")

    def newFile(self):
        return 'f:' + input("Enter the name of the new file: ")


if __name__ == '__main__':
    c = Client()
