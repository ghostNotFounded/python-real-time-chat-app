import socket
import pandas as pd
import os
import time

import hashlib  # Import hashlib module for hashing

# Function to register a new user
def register():
    userData = pd.read_csv('db.csv')  # Read user data from CSV file
    usernames = userData['username']
    user = input('Enter a new username : ')
    
    # Check if the username is already taken
    if user in usernames.values:
        print("Username already exists. Please choose a different username.")
        return False

    password = input('Enter a password : ')
        
    # Hash the password before storing it
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    # Create a new DataFrame with the new user data
    new_user_data = pd.DataFrame({'username': [user], 'password': [hashed_password]})
        
    # Concatenate the new DataFrame with the existing user data
    userData = pd.concat([userData, new_user_data], ignore_index=True)
        
    # Write the updated user data to the CSV file
    userData.to_csv('db.csv', index=False)
        
    print("Registration successful!")
        
    return user  # Return the username

# Function to login with user authentication
def login():
        userData = pd.read_csv('db.csv')  # Read user data from CSV file
        usernames = userData['username']

        user = input('Username : ')
        
        # Check if the username exists in the dataframe
        if user not in usernames.values:
            print("User does not exist. Please create an account to proceed!")
            return False

        password = input('Password : ')
        
        # Hash the entered password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Get the index of the user in the dataframe
        user_index = usernames[usernames == user].index[0]

        # Retrieve the hashed password corresponding to the entered username
        actual_hashed_password = userData['password'][user_index]

        # Check if the entered hashed password matches the actual hashed password
        if hashed_password == actual_hashed_password:
            print('Login successful!')
            return user  # Return the username
        else:
            print('Incorrect password!')
            return False

        
codeplain = "user"
code = hashlib.sha256(codeplain.encode()).hexdigest()

# Define constants for communication
HEADER = 64
PORT = 5050
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"
ADDR = (socket.gethostbyname(socket.gethostname()), PORT)  # Get IP address dynamically

# Create a socket and connect to the server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

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
    
print(code)

# Prompt the user to choose between registering a new user or logging in as an existing user
while True:
    try:
        option = input("Are you a new user? (yes/no): ").lower()
        user = ""
        
        while not user:
            if option == "yes":
                user = register()
                if user:
                    send(f"{code}{user}")
            elif option == "no":
                user = login()
                if user:
                     send(f"{code}{user}")
            else:
                print("Invalid option. Please enter 'yes' or 'no'.")
            time.sleep(2)
            os.system("cls")
        break
    except KeyboardInterrupt:
        disconnect()

# Send messages to the server until disconnected
while True:
    try:
        print("[CONNECTED] You can start typing messages to send, send 'DISONNECT' to disconnect from the server, 'LISTUSERS' to list all online users and 'STEALCOW' for a surprise")
        
        text = input()
        if text.upper() == "DISCONNECT":
            disconnect()
            os.system("cls")
        send(text)
        os.system("cls")
    except KeyboardInterrupt:
        disconnect()
    except Exception as e:
        print("An error occurred:", str(e))
        disconnect()
