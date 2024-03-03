import socket
import threading

# Define the fixed header size for messages
HEADER = 64
# Define the port number for communication
PORT = 5050
# Get the IP address of the local machine dynamically
SERVER = socket.gethostbyname(socket.gethostname())
# Tuple containing the server address and port
ADDR = (SERVER, PORT)
# Define the encoding format for messages
FORMAT = "utf-8"
# Define the message to disconnect a client
DISCONNECT_MSG = "!DISCONNECT"

# Create a socket object for IPv6 communication (AF_INET6) and TCP protocol (SOCK_STREAM)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the server socket to the specified address and port
server.bind(ADDR)

# Function to handle each client connection
def handleClient(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    
    # Flag to control the connection loop
    connected = True
    try:
        while connected:
            # Receive the message length from the client
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                # Convert message length to integer
                msg_length = int(msg_length)
                if (msg_length):
                    # Receive the actual message from the client
                    msg = conn.recv(msg_length).decode(FORMAT)
                    # Check if the client requested disconnection
                    if msg == DISCONNECT_MSG:
                        connected = False
                    # Print the received message
                    print(f"[{addr}] {msg}")
    except Exception as e:
        print(f"An error occurred with client {addr}: {e}")
    finally:
        # Close the connection with the client
        conn.close()
        print(f"[DISCONNECTED] {addr} disconnected.")

# Function to start the server and handle incoming connections
def start():
    # Begin listening for incoming connections
    server.listen()
    print(f"[SERVER STARTED] Waiting for connections on {SERVER}")
    try:
        while True:
            # Accept a new connection
            conn, addr = server.accept()
            # Start a new thread to handle the client connection
            thread = threading.Thread(target=handleClient, args=(conn, addr))
            thread.start()
            # Print the number of active connections
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
    except KeyboardInterrupt:
        print("[INTERRUPTED] Server interrupted. Shutting down...")
        server.close()

# Main entry point of the program
if __name__ == "__main__":
    print("[STARTING] Server is starting...")
    # Start the server
    start()
