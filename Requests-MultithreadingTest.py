import threading
import requests
import time

def req(url,i):
	print(i+1,url)
	req=requests.get(url)
	file=open("/home/labtel/img{}.jpg".format(i+1),"wb")
	imagen=req.content
	file.write(imagen)
	file.close()

def get_req(urls,n,m):
	for i in range(n,m):
		req(urls[i],i)

def get_req_2threads(urls):
	thread1=threading.Thread(target=get_req,args=(urls,0,4))
	thread1.start()
	thread2=threading.Thread(target=get_req,args=(urls,4,7))
	thread2.start()
	thread1.join()
	thread2.join()

def get_req_7threads(urls):
	thread_list=[]
	for i in range(7):
		thread=threading.Thread(target=req,args=(urls[i],i))
		thread_list.append(thread)
	for i in range(7):
		thread_list[i].start()
	for i in range(7):
		thread_list[i].join()

def main():
	urls=[]
	for i in range(1,8):
		url="http://dev.ecm.energyatech.com:5000/maravillas/imagen{}".format(i)
		urls.append(url)

	print("Request sin threading iniciando . . .")
	start=time.time()
	get_req(urls,0,7)
	end=time.time()
	print("Request sin threading demora: {}s".format(end-start))

	print("Request con 2 threads iniciando . . .")
	start=time.time()
	get_req_2threads(urls)
	end=time.time()
	print("Request con 2 threads demora: {}s".format(end-start))


	print("Request con 7 threads iniciando . . .")
	start=time.time()
	get_req_7threads(urls)
	end=time.time()
	print("Request con 7 threads demora: {}s".format(end-start))

if __name__=="__main__":
	main()