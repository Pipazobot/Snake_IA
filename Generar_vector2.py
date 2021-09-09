"""
Libreria personal
Genera el vector de entrada, para el juego Snake
"""

import numpy as np

def distancia_binaria(distancia):
	if distancia > 0:
		d_binaria = +1
	elif distancia < 0:
		d_binaria = -1
	else:
		d_binaria = 0
	return d_binaria

def vector_de_entrada(snake,apple,ancho_vent,alto_vent):
	vect_entrada=np.zeros(12)
	#Manzana

	#esta en el eje x?
	if apple.pos[1]==snake.cabeza[1]:
		#obtener distancia a la manzana en el eje x
		distancia_x = (apple.pos[0]-snake.cabeza[0])/20
		vect_entrada[0] = distancia_binaria(distancia_x)

	#Esta en el eje y?
	if apple.pos[0]==snake.cabeza[0]:
		#obtener distancia a la manzana en el eje y
		distancia_y = (apple.pos[1]-snake.cabeza[1])/20
		vect_entrada[1] = distancia_binaria(distancia_y)

	#Esta en la diagonal positiva?
	pixeles_pendiente_positiva=[]
	x,y = snake.cabeza
	while(x>0 and y<alto_vent): #Llegar al pixel de la esquina inferior izquierda
		x += -20
		y += +20
	while(x<=ancho_vent and y>=0): #Guardar los pixeles de la diagonal pendiente positiva
		pixeles_pendiente_positiva.append([x,y])
		x += +20
		y += -20
	dis=0 #evaluar si la manzana esta en la lista de pixeles de pendiente positiva
	for pixel in pixeles_pendiente_positiva:
		if pixel==apple.pos:
			dis = (apple.pos[0]-snake.cabeza[0])/20
	vect_entrada[2] = distancia_binaria (dis)	

	#Esta en la pendiente negativa?
	pixeles_pendiente_negativa=[]
	x,y = snake.cabeza
	while(x>0 and y>0): #Llegar al pixel de la esquina superior izquierda
		x += -20
		y += -20
	while(x<=ancho_vent and y<=alto_vent): #Guardar los pixeles de la diagonal pendiente negativa
		pixeles_pendiente_negativa.append([x,y])
		x += +20
		y += +20
	dis=0 #evaluar si la manzana esta en la lista de pixeles de pendiente positiva
	for pixel in pixeles_pendiente_negativa:
		if pixel==apple.pos:
			dis = (apple.pos[0]-snake.cabeza[0])/20
	vect_entrada[3] = distancia_binaria(dis)

	#Paredes
	vect_entrada[4] = snake.cabeza[0]/20
	vect_entrada[5] = ancho_vent/20-vect_entrada[4]
	vect_entrada[6] = snake.cabeza[1]/20	
	vect_entrada[7] = alto_vent/20-vect_entrada[6]

	# Propio Cuerpo
	if len(snake.body)>0:
		dis_x_der=[]
		dis_x_izq=[]
		dis_y_up=[]
		dis_y_down=[]
		for idx,body in enumerate(snake.body):
			if snake.cabeza[1]==body[1]: #si hay una interseccion entre la cabeza y cuerpo en el eje x
				distancia=(body[0]-snake.cabeza[0])/20
				if distancia>0:
					dis_x_der.append(distancia)
				else:
					dis_x_izq.append(abs(distancia))
			if snake.cabeza[0]==body[0]: #si hay una interseccion entre la cabeza y cuerpo en el eje y
				distancia=(body[1]-snake.cabeza[1])/20
				if distancia>0:
					dis_y_down.append(distancia)
				else:
					dis_y_up.append(abs(distancia))

		dis_y_up_normal = min(dis_y_up) if dis_y_up!=[] else 0
		dis_x_izq_normal = min(dis_x_izq) if dis_x_izq!=[] else 0
		dis_y_down_normal = min(dis_y_down) if dis_y_down!=[] else 0
		dis_x_der_noraml = min(dis_x_der) if dis_x_der!=[] else 0

		vect_entrada[8] = distancia_binaria(dis_y_up_normal)
		vect_entrada[9] = distancia_binaria(dis_x_izq_normal)
		vect_entrada[10] = distancia_binaria(dis_y_down_normal)
		vect_entrada[11] = distancia_binaria(dis_x_der_noraml )

	return vect_entrada