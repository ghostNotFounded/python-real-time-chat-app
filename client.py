import socket
import pandas as pd
import os
import time

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
    try:
        send(DISCONNECT_MSG)
    except Exception as e:
        print("Error while sending disconnect message:", e)
    client.close()
    exit()


# Function to register a new user
def register():
    try:
        userData = pd.read_csv('db.csv')  # Read user data from CSV file
        usernames = userData['username']
        user = input('Enter a new username : ')
        
        # Check if the username is already taken
        if user in usernames.values:
            print("Username already exists. Please choose a different username.")
            return False

        password = input('Enter a password : ')
        
        # Create a new DataFrame with the new user data
        new_user_data = pd.DataFrame({'username': [user], 'password': [password]})
        
        # Concatenate the new DataFrame with the existing user data
        userData = pd.concat([userData, new_user_data], ignore_index=True)
        
        # Write the updated user data to the CSV file
        userData.to_csv('db.csv', index=False)
        
        print("Registration successful!")
        return True
    except KeyboardInterrupt:
        disconnect()
    except Exception as e:
        print("An error occurred during registration:", str(e))
        disconnect()



# Function to login with user authentication
def login():
    try:
        userData = pd.read_csv('db.csv', dtype={'password': str})  # Read user data from CSV file
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
    except KeyboardInterrupt:
        disconnect()
    except Exception as e:
        print("An error occurred during login:", str(e))
        disconnect()


# Prompt the user to choose between registering a new user or logging in as an existing user
while True:
    try:
        option = input("Are you a new user? (yes/no): ").lower()
        if option == "yes":
            while not register():
                time.sleep(1)
                os.system("cls")
            break
        elif option == "no":
            while not login():
                time.sleep(1)
                os.system("cls")
            break
        else:
            print("Invalid option. Please enter 'yes' or 'no'.")
    except KeyboardInterrupt:
        disconnect()

# Send messages to the server until disconnected
while True:
    try:
        text = input()
        if text.upper() == "DISCONNECT":
            disconnect()
        send(text)
    except KeyboardInterrupt:
        disconnect()
    except Exception as e:
        print("An error occurred:", str(e))
        disconnect()
