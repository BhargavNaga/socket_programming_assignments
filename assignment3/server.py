import socket

def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)  # Number of clients in the queue
    
    print(f"Server listening on {host}:{port}")
    
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address}")
    
    # Receiving the filename from the client
    filename = client_socket.recv(1024).decode()
    print(f"Received filename: {filename}")
    
    # Receiving the text data from the client
    text_data = client_socket.recv(1024).decode()
    print(f"Received text data:\n{text_data}")
    
    filename = "server_data.txt"
    # Write the received text data to the file
    with open(filename, "w") as file:
        file.write(text_data)
        print(f"Data written to file '{filename}'.")
    
    # Closing the file
    file.close()
    print(f"File '{filename}' closed.")
    
    # Sending a response to the client
    response = f"Data written to file '{filename}' on the server."
    client_socket.send(response.encode())
    
    # Closing the client socket and server socket
    client_socket.close()
    server_socket.close()

if __name__ == "__main__":
    host = "127.0.0.1"  # Replace with your server's IP address
    port = 12345       # Choose a suitable port number   
    start_server(host, port)
