	from math import  sqrt
	 
	def poweig(A, x0, maxiter = 100, ztol= 1.0e-5, mode= 0, teststeps=1):
		"""
		Performs iterative power method for dominant eigenvalue.
		 A  - input matrix.
		 x0 - initial estimate vector.
		 maxiter - maximum iterations
		 ztol - zero comparison.
		 mode:
		   0 - divide by last nonzero element.
		   1 - unitize.
		Return value:
		 eigenvalue, eigenvector
		"""
		m	= len(A)
		xi   = x0[:]
	 
		for n in range(maxiter):
		   # matrix vector multiplication.
		   xim1 = xi[:]
		   for i in range(m):
			   xi[i] = 0.0
			   for j in range(m):
				 xi[i] += A[i][j] * xim1[j]
		   print n, xi
		   if mode == 0:
			  vlen = sqrt(sum([xi[k]**2 for k in range(m)]))
			  xi = [xi[k] /vlen for k in range(m)]
		   elif mode == 1:
			  for k in range(m-1, -1, -1):
				 c = abs(xi[k])
				 if c > 1.0e-5:
					xi = [xi[k] /c for k in range(m)]
					break
		   # early termination test.
		   if n % teststeps == 0:
			  S = sum([xi[k]-xim1[k] for k in range(m)])
			  if abs(S) < ztol:
				 break
		   print n, xi
		# Compute Rayleigh quotient.
		numer = sum([xi[k] * xim1[k] for k in range(m)])
		denom = sum([xim1[k]**2 for k in range(m)])
		xlambda = numer/denom
		return xlambda, xi
	 
	 
	if __name__== "__main__":
	   A = [[3,6],[1, 4]]
	   x = [1,1]
	   xlambda, x = poweig(A,x, mode =1, teststeps=1)
	   print "poweig returns", xlambda, x