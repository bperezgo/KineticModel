import numpy as np
from Metodos.Runge_Kutta import Runge_Kutta_Orden2
from Metodos.normalizar import *
from Metodos.Regresion_lineal import *
from Datos.ImpExp import *

class calcular_Yield(object):
	"""
	Con esta clase se puede calcular, después de calculadas las k, las cantidades de pseudocomponentes
	con el método calcular_Y, el error correspondiente a la regresión, los parámetros de la función
	Arrenhius cuando se han calculado los k a diferentes temperaturas y la estimación de las k, dada una
	temperatura y después de haber calculado los parámetros de la función Arrenhius.
	"""
	def __init__(self,vector_k,y_inicial,vector_thao,matriz_nodos_reacciones):
		self.vector_k = vector_k
		self.y_inicial = y_inicial
		self.vector_thao = vector_thao
		self.matriz_nodos_reacciones = matriz_nodos_reacciones
	def calcular_Y(self):

		m = len(self.y_inicial) # Numero de lumps.
		n = len(self.vector_thao) # Numero de tiempos, contando el inicial tiempo = 0 horas

		Y_resultados = np.zeros((n,m))
		Y_resultados[0] = self.y_inicial

		for j in range(1,n):

			Y_resultados[j] = Runge_Kutta_Orden2(self.vector_thao[j-1],self.vector_thao[j],self.vector_k,Y_resultados[j-1],self.matriz_nodos_reacciones)
			Y_resultados[j] = normalizarValores(Y_resultados[j],"PORCENTAJE")

		return(Y_resultados)

	def calcular_error(self,Y_experimental,Y_calculado):
		"""
		Error cuadrático medio
		"""
		criterio = 0
		for i in range(Y_calculado.shape[0]):
			for j in range(Y_calculado.shape[1]):
				if Y_experimental[i][j] == 0:
					continue
				criterio = criterio + ((Y_calculado[i][j] - Y_experimental[i][j])/Y_experimental[i][j])**2
		criterio = criterio/(Y_calculado.shape[0]*Y_calculado.shape[1])
		return(criterio)

	def calcular_parametros_logk(self,matriz_k,Temperaturas,unidades = 'C'):
		"""
		En este metodo se calcula los parametros de la funcion de Arrhenius
		matriz[i] son los parámetros k a la termperatura Temperatura[i]
		log: es el logaritmo natural
		Unidades, si la temperatura se ingresó en °C entonces esta es igual a 'C'
		Si se ingresó como °F entonces esta es igual a 'F'
		"""
		# un try except evitará que se ingrese un valor erróneo
		if unidades == 'C':
			absolut = 273.15
		if unidades == 'F':
			absolut = 459.63
		matriz_k = matriz_k.transpose()
		longitud_k = matriz_k.shape[0]
		longitud_t = len(Temperaturas)
		log_k = np.zeros((longitud_k,3)) #parametros del intercepto y la pendiente
		inv_temp = lambda x: 1/x
		Temperaturas = np.array(Temperaturas)
		Temperaturas.astype(float)
		Temperaturas_inv = np.array(list(map(inv_temp,Temperaturas+absolut)))
		another_len = matriz_k.shape[1]
		for i in range(longitud_k):
			vector = np.array([])
			index = np.array([])
			c = 0
			for j in range(another_len):
				if matriz_k[i][j] != 0:
					c += 1
					vector = np.append(vector,matriz_k[i][j])
					index = np.append(index,j)
			if (c <= 1 ):
				log_k[i] = np.array([np.nan,np.nan,np.nan])
				continue
			elif (c < another_len):
				Temp = np.array([])
				for k in index:
					Temp = np.append(Temp,Temperaturas[k])
				Temp_inv = np.array(list(map(inv_temp,Temp+absolut)))
				log_k[i] = Regresion_lineal(Temp_inv, np.log(vector))
			else:
				log_k[i] = Regresion_lineal(Temperaturas_inv,np.log(matriz_k[i]))

		return(log_k.transpose())

	def calcular_k_de_T(self,Temperatura,vector_con_parametros, unidades = 'C'):
		"""
		vector_con_parametros se calcula con el método anterior.
		"""
		if unidades == 'C':
			absolut = 273.15
		if unidades == 'F':
			absolut = 459.63
		longitud_k = vector_con_parametros.shape[1]
		vector_k = np.exp(vector_con_parametros[1]+vector_con_parametros[0]/(Temperatura+absolut))
		return(vector_k)