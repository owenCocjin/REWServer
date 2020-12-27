#!/usr/bin/python3
## Author:  Owen Cocjin
## Version: 1.2
## Date:    2020.12.22
## Description:  Main script
## Notes:
##    - This file creates the necessary pipes, if missing
## Update:
##    - Added pipes check
import serverdriver
import threading
import miscus.io
from progmenu import menu
from menuentries import *
from constants import GLOBE
from miscus.stringmisc import ctxt
from dataparser import AJAXThread
PARSE=menu.parse(True, strict=True)

#------------#
#    MAIN    #
#------------#
def main():
	print("<|X> Initializing pipes...")
	for p in GLOBE["PIPES"]:
		if miscus.io.checkPipe(f"{GLOBE['ROOT']}/{p}")==2:
			print(f"{ctxt(f'[|X{__name__}:main]:')} Error initializing pipes!")
			return 2
	print("<|X> Setting up socket...")
	serv_sock=serverdriver.socksetup(GLOBE["ADDR"], GLOBE["PORT"])
	print("<|X> Throwing AJAX parse into background...")
	AJAXThread("ajaxd", f"{GLOBE['ROOT']}/{GLOBE['PIPES'][0]}", f"{GLOBE['ROOT']}/{GLOBE['PIPES'][1]}")
	#Start all threads in GLOBE
	for t in GLOBE["THREADS"]:
		t.start()
	print(ctxt("<|X> Starting server...", bg=42))
	while True:
		serverdriver.sockprocess(serv_sock)

if __name__=="__main__":
	'''Error returns:
	1: General Error
	2: Error Initializing pipes'''
	try:
		errno=main()
		exit(errno)
	except KeyboardInterrupt as e:
		print("\033[K")
