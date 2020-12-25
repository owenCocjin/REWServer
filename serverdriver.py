#!/usr/bin/python3
## Author:  Owen Cocjin
## Version: 1.0
## Date:    2020.12.22
## Description:  Manage the web server's socket connections
## Notes:

import socket
from constants import GLOBE
from progmenu import menu
from miscus.stringmisc import ctxt
vprint=menu.verboseSetup(['v', "verbose"])

#---------------#
#    SOCKETS    #
#---------------#
def socksetup(addr, port):
	'''Sets up socket'''
	vprint(f"[|X:{__name__}:socksetup]: Setting up socket...")
	serv_sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
	serv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  #Allow address reuse
	serv_sock.bind((addr, port))
	serv_sock.listen(5)
	vprint(f"[|X:{__name__}:socksetup]: Socket setup on {[addr, port]}!")
	return serv_sock

def sockprocess(sock):
	'''Manages socket processing, such as accepting connections, redirections, etc...'''
	cli_buffer=''
	vprint(f"[|X:{__name__}:sockprocess]: Listening for connections...")
	cli_conn, cli_addr=sock.accept()
	print(ctxt(f"<|X> {cli_addr[0]}:{cli_addr[1]} connected!", 30, 102))
	#Get request from client
	while True:
		justgot=cli_conn.recv(1)
		#vprint(f"sockprocess: Byte got: {justgot} ({justgot.hex()})")
		if justgot.hex()=='0d':  #Read the next 3 bytes, stop if they are '\n\r\n'
			#vprint("socprocess: Testing for EOM...")
			getthree=cli_conn.recv(3)
			cli_buffer+=getthree.decode()
			if getthree.hex()=='0a0d0a':  #Completes the HTTP end of message; break if so
				cli_buffer+='\n'  #For later parsing completion
				break
			#vprint("sockprocess: Continuing...")
		else:
			cli_buffer+=justgot.decode()

	vprint(f"[|X:{__name__}:sockprocess]: Got HTTP Header!")
	vprint(f"[|X:{__name__}:sockprocess]: HTTP Header:\n{cli_buffer}")
	#Get just the first line
	cli_header=cli_buffer.split('\n')
	cli_req=cli_header[0].split()
	print(f"<|X> Request: {cli_req}")
	#Send index.html
	htmlDirect(cli_req[1], cli_conn)
	#Close connection
	vprint(ctxt(f"[|X:{__name__}:sockprocess]: Saying bye to {cli_addr}!", bg=43), end="\n\n")
	cli_conn.close()

def htmlDirect(location, cli_sock):
	'''Sends the file for the requested file to the given client socket; 404 page otherwise'''
	if location=='/':  #Convert plain '/' to default html file
		location="/index.html"
	try:  #The fail will be with opening the file
		with open(f"{GLOBE['ROOT']}{location}", "br") as f:
			vprint(f"[|X:{__name__}:sockprocess]: Sending replies")
			cli_sock.send(b'HTTP/1.1 200 OK\r\n\r\n')
			cli_sock.send(f.read())
	except FileNotFoundError as e:
		vprint(f"[|X:{__name__}:htmlDirect]: {ctxt('Bad page request!', 31)}")
		#Send back the bad request message!
		cli_sock.send(b'HTTP/1.1 404 Not Found\r\n\r\n')
		with open(f"{GLOBE['ROOT']}/pnf.html", "br") as f:
			cli_sock.send(f.read())

if __name__=="__main__":
	try:
		main()
	except KeyboardInterrupt as e:
		print("\033[K")
