#!/usr/bin/python3
## Author:  Owen Cocjin
## Version: 0.2
## Date:    2020.12.27
## Description:  Parse incoming data from cts.bridge
## Notes:
##    - Parses POST data and writes it back to the same pipe
## Update:
##    - Added percent encoding for &
import threading, time, random
import miscus.io
from progmenu import menu
from constants import GLOBE

vprint=menu.verboseSetup(['v', "verbose"])

class AJAXThread(threading.Thread):
	'''Creates a thread for AJAX parser'''
	def __init__(self, name, p_in, p_out):
		threading.Thread.__init__(self, daemon=True)
		self.name=name
		self.p_in=p_in
		self.p_out=p_out
		self.post_data={}
		self.command="command_data"  #keyword to send to tool from POST data
		GLOBE["THREADS"].append(self)

	def run(self):
		vprint(f"[|X:{__name__}:AJAXThread]: {self.name} started!")
		while True:
			self.post_data.clear()
			#Read pipe and parse data
			vprint(f"[|X:{__name__}:AJAXThread]: Reading from pipe")
			pipedata=miscus.io.handlePipe(self.p_in)
			vprint(f"[|X:{__name__}:AJAXThread]: Read: {pipedata}")
			#Go through each line and add data to post_data
			for line in pipedata.split('&'):
				firstpos=line.find('=')
				self.post_data[line[:firstpos]]=line[firstpos+1:]

			#Find command_data and print it
			if self.command in self.post_data:
				cmd=self.post_data[self.command]
				#Revert percent encoded data to original char
				cmd=cmd.replace("%26", '&')
				print(f"<|X> Got command: {cmd}", flush=True)
				miscus.io.handlePipe(self.p_out, f"<p>{cmd}: {random.randint(0, 10)}</p>")
			else:  #Return blank code
				miscus.io.handlePipe(self.p_out, "nocmd")
