import socket
import threading
import os

def DelFile(name,sock):
    user = sock.recv(1024)
    username = user.decode('utf-8')

    sock.send(bytes("100",'utf-8'))

    path = sock.recv(1024)

    sock.send(bytes("100","utf-8"))
    
    path = username+"/"+path.decode('utf-8')
    # check the user folder
    if os.path.exists(path):
        try:
            os.remove(path)
            sock.send(bytes("100",'utf-8'))
        except:
            try:
                os.rmdir(path)
                sock.send(bytes("100",'utf-8'))
            except:
                sock.send(bytes("101",'utf-8'))

    sock.send(bytes("104",'utf-8'))
    sock.close()   
    

# main method
def Main():
    
    port = 5003


    s = socket.socket()
    host= socket.gethostname()
    print(host)
    s.bind((host,port))

    s.listen(1024)

    print ("Server Started.")
    while True:
        # Accepting connections
        c, addr = s.accept()
        
        print ("client connedted ip:<" + str(addr) + ">")

        # starting the thread
        t = threading.Thread(target=DelFile,args=('file_serve',c))
        t.start()
         
    s.close()

if __name__ == '__main__':
    host =''
    Main()
