import socket
import sys
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

def init_client(SERVER_IP, SERVER_PORT, key):
    key = pad(key.encode(), 16)
    #key = key.encode()
    # The client's socket
    cliSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Define the message to be sent to the server
    msg = input("Please enter a message to send to the server: ")
    
    # Encrypt the message
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(msg.encode())

    # Attempt to connect to the server
    cliSock.connect((SERVER_IP, SERVER_PORT))

    # Send the message to the server
    # NOTE: the user input is of type string
    # Sending data over the socket requires.
    # First converting the string into bytes.
    # encode() function achieves this.
    cliSock.send(cipher.nonce)
    cliSock.send(tag)
    cliSock.send(ciphertext)
	
if __name__ == "__main__":
	if len(sys.argv) != 4:
		print("Usage: python client.py <server ip> <server port> <key>")
		sys.exit(1)

	SERVER_IP = sys.argv[1]
	SERVER_PORT = int(sys.argv[2])
	key = sys.argv[3]
	init_client(SERVER_IP, SERVER_PORT, key)