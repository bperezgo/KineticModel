import numpy as np
from sympy import *
from scipy.optimize import least_squares,fmin
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd

from Metodos.Runge_Kutta import Runge_Kutta_Orden2, Runge_Kutta
from Datos.ImpExp import *
from Metodos.normalizar import *
from Metodos.calcular_Yield import *
"""
Este es el módulo principal 
"""
def main():
	"""
	Tareas pendientes:
		- Agregar unos modelos templates para este programa
		- Se deben agregar unos modelos base para reacciones con lumping por rangos de temperatura
		  y para lumping por SARA. (Recordar referenciar)
		- Se debe agregar entonces, una análisis de sensibilidad para verificar si la regresión no
		  lineal estimó bien los parámetros (Revisar referencia 10 para ver cuáles son los análisis
		  que se deben hacer).
		- Utilizar el criterio de Akaike y Bayesiano para mirar si el módelo se ajusta bien.
		- Revisar notas dentro del módulo
	"""
	TOL = 1E-04
	data = {}
	with pd.ExcelFile('Interfaz.xlsx') as xlsx:
		data['Reacción'] = pd.read_excel(xlsx, 'Reacción',index_col=0, na_values=['NA'])
		data['Datos_Experimentales'] = pd.read_excel(xlsx,'Datos_Experimentales',index_col=None, na_values=['NA'])
	reactions = data['Reacción']
	# Ingresar un try except para verificar que los datos de matriz nodos son enteros
	matriz_nodos = reactions.values
	datos = data['Datos_Experimentales']
	# Ingresar un try except para verificar que datos.shape[1] es igual al número de componentes de matriz_nodos
	data_Y_calculado = pd.DataFrame(columns = datos.columns)
	data_Y_calculado[data_Y_calculado.columns[0]] = datos[datos.columns[0]]
	data_Y_calculado[data_Y_calculado.columns[1]] = datos[datos.columns[1]]
	components_number = datos.shape[1] - 2
	temperature_size = []
	Temperature = [datos[datos.columns[0]].iloc[0]]

	c = 1
	for i in range(1,datos.shape[0]):
		if(pd.isna(datos[datos.columns[0]]).iloc[i]):
			c +=  1
		else:
			temperature_size.append(c)
			Temperature.append(datos[datos.columns[0]].iloc[i])
			c = 1
	temperature_size.append(c) # Para manejar el tamaño de los datos
	# Dato provisional para graficar, para conocer valores de Temperatura y de thaos para cada temperatura
	Results = []
	Results_mod = []
	puntero1 = 0
	for i in range(len(temperature_size)):
		puntero = puntero1 + temperature_size[i]
		Y_experimental = datos.drop([datos.columns[0],datos.columns[1]],axis = 1).values[puntero1:puntero]
		thao = datos[datos.columns[1]].values[puntero1:puntero]
		y_inicial = Y_experimental[0]
		ObjetoKutta = Runge_Kutta(thao,Y_experimental,matriz_nodos,'APE')
		# Se debe pensar en una forma de cambiar la TOL en caso de que no ajuste con una TOL predefinida
		# Sólo con cambiar las tolerancias pueden generarse errores
		while TOL > 1E-05:
			# Se debe nuscar un método más óptimo para la selección del primer parámetro
			# Éste método puede no encontrar valores apropiados si la data experimental es poca
			# Entonces,se puede crear un método que permita crear datos experimentales segun tendencia de
			# las gráficas para permitir una mejor convergencia,esto claramente introduce un error
			vector_k_estimacion = ObjetoKutta.vector_k_estimacion_inicial()
			Regresion = least_squares(ObjetoKutta.funcionRungeKutta,vector_k_estimacion,\
							bounds = (-np.inf,np.inf),ftol = 1e-8, method = 'lm', loss= 'linear')
			vector_k = Regresion.x
			Objeto_y = calcular_Yield(vector_k,y_inicial,thao,matriz_nodos)
			Y_calculado = Objeto_y.calcular_Y()
			Error = Objeto_y.calcular_error(Y_experimental,Y_calculado)
			TOL = Error
			vector_k = np.where(abs(vector_k) < 1E-06, 0, vector_k)
			print(vector_k)
			if np.any(vector_k < 0):
				TOL = 1E-04
			#Se dejan los limites de la regresion en todos los reales para que el metodo de regresion converja
			print(Error)
		Results_mod = np.append(Results_mod,Y_calculado)
		# Enviar Y_calculado a .csv
		Results = np.append(Results,np.append(np.append(Temperature[i],vector_k),Error))
		puntero1 = puntero
		print(Temperature[i])
		print("---")
		print(vector_k)
		print("---")
		print(Error)
		TOL = 1e-04

	Results = Results.reshape((len(Temperature),2 + matriz_nodos.shape[0]))
	Results_mod = Results_mod.reshape((np.sum(temperature_size),datos.shape[1]-2))
	data_Y_calculado.iloc[:,2:datos.shape[1]] = Results_mod
	# Cálculo de los parámetros Arrhenius
	Objeto_Y = calcular_Yield([],[],[],[])
	matriz_k = Results[:,1:matriz_nodos.shape[0] + 1]
	log_k_parameters = Objeto_Y.calcular_parametros_logk(matriz_k,Temperature)

	title = ['Temperature °C']
	for i in range(matriz_nodos.shape[0]):
		title.append('k'+str(i+1))
	title.append('Error (%)')
	df1 = pd.DataFrame(Results, columns = title)

	title.remove('Error (%)')
	title.remove('Temperature °C')
	index = ['Pendiente','Intercepto','Ajuste']
	df2 = pd.DataFrame(log_k_parameters, columns = title, index = index)

	with pd.ExcelWriter('Results.xlsx') as writer:
		df1.to_excel(writer, sheet_name='Sheet1', na_rep = 'NaN')
		df2.to_excel(writer, sheet_name='Sheet2', na_rep = 'NaN')
		data_Y_calculado.to_excel(writer, sheet_name = 'Sheet3', na_rep = 'NaN')


	#Con esta función se calcula los k's a una temperatura específica
	print(Objeto_Y.calcular_k_de_T(340,log_k_parameters[0:2]))

if __name__ == '__main__':
	main()
