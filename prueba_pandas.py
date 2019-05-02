import numpy as np

matriz = np.array([[3,5,1,2,6],[1.2,3,.2,4,2],[9,5,96,52,66],[21,1123,573,976,332]])
vector = np.array([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
matriz = matriz.transpose()
matriz = matriz[1:]
matriz = matriz.transpose()

print(matriz)