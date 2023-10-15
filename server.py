import socket
import sys
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
def init_server(PORT_NUMBER, key):
	key = pad(key.encode(), 16)
	#key = key.encode()

	# Create a socket
	serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

	# Associate the socket with the port
	serverSock.bind(('', PORT_NUMBER)) 

	# Start listening for incoming connections (we can have
	# at most 100 connections waiting to be accepted before
	# the server starts rejecting new connections)
	serverSock.listen(100)

	# Keep accepting connections forever
	while True:
		
		print("Waiting for clients to connect...")
		
		# Accept a waiting connection
		cliSock, cliInfo = serverSock.accept()
		
		print("Client connected from: " + str(cliInfo))
		
		# Receive the data the client has to send.
		nonce = cliSock.recv(16)
		tag = cliSock.recv(16)
		ciphertext = cliSock.recv(1024)

		# Decrypt the Message
		cipher = AES.new(key, AES.MODE_EAX, nonce)
		msg = cipher.decrypt_and_verify(ciphertext, tag)

		# Print Decrypted message
		print("Received msg " + msg.decode())
		
		# Hang up the client's connection
		cliSock.close()

if __name__ == "__main__":
	if len(sys.argv) != 3:
		print("Usage: python server.py <port number> <key>")
		sys.exit(1)

	PORT_NUMBER = int(sys.argv[1])
	key = sys.argv[2]
	init_server(PORT_NUMBER, key)