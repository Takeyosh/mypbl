# -*- coding: utf-8 -*-
# client.py

from socket import *
import time
import sys
import pbl2018

def SIZE(client, fn):
	
	client.send(('SIZE ' + fn + "\n").encode())		
	message = client.recv(1024).decode().split()
	if message[0] == 'OK':
		return int(message[2])
	elif message[1] == 101 :
		print('Please change the file name.\n')
		sys.exit()
	else :
		print('Please rewrite the command.\n') 
		sys.exit()

def GET(client, fn, fs, gd):
	message = "GET" + fn + " " + gd + " ALL\n"
	client.send(message.encode())
	recv_bytearray = bytearray()
	while True:
		b = client.recv(1)
		if b == b'\n':
			data = client.recv(int(fs))
	return data
	
def REP(client, fn, dig):
	
	client.send('REP ' + fn + ' ' + dig).encode()
	message = client.recv(1024).decode().split()
	if message[0] == 'OK':
		print('Tile transfer finished: Transmission time: {0}'.format(float(message[9]))) 
	elif message[1] == 101 :
		print('Please change the file name.\n')
		sys.exit()
	elif message[1] =='103':
		print('Failed to receive file data.\n')
		sys.exit()
	else :
		print('Please rewrite the command.\n') 
		sys.exit()


if __name__ == '__main__':
	# main program
	server_name = sys.argv[1]	
	server_port = int(sys.argv[2])	
	file_name = sys.argv[3]		
	token_str = sys.argv[4]		
	genkey_data = pbl2018.genkey(token_str)
	client_socket = socket(AF_INET, SOCK_STREAM)
	client_socket.connect((server_name, server_port))
	
	file_size = SIZE(client_socket, file_name)	
	
	file_data = GET(client_socket, file_name, file_size, genkey_data)
	
	digest = pbl2018.repkey(token_str, file_name)	
	
	REP(client_socket, file_name, digest)
