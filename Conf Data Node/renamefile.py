import socket
import threading
import os

def DelFile(name,sock):


    # Recieve username_________________________
    user = sock.recv(1024)
    username = user.decode('utf-8')


# Send username Response________________________________

    sock.send(bytes("100",'utf-8'))


    # Recieve filename_________________________

    fn = sock.recv(1024)
    filename = fn.decode("utf-8")


    #Send filename Response________________

    sock.send(bytes("100",'utf-8'))


# Recieve nename______________________________
    nn = sock.recv(1024)
    newname = nn.decode('utf-8')

    #Send newname Response____________________

    sock.send(bytes("100" , 'utf-8'))
    
    # check the user folder
    if os.path.exists(username+'/'+filename):
        try:
            os.chdir(username)
            # Send ok
            sock.send(bytes("100",'utf-8'))
        except:
            #Send error
            sock.send(bytes("101",'utf-8'))

    try:
        os.rename(filename,newname)
        #send ok rename
        sock.send(bytes("100","utf-8"))

    except:
        print("101")
    sock.close()   
    

# main method
def Main():
    
    port = 5006


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
