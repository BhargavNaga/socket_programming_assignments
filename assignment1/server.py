import socket
import threading #package for handling multiple client using multi threading concept

IP  = socket.gethostbyname(socket.gethostname()) #Ipaddress dynamically obtained with gethostname()
PORT =  5566# Server port
ADDR = (IP, PORT) #tuple for binding IP address and port
SIZE = 1024
FORMAT="utf-8"
# Message size
DISCONNECT_MSG = "!DISCONNECT" #pass the disconnect message in same format


def handle_client(conn, addr):
    print (f" [NEW CONNECTION] {addr} connected.") # addr return the ip address of the client currently connected
    connected = True
    while connected: #loop will run until disconnect command from client
        msg = conn.recv(SIZE).decode (FORMAT) #size=1024 utf-8 is format
        if msg== DISCONNECT_MSG:
          connected = False#stopping while loop
        else:
          print("enter message")
          message = input()
          send_to_specific_client(conn, f"Server says: {message}")
          
           

        print(f" [{addr}] {msg}") #else127.0.0.1', 5 block for connected 127.0.0.1', 5 
    conn.close() #close the loop

def send_to_specific_client(conn,message):
    conn.send(message.encode(FORMAT))



def main():

    print("[STARTING] Server is starting...") #to check wether socket is created successfully
    print(IP)
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR) #passing Tuple
    server.listen(5)
    print("[LISTENING] Server is listening on {IP}: {PORT}") #to check wether socket is listening

    while True: #Loop will run until program is stopped
      conn,addr = server.accept()
      thread = threading.Thread (target=handle_client, args=(conn, addr)) #thread created with threading library; handle_client
      thread.start()
      print(f"[ACTIVE CONNECTIONS] {threading.active_count()-1}")

if __name__ == "__main__":
   main()