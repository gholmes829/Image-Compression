"""
Popular matrix decompositions for lossy image compression.

Methods:
	PCA
	SVD
	logData
"""

import numpy as np
import numpy.linalg as la

def pca(data: np.array, mode, compression, overflow=False) -> (np.array, list):
	"""
	Principal component analysis

	mode:
		v: Percentage of variance to keep   
		c: Number of components to keep.
	
	Value corresponding to mode in compression arg
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
		#print("\nTotal possible variance for channel: " + str(round(np.real(total), 3)))
		while round(percent, 1) < compression:  # need to keep increasing components
			accumulated += eigVal[pcs]
			percent = (accumulated/total)*100
			pcs += 1
			log.append((pcs, np.real(percent)))

			#if ((np.real(percent) < 50 or np.real(percent) >= 99.95 or np.real(percent) >= compression) and pcs%1==0) \
			#	or (50 <= np.real(percent) < 70 and pcs%2==0) \
			#	or (70 <= np.real(percent) < 85 and pcs%3==0) \
			#	or (85 <= np.real(percent) < 95 and pcs%5==0) \
			#	or (95 <= np.real(percent) < 99 and pcs%10==0):
			#	print("\t- accumulated " + str(pcs) + " component(s): " + str(round(np.real(variance), 2)) + " (" + str(round(np.real(percent), 2)) + "%)")
		
		#print("\n\t- using " + str(pcs) + " components to achieve " + str(round(np.real(percent), 2)) + "% variance\n") 

	elif mode == "c":
		#print("\nUsing " + str(compression) + " components...")
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

def svd(data: np.array, mode, k, overflow=False) -> np.array:
	"""
	Singular value decomposition
	"""
	U, S, V = np.linalg.svd(data)
	k = np.min((k, S.shape[0]))

	total = np.sum(S)
	
	log = []

	components = 0
	accumulated = 0
	percent = 0

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





