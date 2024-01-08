import socket

def start_client(host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    
    return client_socket

if __name__ == "__main__":
    host = "127.0.0.1"  # Replace with your server's IP address
    port = 12345       # Choose the same port number as the server
    
    client_socket = start_client(host, port)
    print("Connected to the server.")
    
    filename = "client_data.txt"  # Replace with your desired filename
    
    # Reading data from the text file
    with open(filename, "r") as file:
        text_data = file.read()
    
    # Sending the filename to the server
    client_socket.send(filename.encode())
    
    # Sending the text file data to the server
    client_socket.send(text_data.encode())
    
    # Receiving the response from the server
    response = client_socket.recv(1024).decode()
    print("Server response:", response)
    
    # Closing the file
    file.close()
    print(f"File '{filename}' closed.")
    
    # Closing the client socket
    client_socket.close()
    print("Client socket closed.")
