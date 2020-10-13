"""
Popular matrix decompositions for lossy image compression.

Methods:
	PCA
	SVD
"""

import numpy as np
import numpy.linalg as la

def pca(data: np.array, mode="v", compression=99.99) -> np.array:
	"""
	mode:
		v: Select a percentage of variance to keep. Only valid if mode=pca.    
		c: Select a number of components to keep.
	"""

	rows, cols = data.shape

	mean, std = data.mean(axis=0), data.std(axis=0)  # mean and std of each column
	
	std[std == 0] = 0.00001
	
	standardized = (data-mean)/std  # center data at origin and force variance to one for each dimension

	covariance = np.dot(standardized, standardized.T)/cols  # covariance matrix for data

	eigVal, eigVec = la.eig(covariance)  # find unit eigen vectors and corresponding eigen values of covariance matrix
	order = eigVal.argsort()[::-1]  # sort by descending order
	eigVal = eigVal[order]
	eigVec = eigVec[:,order]

	total = eigVal.sum()  # represents total variance

	if mode == "v":
		pcs = 0
		variance = 0
		percent = 0
		print("\nTotal possible variance for channel: " + str(round(np.real(total), 3)))
		while round(percent, 1) < compression:  # need to keep increasing components
			variance += eigVal[pcs]
			percent = (variance/total)*100
			pcs += 1
			print("\t- accumulated variance with " + str(pcs) + " component(s): " + str(round(np.real(variance), 2)) + " (" + str(round(np.real(percent), 2)) + "%)")
		
		print("\n\t- using " + str(pcs) + " components to achieve " + str(round(np.real(percent), 2)) + "% variance\n") 

	elif mode == "c":
		print("\nUsing " + str(compression) + " components...")
		pcs = compression
	
	feature = eigVec.copy()[:, 0:pcs]  # compress image by removing columns

	inverseTransform = la.multi_dot([feature, feature.T, standardized])*std+mean  # data projected onto principal subspace and then normalized with respect to original basis
	normalized = np.absolute(inverseTransform)  # normalize data by elimating negatives and complex values for image data 
	return normalized

def svd(data: np.array, mode="c", k=1) -> np.array:
	U, s, V = np.linalg.svd(data)
	k = np.min((k, s.shape[0]))
	
	return np.absolute(la.multi_dot([U[:,:k], np.diag(s[:k]), V[:k,:]]))


