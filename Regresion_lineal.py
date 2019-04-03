import numpy as np
def Regresion_lineal(X, Y):
	X = np.array(X)
	Y = np.array(Y)
	N = len(X)
	suma1 = np.sum(X)
	suma2 = np.sum(Y)
	suma3 = np.sum(X*Y)
	suma4 = np.sum(X**2)

	m = (N*suma3 - suma1*suma2)/(N*suma4-suma1*suma1)
	b = (suma2 - m*suma1)/N

	Vector_Y = b + m*X
	Promedio_Y = suma2/N
	Diferencia1 = Vector_Y - Y
	Diferencia2 = Y - Promedio_Y

	suma_dif1 = np.sum(Diferencia1**2)
	suma_dif2 = np.sum(Diferencia2**2)

	r_2 = 1 - suma_dif1/suma_dif2
	# r_2 no se devuelve
	return([m,b,r_2])
