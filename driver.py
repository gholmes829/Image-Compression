"""

"""

from core.image import Image

class Driver:

	def __init__(self):
		print("IMAGE COMPRESSOR")

	def run(self, fileName=None, mode=None, compression=None, convertBW=None):
		if fileName is not None:
			print("\nSome parameters inferred from command line arguments")

		if fileName is None:
			fileName = input("\nInput file name (needs to exist in \"images\" directory): ")

		image = Image(fileName)
		
		if convertBW is None:
			convertBW = input("\nConvert image to black and white? (y/n): ")
			convertBW = convertBW == "y" or convertBW == "Y"
		else:
			convertBW = bool(int(convertBW))

		if convertBW:
			print("Converting image to black and white...")
			image.makeBW()
		
		if mode is None:
			print("\nWith which parameter would you like to determine compression?")
			mode = int(input("\t1) Variance\n\t2) Component\n\t3) Qualitative\n\nChoice: "))

		if compression is None:
			if mode == 1:
				print("\t- mode set to \"variance\"...")
				compression = float(input("\nHow much variance would you like to retain? (0, 100): "))
				print("\nRetaining approximately " + str(compression) + "% variation")				
				
			elif mode == 2:
				print("\t- mode set to \"components\"...")
				compression = int(input("\nHow many components would you like to use? (0, " + str(image.data.shape[1]) + "): "))
				print("Using " + str(compression) + " components...")				
			
			elif mode == 3:
				print("\t- mode set to \"qualitative\"...")
				print("\nSelect degree of compression:")
				degrees = {
					1: "min",
					2: "medium",
					3: "high",
				}

				compression = degrees[int(input("\t1) Min (retain max quality)\n\t2) Medium\n\t3) High\n\nChoice: "))]
				print("\t- mode set to \"" + compression + "\"...")	
		elif int(mode) == 1:
			compression = float(compression)
		elif int(mode) == 2:
			compression = int(compression)
		
		image.compress(compression)

		print("\nShowing image...")
		image.show()

		shouldSave = input("\nSave compressed image? (y/n): ")
		shouldSave = shouldSave == "y" or shouldSave == "Y"

		if shouldSave:
			name = input("\nEnter name to save image as (no extensions): ")
			print("\t- saving image as \"" + name + "\"...")
			image.save(name)

		
		
		#toTest = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 25, 30, 40, 50, 60, 70, 80, 90, 100, 125, 150, 175, 200, 300, 400, 800]
		
		#for c in toTest:
			#image = Image(fileName)
			#image.makeBW()
			#image.compress(c)
			#image.save("test#"+str(c))
			#image.show()
		
		

