import socket

# Define the fixed header size for messages
HEADER = 64
# Define the port number for communication
PORT = 5050
# Get the IP address of the local machine dynamically
SERVER = socket.gethostbyname(socket.gethostname())
# Define the encoding format for messages
FORMAT = "utf-8"
# Define the message to disconnect a client
DISCONNECT_MSG = "!DISCONNECT"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    
send("Hello World")
    