import socket
import threading

# Set up IP and port
HOST = '127.0.0.1'    # Your own computer will host
PORT = 12345        # Random port number

# List of current Connections
clients = {}

def server_start():
    # Create socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:

        #Start server
        server.bind((HOST, PORT))
        server.listen()

        print('Server started successfully\n')

        while True:
            # Wait for a connection
            c_socket, c_address = server.accept()
            # Start thread
            client_thread = threading.Thread(target=handle_client, args=(c_socket, c_address))
            client_thread.start()
        

def handle_client(socket, address):
    # This function handles the connection between the server and its clients

    #First add them to the clients dictionary
    clients[socket] = 'Anonymous'

    print(f'New client connected')

    with socket:
        while True:
            # Receive data from client
            data = socket.recv(1024).decode('utf-8')

            # Used to end function if the client disconnects
            if not data:
                del clients[socket]
                break
            # Start processing the data
            data_parts = [part.strip() for part in data.split('`')]
            # Data Organizations:
            # 0. Command
            # 1. Second Command
            # 2. Message

            # Get the list of the other users for later
            other_users = [key for key in clients if key != socket]

            #First check the first letter to see if its a request
            if data_parts[0] == '/':
                #Depending on the request, do the corresponding action

                if data_parts[1] == 'List':
                    # Request for client list
                    nicknames = [clients[user] for user in other_users]
                    socket.sendall(f'@``{nicknames}'.encode('utf-8'))

                elif data_parts[1] == 'Nickname':
                    # Request to change nickname
                    send_message(f'{clients[socket]} is now {data_parts[2]}', other_users)
                    print(f'{clients[socket]} renamed themselves to {data_parts[2]}')
                    clients[socket] = data_parts[2]

                elif data_parts[1] == 'Disconnect':
                    # Request to disconnect
                    send_message(f'{clients[socket]} has disconnected', other_users)
                    del clients[socket]
                    break

            # If not a request check message types
            elif data_parts[0] == '!':
                # Send message to all connected clients
                send_message(data_parts[2], other_users)
                print(f'{clients[socket]} to all: {data_parts[2]}')

            elif data_parts[0] == '^':
                # Send message to specific client
                # Recipients are listed to the client in the order they are in the dictionary
                # The index sent back is the index corresponding to the socket of the recipient in "other_users"
                recipient = other_users[int(data_parts[1])]
                send_message(data_parts[2], recipient)
                print(f'{clients[socket]} to {clients[recipient]}: {data_parts[2]}')

def send_message(message, recipients):
    # Send a message to a list of recipients
    if isinstance(recipients, list):
        # If its going to everybody it will be a list and you can iterate through it
        for recipient in recipients:
            recipient.sendall(message.encode('utf-8'))
    else:
        # Only one recipient
        recipients.sendall(message.encode('utf-8'))

if __name__ == '__main__':
    server_start()