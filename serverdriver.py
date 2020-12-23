#!/usr/bin/python3
## Author:  Owen Cocjin
## Version: 0.1
## Date:    2020.12.18
## Description:  Manage the web server's socket connections
## Notes:

import socket
from constants import *
from progmenu import menu
vprint=menu.verboseSetup(['v', "verbose"], prefix=f"[|X:{__name__}]:")

#---------------#
#    SOCKETS    #
#---------------#
def socksetup(addr, port):
	'''Sets up socket'''
	vprint("socksetup: Setting up socket...")
	serv_sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
	serv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  #Allow address reuse
	serv_sock.bind((addr, port))
	serv_sock.listen(5)
	vprint(f"socksetup: Socket setup on {[addr, port]}!")
	return serv_sock

def sockprocess(sock):
	'''Manages socket processing, such as accepting connections, redirections, etc...'''
	cli_buffer=''
	vprint("sockprocess: Listening for connections...")
	cli_conn, cli_addr=sock.accept()
	print(f"<|X> {cli_addr} connected!")
	#Get request from client
	while True:
		justgot=cli_conn.recv(1)
		#vprint(f"sockprocess: Byte got: {justgot} ({justgot.hex()})")
		if justgot.hex()=='0d':  #Read the next 3 bytes, stop if they are '\n\r\n'
			vprint("socprocess: Testing for EOM...")
			getthree=cli_conn.recv(3)
			cli_buffer+=getthree.decode()
			if getthree.hex()=='0a0d0a':  #Completes the HTTP end of message; break if so
				cli_buffer+='\n'  #For later parsing completion
				break
			vprint("sockprocess: Continuing...")
		else:
			cli_buffer+=justgot.decode()

	print(f"<|X> Got HTTP Header!")
	vprint(f"sockprocess: HTTP Header:\n{cli_buffer}")
	#Get just the first line
	cli_header=cli_buffer.split('\n')
	cli_req=cli_header[0].split()
	print(f"<|X> Request: {cli_req}")
	#Send back the OK message!
	cli_conn.send(b'HTTP/1.1 200 OK\r\n\r\n')
	#Send index.html
	htmlDirect(cli_req[1], cli_conn)
	#Close connection
	print(f"<|X> Saying bye to {cli_addr}!")
	cli_conn.close()

def htmlDirect(location, cli_sock):
	'''Sends the file for the requested file to the given client socket; 404 page otherwise'''
	if location=='/':
		location="/index.html"
	try:
		with open(f"{ROOT}{location}", "br") as f:
			cli_sock.send(f.read())
	except FileNotFoundError as e:
		vprint("htmlDirect: Bad page request!")
		with open(f"{ROOT}/pnf.html", "br") as f:
			cli_sock.send(f.read())

if __name__=="__main__":
	try:
		main()
	except KeyboardInterrupt as e:
		print("\033[K")
