"""

"""

from core.image import Image

class Driver:

	def __init__(self):
		print("Image compressor...")

	def run(self, fileName):
		
		image = Image(fileName)
		image.makeBW()
		image.compress(50)
		image.show()
		
		"""
		toTest = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 125, 150, 175, 200, 300, 400, 800]
		
		for c in toTest:
			image = Image(fileName)
			image.makeBW()
			image.compress(c)
			image.save("test#"+str(c))
			#image.show()
		"""
		

