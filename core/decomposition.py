"""
Popular matrix decomposition algorithms for lossy image compression.

Methods:
	PCA
	SVD
"""

import numpy as np
import numpy.linalg as la

def pca(data: np.array, mode: str, compression: float or int, overflow: bool=False) -> (np.array, list):
	"""
	Principal component analysis.

	Determines orthogonal components that retain maximum variance, projects data to these components
		then recontructs data by transforming back to original basis.

	mode:
		v: Determine compression by target percentage of variance to keep   
		c: Determine compression by target number of components to keep.
	
	compression:
		value corresponding to mode

	overflow:
		whether or not to allow overflow when converting data from float64 to uint8

	Returns: compressed image data and log describing components used and percentage variance
	"""

	rows, cols = data.shape
	mean, std = data.mean(axis=0), data.std(axis=0)  # mean and std of each column
	std[std == 0] = 0.000001  # prevents division by 0
	standardized = (data-mean)/std  # center data at origin and force variance to one for each dimension
	covariance = np.dot(standardized, standardized.T)/cols  # covariance matrix for data
	
	eigVal, eigVec = la.eig(covariance)  # find unit eigen vectors and corresponding eigen values of covariance matrix
	order = eigVal.argsort()[::-1]  # sort by descending order
	eigVal = eigVal[order]
	eigVec = eigVec[:,order]

	total = eigVal.sum()  # represents total variance

	pcs = 0
	accumulated = 0
	percent = 0

	log = []
	log.append((pcs, percent))

	if mode == "v":
		while round(percent, 1) < compression:  # need to keep increasing components
			accumulated += eigVal[pcs]
			percent = (accumulated/total)*100
			pcs += 1
			log.append((pcs, np.real(percent)))

	elif mode == "c":
		while pcs < compression:
			accumulated += eigVal[pcs]
			percent = (accumulated/total)*100
			pcs += 1
			log.append((pcs, np.real(percent)))
	
	feature = eigVec.copy()[:, 0:pcs]  # compress image by removing columns

	inverseTransform = la.multi_dot([feature, feature.T, standardized])*std+mean  # data projected onto principal subspace and then normalized with respect to original basis
	normalized = np.absolute(inverseTransform)  # normalize data by elimating negatives and complex values for image data

	if overflow:
		return normalized.astype(np.uint8), log
	else:
		return normalized.clip(0, 255), log

def svd(data: np.array, mode: str, k: int, overflow: bool=False) -> (np.array, list):
	"""
	Singular value decomposition.

	Compresses image by eliminating singular values that least contribute to variance.

	mode:
		c: Determine compression by target number of components to keep.
	
	k:
		Number of components to keep

	overflow:
		whether or not to allow overflow when converting data from float64 to uint8

	Returns: compressed image data and log describing components used and percentage variance
	"""
	U, S, V = np.linalg.svd(data)
	k = np.min((k, S.shape[0]))

	total = np.sum(S)

	components = 0
	accumulated = 0
	percent = 0

	log = []
	log.append((components, percent))

	while components < k:
		accumulated += S[components]
		percent = (accumulated/total)*100
		components += 1
		log.append((components, np.real(percent)))

	if overflow:
		return np.absolute(la.multi_dot([U[:,:k], np.diag(S[:k]), V[:k,:]])).astype(np.uint8), log
	else:
		return np.absolute(la.multi_dot([U[:,:k], np.diag(S[:k]), V[:k,:]])).clip(0, 255), log

