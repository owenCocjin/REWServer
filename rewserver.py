#!/usr/bin/python3
## Author:  Owen Cocjin
## Version: 0.2
## Date:    2020.12.22
## Description:  Main script
## Notes:
import serverdriver
from progmenu import menu
from menuentries import *
from constants import GLOBE
from miscus.stringmisc import ctxt
PARSE=menu.parse(True, strict=True)

#------------#
#    MAIN    #
#------------#
def main():
	print("<|X> Setting up socket...")
	serv_sock=serverdriver.socksetup(GLOBE["ADDR"], GLOBE["PORT"])
	print(ctxt("<|X> Starting server...", bg=42))
	while True:
		serverdriver.sockprocess(serv_sock)


if __name__=="__main__":
	try:
		main()
	except KeyboardInterrupt as e:
		print("\033[K")
