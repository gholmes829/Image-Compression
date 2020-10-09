#!/usr/bin/env python3

import numpy as np
import numpy.linalg as la

# Testing new example independent of image
#data = np.array([[1., 2., 3.], [4., 5., 6.], [3., 4., 0.], [7., 1., 7.]])  # initial data		
data = np.array([[-1., 6., 5.], [1., 4., 3.], [0., 0., 10.], [1., 2., 3.]])		
samples = data.shape[0]		
variables = data.shape[1]
mean = data.mean(axis=0)  # mean of each column
std = data.std(axis=0)  # standard deviation of each column
centered = data-mean  # centered at origin
adjusted = centered/std  # variance 1 across each axis
covariance = np.dot(adjusted.T, adjusted)/samples  # X.T*X/(n-1) 
eigVal, eigVec = la.eig(covariance)  # find unit eigen vectors and eigen values of covariance matrix
	
order = eigVal.argsort()[::-1]
eigVal = eigVal[order]
eigVec = eigVec[:,order]

feature = eigVec.copy()  # don't remove any principal components
# good up to here
#feature[:,2] = np.zeros(variables).T
#feature[:,1] = np.zeros(variables).T
#feature[:,0] = np.zeros(variables).T
projected = np.dot(feature.T, adjusted.T).T
normalized = la.multi_dot([feature, feature.T, adjusted.T]).T  # data projected onto principal subspace 
restored = normalized*std+mean
simplified = np.float64(np.absolute(restored))
rounded = np.round(restored, 8)

print("\n\n\nTesting:")	

print("\nTest data:")
print(data)

print("\nMean:")
print(mean)

print("\nStd:")
print(std)

print("\nCentered:")
print(centered)

print("\nAdjusted:")
print(adjusted)

print("\nCovariance:")
print(covariance)

print("\nEigen vectors:")
print(eigVec)

print("\nEigen values:")
print(eigVal)

print("\nFeature matrx:")
print(feature)

print("\nProjected:")
print(projected)

print("\nNormalized:")
print(normalized)

print("\nRestored:")
print(restored)

print("\nSimplified:")
print(simplified)

print("\nRounded:")
print(rounded)

