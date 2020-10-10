"""

"""

import numpy as np
import numpy.linalg as la
from PIL import Image as IM
import matplotlib.pyplot as plt
import os
from time import time

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

def pca(data, compression):
	rows = data.shape[0]		
	cols = data.shape[1]

	mean = data.mean(axis=0)  # mean of each column
	std = data.std(axis=0)  # standard deviation of each column
	centered = data-mean  # centered at origin
	adjusted = centered/std  # variance 1 across each axis
	covariance = np.dot(adjusted.T, adjusted)/rows  # X.T*X/(n-1) 
	eigVal, eigVec = la.eig(covariance)  # find unit eigen vectors and eigen values of covariance matrix
	order = eigVal.argsort()[::-1]
	eigVal = eigVal[order]
	eigVec = eigVec[:,order]

	total = eigVal.sum()

	percentVar = 0
	components = 0
	print("\nTotal: " + str(total))
	while round(percentVar, 2) < compression:  # need to keep increasing components
		percentVar += (eigVal[components]/total)*100
		components += 1
		print("\t" + str(round(eigVal[components], 3)) + ", " + str(round(percentVar, 3)))
	
	print("Using " + str(components) + " components to achieve " + str(round(percentVar, 2)) + "% variance:") 

	feature = eigVec.copy()

	for i in range(1, min(rows, cols)-components + 1):
		feature[:,feature.shape[1]-i] = np.zeros(cols).T
	
	projected = np.dot(feature.T, adjusted.T).T
	normalized = la.multi_dot([feature, feature.T, adjusted.T]).T  # data projected onto principal subspace 
	restored = normalized*std+mean
	restored = np.absolute(restored).astype(np.float64)
	return restored

class Image:
	validExt = {".jpg", ".jpeg", ".png"}

	def __init__(self, fileName):
		self.resourcePath = os.path.join(os.getcwd(), "images")
		self.outputPath = os.path.join(os.getcwd(), "output")
		self.imagePath = os.path.join(self.resourcePath, fileName)

		availableImages = os.listdir(self.resourcePath)

		if fileName not in availableImages:
			raise ValueError(fileName + " is not in resources folder!!!")

		self.ext = None

		for ext in Image.validExt:
			if ext in fileName:
				valid = True
				for i in range(1, len(ext)+1):
					if fileName[-1*i] != ext[-1*i]:
						valid = False
				if valid:
					self.ext = ext
		
		if self.ext is None:
			raise ValueError("Invalid filename for image: " + fileName)

		print("\nLoading image data from " + self.imagePath)
		self._img = IM.open(self.imagePath)
		self.isRGB = self.mode == "RGB"
		self.data = ImageData(self._img)
		
		print("\t- dimensions of image: " + str(self.data.shape))
		print("\t- image mode: " + self._img.mode)
		print("\nImage loaded successfully!")		

	def makeBW(self):
		self._img = self.convert("L")
		self.isRGB = False
		self.data = ImageData(self._img)
		

	def compress(self, compression):
		if compression < 0 or compression > 100:
			raise ValueError(str(compression) + " is not between 0 and 100!")
		#componentsRange = [0, min([self.data.shape[0], self.data.shape[1]]))]
		print("\nCompressing with "+str(compression)+"% compression...")
		#print("Components in range: " + str(componentsRange))
		timer = time()
		if self.isRGB:
			r = self.data._data[:,:,0]
			g = self.data._data[:,:,1]
			b = self.data._data[:,:,2]
			
			d_r, d_g, d_b = pca(r, compression), pca(g, compression), pca(b, compression)
			self.data._data = np.dstack((d_r, d_g, d_b))
			self.data.floatToInt()
			self._img = IM.fromarray(self.data)
		else:
			self.data._data = pca(self.data._data, compression)
			self.data.floatToInt()
			self._img = IM.fromarray(self.data)
		print("\t- operation took " + str(round(time()-timer, 2)) + " secs")

	def save(self, name):
		path = os.path.join(self.outputPath, name+self.ext)
		print("\nSaving image to: " + str(self.outputPath) + " as " + name+self.ext)
		self._img.save(path)

	def __getattr__(self, key):
		if key == "_img":
			raise AttributeError()
		return getattr(self._img, key)

class ImageData:
	
	def __init__(self, image):
		self._data = np.asarray(image)
		self.isRGB = len(self.shape) == 3 and self.data.shape[2] == 3

	def floatToInt(self):
		minimum = self.min()
		maximum = self.max()
		diff = maximum-minimum
		self._data = ((self._data-minimum)/maximum) * 255
		self._data = self._data.astype(np.uint8)
	
	def __getattr__(self, key):
		if key == "_data":
			raise AttributeError()
		return getattr(self._data, key)
		
