"""
Classes to wrap and manage images

Classes:
	Image
"""

import numpy as np
from PIL import Image as IM
import matplotlib.pyplot as plt
from time import time

from core.reduction import pca, svd

class Image:
	"""
	Wrapper for PIL Image
	"""
	def __init__(self, name: str, path: str):
		self.name = name
		self.path = path
		print("\nLoading image data from " + self.path)
		self._img = IM.open(self.path)
		self.mode = self._img.mode
		self.data = np.array(self._img)

		self.algorithms = {
			"pca": pca,
			"svd": svd,
		}

		print("\nImage loaded successfully!")
		print("\t- dimensions of image: " + str(self.data.shape))
		print("\t- image mode: " + self.mode)

	def compress(self, algorithm: str, mode: str, compression: int or float, overflow=False) -> dict:
		reduceDimensions = self.algorithms[algorithm]
		channels = self._img.getbands()

		timer = time()

		logs = {}

		for channel in range(0, len(channels)):
			print("\nCALCULATING: [" + str(channels[channel]) + "]")

			self.data[:, :, channel], log = reduceDimensions(self.data[:, :, channel], mode, compression, overflow=overflow)
			logs[channels[channel]] = log

		self._img = IM.fromarray(self.data)
		print("\nOperation took " + str(round(time()-timer, 2)) + " secs")
		return logs

	def save(self, path: str):
		print("\nSaving image as: " + str(path))
		self._img.save(path)

	def show(self):
		self._img.show()

