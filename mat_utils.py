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

def norm_row(A):
	"normalize the columns of a sparse matrix A"
	






