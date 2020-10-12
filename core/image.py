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
	if type(compression) == float:
		mode = "variance"
	elif type(compression) == int:
		mode = "components"
	elif type(compression) == str:
		mode = "degree"
		percentVar = {
			"min": 99.99,
			"medium": 97.5,
			"high": 92.5,
		}
		
		print("\nUsing approximately " + str(percentVar[compression]) + "% variance for \"" + compression + "\" compression")
		return pca(data, percentVar[compression])

	rows, cols = data.shape

	mean, std = data.mean(axis=0), data.std(axis=0)  # mean and std of each column
	standardized = (data-mean)/std  # variance 1 across each axis

	covariance = np.dot(standardized, standardized.T)/cols  # X.T*X/(n) 

	eigVal, eigVec = la.eig(covariance)  # find unit eigen vectors and eigen values of covariance matrix
	order = eigVal.argsort()[::-1]  # sort by descending order
	eigVal = eigVal[order]
	eigVec = eigVec[:,order]

	total = eigVal.sum()

	if mode == "variance":
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

	elif mode == "components":
		pcs = compression
	
	feature = eigVec.copy()[:, 0:pcs]  # compress image by removing columns
	
	projected = np.dot(feature.T, standardized)  
	inverseTransform = la.multi_dot([feature, feature.T, standardized])  # data projected onto principal subspace and then normalized with respect to original basis
	normalized = np.absolute(inverseTransform*std+mean)  # normalize data by elimating negatives and complex values for image data 
	return normalized

class Image:
	validExt = {".jpg", ".jpeg", ".png", ".tif"}

	def __init__(self, fileName):
		self.resourcePath = os.path.join(os.getcwd(), "images")
		self.outputPath = os.path.join(os.getcwd(), "output")
		self.imagePath = os.path.join(self.resourcePath, fileName)

		availableImages = os.listdir(self.resourcePath)

		if fileName not in availableImages:
			raise ValueError("\"" + fileName + "\" is not in images folder! Add file to images folder to use.")

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
			raise ValueError("Invalid extension for file: " + fileName)

		print("\nLoading image data from " + self.imagePath)
		self._img = IM.open(self.imagePath)
		self.isRGB = self._img.mode == "RGB"
		self.data = ImageData(self._img)
		
		print("\t- dimensions of image: " + str(self.data.shape))
		print("\t- image mode: " + self._img.mode)
		print("\nImage loaded successfully!")		

	def makeBW(self):
		self._img = self._img.convert("L")
		self.isRGB = False
		self.data = ImageData(self._img)
		

	def compress(self, compression, preventOverflow=False):
		timer = time()
		if self.isRGB:
			print("\t- RGB: "+str(self.isRGB))
			r = self.data._data[:,:,0]
			g = self.data._data[:,:,1]
			b = self.data._data[:,:,2]
			
			print("\t- by channel (r, g, b)")
			d_r, d_g, d_b = pca(r, compression), pca(g, compression), pca(b, compression)
			
			if preventOverflow:
				self.data._data = np.dstack((d_r, d_g, d_b))
				self.data.toUint8()
			else:
				self.data._data = np.array(np.dstack((d_r, d_g, d_b)), dtype=np.uint8)

			self._img = IM.fromarray(self.data._data)
		else:
			print("\t- by luminosity")
			self.data._data = np.array(pca(self.data._data, compression), dtype=np.uint8)
			print(self.data._data.dtype)
			self._img = IM.fromarray(self.data._data)
		print("\nOperation took " + str(round(time()-timer, 2)) + " secs")

	def save(self, name):
		path = os.path.join(self.outputPath, name+self.ext)
		print("\nSaving image to: " + str(self.outputPath) + " as " + name+self.ext)
		self._img.save(path)

	def show(self):
		self._img.show()

class ImageData:
	
	def __init__(self, image):
		self._data = np.array(image)
		self.isRGB = len(self.shape) == 3 and self.data.shape[2] == 3
	
	def toUint8(self):
		minimum = self.min()
		maximum = self.max()
		diff = maximum-minimum
		self._data = (((self._data-minimum)/maximum) * 255).astype(np.uint8)

	def __getattr__(self, key):
		if key == "_data":
			raise AttributeError()
		return getattr(self._data, key)
		
