import time
import numpy as np
import random
from multiprocessing import Pool
from itertools import repeat

"""
Entradas: los 2 vectores
Salidas: El producto de la multiplicacion(numero entero)
"""

def mult_serial(m,a):
    mult=[0]*len(m)
    for i in range(len(m)) :
        for j in range(len(a)):
            mult[i]=mult[i]+m[i][j]*a[j]
    return mult

def multiplica_vectorxvector(m,a):
    mult=0
    for i in range(len(m)):
        mult=mult+m[i]*a[i]
    return mult

if __name__ == '__main__':

    #Llenamos la matriz y el vector con valores aleatorios
    vector_size=5000
    m=5000
    n=vector_size

    matrix_M = np.random.randint(100,size=(m,n))
    vector_A = np.random.randint(100,size=(vector_size))
    #Hacemos multiplicacion en serial y medimos el tiempo de ejeccuion
    t1 = time.time()
    result_serial=mult_serial(matrix_M,vector_A)
    print("Tiempo de ejecucion en serial: ", time.time() - t1)

    #Hacemos multiplicacion en paralelo y medimos el tiempo de ejecucion
    joined_vector = zip(matrix_M, repeat(vector_A))	#joined_vector va a ser la entrada a starmap
    t2=time.time()
    p=Pool()
    result_paralelo=p.starmap(multiplica_vectorxvector,joined_vector)
    p.close()
    p.join()
    print("Tiempo de ejecucion en paralelo: ",time.time()-t2)

    assert(result_serial == result_paralelo)
