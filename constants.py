#!/usr/bin/python3
## Author:  Owen Cocjin
## Version: 0.2
## Date:    2020.12.26
## Description:  Uses a dict named "GLOBE" to manage constants
## Notes:
##    - GLOBE is a dict used for globals that may change across all files
##    - You can include normal globals as their own variables, but don't change them!
## Update Notes:
GLOBE={
"ADDR":"0.0.0.0",
"PIPES":["AJAX/cts.bridge", "AJAX/stc.bridge"],  #[client to server, server to client]
"PORT":8080,
"ROOT":"HTML",
"THREADS":[]}
