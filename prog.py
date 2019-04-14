#lang python

cpyimport numpy as np
import "racket" as rkt
# from name_mangling import mangle
cpyimport re
import predicates

# print(mangle("math/array"))

def construct(racket_array):
	return np.array(eval(racket_array.__repr__().replace(" ", ",")))

def destruct(numpy_array):
	python_list = numpy_array.tolist()
	racket_array = rkt.list()
	for i in range(len(python_list)-1, -1, -1):
		racket_list = rkt.list()
		for j in range(len(python_list[i])-1, -1, -1):
			racket_list = rkt.cons(python_list[i][j], racket_list)
		racket_array = rkt.cons(racket_list, racket_array)
	return racket_array


def transpose(n):
	arr = construct(n)
	tpose = arr.T
	return destruct(tpose)
