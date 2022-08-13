import socket
import os
import sys

def inputReceiver():
    print("1) get the list of file in the server")
    print("2) get a file from the server")
    print("3) upload a file on the server")
    print("4) exit")
    command: int = input("What do you want to do?[1/2/3/4] ")
    return command


# initialize socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#set server address
server_address = ('localhost', 12000)

#starting main continious loop, which controlls the UPD communications with the server
while True:

    commandRequested: int
    waitingForCommand = True

    while waitingForCommand:
        commandRequested = inputReceiver()
        print (commandRequested)
        if commandRequested == 1 :
            waitingForCommand = False


    print("command received")
    break