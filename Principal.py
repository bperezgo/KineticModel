import numpy as np
from sympy import *
from scipy.optimize import least_squares,fmin
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd

from Metodos.Runge_Kutta import Runge_Kutta_Orden2, Runge_Kutta
from Datos.ImpExp import *
from Metodos.normalizar import *
from calcular_Yield import *
"""
Este sería el programa principal que traería los otros módulos y mostraría los resultados
finales.
"""
def main():
	"""
	Tareas pendientes:
		- Revisar metodo para calcular las k, dado Temperatura (np.innan(), np.isinf())
		- Manejar mejor los datos (pandas)
		- Agregar unos modelos templates para este programa
		- Se puede agregar el algoritmo de Monte Carlo para elegir el vector_k_estimación
		- Se deben agregar unos modelos base para reacciones con lumping por rangos de temperatura
		  y para lumping por SARA. (Recordar referenciar)
		- Se debe agregar entonces, una análisis de sensibilidad para verificar si la regresión no
		  lineal estimó bien los parámetros (Revisar referencia 10 para ver cuáles son los análisis
		  que se deben hacer).
		- Utilizar el criterio de Akaike y Bayesiano para mirar si el módelo se ajusta bien.
	"""
	
	matriz_nodos = np.array([[1,2],[1,3],[1,4],[1,5],[2,3],[2,4],[2,5],[3,4],[3,5],[4,5]])
	Y_experimental = np.array(pasarArchivosAMatriz('Resultados1.csv'))
	vector_k_estimacion = np.array([0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0, 0.001, 0 , 0])

	y_inicial = Y_experimental[0]
	thao = np.array([0,1,5,10,50,100])

	ObjetoKutta = Runge_Kutta(thao,Y_experimental,matriz_nodos)
	Regresion = least_squares(ObjetoKutta.funcionRungeKutta,vector_k_estimacion,\
					bounds = (0,np.inf),ftol = 1e-12, method = 'trf', loss= 'soft_l1')
	print(Regresion)
	vector_k = Regresion.x

	Objeto_y = calcular_Yield(vector_k,y_inicial,thao,matriz_nodos)
	Y_calculado = Objeto_y.calcular_Y('Prueba.csv')
	Error = Objeto_y.calcular_error(Y_experimental,Y_calculado)

	print(vector_k)
	print("---")
	print(Error)

	label = ['Y_R_exp','Y_VGO_exp','Y_D_exp','Y_N_exp','Y_G_exp']
	label_2 = ['Y_R_mod','Y_VGO_mod','Y_D_mod','Y_N_mod','Y_G_mod']
	styles = []
	for i in range(5):
		plt.plot(thao, Y_calculado.transpose()[i],'*' ,label = label_2[i])
		plt.plot(thao, Y_experimental.transpose()[i],'s' ,label=label[i])

	plt.axis([0,100,0,100])
	plt.xlabel('Residence tiem (h)')
	plt.ylabel('Component Yield (%)')

	plt.title("Results")

	plt.legend()

	plt.show()

if __name__ == '__main__':
	main()

