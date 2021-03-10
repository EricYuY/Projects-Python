import math
import random
import time
from pprint import pprint
from itertools import repeat
from multiprocessing import Pool

#Inputs son RANGO (field radius), Madera total (field total wood) y rango de busqueda (search radius)

#Se generan arboles en todo el radio y se calcula el tiempo que demora 1 jugador encontrar los arboles vs multiples.
FIELD_RADIUS=3
FIELD_TOTAL_WOOD= 1000000
SEARCH_RADIUS=1


def generate_random_wood():
	wood_coordinates = []
	x = []
	y = []

	for i in range(FIELD_TOTAL_WOOD):
		theta = random.uniform(0.0, 2 * math.pi)
		r = FIELD_RADIUS * math.sqrt(random.uniform(0.0, 1.0))
		new_coordinate = []
		x.append(r * math.cos(theta))
		y.append(r * math.sin(theta))

	return x, y

"""
player_pos: lista de 2 elementos con las coordenadas en las que se encuentra actualmente el jugador
x_list: Lista de todas las coordenadas X donde se encuentra la madera generada de manera aleatoria
y_list: Lista de todas las coordenaas Y donde se encuentra la madera generada de manera aleatoria
"""
def find_wood(player_pos, x_list, y_list):
	#TODO: Escriba su funcion aqui
	wood=0
	for i in range(len(x_list)):
		validoX=abs(player_pos[0]-x_list[i])
		validoY=abs(player_pos[1]-y_list[i])
		if (validoX <1 and validoY<1):
			wood = wood +1
	return wood


if __name__ == '__main__':
	total_wood_serial=0
	total_wood_paralelo=0
	x_list, y_list = generate_random_wood() #Wood generation
	#print(x_list)
	#print(y_list)
	centers=[(-1,2),(1,2),(-2,0),(0,0),(2,0),(-1,-2),(1,-2)]
	"""
	"""
	t1=time.time()
	for i in range(len(centers)):
		wood=find_wood(centers[i],x_list,y_list)
		#print(wood,centers[i])
		total_wood_serial=total_wood_serial+wood
	print("Duración de recolección de 1 jugador: {}s".format(time.time()-t1))
	print("Se recolectaron: {} arboles".format(total_wood_serial))
	"""
	La siguiente linea crea la lista con los componentes necesarios para llamar a find_wood() en paralelo
	player_positions viene a ser la lista donde estan guardadas las coordenadas de los centros de los circulos.
	"""
	joined_vector = [(pos, x_list, y_list) for pos in centers]
	t2=time.time()
	p=Pool()
	total_wood_paralelo_list=p.starmap(find_wood,joined_vector)
	p.close()
	p.join()
	total_wood_paralelo=sum(total_wood_paralelo_list)
	print("Duración de recolección de 7 jugadores: {}s".format(time.time()-t2))
	print("Se recolectaron: {} arboles".format(total_wood_paralelo))
