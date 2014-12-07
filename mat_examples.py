#!/usr/bin/env python
"Some examples of matrix manipulation"

import numpy as np
import scipy.sparse as sparse
import operator as op

# COO matrix creation
a_coo_m = sparse.coo_matrix((np.array([1,2,3,4,5]),(np.array([0,0,2,3,4]),np.array([0,1,1,2,0]))), shape=(5,3))
# Vector creation (numpy array)
a_vec = np.array([1,0,-1])
# Vector - matrix product
a_product_vec = a_coo_m.dot(a_vec)
# Conversion to CSR format
a_csr_m = a_coo_m.tocsr()

def normalize(vec):
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

