import socket
import threading
import os

def SaveFile(name,sock):
    user = sock.recv(1024)
    username = user.decode('utf-8')

    sock.send(bytes("ok",'utf-8'))
    # check the user folder
    if not os.path.exists(username):
        os.makedirs(username)

    
    # recieve name of file
    name = sock.recv(1024)
    filename = name.decode('utf-8')

    upload = username +"/"+filename

    sock.send(bytes('ok','utf-8'))

    size = sock.recv(1024)
    fs = size.decode('utf-8')
    filesize = int(fs)
       

    sock.send(bytes('ok','utf-8'))

    # write file on the disk
    with open(upload,'wb') as f:
        data = sock.recv(1024)
        totalRecv = len(data)
        f.write(data)

        while totalRecv < filesize:
            data = sock.recv(1024)
            totalRecv += len(data)
            f.write(data)
            print("{0:.2f}".format((totalRecv/float(filesize))*100)+ "% Done")
            print ("Download Complete!")
    f.close()

    sock.send(bytes(upload,'utf-8'))

    sock.recv(1024)

# main method
def Main():
    
    port = 5005


    s = socket.socket()
    host= socket.gethostname()
    print(host)
    s.bind((host,port))

    s.listen(5)

    print ("Server Started.")
    while True:
        # Accepting connections
        c, addr = s.accept()
        
        print ("client connedted ip:<" + str(addr) + ">")

        # starting the thread
        t = threading.Thread(target=SaveFile,args=('file_serve',c))
        t.start()
         
    s.close()

if __name__ == '__main__':
    host =''
    Main()
