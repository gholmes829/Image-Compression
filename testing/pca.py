#!/usr/bin/env python3

import numpy as np
import numpy.linalg as la
import matplotlib.pyplot as plt
from math import ceil

plt.style.use(["dark_background"])
plt.rc("grid", linestyle="dashed", color="white", alpha=0.5) 

def fitFunc(x, a, b):
    return a*x + b

# Testing new example independent of image		
data = np.array([(-1., 1.), (0., -2.), (-6, 5), (-8., 4.), (1., -2.), (-5., 2.), (-2., 2.), (2., -1.)])	

samples = data.shape[0]		
variables = data.shape[1]
mean = data.mean(axis=0)  # mean of each column
std = data.std(axis=0)  # standard deviation of each column
centered = data-mean  # centered at origin
adjusted = centered/std  # variance 1 across each axis
covariance = np.dot(adjusted.T, adjusted)/(samples)  # X.T*X/(n) 
eigVal, eigVec = la.eig(covariance)  # find unit eigen vectors and eigen values of covariance matrix
	
order = eigVal.argsort()[::-1]
eigVal = eigVal[order]
eigVec = eigVec[:,order]

feature = eigVec.copy()  # don't remove any principal components

feature[:,1] = np.zeros(variables).T
varianceLeft = eigVal[0]/eigVal.sum()

projected = np.dot(feature.T, adjusted.T).T
normalized = la.multi_dot([feature, feature.T, adjusted.T]).T  # data projected onto principal subspace 
restored = normalized*std+mean
simplified = np.float64(np.absolute(restored))
rounded = np.round(restored, 8)

print("Testing:")	

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

print("\nVariance Retained with 1 Principal Component:")
print("\t" + str(round(varianceLeft*100, 2)) + "%")

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

x1 = data[:,0]
y1 = data[:,1]

x2 = restored[:,0]
y2 = restored[:,1]

a = (y2[1]-y2[0])/(x2[1]-x2[0])
b = y2[0]-a*x2[0]

x_fit = []
y_fit = []

min_x2 = min(x2)
max_x2 = max(x2)

for i in range(-1, ceil(abs(max_x2-min_x2)+1)):
    x_fit.append(i-abs(min_x2))
    y_fit.append(fitFunc(i-abs(min_x2), a, b))

x_fit = np.array(x_fit)
y_fit = np.array(y_fit)


plt.figure()

plt.subplot(211)
plt.title("Original Data")
plt.xlabel("x")
plt.ylabel("y")
plt.grid(True)
plt.scatter(x1, y1, s=75, c="red", label="Data")
plt.legend(loc="upper right")

plt.subplot(212)
plt.title("Reconstructed Data with 1 Principal Component")
plt.xlabel("x")
plt.ylabel("y")
plt.grid(True)
plt.scatter(x2, y2, c="red", s=75, zorder=2, label="Reconstructed Data")
plt.plot(x_fit, y_fit, "-r", c="white", linewidth=2, zorder=1, alpha=0.5, label="Best Fit")
plt.legend(loc="upper right")

plt.tight_layout()
plt.show()
