"""

"""

import numpy as np
import numpy.linalg as la
from PIL import Image as IM
import matplotlib.pyplot as plt
import os

"""

Steps:
	1) Standardize and center data by: (original data - mean)/standard deviation
	2) Compute covariance matrix
	3) Compute eigen vectors and eigen values of covariance matrix (make sure eigen vectors are unit vectors)
	4) Order eigen vectors
	5) Use input to decide how much to reduce dimensions and create feature matrix
	6) Recast data by: new data = FM*FM^T*modded data*standard deviation + mean

Notes:
	- Calculate percent accuracy by looking at sum(eigenvalues for feature matrix)/sum(eigenvalues of covariance matrix)
	- Calculate error (?)
	- Consider complexity of operation, both as a whole and with images of different sizes/ color channels
	- Compare with SVD (?)
"""

class Image:
	def __init__(self, fileName):
		self.resourcePath = os.path.join(os.getcwd(), "images")
		self.path = os.path.join(self.resourcePath, fileName)
		print("\nLoading image data from " + self.path)
		self._img = IM.open(self.path)
		self.isRGB = self.mode == "RGB"
		self.data = ImageData(self._img)
		
		print("\t- operation was successful")
		print("\nDimensions of image: " + str(self.data.shape))		

	def makeBW(self):
		self._img = self.convert("L")
		self.data = ImageData(self._img)

	def compress(self, components):
		print("\nCompressing with "+str(components)+" components...")
		self.data._data = pca(self.data._data, components, self.isRGB)
		self.data.toInt()
		self._img = IM.fromarray(self.data)


	def save(self, name):
		path = os.path.join(self.resourcePath, name+".jpg")
		self._img.save(path)

	def __getattr__(self, key):
		if key == "_img":
			raise AttributeError()
		return getattr(self._img, key)

class ImageData:
	
	def __init__(self, image):
		self._data = np.asarray(image)
		self.isRGB = len(self.shape) == 3 and self.data.shape[2] == 3

	def toInt(self):
		minimum = self.min()
		maximum = self.max()
		diff = maximum-minimum
		self._data = ((self._data-minimum)/maximum) * 255
		self._data = self._data.astype(np.uint8)
	
	def __getattr__(self, key):
		if key == "_data":
			raise AttributeError()
		return getattr(self._data, key)

def pca(data, components, isRGB=True):
	rows = data.shape[0]		
	cols = data.shape[1]

	if isRGB:
		pass

	mean = data.mean(axis=0)  # mean of each column
	std = data.std(axis=0)  # standard deviation of each column
	centered = data-mean  # centered at origin
	adjusted = centered/std  # variance 1 across each axis
	covariance = np.dot(adjusted.T, adjusted)/rows  # X.T*X/(n-1) 
	eigVal, eigVec = la.eig(covariance)  # find unit eigen vectors and eigen values of covariance matrix
	order = eigVal.argsort()[::-1]
	eigVal = eigVal[order]
	eigVec = eigVec[:,order]

	feature = eigVec.copy()
	
	for i in range(1, feature.shape[1]-components + 1):
		feature[:,feature.shape[1]-i] = np.zeros(cols).T
	
	projected = np.dot(feature.T, adjusted.T).T
	normalized = la.multi_dot([feature, feature.T, adjusted.T]).T  # data projected onto principal subspace 
	restored = normalized*std+mean
	restored = np.absolute(restored).astype(np.float64)
	return restored
		
