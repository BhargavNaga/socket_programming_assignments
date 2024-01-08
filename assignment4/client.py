import socket
import threading
import os

def receive_files():
  while True:
    try:
            message = client_socket.recv(1024).decode('utf-8')
            if(not(message.endswith(".txt") or message.endswith(".png") or message.endswith(".pdf") or message.endswith(".docx") or message.endswith(".mp4"))):
              print(message)
              continue
            
            
        # Receiving the filename from the client
            client_id, filename = message.split(':', 1)
            if not filename:
                break

            parent_dir = "D:/CN/lab5"
            path = os.path.join(parent_dir,client_id)
            if not os.path.exists(path):
              os.mkdir(path)
            else:
              print(f"The directory '{path}' already exists, no need to create it.")
            
            if filename.endswith(".txt"):
                filename = "new.txt"
                file_path = os.path.join(path, "new.txt")
            elif filename.endswith(".png"):
                filename = "new.png"
                file_path = os.path.join(path, "new.png")
            elif filename.endswith(".pdf"):
                filename = "new.pdf"
                file_path = os.path.join(path, "new.pdf")
            elif filename.endswith(".docx"):
                filename = "new.docx"
                file_path = os.path.join(path, "new.docx")
            elif filename.endswith(".mp4"):
                filename = "new.mp4"
                file_path = os.path.join(path, "new.mp4")
            
            
            
            print(f"Received filename: {message}")

            
            # Receiving the file data from the client
            file_data = b""
        
            if filename.endswith(".txt"):
                with open(file_path, "w") as file:
                    data_chunk = client_socket.recv(1024).decode()
                    while (len(data_chunk)==1024):
                        file.write(data_chunk)
                        data_chunk = client_socket.recv(1024).decode()

                    file.write(data_chunk)
            else:
                with open(file_path, "wb") as file:
                    data_chunk = client_socket.recv(1024)
                    while (len(data_chunk)==1024):
                        file.write(data_chunk)
                        data_chunk = client_socket.recv(1024)
        
                    file.write(data_chunk)
                
            print(f"File '{filename}' received and saved.")
            
    
    except:
            print("Error receiving file.")
            break
   
   
   

def send_files():
    while True:
        recipient_id = input("Enter recipient's unique ID (or 'list' to see online clients)(or disconnect to remove connection): ")
        if recipient_id.lower() == "list":
            client_socket.send(recipient_id.encode('utf-8'))
        elif recipient_id.lower() == "disconnect":
            client_socket.send(recipient_id.encode('utf-8'))
            client_socket.close()
            print("Client socket closed.")
            break

        else:
            print(f"Hello {client_id} which file do you want to send? to {recipient_id}")
            print("1. client_data.txt")
            print("2. client_image.png")
            print("3. client.pdf")
            print("4. client_word.docx")
            print("5. client.mp4")

            num = input("Enter your choice: ")
            if num == "1":
                filename = "client_data.txt"
            elif num == "2":
                filename = "client_img.png"
            elif num == "3":
                filename = "client.pdf"
            elif num == "4":
                filename = "client_word.docx"
            elif num == "5":
                filename = "client.mp4"
            else:
                print("Invalid choice")
                continue

             # Reading data from the text file
            if filename.endswith(".txt"):
             with open(filename, "r") as file:
              text_data = file.read()
            
             full_message = f"{recipient_id}:{filename}"
             client_socket.send(full_message.encode())
    # Sending the text file data to the server
             client_socket.send(text_data.encode())
    
            else:
             with open(filename, "rb") as file:
               text_data = file.read()
    
        # Sending the filename to the server
             full_message = f"{recipient_id}:{filename}"
             client_socket.send(full_message.encode())
        
        # Sending the text file data to the server
             client_socket.send(text_data)

             # Closing the file
            file.close()
            print(f"File '{filename}' closed.")
    

    
def start_client(host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    
    return client_socket

if __name__ == "__main__":
    host = "127.0.0.1"  # Replace with your server's IP address
    port = 12345       # Choose the same port number as the server
    client_id = input("Enter your unique ID: ")
    
    client_socket = start_client(host, port)
    print("Connected to the server.")
    client_socket.send(client_id.encode())

    recv_thread = threading.Thread(target=receive_files)
    recv_thread.start()

    send_thread = threading.Thread(target=send_files)
    send_thread.start()

