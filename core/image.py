"""

"""

import numpy as np
from matplotlib.image import imread
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

class ImageData:
	
	def __init__(self, fileName):
		resourcePath = os.path.join(os.getcwd(), "images")
		self.path = os.path.join(resourcePath, fileName)
		print("Loading image data from " + self.path)
		self.data = imread(self.path)
		print("\t- operation was successful")

		print("\nDimensions of image: " + str(self.data.shape))
		
