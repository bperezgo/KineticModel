# KineticModel
# As soon as posible

import numpy as np
import pandas as pd

from Metodos.Runge_Kutta import Runge_Kutta_Orden2, Runge_Kutta
from Datos.ImpExp import *
from Metodos.normalizar import *
from calcular_Yield import *

data = {}
with pd.ExcelFile('Interfaz.xlsx') as xlsx:
	data['Reacción'] = pd.read_excel(xlsx, 'Reacción',index_col=0, na_values=['NA'])
	data['Datos_Experimentales'] = pd.read_excel(xlsx,'Datos_Experimentales',index_col=None, na_values=['NA'])

reacciones = data['Reacción']
# Ingresar un try except para verificar que los datos de matriz nodos son enteros
matriz_nodos = np.array(reacciones.to_numpy())
print(matriz_nodos.dtype)
datos = data['Datos_Experimentales']
tamaño_datos = datos.shape
# Ingresar un try except para verificar que datos.shape[1] es igual al número de componentes de matriz_nodos
numero_componentes = datos.shape[1] - 2
print(numero_componentes)
print(datos)

iteraciones = []
#for i in iterador_temperatura:
#	print(i)

vector_k_estimacion = np.array([0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0, 0.001, 0 , 0])
