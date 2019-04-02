import numpy as np
def normalizarValores(vector,tipo = "PORCENTAJE"):
	suma = vector.sum()
	for i in range(vector.size):
		vector[i] = vector[i]/suma
	if tipo == "PORCENTAJE":
		vector = vector*100
	return(vector)

