import socket 
import shutil
import threading

def retrspace(name, sock):
    size = sock.recv(1024)
    filesize =int(size.decode('utf-8')) 

    total, used, free = shutil.disk_usage("D:/")

    if free < filesize:
        sock.send(bytes('false','utf-8'))
    else:
        sock.send(bytes('true','utf-8'))
    sock.close()
    
def Main():
    
    host = socket.gethostname()
    hostaddr = socket.gethostbyname(host)
    port = 5001
    print(hostaddr)

    s = socket.socket()
    s.bind((hostaddr,port))

    s.listen(5)

    print ("Server Started.")
    while True:
        # Accepting connections
        c, addr = s.accept()

        # putting accepted client in dictionary
        
        print ("client connedted ip:<" + str(addr) + ">")

        
        

        t = threading.Thread(target=retrspace,args=('check_space',c))
        
        t.start()
         
    s.close()

if __name__ == '__main__':
    Main()