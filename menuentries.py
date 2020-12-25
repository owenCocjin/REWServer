## Author:  Owen Cocjin
## Version: 0.1
## Date:    2020.12.22
## Description:  holds Menu Entry data
## Notes:
##    - Very few of these entries validate args
from progmenu import EntryArg, MenuEntry
from constants import GLOBE

def addrFunc(addr):
	'''Sets & returns address'''
	str(addr)
	GLOBE["ADDR"]=addr
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
	'''Sets & Returns port if it can be converted to an int'''
	try:
		port=int(port)
		GLOBE["PORT"]=port
		return port
	except:
		return None

def rootFunc(root):
	'''Sets & returns root for HTML'''
	GLOBE["ROOT"]=root
	return root

EntryArg("addr", ['a', "addr"], addrFunc)
MenuEntry("helper", ['h', "help"], helpFunc, 0)
EntryArg("port", ['p', "port"], portFunc)
EntryArg("root", ['r', "root"], rootFunc)
