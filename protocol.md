# Protocol for communicating with server
The protocol for communicating with the server to get printer info or contact discord is very basic. Its a simple TCP protocol with a varying number of uint bytes for each call and sometimes json. 
## First byte
The first byte sent signifies if you want the server to check the bot connection, get printer/job information, add a printer/job, 
