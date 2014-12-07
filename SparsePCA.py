#!/usr/bin/env python
"implement the modified power iteration algo with sparse matrix"

import numpy as np
import scipy.sparse as sparse
import operator as op
import mat_utils as mu


def powit(A,k,h):
	"A is the sparse matrix already"
	n=A.get_shape()[0]
	pi = np.ones(n)
	qi=A.transpose(copy=True).dot(pi)

	tA = mu.transpose_to_csr(A)

	"fix parameter that could be put as input as well"
	maxiter=100
	ztol=1.0e-5
	for i in range(maxiter):
		pi1=A.dot(qi)
		pi1=mu.project_unit_circle(mu.threshold(k,pi1))
		
		qi1=tA.dot(pi1)
		qi1=mu.threshold(h,qi1)

		#print qi1, pi1
		
		c=np.linalg.norm(pi-pi1)/np.linalg.norm(pi1)
		if c<ztol:
			return pi,qi
		else:
			pi = pi1
			qi = qi1
	print pi, qi, c, i
	return pi



def blabla(A,k,h):
	p=powit(A,k,h)
	B=np.diag(p)
	for i in range B.get_shape()[1]:
		if B[i][i]=0:
			B[i][i]=1
		else :
			B[i][i]=0
	return B.A	






























