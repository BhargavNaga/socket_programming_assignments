import socket
import threading

clients = {}
lock = threading.Lock()

def handle_client(client_socket, client_id):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            if message == "list":
                send_online_clients(client_socket)
            elif message == "disconnect":
                with lock:
                    del clients[client_id]
                    print(f"Client {client_id} disconnected")
                    client_socket.close()
                    break
            else:
                print(message)
                recipient_id, filename = message.split(':', 1)
                with lock:
                    if recipient_id in clients.keys():
                        recipient_socket = clients[recipient_id]
                        try:
                            if filename.endswith(".txt"):
                                    #send file name
                                    recipient_socket.send(f"{recipient_id}: {filename}".encode('utf-8'))
                                    data_chunk = client_socket.recv(1024).decode()
                                    while (len(data_chunk)==1024):
                                        recipient_socket.send(data_chunk.encode())
                                        data_chunk = client_socket.recv(1024).decode()
                                
                                    recipient_socket.send(data_chunk.encode())
                                    client_socket.send(f"{recipient_id} says : File '{filename}' received and saved.".encode('utf-8'))
                                
                            else :     
                                    #send file name
                                    recipient_socket.send(f"{recipient_id}: {filename}".encode('utf-8'))
                                    data_chunk = client_socket.recv(1024)
                                    while (len(data_chunk)==1024):
                                        recipient_socket.send(data_chunk)
                                        data_chunk = client_socket.recv(1024)
                    
                                    recipient_socket.send(data_chunk)
                                    client_socket.send(f"{recipient_id} says : File '{filename}' received and saved.".encode('utf-8'))
                            
                                

                            
                        except:
                            pass
                
        except:
            break



def send_online_clients(client_socket):
    online_clients = []
    with lock:
        for client_id in clients.keys():
            online_clients.append(client_id)
    online_clients_str = ', '.join(online_clients)
    client_socket.send(f"Online Clients: {online_clients_str}".encode('utf-8'))



def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(3)  # Number of clients in the queue
    
    print(f"Server listening on {host}:{port}")
    
    # Accepting a client connection
    while True:
     client_socket, client_address = server_socket.accept()
     with lock:
         client_id = client_socket.recv(1024).decode()
         clients[client_id] = client_socket
         print(f"Client {client_id} connected from", client_address)
         client_thread = threading.Thread(target=handle_client, args=(client_socket, client_id))
         client_thread.start()
         


host = "127.0.0.1" 
port = 12345       # Choose a suitable port number   
start_server(host, port)

