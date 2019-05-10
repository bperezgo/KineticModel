import numpy as np

class Runge_Kutta(object):
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
	def __init__(self,thao,matriz_y_experimental,matriz_nodos_reacciones, metodo = 'estandar'):
		"""
		vector_y_experimental hace referencia al valor experimental, con el que se calcularía
		el error respecto al valor que de la aproximación deRunge Kutta

		metodo = 'estandar' -> encuentra el valor de k de manera vectorial, ha dado buenos resultados
		metodo = 'PI' -> Performance index, es una función no vectorizada, es lento.
		metodo = 'APE' -> Average percentage error, función no vectorizada
		metodo = 'Weight'
		"""
		self.thao = thao
		self.matriz_y_experimental = matriz_y_experimental
		self.matriz_nodos_reacciones = matriz_nodos_reacciones
		self.metodo = metodo
		self.n = 0
		self.order = 1
	
	def funcionRungeKutta (self,vector_k):
		"""
		Éste método sólo está diseñado para utilizarse en la regresión no lineal
		Esta es la función objetivo, se puede usar 3 tipos de función objetivo,
		más esta que ya fue definida.
		"""
		vector = []
		for i in range(self.thao.shape[0] - 1):
			vector = np.append(vector, Runge_Kutta_Orden2(self.thao[i],self.thao[i+1],vector_k,\
			self.matriz_y_experimental[i],self.matriz_nodos_reacciones) - self.matriz_y_experimental[i + 1])

		if self.metodo == 'PI':
			return(np.sum(vector*vector))

		if self.metodo == 'estandar':
			return(vector)

		if self.metodo == 'APE':
			vector = np.abs(vector)
			divisor = np.append([],self.matriz_y_experimental[1:])
			vector = vector/divisor
			return(vector/len(divisor))


	def vector_k_estimacion_inicial(self):
		# Usar algoritmo de Monte Carlo para el vector_k_estimacion
		size = self.matriz_nodos_reacciones.shape[0]
		self.n += 1
		if (self.n <= 40*self.order):
			self.order += 1
			if self.order == 10:
				self.n = 0
				self.order = 1
		vector_k = np.random.random(size)*10**(4-self.order)
		return(vector_k)

	@property
	def matriz_concentraciones(self):
		"""
		Esta es un tensor donde el primer índice representa el número del componente, el segundo índice
		representa el subíndice de la reacción y el tercer índice hace referencia al tiempo.
		Esta matriz será útil para expresar de manera matricial el modelo cinético
		"""
		m = len(self.thao) - 1 # No se necesita tomar el tiempo final para definir el modelo
		n = len(self.matriz_nodos_reacciones)
		numero_componentes = np.amax(self.matriz_nodos_reacciones)
		self.matriz_concentraciones = np.zeros((numero_componentes,n,m))
		ki = 1
		for j in range(m):
			for pareja in self.matriz_nodos_reacciones:
				self.matriz_concentraciones[pareja[0]-1][ki-1][j] = -self.matriz_y_experimental[j][pareja[0]-1]
				self.matriz_concentraciones[pareja[1]-1][ki-1][j] = +self.matriz_y_experimental[j][pareja[0]-1]
				ki = ki + 1
		return(self.matriz_concentraciones)		

def matriz_concentraciones(vector_y,matriz_nodos_reacciones):

	n = len(matriz_nodos_reacciones)
	numero_componentes = len(vector_y)
	#numero_componentes = np.amax(matriz_nodos_reacciones)
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

