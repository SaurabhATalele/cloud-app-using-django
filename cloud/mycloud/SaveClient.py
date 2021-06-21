import socket
import os
from pathlib import Path

def save(user,name,size,file,host):
    Host = host
    port = 5005

    s = socket.socket()
    s.connect((Host, port))

    username = user

    s.send(bytes(username,'utf-8'))

    rec = s.recv(1024)
    data = rec.decode('utf-8')

    if data == 'ok':
        s.send(bytes(name,'utf-8'))

        s.recv(1024)

        size =bytes(str(size),'utf-8')
        s.send(size)

        s.recv(1024)

        
        bytesToSend = file
                    
        s.send(bytesToSend)
       

        loc = s.recv(1024)
        location = loc.decode('utf-8')
        return [username, location, Host]

