"""

"""

from core.image import Image

class Driver:

	def __init__(self, argv, argc):
		self.fileName = None
		self.mode = None
		self.compression = None
		self.convertBW = None

		if argc >= 2:
			self.fileName = argv[1]
		if argc >= 3:		
			self.mode = argv[2]
		if argc >= 4:		
			self.compression = argv[3]
		if argc >= 5:
			self.convertBW = argv[4]

		print("IMAGE COMPRESSOR")

		if self.fileName is None:  # get file name
			self.fileName = input("\nInput file name (needs to exist in \"images\" directory): ")
			self.inferred = False
		else:  # at least 1 parameter passed from command line
			self.inferred = True
			print("\nSome parameters inferred from command line arguments")

		if self.convertBW is None:  # check if user wants to convert
			convertBW = input("\nConvert image to black and white? (y/n): ")
			self.convertBW = convertBW == "y" or convertBW == "Y"
		else:
			self.convertBW = bool(int(self.convertBW))
	
		if self.mode is None:  # check which mode user wants to use
			print("\nWith which parameter would you like to determine compression?")
			self.mode = int(input("\t1) Variance\n\t2) Component\n\t3) Qualitative\n\nChoice: "))

		if self.compression is None:  # get value for compression
			if self.mode == 1:  # mode is variance
				print("\t- mode set to \"variance\"...")
				self.compression = float(input("\nHow much variance would you like to retain? (0, 100): "))
				print("\nRetaining approximately " + str(self.compression) + "% variation")				
				
			elif self.mode == 2:  # mode is components
				print("\t- mode set to \"components\"...")
				self.compression = int(input("\nHow many components would you like to use? (0, " + str(image.data.shape[0]) + "): "))
				print("Using " + str(self.compression) + " components...")				
			
			elif self.mode == 3:  # mode is qualitative
				print("\t- mode set to \"qualitative\"...")
				print("\nSelect degree of compression:")
				degrees = {
					1: "min",
					2: "medium",
					3: "high",
				}

				self.compression = degrees[int(input("\t1) Min (retain max quality)\n\t2) Medium\n\t3) High\n\nChoice: "))]
				print("\t- mode set to \"" + self.compression + "\"...")	

		elif int(self.mode) == 1:
			self.compression = float(self.compression)

		elif int(self.mode) == 2:
			self.compression = int(self.compression)

	def run(self):
		image = Image(self.fileName)

		if self.convertBW:
			print("Converting image to black and white...")
			image.makeBW()
		
		image.compress(self.compression)

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
		
		

