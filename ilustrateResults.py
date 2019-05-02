import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import numpy as np

datos = pd.read_excel('Interfaz.xlsx','Datos_Experimentales',index_col=None, na_values=['NA'])

dataResults = {}
with pd.ExcelFile('Results.xlsx') as xlsx:
	dataResults['k_parameters'] = pd.read_excel(xlsx, 'Sheet1',index_col=0, na_values='NaN')
	dataResults['Arrhenius_parameters'] = pd.read_excel(xlsx,'Sheet2',index_col=0, na_values='NaN')

print(dataResults[])
print('-----')
label = datos.columns.tolist()
label = label[2:len(label)]
label_exp = [0]*len(label)
label_mod = [0]*len(label)
for i in range(len(label)):
	label_exp[i] = label[i] + '_exp'
	label_mod[i] = label[i] + '_mod'


"""
styles = []
for i in range(5):
	plt.plot(thao, Y_calculado.transpose()[i],'*' ,label = label_2[i])
	plt.plot(thao, Y_experimental.transpose()[i],'s' ,label=label[i])

plt.axis([0,100,0,100])
plt.xlabel('Residence tiem (h)')
plt.ylabel('Component Yield (%)')

plt.title("Results")

plt.legend()

plt.show()
"""