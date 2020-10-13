"""
Contains classes to manage image and image data.

Classes:
	Image
	Image data
"""

import numpy as np
from pathlib import Path
from PIL import Image as IM
import matplotlib.pyplot as plt
from time import time

from core.decomposition import pca, svd

class Image:
	"""
	Wrapper for PIL Image
	"""
	def __init__(self, path):
		self.path = path
		self.name = Path(self.path).stem
		print("\nLoading image data from " + self.path)
		self._img = IM.open(self.path)
		self.mode = self._img.mode
		self.data = ImageData(self._img)

		print("\nImage loaded successfully!")
		print("\t- dimensions of image: " + str(self.data.shape))
		print("\t- image mode: " + self.mode)

	def compress(self, algorithm: str, mode: str, compression: str or int or float, preventOverflow: bool, log=False):
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

		channels = self._img.getbands()

		timer = time()

		if preventOverflow:
			for channel in range(0, len(channels)):
				if log:
					name = self.name+"_"+algorithm.__name__+"_"+mode+"_"+str(int(compression))+"_"+channels[channel]+"_"+str(int(preventOverflow))
				else:
					name = None
				print("\nCALCULATING: [" + str(channels[channel]) + "]")
				self.data._data[:, :, channel] = algorithm(self.data._data[:, :, channel], mode, compression, log=name).clip(0, 255)
		else:
			for channel in range(0, len(self._img.getbands())):
				if log:
					name = self.name+"_"+algorithm.__name__+"_"+mode+"_"+str(int(compression))+"_"+channels[channel]+"_"+str(int(preventOverflow))
				else:
					log=None
				self.data._data[:, :, channel] = algorithm(self.data._data[:, :, channel], mode, compression, log=name).astype(np.uint8)

		self._img = IM.fromarray(self.data._data)
		print("\nOperation took " + str(round(time()-timer, 2)) + " secs")

	def save(self, path: str):
		print("\nSaving image as: " + str(path))
		self._img.save(path)

	def show(self):
		self._img.show()

class ImageData:
	"""
	Wrapper for np.array
	"""
	def __init__(self, image):
		self._data = np.array(image)
		self.isRGB = len(self.shape) == 3 and self.data.shape[2] == 3

	def __getattr__(self, key):
		if key == "_data":
			raise AttributeError()
		return getattr(self._data, key)
		
