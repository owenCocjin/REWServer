#!/usr/bin/python3
## Author:  Owen Cocjin
## Version: 0.1
## Date:    2020.12.18
## Description:  Main script
## Notes:
import serverdriver
from progmenu import menu
from menuentries import *
from constants import *
PARSE=menu.parse(True, strict=True)

#------------#
#    MAIN    #
#------------#
def main():
	print("<|X> Setting up socket...")
	serv_sock=serverdriver.socksetup(ADDR, PORT)
	print("<|X> Starting server...")
	while True:
		serverdriver.sockprocess(serv_sock)
		print()


if __name__=="__main__":
	try:
		main()
	except KeyboardInterrupt as e:
		print("\033[K")
