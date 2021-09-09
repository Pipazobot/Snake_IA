"""Hacer el juego de la serpiente"""

import random
import numpy as np
import Generar_vector2

class Snake:
	def __init__(self):
		self.cabeza = [100, 80]
		self.vel = [1,0]
		self.puntaje = 0 #inicialmente no tiene puntos
		self.con_vida = True
		self.body = []

	def move(self,pixel):
		#primero muevo el cuerpo
		self.body.insert(0,[self.cabeza[0],self.cabeza[1]])
		self.body.pop()

		#muevo la cabeza
		self.cabeza[0] = self.cabeza[0]+self.vel[0]*pixel
		self.cabeza[1] = self.cabeza[1]+self.vel[1]*pixel

	def draw(self,ventana,pygame):
		if len(self.body)>0:
			for part_of_body in self.body:
				pygame.draw.circle(ventana,(255,255,255),part_of_body,10)
		#Dibujar la cabeza al final
		pygame.draw.circle(ventana,(20,255,20),self.cabeza,10)

	def sigue_viva(self,ancho_vent,alto_vent):
		if self.cabeza[0]<0 or self.cabeza[0]>ancho_vent:
			self.con_vida = False
		if self.cabeza[1]<0 or self.cabeza[1]>alto_vent:
			self.con_vida = False
		#si choca con su cuerpo
		if self.cabeza in self.body:
			self.con_vida = False

	def add(self,comido):
		if comido==True:
			self.body.insert(0,[self.cabeza[0],self.cabeza[1]])


class Apple:
	def __init__(self,ancho_vent,alto_vent):
		self.color = (250,0,0) #color rojo
		self.pos = [240, 80]
		self.pos[0]=random.randint(1,ancho_vent/20)*20 #eje x
		self.pos[1]=random.randint(1,alto_vent/20)*20 #eje y
		self.r = 9
		self.comido = False
		#self.ocupado = True

	def draw(self,ventana,snake_body,ancho_vent,alto_vent,pygame):
		if self.comido==False:
			pygame.draw.circle(ventana,self.color,self.pos,self.r) #MANZANA
		else: #Si se la comio, debo crear una nueva manzana
			self.ocupado = True
			while(self.ocupado):
				self.pos[0]=random.randint(1,ancho_vent/20)*20 #eje x
				self.pos[1]=random.randint(1,alto_vent/20)*20 #eje y
				if self.pos in snake_body:
					self.ocupado = True
				else:
					self.ocupado = False
			pygame.draw.circle(ventana,self.color,self.pos,self.r) #MANZANA
			self.comido=False 

		
def show_vector(ventana,vect_entrada,ancho_vent,alto_vent,pygame):
	font = pygame.font.Font('freesansbold.ttf', 20)
	text = font.render(str(vect_entrada), True, (0, 255, 0), (0, 0, 250))
	textRect = text.get_rect()
	textRect.center = (ancho_vent/2, alto_vent/2)
	ventana.blit(text, textRect)

def show_salida(ventana,salida,ancho_vent,alto_vent,pygame):
	font = pygame.font.Font('freesansbold.ttf', 15)
	text = font.render(str(salida), True, (0, 255, 0), (0, 0, 250))
	textRect = text.get_rect()
	textRect.center = (ancho_vent/2, 50+alto_vent/2)
	ventana.blit(text, textRect)

def draw_grid(surface,ancho_vent,alto_vent,pygame):
	for x in range(10,ancho_vent,20):
		pygame.draw.line(surface, (50,50,50), (x,0),(x,alto_vent))
	for y in range(10,alto_vent,20):
		pygame.draw.line(surface, (50,50,50), (0,y),(ancho_vent,y))

def play_game(red, display=True):
	bomb_timer = 300 #esta bomba explota si la serpiente no sube su puntaje, se reinicia si come una manzana 
	ancho_vent,alto_vent = 500, 500
	#creo el objeto a partir de la clase
	snake=Snake()
	apple = Apple(ancho_vent,alto_vent) 

	if display==True:
		import pygame
		pygame.init()
		#'ventana' es una superficie para pygame
		ventana = pygame.display.set_mode((ancho_vent,alto_vent))
		pygame.display.set_caption("Juego de Snake -- Pipe Mercado") #titulo de la ventana

	run=True
	while run:
		if display==True:
			#como cerrar la ventana
			for evento in pygame.event.get():
				if evento.type==pygame.QUIT:
					run=False

		snake.move(20) #se mueve 20 pixeles. 
		snake.sigue_viva(ancho_vent,alto_vent)
		if snake.con_vida==False:
		 	run = False

		vect_entrada = Generar_vector2.vector_de_entrada(snake,apple,ancho_vent,alto_vent)

		salida = red.predict(vect_entrada)
		salida = np.around(salida,2) #redondear los elementos del arreglo
		accion = np.argmax(salida) #indice de la neurona con mayor activación

		if accion==0 and snake.vel!=[0,1]: #arriba
			snake.vel=[0,-1]
		if accion==1 and snake.vel!=[0,-1]: #abajo
			snake.vel=[0,1]
		if accion==2 and snake.vel!=[-1,0]: #derecha
			snake.vel=[1,0]
		if accion==3 and snake.vel!=[1,0]: #izquierda
			snake.vel=[-1,0]

		if display==True:
			#Dibujar
			ventana.fill((0,0,0)) 
			draw_grid(ventana,ancho_vent,alto_vent,pygame)
			apple.draw(ventana,snake.body,ancho_vent,alto_vent,pygame)
			snake.draw(ventana,pygame)
			show_vector(ventana,vect_entrada,ancho_vent,alto_vent,pygame)
			show_salida(ventana,salida,ancho_vent,alto_vent,pygame)

			pygame.display.flip() #esto es como pygame.update
			pygame.time.delay(100) #lo retraso por si va muy rapido

		#verificar si se comio la manzana
		if snake.cabeza==apple.pos:
			snake.puntaje += 1
			apple.comido = True
			snake.add(apple.comido)
			bomb_timer = 300 #reiniciar el bomb_timer

		bomb_timer += -1
		if bomb_timer<=0:
			snake.con_vida = False

	if display==True:
		pygame.quit()
		
	return snake.puntaje
