import numpy as np

def matriz_concentraciones(vector_y,matriz_nodos_reacciones):
	"""
	Ejemplo de matriz_nodos_reacciones:
	Si la reacción es del estilo:
		[componente 1] reacciona y genera [componente 2] correspondiente a k1
		[componente 1] reacciona y genera [componente 3] correspondiente a k2
		[componente 2] reacciona y genera [componente 3] correspondiente a k3
		[componente 2] reacciona y genera [componente 4] correspondiente a k4
		[componente 3] reacciona y genera [componente 4] correspondiente a k5

	entonces matriz_nodos_reacciones debe ingresarse de la siguiente manera:

	matriz_nodos_reacciones = [[1,2],[1,3],[2,3],[2,4],[3,4]], una matriz nx2,
	donde n es igual al número de constantes cinéticas de la reacción.
	"""
	n = len(matriz_nodos_reacciones)
	numero_componentes = np.amax(matriz_nodos_reacciones)
	matriz_concentraciones = np.zeros((numero_componentes,n))
	ki = 1
	for pareja in matriz_nodos_reacciones:
		matriz_concentraciones[pareja[0]-1][ki-1] = -vector_y[pareja[0]-1]
		matriz_concentraciones[pareja[1]-1][ki-1] = +vector_y[pareja[0]-1]
		ki = ki + 1
	return(matriz_concentraciones)

def Runge_Kutta_Orden2(t_i, t_i_1, vector_k, vector_y,matriz_nodos_reacciones):
	k1 = calculo_k1(vector_k,vector_y,matriz_nodos_reacciones)
	k2 = calculo_k2(vector_k, vector_y, t_i, t_i_1, k1,matriz_nodos_reacciones)
	return(vector_y + 0.5*(t_i_1 - t_i)*(k1 + k2))

def calculo_k1(vector_k, vector_y,matriz_nodos_reacciones):
	matriz_y = matriz_concentraciones(vector_y,matriz_nodos_reacciones)
	vector_k_1 = matriz_y @ vector_k
	return(vector_k_1)

def calculo_k2(vector_k, vector_y, t_i, t_i_1, vector_k_1,matriz_nodos_reacciones):
	delta_t = t_i_1 - t_i
	vector_y_temporal = vector_y + delta_t*vector_k_1
	matriz_y = matriz_concentraciones(vector_y_temporal,matriz_nodos_reacciones)
	vector_k_2 = matriz_y @ vector_k
	return(vector_k_2)

class Runge_Kutta(object):
	def __init__(self,thao,matriz_y_experimental,matriz_nodos_reacciones):
		# vector_y_experimental hace referencia al valor experimental, con el que se calcularía
		# el error respecto al valor que de la aproximación deRunge Kutta
		self.thao = thao
		self.matriz_y_experimental = matriz_y_experimental
		self.matriz_nodos_reacciones = matriz_nodos_reacciones
	def funcionRungeKutta (self,vector_k):
		"""
		Éste método sólo está diseñado para utilizarse en la regresión no lineal
		"""
		vector = []
		for i in range(self.thao.shape[0] - 1):
			vector = np.append(vector, Runge_Kutta_Orden2(self.thao[i],self.thao[i+1],vector_k,\
			self.matriz_y_experimental[i],self.matriz_nodos_reacciones) - self.matriz_y_experimental[i + 1])
		return(vector)
	def vector_k_estimacion_inicial(self):
		# Usar algoritmo de Monte Carlo para el vector_k_estimacion
		size = self.matriz_nodos_reacciones.shape[0]
		vector_k = np.random.random(size)
		return(vector_k)