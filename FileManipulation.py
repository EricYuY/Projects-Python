import requests
import time
from datetime import datetime, timedelta
import threading
from multiprocessing import Pool
from itertools import repeat


def format_line(line):
    l= line.split(",")
    lista = []
    for i in range(len(l)):
        if i>=1:
            if i == len(l)-1:
                l[i] = l[i][:len(l[i])-1] #Quita \n
            num = float(l[i])
            lista.append(num)
        elif i==0:
            temp=l[0].split(" ")
            lista.append(temp[0])
            lista.append(temp[1])
    return lista

def download(url):
    req=requests.get(url)
    file=open("/home/labtel/Documentos/20170903/household.csv","w")
    content=req.text
    file.write(content)
    file.close

def get_cols(content):
    a=content[0].split(",")
    a[8] = a[8][:len(a[8])-1]
    return a

def get_day(lista,fecha):
    datos=[]
    for i in range(len(lista)):
        if fecha == lista[i][0]:
            datos.append(lista[i][2:10])
    return datos

def get_mean(lista,fecha):
    prom=0
    n=0
    for i in range(len(lista)):
        if fecha == lista[i][0]:
            prom=prom+lista[i][2]
            n=n+1
    return prom/n

def get_max(lista,fecha):
    potencias=[]
    n=0
    for i in range(len(lista)):
        if fecha == lista[i][0]:
            potencias.append(lista[i][2])
    maximo=max(potencias)
    for i in range(len(lista)):
        if maximo== lista[i][2] and fecha == lista[i][0]:
            hora_max=lista[i][1]
    datos={"potencia":maximo,"hora":hora_max}
    return datos

def get_min(lista,fecha):
    potencias=[]
    n=0
    for i in range(len(lista)):
        if fecha == lista[i][0]:
            potencias.append(lista[i][2])
    minimo=min(potencias)
    for i in range(len(lista)):
        if minimo== lista[i][2] and fecha == lista[i][0]:
            hora_min=lista[i][1]
    datos={"potencia":minimo,"hora":hora_min}
    return datos

def gen_day_dict(fecha_inicio,fecha_fin,lista):
    flag=False
    dates=[]
    i=0
    #Analizando los dias que hay en el rango
    while flag==False:
        fecha_temp = (datetime.strptime(fecha_inicio, '%Y-%m-%d') + timedelta(days=i)).strftime('%Y-%m-%d')
        if fecha_temp==fecha_fin:
            flag=True
        dates.append(fecha_temp)
        i=i+1
    #print("Dias:",dates)
    temp=[]
    datos={}
    #Calculando diccionario
    for i in dates:
        for j in range(len(lista)):
            if i==lista[j][0]:
                temp.append(lista[j][2:10])
        datos[i]=temp
        temp=[]
    return datos

def get_exec_time_a(url):
    repeticiones=10
    t0=time.time()
    for i in range(repeticiones):
        download(url)
    return (time.time()-t0)*1000000/repeticiones

def get_exec_time_b(lista):
    fecha_inicio="2007-12-23"
    fecha_fin="2008-01-23"
    t0=time.time()
    resultado=gen_day_dict(fecha_inicio,fecha_fin,lista)
    return (time.time()-t0)*1000000

def hilo_gen_day_dict(date,lista,datos):
    temp=[]
    for j in range(len(lista)):
            if date==lista[j][0]:
                temp.append(lista[j][2:10])
    datos[date]=temp

def gen_day_dict_threaded(fecha_inicio,fecha_fin,lista):
    flag=False
    dates=[]
    datos={}
    thread_list=[]
    i=0
    #Analizando los dias que se encuentran en el rango
    while flag==False:
        fecha_temp = (datetime.strptime(fecha_inicio, '%Y-%m-%d') + timedelta(days=i)).strftime('%Y-%m-%d')
        if fecha_temp==fecha_fin:
            flag=True
        dates.append(fecha_temp)
        i=i+1
    #Enviando por 1 dia por thread
    for i in dates:
        thread=threading.Thread(target=hilo_gen_day_dict,args=(i,lista,datos))
        thread_list.append(thread)
    for i in range(len(dates)):
        thread_list[i].start()
    for i in range(len(dates)):
        thread_list[i].join()
    return datos

def multiproc_gen_day_dict(date,lista):
    temp=[]
    for j in range(len(lista)):
            if date==lista[j][0]:
                temp.append(lista[j][2:10])
    datos=temp
    return datos

