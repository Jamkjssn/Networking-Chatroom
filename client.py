import socket
import threading

# Setup IP and Port
HOST = '127.0.0.1'  # Server is hosted by the same computer
PORT = 12345        # The port used by the server

connected = False

other_users = []

def start_client():
    # Create a socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))

        # Thread for receiving messages
        threading.Thread(target=receive_message, args=(client_socket,), daemon=True).start()

        print("You are now connected to the server")

        # Have the client set their nickname
        nickname = input("What would you like your nickname to be? \nEnter Nickname:")
        change_nickname(client_socket, nickname)

        # Connection variable for while loop
        global connected
        connected = True
        while(connected):
            # First update other_users
            request_users(client_socket)

            # Send the user to the menu
            choice = server_menu()

            if choice == 1:
                # Figure out the recipient first
                print("Who would you like to message?")
                print("(1) All Users")
                if len(other_users) > 0:
                    print(len(other_users))
                    for i, user in enumerate(other_users):
                        print(f'({i+2}) {user}')
                recipient = input("Recipient number: ")

                if int(recipient) < 1 or int(recipient) > len(other_users) + 1:
                    print("Invalid recipient number, please try again")
                    continue


                # Get the message to be sent
                message = input("Message: ")

                if recipient == "1":
                    # Message to all users
                    client_socket.sendall(f'!``{message}'.encode('utf-8'))
                    print(f'You: {message}')
                else:
                    # Any Private messages
                    recipient_index = int(recipient)-2
                    client_socket.sendall(f'^`{recipient_index}`{message}'.encode('utf-8'))
                    print(f'To {other_users[recipient_index]}: {message}')

            elif choice == 2:
                # Get the new nickname
                new_nickname = input("What would you like your new nickname to be? \nEnter Nickname:")
                change_nickname(client_socket, new_nickname)

            elif choice == 3:
                # Disconnect from the server
                connected = False
                print("Disconnecting from server.")
                disconnect(client_socket)

def server_menu():
    print("\n\t\t Server Options:\n\n(1) Send a message\n(2) Change Nickname\n(3) Disconnect\n\nWhat would you like to do:", end='')
    choice = int(input())
    return choice
        

def request_users(client_socket):
    # Sending /`List command to the server should return a list of the current users
    client_socket.sendall('/`List'.encode('utf-8'))

def change_nickname(client_socket, new_nickname):
    # Sending /`Nickname sends a request to change the users nickname
    client_socket.sendall(f'/`Nickname`{new_nickname}'.encode('utf-8'))

def disconnect(client_socket):
    # Sending /`Disconnect removes the user from the server list
    client_socket.sendall('/`Disconnect'.encode('utf-8'))

def receive_message(client_socket):
    while True:
        #Constantly poll for the a message
        data = client_socket.recv(1024).decode('utf-8')
        # Start decoding
        data_parts = [part.strip() for part in data.split('`')]
        if data_parts[0] == '@':
            # Update the list of users from the server
            global other_users
            other_users = [name.strip() for name in data_parts[1].split(',')]

        elif data_parts[0] == 'Whisper':
            # Handle whisper message
            print(f'Private message from {data_parts[1]}: {data_parts[2]}')

        elif data_parts[0] == 'Message':
            # Handle public message
            print(f'{data_parts[1]}: {data_parts[2]}')

        if not data:
            print("Disconnected")
            global connected
            connected = False
            break

if __name__ == "__main__":
    start_client()