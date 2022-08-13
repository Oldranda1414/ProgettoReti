from distutils.log import set_verbosity
import socket
import os
import sys


#function that asks the user for what it wants to do and returns an integer.
#It returns the command if a valid command if a valid command has been
#requested, otherwise it returns 0.
def inputReceiver():
    print("1) get the list of file in the server")
    print("2) get the contents of a file from the server")
    print("3) upload a file on the server")
    print("4) exit")
    command = input("Input a valid command[1/2/3/4] ")
    if(command.isnumeric()):
        command = int(command)
        if command == 1 or command == 2 or command == 3 or command == 4:
            return command
        else:
            return 0
    else :
        return 0


# initialize socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#set server address
server_address = ('localhost', 12000)

#starting main continious loop, which controlls the UPD communications with the server
while True:

    #waitingForCommand will be used to ask the user for a valid command until one is entered
    waitingForCommand = True

    #while loop askd for user to input a valid command until it is entered
    while waitingForCommand:
        commandRequested = int(inputReceiver())
    
        if commandRequested != 0:
            print("command accepted")
            waitingForCommand = False
        else :
            print("command not acceptable")

    #incapsulating in a try to catch any exeptions
    try:
        
        if commandRequested == 1:

            #sending the request of the list message to the server
            message = "get list"
            sock.sendto(message.encode(), server_address)

            #receiving the list from the server. the first word is the number of files in the list, then the filenames are listed
            data, server = sock.recvfrom(4096)
            data.decode()

            #checking if the server sent a valid answer
            if (data.split[1]).isnumerical():

                data = data.split()

                #printing the number of files
                print("there are " + data[1] + "files on the server")

                #printing the filenames
                numberFiles = int(data[1])
                print("there are " + numberFiles + " files in the server:")
                for i in range(2,  + 1):
                    print(data[i])

            #printing the error message of the server, if the awnswer wasn't valid
            else:
                print("an error has occured on the server.")
                print(data)

        elif commandRequested == 2:

            #requesting the filename of the file the user wants to download
            fileName = input("input the name of the file you want to download: ")

            #sending the request of the file to the server
            message = "get file"
            sock.sendto(message.encode(), server_address)
            sock.sendto(fileName.encode(), server_address)

            #receiving the request flag
            #if the flag is 0 then the file has been found
            data, server = sock.recvfrom(4096)
            data = data.decode()
            
            if data == "0":

                #downloading the file on the client
                print("file found on the server\n downloading the file...")

                #receiving the file contents from the server
                data, server = sock.recvfrom(4096)
                data = data.decode()
                #creating a new file with as name the fileName and writing the contents
                fileFolder = os.path.join(os.getcwd(),'file')
                filePath = os.path.join(fileFolder,fileName)
                newFile = open(filePath, 'w')
                newFile.write(data)
                print("file downloaded")

            #if the flag is 1 then the file has not been found
            elif data == "1":
                print("the file has not been found")

            else:
                print("an error has occured on the server.")
                print(data)

    
        elif commandRequested == 3:

            #requesting the filename of the file the user wants to upload
            fileName = input("input the name of the file you want to upload: ")

            #reading the file
            file = open(fileName, "r+")
            data = file.read()

            #sending the request, filename and file contents to the server
            message = "upload"
            sock.sendto(message.encode(), server_address)
            sock.sendto(fileName.encode(), server_address)
            sock.sendto(data.encode(), server_address)
            file.close()

            print("sending " + fileName + " to the server...")

            #waiting for the server to awnser, telling the client the file has been uploaded
            data, server = sock.recvfrom(4096)
            data = data.decode()

            #if the request flag is == "0" the file has been correctly uploaded
            if data == "0":
                print(fileName + " uploaded correctly to the server")
            else:
                print("an error has occured on the server.")
                print(data)

    
        #closing the client program
        elif commandRequested == 4:
            sock.close()
            sys.exit()

    except Exception as e:
        print(e)
    
    print("\n\n\n\n")
