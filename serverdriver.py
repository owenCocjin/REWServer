#!/usr/bin/python3
## Author:  Owen Cocjin
## Version: 1.1
## Date:    2020.12.22
## Description:  Manage the web server's socket connections
## Notes:
## Update:
##    - Included miscus for pipe handling
##    - Ensure appropriate messages are sent
##    - Changde htmlDirect's functionality slightly

import socket
import miscus.io
from typing import List, Dict
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
	print(f"\n{ctxt(f'[|X:{__name__}:sockprocess]:', 95)} Listening for connections...")
	cli_conn, cli_addr=sock.accept()
	print(f"<|X> {cli_addr[0]}:{cli_addr[1]} connected!")
	#Get request from client
	vprint(f"[|X:{__name__}:sockprocess]: Reading byte", end='')
	while True:
		vprint('\033[1D.', end='')
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
		vprint('\033[1D ', end='')

	vprint(f"\n[|X:{__name__}:sockprocess]: Got HTTP Header!")
	vprint(f"[|X:{__name__}:sockprocess]: HTTP Header:\n{cli_buffer}")
	#Get just the first line
	cli_header=cli_buffer.split('\n')
	cli_req=cli_header[0].split()
	print(f"<|X> Request: {cli_req}")
	#Send index.html
	if cli_req[0]=="GET":
		htmlDirect(cli_req[1], cli_conn)
	elif cli_req[0]=="POST":
		splithead=splitHeader(cli_header)
		htmlDirect(cli_req[1], cli_conn, splithead["Content-Length"])
	#Close connection
	vprint(f"{ctxt(f'[|X:{__name__}:sockprocess]:', 93)} Saying bye to {cli_addr}!")
	cli_conn.close()

def htmlDirect(location, cli_conn, contentsize=0):
	'''Sends the file for the requested file to the given client socket; 404 page otherwise.
	Reads contentsize bytes from cli_conn if contentsize>0'''
	if location=='/':  #Convert plain '/' to default html file
		location="/index.html"
	try:  #The fail will hopefully be with opening the file
		contentsize=int(contentsize)
		#if contentsize>0, assume POST request
		if contentsize==0 and location==f"/{GLOBE['PIPES'][0]}":
			#Send client error 411 "Length Required"
			vprint(f"{ctxt(f'[|X:{__name__}:htmlDirect]:', 31)} Requested pipe with no data!")
			cli_conn.send(b'HTTP/1.1 411 Length Required\r\n\r\n')
		elif contentsize>0 and location==f"/{GLOBE['PIPES'][0]}":
			vprint(f"[|X:{__name__}:htmlDirect]: Got POST request to pipe!")
			cli_body=cli_conn.recv(contentsize).decode()
			#Write the content data to pipe
			miscus.io.handlePipe(f"{GLOBE['ROOT']}/{GLOBE['PIPES'][0]}", cli_body)
			vprint(f"[|X:{__name__}:htmlDirect]: Wrote to pipe: {cli_body}")
			#Read data from pipe
			pipedata=miscus.io.handlePipe(f"{GLOBE['ROOT']}/{GLOBE['PIPES'][1]}")
			cli_conn.send(pipedata.encode("utf-8"))
		else:
			with open(f"{GLOBE['ROOT']}{location}", "br") as f:
				vprint(f"{ctxt(f'[|X:{__name__}:sockprocess]: ', 92)}Sending OK reply!")
				cli_conn.send(b'HTTP/1.1 200 OK\r\n\r\n')
				cli_conn.send(f.read())

	except FileNotFoundError as e:
		vprint(f"[|X:{__name__}:htmlDirect]: {ctxt('Bad page request!', 31)}")
		#Send back the bad request message!
		cli_conn.send(b'HTTP/1.1 404 Not Found\r\n\r\n')
		with open(f"{GLOBE['ROOT']}/pnf.html", "br") as f:
			cli_conn.send(f.read())

#--------------------#
#    HELPER FUNCS    #
#--------------------#
def splitHeader(header:List)->Dict:
	'''Splits a header (already split by line) up and returns a dict.
	Ex return: {"Content-length":30}'''
	toRet={}
	for line in header:
		splitloc=line.find(':')
		title=line[:splitloc].strip()
		content=line[splitloc+1:].strip()
		toRet[title]=content
	return toRet

if __name__=="__main__":
	try:
		main()
	except KeyboardInterrupt as e:
		print("\033[K")
