import numpy as np
import scipy, scipy.ndimage
import cvxpy as cp
import matplotlib.pyplot as plt

def circular_convolution(w, x):
	L = len(w)
	y = np.zeros(L)
	for i in range(L):
		y[i] = sum(w[j] * x[i-j]
				   for j in range(L))
	return y

def checking_y_hat(B_hat, C_hat, h, m, y_hat):
	y_hatt = np.zeros(L, dtype=complex)
	for i in range(L):
		tmp = np.outer(np.sqrt(L)*C_hat[i,:], B_hat[i,:])
		y_hatt[i] = np.trace( tmp @ np.outer(h,m) )
	if np.linalg.norm(y_hat-y_hatt) > 1e-10:
		print('difference of y_hat: ', np.linalg.norm(y_hat-y_hatt))
	
def cvx(L, K, N, B_hat, C_hat, y_hat):
	X = cp.Variable((K,N))

	objective = cp.Minimize(cp.norm(X, 'nuc'))
	constraints = [
		cp.trace( np.outer(np.sqrt(L)*C_hat[i,:], B_hat[i,:]) @ X ) == y_hat[i] 
		for i in range(L)
	]
	prob = cp.Problem(objective, constraints)
	prob.solve(verbose=False)
	
	return X

def error_rate(X, B, C, w, x):
	if X.value is None:
		print('No X')
		return 1
	
	X = X.value
	h_ = X[:,0] / np.linalg.norm(X[:,0])
	m_ = X[0,:] / h_[0]
	
	w_ = np.dot(B, h_)
	x_ = np.dot(C, m_)
	
	X_ = np.outer(w_, x_)
	err = np.linalg.norm(X_ - np.outer(w, x)) / np.linalg.norm(np.outer(w, x))
	return err

def experiment(L, K, N, F, R):
	errs = np.zeros(R)
	for i in range(R):
		# (a)
#		 r = np.random.choice(L, K)
#		 B = np.eye(L)[:,r]
		# (b)
		B = np.eye(L)[:,0:K]
		
		C = np.random.normal(0, np.sqrt(1/L), (L, N))

		h = np.random.normal(0, 1, K)
		m = np.random.normal(0, 1, N)

		w = np.dot(B, h)
		x = np.dot(C, m)
		y = circular_convolution(w, x)

		B_hat = np.dot(F,B)
		C_hat = np.dot(F,C)
		y_hat = np.dot(F,y)

		# checking_y_hat(B_hat, C_hat, h, m, y_hat)

		X = cvx(L, K, N, B_hat, C_hat, y_hat)

		errs[i] = error_rate(X, B, C, w, x)

	success_rate = sum(np.array(errs < 0.02)) / R
	return success_rate

if __name__ == '__main__':
	L, K, N = 60, 40, 40
	F = 1/np.sqrt(L) * scipy.linalg.dft(L)
	R = 20 # number of experiments with the same L, K, N
	step = 1

	result = []
	for k in range(2, K+step, step):
		tmp = []
		for n in range(2, N+step, step):
			
			if len(tmp)>3 and (tmp[-1]+tmp[-2]+tmp[-3])<0.15:
				print('K=', '%2d' %k, ' N=', '%2d' %n, ' rate: ---')
				tmp.append(0)
				continue
			
			success_rate = experiment(L, k, n, F, R)
			print('K=', '%2d' %k, ' N=', '%2d' %n, ' rate:', success_rate)
			tmp.append(success_rate)
			
		result.append(tmp)

	r = np.array(result)
	r = r.T

	plt.figure(figsize=(7,7))
	plt.title("L = 60")
	plt.xlabel("K")
	plt.ylabel("N")
	plt.grid()
	plt.imshow(r, cmap='Greys_r', origin='lower', extent=[1,40,1,40])
	plt.colorbar()
	plt.show()