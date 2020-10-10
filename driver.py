"""

"""

from core.image import Image

class Driver:

	def __init__(self):
		print("IMAGE COMPRESSOR")

	def run(self, fileName=None, convertBW=None, accuracy=None):
		
		image = Image(fileName)
		
		if convertBW is None:
			convert = input("\nConvert image to black and white? (y/n): ")
		convert = convert == "y" or convert == "Y" or (convertBW is not None and convertBW)
		if convert:
			image.makeBW()

		compression = float(input("\nHow compressed? (0, 100): "))

		image.compress(compression)

		shouldSave = input("\nSave compressed image? (y/n): ")
		shouldSave = shouldSave == "y" or shouldSave == "Y"
		if shouldSave:
			name = input("\nEnter name to save image as (no extensions): ")
			image.save(name)

		image.show()
		
		#toTest = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 25, 30, 40, 50, 60, 70, 80, 90, 100, 125, 150, 175, 200, 300, 400, 800]
		
		#for c in toTest:
			#image = Image(fileName)
			#image.makeBW()
			#image.compress(c)
			#image.save("test#"+str(c))
			#image.show()
		
		

