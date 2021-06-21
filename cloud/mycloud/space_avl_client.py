import socket


def Check_space(host,size):
    Host = host
    port = 5001

    s = socket.socket()
    s.connect((Host, port))
    size = str(size)
    filesize = bytes(size,'utf-8')

    s.send(filesize)

    res = s.recv(1024)
    if res.decode() == 'true':
         return True
    else:
         return False

    s.close()

