# Echo client program
import socket
import sys, getopt
from time import strftime, gmtime
import time
import termios
import fcntl
import os 

helpmsg = '''
OPTIONS:
-c		Continuous echo mode.
-h		Display the available options
-ip IPADD	Specify the server IP Address
-t TCP/UDP	Specify the transport layer protocol.
-v		Print the software version
''';
version = 'version1.0'
HOST = '127.0.0.1'
protocol = 'TCP'
continouos = False 
PORT = 4002
debug = 0
sendstr = ""
prompt=">"
time_sleep = 0

############################################################################
def main(argv):
	inputfile = ''
	outputfile = ''
	global protocol
	global HOST
	global continouos
	
	try:
		opts, args = getopt.getopt(argv,"hvct:ip:",["ifile=","ofile=","ip="])
	except getopt.GetoptError:
		print sys.argv[0]+' opcion no reconocida'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print helpmsg
			sys.exit()
		elif opt == "-v":
			print  sys.argv[0]+" "+version
			sys.exit()
		elif opt == "-c":
			continouos = True
			print  "continouos "
		elif opt in ("-t"):
			protocol = arg
			if protocol == "TCP":
				print "protocolo "+arg
			elif protocol == "UDP":
				print "protocolo "+arg
			else:
				print "Wrong Protocol "+arg
				sys.exit()
		elif opt in ("-ip", "--ip", "ip"):
			HOST = arg
			#HOST = sys.argv[2]
			print  HOST+" "+version
############################################################################
#Function to receive from the socket
def receive():
	time.sleep(time_sleep) #Pause to make sure you don't receive too fast
	rec = s.recv(1024) #Receive data from socket
	return rec
############################################################################
#Function to send a command to the socket	
def send(str):
	s.sendall(str) #Send string with line return
############################################################################
def tcpClient():
	global HOST
	global PORT
	global sendstr
	global s
	
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((HOST, PORT))

	while sendstr.startswith("quit")==False:
		sys.stdout.write(prompt)		 #Set up the prompt
		sendstr = sys.stdin.readline() #read command
		send(sendstr)
		rec = receive()

		sys.stdout.write (">ECHO:"+rec)
############################################################################
def tcpClientContinouos():
	global HOST
	global PORT
	global sendstr
	global s
	
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((HOST, PORT))
	while True:
		c = myGetch()
		sys.stdout.write (c)
		send(c)
		rec = receive()
		sys.stdout.write (rec)
		
############################################################################
def udpClient():
	global HOST
	global PORT
	global sendstr
	global s
	
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	while sendstr.startswith("quit")==False:
		sys.stdout.write(prompt)		 #Set up the prompt
		sendstr = sys.stdin.readline() #read command
		d = s.sendto(sendstr, (HOST, PORT))
		
		# receive data from client (data, addr)
		d = s.recvfrom(1024)
		rec  = d[0]
		addr = d[1]
		
		
		sys.stdout.write (">ECHO:"+rec)
############################################################################
def udpClientContinouos():
	global HOST
	global PORT
	global sendstr
	global s
	
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	
	while True:
		c = myGetch()
		sys.stdout.write (c)
		d = s.sendto(c, (HOST, PORT))
		# receive data from client (data, addr)
		d = s.recvfrom(1024)
		rec  = d[0]
		addr = d[1]
		sys.stdout.write (rec)
		
############################################################################
def myGetch():
    fd = sys.stdin.fileno()

    oldterm = termios.tcgetattr(fd)
    newattr = termios.tcgetattr(fd)
    newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
    termios.tcsetattr(fd, termios.TCSANOW, newattr)

    oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

    try:        
        while 1:            
            try:
                c = sys.stdin.read(1)
                break
            except IOError: pass
    finally:
        termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
        fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
	return c
############################################################################

if __name__ == "__main__":
	main(sys.argv[1:])

if protocol == "TCP":
	if continouos == False:
		tcpClient()
	else:
		tcpClientContinouos()
elif protocol == "UDP":
	if continouos == False:
		udpClient()
	else:
		udpClientContinouos()