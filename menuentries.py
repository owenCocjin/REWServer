## Author:  Owen Cocjin
## Version: 0.1
## Date:    2020.12.22
## Description:  holds Menu Entry data
## Notes:
from progmenu import EntryArg, MenuEntry

def addrFunc(addr):
	'''Returns address'''
	return addr

def helpFunc():
	'''Prints help'''
	print("""  REWServer [-ahp]:
\tReverse Engineering Web Server
\t  -a, --addr=0.0.0.0 | Set server address
\t  -h, --help         | Prints this page
\t  -p, --port=8080    | Set server port""")
	exit(0)

def portFunc(port):
	'''Returns port if it can be converted to an int'''
	try:
		return int(port)
	except:
		return None

addr=EntryArg("addr", ['a', "addr"], addrFunc)
helper=MenuEntry("helper", ['h', "help"], helpFunc, 0)
port=EntryArg("port", ['p', "port"], portFunc)
