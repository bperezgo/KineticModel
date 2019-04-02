import csv
from math import log
def pasarArchivosAMatriz(ArchivoCSV):
	matriz = []
	with open(ArchivoCSV,newline='') as csvfile:
		Archivo =csv.reader(csvfile, delimiter ='\t',quotechar = '|')
		for row in Archivo:
			matriz.append(row)
	numero_filas_matriz = len(matriz)
	numero_columnas_matriz = len(matriz[0]) #No se puede asegurar que la lista tiene el mismo número de elementos

	
	for i in range(numero_filas_matriz):
		for j in range(numero_columnas_matriz):
			matriz[i][j] = float(matriz[i][j])
	return(matriz)
def pasarMatrizAArchivos(matriz, ArchivoCSV):
	with open(ArchivoCSV, 'w') as csvfile:
	   	escritor = csv.writer(csvfile, delimiter='\t', quotechar='|',quoting=csv.QUOTE_MINIMAL)
	   	for row in range(len(matriz)):
	   		escritor.writerow(matriz[row])