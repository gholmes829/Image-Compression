"""
Driver to handle inputs and configure compression.
"""

from core.image import Image
import os

class Driver:

	def __init__(self, argv: list, argc: int):
		"""
		argv: ./__main__.py [SOURCE] [ALGORITHM] [MODE] [COMPRESSION] [TARGET] [PREVENT OVERFLOW]
		"""
		self.name = argv[0]
		self.validExt = (".jpg", ".jpeg", ".png", ".tif")
		self.initialized = False
			
		if argc == 2:
			print(self.usage() + "\n")
		elif argc == 1 or argc > 8:
			print(self.usage())
			return

		print("Initializing...")		

		self.imgName = None
		self.source = None
		self.algorithm = None
		self.mode = None
		self.compression = None
		self.overflow = False
		self.shouldLog = False
		self.target = None

		self.resourcePath = os.path.join(os.getcwd(), "input")
		self.outputPath = os.path.join(os.getcwd(), "output")

		self.variances = {
			"low": 90.,
			"medium": 95.,
			"high": 99.99,
		}

		if argc >= 2:
			self.imgName = argv[1]
			self.source = argv[1]
			if argc >= 3:
				self.algorithm = argv[2]
				if argc >= 4:
					self.mode = argv[3]
					if argc >= 5:
						self.compression = argv[4]
						if argc >= 6:
							try:
								self.overflow = bool(int(argv[5]))
							except:
								self.overflow = None
								while self.overflow is None:
									try:
										choice = int(input("\nAllow overflow?\n\t1) True\n\t2) False\n\nChoice: "))-1
										if choice in {0, 1}:
											self.overflow = not bool(choice)
									except ValueError:
										pass
							if argc >= 7:
								try:
									self.shouldLog = bool(int(argv[6]))
								except:
									self.shouldLog = None
									while self.shouldLog is None:
										try:
											choice = int(input("\nLog data?\n\t1) True\n\t2) False\n\nChoice: "))-1
											if choice in {0, 1}:
												self.shouldLog = not bool(choice)
										except ValueError:
											pass
								if argc == 8:
									self.target = argv[7]

		if self.source is None or not self.validImageFile(self.source):  # get valid image file name
			choice = ""

			while not self.validImageFile(choice):
				print("\nSelect valid file from \"images\" folder or add more and restart.")
				available = os.listdir(self.resourcePath)

				if len(available) == 0:
					print("No images in \"images\" folder. You need to add more and try again...")
					return
				else:
					for imageName in available:
						print("\t- " + imageName)

				choice = input("\nChoice: ")
			self.source = os.path.join(self.resourcePath, choice)
		else:
			self.source = os.path.join(self.resourcePath, self.source)

		name = ""

		for l in self.imgName:
			if l != ".":
				name+=l
			else:
				break	

		self.image = Image(name, self.source)
	
		if self.algorithm is None or self.algorithm not in {"pca", "svd"}:  # check which algorithm user wants to use
			choice = 0
			options = {"1", "2"}
			print("\nWhich algorithm would you like to use?\n\t1) PCA\n\t2) SVD")

			while choice not in options:
				choice = input("\nChoice: ")
			if choice == "1":
				self.algorithm = "pca"
			else:  # choice == "2"
				self.algorithm = "svd"

		if self.algorithm == "svd" and not (self.mode is None or self.mode == "c"):
			print("Invalid mode for SVD. Setting mode to \"components\".")
			self.mode = "c"
			self.compression = None

		if self.mode is None or self.mode not in {"v", "c", "q"}:  # check which mode user wants to use
			if self.algorithm == "pca":
				choice = 0
				options = {"v", "c", "q"}
				print("\nWith which parameter would you like to determine compression?\n\tv) Variance\n\tc) Component\n\tq) Qualitative")
				while choice not in options:
					choice = input("\nChoice: ")
			else:  # self.algorithm == "svd"
				choice = "c"
			self.mode = choice

		if self.compression is None or not self.validCompression(self.mode, self.compression):  # get value for compression
			if self.mode == "v":  # mode is variance
				choice = -1
				print("\nHow much variance would you like to retain? (0, 100): ")		
				while not self.validCompression(self.mode, choice): 
					choice = input("\nChoice: ")

				choice = float(choice)
				
			elif self.mode == "c":  # mode is components
				choice = -1
				print("\nHow many components would you like to use? (0, " + str(self.image.data.shape[0]) + "): ")
				while not self.validCompression(self.mode, choice):
					choice = input("\nChoice: ")

				choice = int(choice)	
			
			else:  # mode is qualitative
				
				quality = {
					1: "high",
					2: "medium",
					3: "low",
				}

				choice = ""
				
				print("\nHow much quality would you like?\n\t1) High\n\t2) Medium\n\t3) Low")
				while not self.validCompression(self.mode, choice):
					choice = input("\nChoice: ")
					try:
						choice = int(choice)
						try:
							choice = quality[choice]
						except KeyError:
							choice = ""
					except ValueError:
						choice = ""

			self.compression = choice

		elif self.mode == "v":  # compression passed through command line
			self.compression = float(self.compression)

		elif self.mode == "c":  # compression passed through command line
			self.compression = int(self.compression)

		if self.target is not None:
			choice = self.target
			while not self.validExtension(choice):
				choice = input("\nInput valid target file name: ")
			self.target = choice
	
		if self.mode == "q":
			self.compression = self.variances[self.compression]
			self.mode = "v"

		self.initialized = True
				
	def usage(self) -> str:
		return  f"""\
{"o"+"="*85+"o"}
{"IMAGE COMPRESSOR!!!"}

Runs lossy image compression on images with choice parameters.

Usage:
	{self.name} [SOURCE] [ALGORITHM] [MODE] [COMPRESSION] [OVERFLOW] [TARGET]
	{self.name} [SOURCE] [ALGORITHM] [MODE] [COMPRESSION] [OVERFLOW]
	{self.name} [SOURCE] [ALGORITHM] [MODE] [COMPRESSION]
	{self.name} [SOURCE] [ALGORITHM] [MODE]
	{self.name} [SOURCE]

Note: If the former is used, user will complete parameters through terminal

Run image compression on image with valid extension: {self.validExt}

Algorithms:
	pca: Principal Component Analysis
	svd: Singular Value Decomposition

Modes:
	v: Select a percentage of variance to keep. Only valid if mode=pca.    
	c: Select a number of components to keep.
	q: Select compression level from predefined settings. Only valid if mode=pca.  

Compression ranges:
	Given mode...
		v -> float between 0 and 100
		c -> int
		q -> Either low, medium, or high quality

Overflow:
	1: True, values of pixels on one or more channels may overflow, resulting in cool noise
	0: False, prevent cool noise but retain maximum image quality
	Optional

Log:
	1: True, log data to logs/
	0: False do not log data to logs/
	Optional

Target:
	file name: name with valid extension which will be saved to "output" folder
	Optional

Examples:
	{self.name} tiger.jpg pca 1 95 tiger_pca_v_95.tif 0
	{self.name} flower.jpg svd 3 min
	{self.name} knight.png

{"o"+"="*85+"o"}"""

	def validImageFile(self, fileName: str) -> bool:
		availableImages = os.listdir(self.resourcePath)
		exists = fileName in availableImages
		extValid = self.validExtension(fileName)

		return exists and extValid

	def validExtension(self, fileName: str) -> bool:
		extValid = False		

		for ext in self.validExt:
			if ext in fileName:
				valid = True
				for i in range(1, len(ext)+1):
					if fileName[-1*i] != ext[-1*i]:
						valid = False
				if valid:
					return True
		return False
	
	def validCompression(self, mode: str, compression: int or float or str) -> bool:
		if mode == "v":
			try:
				return (0 <= float(compression) <= 100)
			except ValueError:
				return False
				
		elif mode == "c":
			try:
				return (0 <= int(compression) <= self.image.data.shape[0])
			except ValueError:
				return False
		else:  # mode == q
			return compression in {"low", "medium", "high"}
	
	def saveLog(self, name: str, data: list):
		"""
		Save data to text file in "logs"
		"""
		path = "logs/" + name + ".txt"
		
		f = open(path, "w+")
		print("Writing log files to " + path)
		for pt in data:
			f.write(str(pt[0])+" "+str(pt[1])+"\n")
		f.close()

	def run(self):
		if not self.initialized:
			return

		logs = self.image.compress(self.algorithm, self.mode, self.compression, overflow=self.overflow)

		print()
		
		if self.shouldLog:
			for channel, log in logs.items():
				name = self.image.name +"_"+self.algorithm+"_"+self.mode+"_"+str(self.compression).replace(".", "-")+"_"+channel+"_"+str(int(self.overflow))
				self.saveLog(name, log)
	
		if self.target is not None:
			path = os.path.join(self.outputPath, self.target)
			self.image.save(path)
		else:
			print("\nShowing image...")
			self.image.show()

