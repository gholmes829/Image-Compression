"""

"""

import numpy as np

from PIL import Image as IM
import matplotlib.pyplot as plt
from time import time

from core.decomposition import pca, svd

class Image:
	
	def __init__(self, path):
		self.path = path
		print("Loading image data from " + self.path)
		self._img = IM.open(self.path)
		self.mode = self._img.mode
		self.data = ImageData(self._img)
		
		print("\nImage loaded successfully!")
		print("\t- dimensions of image: " + str(self.data.shape))
		print("\t- image mode: " + self.mode)

	def compress(self, algorithm, mode, compression, preventOverflow=True):
		variances = {
			"low": 90.,
			"medium": 95.,
			"high": 99.99,
		}

		algorithms = {
			"pca": pca,
			"svd": svd,
		}

		algorithm = algorithms[algorithm]

		if mode == "q":
			mode = "v"
			compression = variances[compression]

		timer = time()
		
		if preventOverflow:
			for channel in range(0, len(self._img.getbands())):
				self.data._data[:, :, channel] = algorithm(self.data._data[:, :, channel], mode, compression).clip(0, 255)
		else:
			for channel in range(0, len(self._img.getbands())):
				self.data._data[:, :, channel] = algorithm(self.data._data[:, :, channel], mode, compression).astype(np.uint8)

		"""
		if self.isRGB:
			print("\t- RGB: "+str(self.isRGB))
			r = self.data._data[:,:,0]
			g = self.data._data[:,:,1]
			b = self.data._data[:,:,2]
			
			print("\t- by channel (r, g, b)")
			d_r, d_g, d_b = pca(r, compression), pca(g, compression), pca(b, compression)
			
			if preventOverflow:
				self.data._data = np.array(np.dstack((d_r, d_g, d_b)).clip(0, 255), dtype=np.uint8)
			else:
				self.data._data = np.array(np.dstack((d_r, d_g, d_b)), dtype=np.uint8)

			self._img = IM.fromarray(self.data._data)
		else:
			print("\t- by luminosity")
			self.data._data = np.array(pca(self.data._data, compression), dtype=np.uint8)
			print(self.data._data.dtype)
			self._img = IM.fromarray(self.data._data)
		"""
		self._img = IM.fromarray(self.data._data)
		print("\nOperation took " + str(round(time()-timer, 2)) + " secs")

	def save(self, path):
		print("\nSaving image as: " + str(path))
		self._img.save(path)

	def show(self):
		self._img.show()

class ImageData:
	
	def __init__(self, image):
		self._data = np.array(image)
		self.isRGB = len(self.shape) == 3 and self.data.shape[2] == 3

	def __getattr__(self, key):
		if key == "_data":
			raise AttributeError()
		return getattr(self._data, key)
		
