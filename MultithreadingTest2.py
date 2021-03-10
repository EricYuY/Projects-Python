import subprocess
import threading
import time

def  ping_computer(ip_address):

	response = subprocess.call(['ping', '-c', '4', '-W', '1', ip_address], stdout=open('/dev/null', 'w'))

	if(response == 0):
		print("Sucess from IP: {}".format(ip_address))

def ping_NoThread(ip_list):
	for i in range(256):
		ping_computer(ip_list[i])
				

def ping_Thread(ip_list):
	thread_list=[]
	for i in range(256):
		thread=threading.Thread(target=ping_computer,args=(ip_list[i],))
		thread_list.append(thread)
	for i in range(256):
		thread_list[i].start()
	for i in range(256):
		thread_list[i].join()
	


def main():
	ip_list=[]
	for i in range(256):
		ip_address="192.168.0.{}".format(i)
		ip_list.append(ip_address)

	print("Comenzando Ping CON threading . . .")
	start=time.time()
	ping_Thread(ip_list)
	end=time.time()
	print("Ping CON threading demora: {} s".format(end-start))

	print("Comenzando Ping SIN threading . . .")
	start=time.time()
	ping_NoThread(ip_list)
	end=time.time()
	print("Ping SIN threading demora: {} s".format(end-start))
		
if __name__=="__main__":
	main()