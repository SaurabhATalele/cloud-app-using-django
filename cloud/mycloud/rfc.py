import socket
import os
from pathlib import Path

def renamefile(user,filename, newname,host):
    Host = host
    port = 5006

    s = socket.socket()
    s.connect((Host, port))
    print('connected')

    username = user
    # Send username_____________________________
    s.send(bytes(username,'utf-8'))


    # Recieve username REsponse__________________________
    rec = s.recv(1024)
    data = rec.decode('utf-8')


    #Check username response_____________________________
    if data == '100':

        #Send Filename_______________________
        s.send(bytes(filename,"utf-8"))

        #Recieve Filename resp________________
        s.recv(1024)


        #send newname
        s.send(bytes(newname,"utf-8"))
        
        #recieve newname response
        s.recv(1024)

        #last response
        message = s.recv(1024)

        msg = message.decode("utf-8")
        print(msg)
        return(msg)

