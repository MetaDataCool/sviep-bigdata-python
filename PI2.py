from math import  sqrt
from operator import itemgetter
 

def tronk(x, k):
	"""
	keep the k highest of x0 and set the others at 0
	"""
	n= len(x)
	pair = [(x[i],i) for i in range(n)]
	b = sorted(pair,key=itemgetter(0),reverse=True)
	print b
	x0 =[0 for i in range(n)]
	for i in range(k):
		x0[b[i][1]]=b[i][0]
	return x0



def poweig2(A, p0, q0, k, h, maxiter = 100, ztol= 1.0e-5, mode= 0, teststeps=1):
	"""
	Performs iterative power method for dominant eigenvalue.
	 A  - input matrix.
	 p0, q0 - initial estimate vectors.
	 k,h - sparcity constraint
	 maxiter - maximum iterations
	 ztol - zero comparison.
	 mode:
	   0 - divide by last nonzero element.
	   1 - unitize.
	Return value:
	 eigenvalue, eigenvector
	"""
	m	= len(A)
	pi   = p0[:]
	qi=q0[:]
 
	for n in range(maxiter):
	   # matrix vector multiplication.
	   	pim1 = pi[:]
	   	qim1 = qi[:]
	  	for i in range(m):
		   pi[i] = 0.0
		   qi[i] = 0.0
		   for j in range(m):
			 pi[i]+=A[i][j] * qim1[j]
			 qi[i]+=A[j][i] * pim1[j]
		print n, pi, qi
		pi = tronk(pi,k)
		qi = tronk(qi,h)
		print pi, qi		
		if mode == 0:
		  vlen1 = sqrt(sum([pi[l]**2 for l in range(m)]))
		  pi = [pi[l] /vlen1 for l in range(m)]
		  vlen2 = sqrt(sum([qi[l]**2 for l in range(m)]))
		  qi = [qi[l] /vlen2 for l in range(m)]
	   	elif mode == 1:
		  for l in range(m-1, -1, -1):
			 c = abs(pi[l])
			 if c > 1.0e-5:
				pi = [pi[l] /c for l in range(m)]
				break
	   # early termination test.
	   	if n % teststeps == 0:
		  S = sum([pi[l]-pim1[l] for l in range(m)])
		  S2= sum([qi[l]-qim1[l] for l in range(m)])
		  if abs(S) < ztol and abs(S2)< ztol:
			break
	  	print n, pi, qi
	# Compute Rayleigh quotient.
	numer = sum([pi[l] * pim1[l] for l in range(m)])
	denom = sum([pim1[l]**2 for l in range(m)])
	plambda = numer/denom
	return plambda, pi,qi
 

 