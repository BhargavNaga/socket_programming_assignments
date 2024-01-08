#client will not have any threading concept
import socket
IP = socket.gethostbyname(socket.gethostname())
print(IP)
PORT = 5566 
ADDR = (IP, PORT)
SIZE = 1024
FORMAT="utf-8"
DISCONNECT_MSG= "!DISCONNECT"

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    client.connect(ADDR) #connect to the ip address and port 
    print (f" [CONNECTED] Client connected to server at {IP}: {PORT}")
    connected = True 


    while connected:#
        msg = input(">") #get the input message from client with ">" prompt
        client.send(msg.encode(FORMAT)) #sending the message to client
        if msg== DISCONNECT_MSG: #if !Disconnect (use same format) message is sent come out of the while loop 
            connected = False
            client.close()
        else:
            msg = client.recv(SIZE).decode(FORMAT)
            print(f" [SERVER] {msg}") #server is sending message

if __name__ =="__main__":
  main()