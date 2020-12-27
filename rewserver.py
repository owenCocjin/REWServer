#!/usr/bin/python3
## Author:  Owen Cocjin
## Version: 1.1
## Date:    2020.12.22
## Description:  Main script
## Notes:
## Update:
##    - Added threading
##    - Now runs AJAXThread (which is a daemon)
import serverdriver
import threading
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
	try:
		main()
	except KeyboardInterrupt as e:
		print("\033[K")
