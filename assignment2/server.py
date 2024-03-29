import socket
import threading

clients = {}
lock = threading.Lock()
ADDR1 = ("localhost",6000)

def handle_client(client_socket, client_id):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            if message == "list":
                send_online_clients(client_socket)
            else:
                recipient_id, content = message.split(':', 1)
                send_message(client_id, recipient_id, content)
        except:
            break

    with lock:
        del clients[client_id]
        print(f"Client {client_id} disconnected")
        client_socket.close()
        

def send_online_clients(client_socket):
    online_clients = []
    with lock:
        for client_id in clients.keys():
            online_clients.append(client_id)
    online_clients_str = ', '.join(online_clients)
    client_socket.send(f"Online Clients: {online_clients_str}".encode('utf-8'))

def send_message(sender_id, recipient_id, content):
    with lock:
        if recipient_id in clients:
            recipient_socket = clients[recipient_id]
            try:
                recipient_socket.send(f"From {sender_id}: {content}".encode('utf-8'))
            except:
                pass

def change_server(conn,addr):
    server2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server2.bind(ADDR1) #passing Tuple
    server2.listen(5)
    print(f"[LISTENING] Server2 is listening on {ADDR1}") #to check wether socket is listening
    while True:
        client_socket, client_addr = server2.accept()
   # with lock:
        client_id = client_socket.recv(1024).decode('utf-8')
        clients[client_id] = client_socket
        print(f"Client {client_id} connected from", client_addr)
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_id))
        client_thread.start()


HOST = socket.gethostbyname(socket.gethostname())
PORT = 5566

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print("Server listening on", HOST, PORT)

while True:
    print(f"[ACTIVE CONNECTIONS] {threading.active_count()-1}")
    if threading.active_count()-1 == 2:
         new_thread = threading.Thread(target = change_server,args = (client_socket,client_id))
         new_thread.start()
         print("this server exceeds limit ")
         while 1:
            pass
    client_socket, client_addr = server.accept()
   # with lock:
    client_id = client_socket.recv(1024).decode('utf-8')
    clients[client_id] = client_socket
    print(f"Client {client_id} connected from", client_addr)
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_id))
    client_thread.start()
