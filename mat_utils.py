#!/usr/bin/env python
"Matrix utilities for the project"

import numpy as np
import scipy.sparse as sparse
import operator as op

def project_unit_circle(vec):
	"Normalizes the specified numpy array (divides by euclidian norm)"
	return vec / np.linalg.norm(vec)

def transpose_to_csr(mat):
	"Fast transposition to CSR using COO as an intermediate format"
	return mat.tocoo().transpose(copy=True).tocsr()

def threshold(k,arr):
	"""
	Hard tresholding operator on a Numpy array.
	Zeroes all but the k greatest values of the vector
	"""
	non_zero_is = np.nonzero(arr)[0].tolist() # list of nonzero values indices
	pairs = [(abs(arr[i]),i) for i in non_zero_is]
	sorted_pairs = sorted(pairs,key=op.itemgetter(0),reverse=True)
	res = np.zeros(arr.size)
	for (v,i) in sorted_pairs[0:k]:
		res[i] = arr[i]
	return res


def zero_or_inverse(x):
	"Returns the inverse of a number, or 0 if it's 0"
	if x == 0.0:
		return x
	else:
		return 1.0 / x

def csr_diag(arr):
	"Creates a diagonal CSR matrix from given numpy array"
	res = sparse.csr_matrix((arr.size,arr.size))
	res.setdiag(arr)
	return res

def normalize_by_row(m):
	"Normalizes a matrix so that its rows all have sum 1.0"
	rows_sum = np.asarray(m.sum(1).transpose())[0]
	inv_rs = np.array([zero_or_inverse(v) for v in  rows_sum])
	#m = M.tocsc() # TODO : multiply by m as CSC ?
	return csr_diag(inv_rs) * m





