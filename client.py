import socket
import pandas as pd

# Define constants for communication
HEADER = 64
PORT = 5050
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"
ADDR = (socket.gethostbyname(socket.gethostname()), PORT)  # Get IP address dynamically

# Create a socket and connect to the server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

print("[CONNECTED] You can type in a message to send to the user, enter 'DISCONNECT' to terminate your connection")


# Function to send a message to the server
def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    

# Function to disconnect from the server
def disconnect():
    print("Disconnecting...")
    send(DISCONNECT_MSG)
    client.close()
    exit()


# Function to login with user authentication
def login():
    try:
        # Read user data from CSV file
        userData = pd.read_csv('db.csv', dtype={'password': str})  # Specify password column as string
        usernames = userData['username']
        passwords = userData['password']

        user = input('Username : ')
        
        # Check if the username exists in the dataframe
        if user not in usernames.values:
            print("User does not exist. Please create an account to proceed!")
            return False

        # Get the index of the user in the dataframe
        user_index = usernames[usernames == user].index[0]

        # Retrieve the password corresponding to the entered username
        actual_password = passwords[user_index]

        # Prompt for password and check if it matches the actual password
        password = input('Password : ')
        if password.strip() == str(actual_password).strip():  # Convert actual_password to string
            print('Login successful!')
            return True
        else:
            print('Incorrect password!')
            return False
    except Exception as e:
        print("An error occurred during login:", str(e))
        disconnect()


# Perform login until successful
while not login():
    pass

# Send messages to the server until disconnected
while True:
    try:
        text = input()
        if text.upper() == "DISCONNECT":
            disconnect()
        send(text)
    except Exception as e:
        print("An error occurred:", str(e))
        disconnect()