def gen_day_dict_multi(fecha_inicio,fecha_fin,lista):
    flag=False
    dates=[]
    datos={}
    thread_list=[]
    i=0
    #Analizando los dias que se encuentran en el rango
    while flag==False:
        fecha_temp = (datetime.strptime(fecha_inicio, '%Y-%m-%d') + timedelta(days=i)).strftime('%Y-%m-%d')
        if fecha_temp==fecha_fin:
            flag=True
        dates.append(fecha_temp)
        i=i+1
    joined_vector=zip(dates,repeat(lista))
    p=Pool()
    result_datos=p.starmap(multiproc_gen_day_dict,joined_vector)
    p.close()
    p.join()
    for i in range(len(result_datos)):
        datos[dates[i]]=result_datos[i]
    return datos

def calc_speedup_e(lista):
    fecha_inicio="2007-12-16"
    fecha_fin="2007-12-18"
    #Tiempo normal
    t0=time.time()
    resultado1=gen_day_dict(fecha_inicio,fecha_fin,lista)
    tiempo_dict=(time.time()-t0)*1000000
    print(tiempo_dict,"s")

    #Tiempo thread
    t0=time.time()
    resultado2=gen_day_dict_threaded(fecha_inicio,fecha_fin,lista)
    tiempo_threaded=(time.time()-t0)*1000000
    print(tiempo_threaded,"s")

    #Tiempo multi
    t0=time.time()
    resultado3=gen_day_dict_multi(fecha_inicio,fecha_fin,lista)
    tiempo_multi=(time.time()-t0)*1000000
    print(tiempo_multi,"s")

    SpeedUpThread=tiempo_dict/tiempo_threaded
    SpeedUpMulti=tiempo_dict/tiempo_multi
    print("SpeedUp de operacion con hilos {}".format(SpeedUpThread))
    print("SpeedUp de operacion con multiprocessing {}".format(SpeedUpMulti))

def calc_stats(fecha_inicio,fecha_fin,lista):
    flag=False
    dates=[]
    i=0
    #Analizando los dias que hay en el rango
    while flag==False:
        fecha_temp = (datetime.strptime(fecha_inicio, '%Y-%m-%d') + timedelta(days=i)).strftime('%Y-%m-%d')
        if fecha_temp==fecha_fin:
            flag=True
        dates.append(fecha_temp)
        i=i+1
    #print("Dias:",dates)
    maximos=[]
    for i in range(len(dates)):
        maximos.append(get_max(dates[i],listas)

def main():
 	pass main():
    #Descargar archivo
    url="https://jobenas-misc-bucket.mda.amazonaws.com/household_power_consumption.csv"
    print("Descargando archivo . . . ")
    #tiempo=get_exec_time_a(url)
    #print("Duracion de la descarga fue: {} us".format(tiempo))
    #Calculo tamano
    i=0
    file = open("/home/labtel/Documentos/20170903/household.csv","r")
    c= file.readline()
    while(c!= ""):
        c=file.readline()
        i = i+1
    tam = i-1 ##calculo tamano
    file.close()
    print("Archivo tiene",tam,"lineas")

    n=tam

    #Analizo archivo
    print("Leyendo archivo . . .")
    content=[]
    a=[]
    file = open("/home/labtel/Documentos/20170903/household.csv","r")
    for i in range(n):
        content.append(file.readline())
    file.close()
    lista=[]
    for i in range(1,n):
        lista.append(format_line(content[i]))

    a=get_cols(content)
    print(a)

    #for i in lista:
    #    print(i)

    fecha ="2006-12-16"

    datos_day=get_day(lista,fecha)

    #print(len(datos_day))
    #print(len(lista))

    #print("DATOS")
    #for i in datos_day:
    #    print(i)

    fecha_inicio="2006-12-16"
    fecha_fin="2007-12-17"

    tiempo=get_exec_time_b(lista)
    print("Tiempo de ejecución de gen_day_dict fue: {} us".format(tiempo))

    #Threaded
    resultado1=gen_day_dict_threaded(fecha_inicio,fecha_fin,lista)
    #print(resultado1[fecha_fin])

    #Multiprocessing
    resultado2=gen_day_dict_multi(fecha_inicio,fecha_fin,lista)
    #print(resultado[fecha_inicio])
    #print(resultado2[fecha_fin])

    #if resultado1[fecha_fin]==resultado2[fecha_fin]:
    #    print("Son iguales")

    print("Calculando SpeedUp . . . ")
    calc_speedup_e(lista) #El speedup sale menor a 1 pero las funciones se ejecutan más rápido aisladamente

if __name__ == "__main__":
    main()
