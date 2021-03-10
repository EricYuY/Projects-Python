import socket
import time
import threading


Datos_potencia=[]
MAX_POT=0
flag=False

def thread1():
	global Datos_potencia
	msg="GET"
	msgb=msg.encode()
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.connect(("192.168.35.137", 5000))
		while True:
			time.sleep(2)
			s.sendall(msgb)
			data=s.recv(1024)
			dataDec=int.from_bytes(data,"big")
			print("Dato:   ",dataDec)
			Datos_potencia.append(dataDec)



def thread2():
	global flag
	global MAX_POT
	global Datos_potencia
	while True:
		time.sleep(2)
		maximo=max(Datos_potencia, default=0)
		if maximo>MAX_POT:
			MAX_POT=maximo
			flag=True

def thread3():
	global flag
	global MAX_POT
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.connect(("192.168.35.150", 5000))
		while True:
			time.sleep(2)
			PotenciaMaxb=bytes(MAX_POT)
			if flag==True:
				print("MAXIMO: ",MAX_POT)
				s.sendall(PotenciaMaxb)
				flag=False


def main():
	T1=threading.Thread(target=thread1,args=())
	T1.start()
	T2=threading.Thread(target=thread2,args=())
	T2.start()
	T3=threading.Thread(target=thread3,args=())
	T3.start()

	T1.join()
	T2.join()
	T3.join()
if __name__=="__main__":
	main()