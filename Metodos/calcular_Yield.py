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

	def calcular_parametros_logk(self,matriz_k,Temperaturas):
		"""
		En este metodo se calcula los parametros de la funcion de Arrhenius
		matriz[i] son los parámetros k a la termperatura Temperatura[i]
		log: es el logaritmo natural
		"""
		matriz_k = np.array(matriz_k)
		longitud_k = matriz_k.shape[1]
		longitud_t = len(Temperaturas)
		log_k = np.zeros((2,longitud_k)) #parametros del intercepto y la pendiente
		matriz = matriz_k.transpose()
		vector = np.zeros((longitud_k,2))
		for i in range(longitud_k):
			vector[i] = Regresion_lineal(1/Temperaturas,np.log(matriz[i]))

		return(vector.transpose())

	def calcular_k_de_T(Temperatura,vector_con_parametros):
		"""
		vector_con_parametros se calcula con el método anterior.
		"""
		longitud_k = vector_con_parametros.shape[1]
		vector_k = np.exp(vector_con_parametros[0])*np.exp(vector_con_parametros[1]/Temperatura)
		return(vector_k)