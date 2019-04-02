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


Temperature = [320,350,360,380]
Error = [0.02,4.58,6.61,0.69]
vector_k1 = [0.00214,0.00131,0.00030,0.00006,0.00670,0.00491,0,0.00105,0,0]
vector_k2 = [0.00845,0.00610,0.00113,0.00073,0.00282,0.00141,0,0.00046,0,0]
vector_k3 = [0.01324,0.00951,0.00251,0.00085,0.00181,0.00073,0,0.00032,0,0]
vector_k4 = [0.02650,0.03093,0.01130,0.00902,0.00045,0.00014,0,0.00007,0,0]

Results = []
Results = np.append(Results,np.append(np.append(Temperature[0],vector_k1,),Error[0]))
Results = np.append(Results,np.append(np.append(Temperature[1],vector_k2,),Error[1]))
Results = np.append(Results,np.append(np.append(Temperature[2],vector_k3,),Error[2]))
Results = np.append(Results,np.append(np.append(Temperature[3],vector_k4,),Error[3]))

Results = Results.reshape((4,12))
title = ['Temperature °C']
for i in range(10):
	title.append('k'+str(i+1))
title.append('Error (%)')
print(title)
df = pd.DataFrame(Results, columns = title)
print(df)
df.to_excel('path_to_file.xlsx', sheet_name='Sheet1',index = False)