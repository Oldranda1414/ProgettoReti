import socket
import os

#initialize socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#associating the socket to the port
server_address = ("localhost", 12000)
sock.bind(server_address)
print("starting up the server on " + server_address[0] + " on port " + str(server_address[1]))

while True:

    #waiting for a message to be received
    print("ready to receive a message...")
    data, address = sock.recvfrom(4096)
    data = data.decode()

    #printing the message once received
    print("message received: " + data)

    #incapsulating in try so that in case of any internal errors the server can send them to the client
    try:

        if data == "get list":
            
            #fectching the file list and number of files on the server
            filePath = os.path.join(os.getcwd(), "server_files")
            fileList = os.listdir(filePath)
            numberFiles = len(fileList)

            #sending the data to the client
            message = str(numberFiles)
            sock.sendto(message.encode(), address)
            message = str(fileList)
            sock.sendto(message.encode(), address)
            print("list of files sent to the client")

            
        elif data == "get file":

            #waiting for filename
            print("waiting for filename...")
            data, address = sock.recvfrom(4096)
            fileFolder = os.path.join(os.getcwd(), "server_files")
            filePath = os.path.join(fileFolder, data.decode())

            #if the requested file is present on the server, it is sent
            if os.path.exists(filePath):

                #sending flag to client
                message = "0"
                sock.sendto(message.encode(), address)

                #fetching file contents and sending them to the client
                file = open(filePath, "r+")
                data = file.read()
                sock.sendto(data.encode(), address)
                print("file sent to the client")
            else:
                
                #if the file is not present on the server, the server sends an error flag to the client
                message = "1"
                sock.sendto(message.encode(), address)

        elif data == "upload":

            #waiting for the filename
            print("waiting for filename...")
            fileName, address = sock.recvfrom(4096)
            fileName = fileName.decode()
            print("filename received")

            #waiting for the file contents
            print("waiting for the file contents...")
            data, address = sock.recvfrom(4096)
            data = data.decode()
            print("file contents received")

            #creating the new file on the server
            fileFolder = os.path.join(os.getcwd(), "server_files")
            filePath = os.path.join(fileFolder, fileName)
            file = open(filePath, "w")
            file.write(data)
            file.close()
            print("file uploaded to the server")

            #sending the upload confirmed message to the client
            message = "0"
            sock.sendto(message.encode(), address)

        #if the request is not recongnised the server sends a message to the client
        else:
            message = "UNKNOWN REQUEST"
            sock.sendto(message.encode(), address)

    #if an internal error has occured the server sends the error log to the client
    except Exception as info:
        message = ("server error\n" + str(info))
        sock.sendto(message.encode(), address)
        sock.close()