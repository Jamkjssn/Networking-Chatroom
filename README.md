## Overview

**Project Title**: Networking Chatroom

**Project Description**: This project is a simple client-server chat program. The server is able to handle multiple client connections simultaneously and allows clients to send public or private messages.
Clients can also change their nicknames, or disconnect from the server. The program also utilizes threading in the background to keep an updated list of connected users. 

**Project Goals**: Create a simple chat room that can be accessed by multiple clients connected by a single server. 

## Instructions for Build and Use

Steps to build and/or run the software:

1. have Python installed on your computer  
2. First run the server.py file  
3. Run the client.py file in one or more terminals

Instructions for using the software:

1. First make sure the server is already running
2. Run one of more client terminals to connect to the server
3. Follow the menu in the client terminal to send messages and do other actions

## Development Environment 

To recreate the development environment, you need the following software and/or libraries with the specified versions:

* VS Code
* Latest version of python

## Useful Websites to Learn More

I found these websites useful in developing this software:

* [Python Socket Programming Documentation](https://docs.python.org/3/library/socket.html)
* [Python Threading Documentation](https://docs.python.org/3/library/threading.html)
* [Build a Chatroom in python](https://www.scaler.in/build-a-chatroom-in-python/)
* [ChatGPT](https://chatgpt.com/)

## Future Work

The following items I plan to fix, improve, and/or add to this project in the future:

* [ ] Impelement non-blocking input so that messages can be recieved without problems
* [ ] Clean up the user interface to keep input and received messages seperate
* [ ] Add an admin role that allows forcefully disconnecting clients
