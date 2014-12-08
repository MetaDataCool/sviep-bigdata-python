#!/usr/bin/env python
"implement the modified power iteration algo with sparse matrix"

import numpy as np
import scipy.sparse as sparse
import operator as op
import mat_utils as mu


def powit(A,k,h):
	"A is the sparse matrix already"
	n=A.get_shape()[0]
	print n
	pi = np.ones(n)
	qi=A.transpose(copy=True).dot(pi)

	tA = mu.transpose_to_csr(A)

	"fix parameter that could be put as input as well"
	maxiter=1000
	ztol=1.0e-5
	for i in range(maxiter):
		pi1=A.dot(qi)
		pi1=mu.project_unit_circle(mu.threshold(k,pi1))
		
		qi1=tA.dot(pi1)
		qi1=mu.threshold(h,qi1)

		#print qi1, pi1
		
		c=np.linalg.norm(pi-pi1)/np.linalg.norm(pi1)
		if c<ztol:
			print "success"
			print pi, qi, c, i
			return pi
		else:
			pi = pi1
			qi = qi1
	print pi, qi, c, i
	return pi



def zero_rows(p,M):
	def f(x):
		if(x == 0.0):
			return 1.0
		else:
			return 0.0

	d = np.array([f(x) for x in p])
	return mu.csr_diag(d) * M


def components(A,k,h,m, norm_row):
	res = []
	for i in range(m):
		pi = powit(A,k,h)
		res.append(pi)
		if norm_row:
			A=mu.normalize_by_row(zero_rows(pi,A))
		else:
			A=mu.normalize_by_col(zero_rows(pi,A))
	return res

		


	





























