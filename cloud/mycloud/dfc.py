import socket
import os
from pathlib import Path

def deletefile(user,filename,host):
    Host = host
    port = 5003

    s = socket.socket()
    s.connect((Host, port))

    username = user

    s.send(bytes(username,'utf-8'))

    rec = s.recv(1024)
    data = rec.decode('utf-8')

    if data == '100':
        s.send(bytes(filename,'utf-8'))

        s.recv(1024)
        message = s.recv(1024)

        msg = message.decode("utf-8")
        
        return(msg)

