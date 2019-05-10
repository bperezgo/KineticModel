import numpy as np

class Objective_Function(object):

	def __init__(self, associative_array, kinetic_vector):
		self.associative_array = associative_array
		self.kinetic_vector = kinetic_vector

	@property
	def size(self):
		return(len(self.associative_array))

	@property
	def elem_num(self):
		reactions = 0
		STQ_coef = 0
		for k, list_k in self.associative_array.items():
			reactions += 1
			STQ_coef += len(list_k)
		return([STQ_coef,reactions])

	@property
	def initial_value(self):
		array = np.zeros(sum(self.elem_num))
		k = 0
		for e, element in enumerate(self.associative_array):
			for j in range(len(self.associative_array[element])):
				array[k] = 1/len(self.associative_array[element])
				array[self.elem_num[0]+e] += self.kinetic_vector[k]
				k += 1
			array[self.elem_num[0]+e] = array[self.elem_num[0]+e]/len(self.associative_array[element])
			
		return(array)
		
	def root_function(self, array):
		root_function = np.zeros(len(array))
		temp = 0
		for k, list_k in enumerate(self.associative_array):
			for i in range(len(self.associative_array[list_k])):
				root_function[temp+i] = array[self.elem_num[0]+k]*array[temp+i]-self.kinetic_vector[temp+i]
				root_function[self.elem_num[0]+k] += array[temp+i]
			temp += len(self.associative_array[list_k])
			root_function[self.elem_num[0]+k] = root_function[self.elem_num[0]+k] - 1
		return(root_function)
