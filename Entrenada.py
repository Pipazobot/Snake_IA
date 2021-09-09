
# Ayuda

import numpy as np
import RedNeuronal_2
import Snake_NeuralNet2 as snake


#Crear la red
arquitectura = [12,10,4]
red = RedNeuronal_2.totalmente_conectada(arquitectura)

# Cargar los pesos de un entrenamiento anterior
W_mejores = np.load('W_mejores_fit_[55.].npy')
red.Insertar_parametros(W_mejores)

puntaje = []
for _ in range(2):
	score = snake.play_game(red,display=True) #se van sumando los puntajes
	puntaje.append(score)

print('Todo bien, puntaje: ', puntaje )