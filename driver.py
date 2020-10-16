"""
Driver to handle inputs and configure compression.

Classes:
	Driver
"""

from core.image import Image
import os

class Driver:
	def __init__(self, argv: list, argc: int):
		"""
		argv: ./__main__.py [SOURCE] [ALGORITHM] [MODE] [COMPRESSION] [OVERFLOW] [TARGET]
		argc: number of command line arguments

		Methods:
			validImageFile
			validExtension
			validCompression
			saveLog
			run
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
		self.path = None
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

		# parse cmd line arguments and get user input
		if argc >= 2:
			imgName = argv[1]
			self.source = argv[1]  # will get changed to full path later
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
								self.overflow = not bool(self.getValidInput("\nAllow overflow?\n\t1) True\n\t2) False", int, valid={1, 2})-1)
							if argc >= 7:
								try:
									self.shouldLog = bool(int(argv[6]))
								except:
									self.shouldLog = not bool(self.getValidInput("\nLog data?\n\t1) True\n\t2) False: ", int, valid={1, 2})-1)
								if argc == 8:
									self.target = argv[7]
									if not self.validExtension(self.target):
										self.target = self.getValidInput("\nInput valid target file name: ", str, isValid=self.validExtension)

		if self.source is None or not self.validImageFile(self.source):  # get valid image file name
			available = os.listdir(self.resourcePath)

			if len(available) == 0:
				print("No images in \"images\" folder. Add more and try again...")
				return

			options = ""

			for imageName in available:
				options += "\n\t- " + imageName

			self.source = self.getValidInput("\nSelect valid file from \"images\" folder."+options, str, isValid=self.validImageFile)
		
		self.path = os.path.join(self.resourcePath, self.source)

		self.imgName = ""

		for l in imgName:
			if l != ".":
				self.imgName += l
			else:
				break

		self.image = Image(self.imgName, self.path)
	
		if self.algorithm is None or self.algorithm not in {"pca", "svd"}:  # check which algorithm user wants to use
			choice = self.getValidInput("\nWhich algorithm would you like to use?\n\t1) PCA\n\t2) SVD", int, valid={1, 2})
			if choice == 1:
				self.algorithm = "pca"
			else:  # choice == 2
				self.algorithm = "svd"

		if self.mode is None or self.mode not in {"v", "c", "q"}:  # check which mode user wants to use
			if self.algorithm == "pca":
				choice = self.getValidInput("\nHow would you like to determine compression?\n\tv) Variance\n\tc) Component\n\tq) Qualitative", str, valid={"v", "c", "q"})
			else:  # self.algorithm == "svd"
				choice = "c"
			self.mode = choice

		if self.algorithm == "svd" and not self.mode == "c":
			print("Invalid mode for SVD: " + str(self.mode) + "\n\t- setting mode to \"c\", \"components\"")
			self.mode = "c"
			self.compression = None

		if self.compression is None or not self.validCompression(self.mode, self.compression):  # get value for compression
			if self.mode == "v":  # mode is variance
				choice = self.getValidInput("\nHow much variance would you like to retain? (0, 100): ", float, lower=0, upper=100)
				
			elif self.mode == "c":  # mode is components
				choice = self.getValidInput("\nHow many components would you like to use? (0, " + str(self.image.data.shape[0]) + "): ", int, lower=0, upper=self.image.data.shape[0])
		
			else:  # mode is qualitative
				quality = {
					1: "high",
					2: "medium",
					3: "low",
				}

				choice = quality[self.getValidInput("\nHow much quality would you like?\n\t1) High\n\t2) Medium\n\t3) Low", int, valid={1, 2, 3})]
			
			self.compression = choice

		elif self.mode == "v":  # compression passed through command line
			self.compression = float(self.compression)

		elif self.mode == "c":  # compression passed through command line
			self.compression = int(self.compression)

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
	{self.name} tiger.jpg pca 1 95 1 0 tiger_pca_v_95.tif
	{self.name} flower.jpg svd 3 min 1
	{self.name} knight.png

{"o"+"="*85+"o"}"""

	def validImageFile(self, fileName: str) -> bool:
		"""
		Determine whether image file is in "input" folder and whether it has a proper extension

		fileName: name of file w/o full path

		Returns: True/ False
		"""
		availableImages = os.listdir(self.resourcePath)
		exists = fileName in availableImages
		extValid = self.validExtension(fileName)
		return exists and extValid

	def validExtension(self, fileName: str) -> bool:
		"""
		Determine whether image file has proper extension

		fileName: name of file w/o full path

		Returns: True/ False
		"""
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
		"""
		Determines whether "compression" value is valid given "mode" parameter

		mode: mode to use, either "v", "v", or "q"
		compression: degree of compression associated with mode

		Returns: True/ False
		"""
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

	def getValidInput(self, msg: str, dtype: any, lower: float=None, upper: float=None, valid: set=None, isValid: callable=None) -> any:
		print(msg)
		while True:
			try:
				choice = dtype(input("\nChoice: "))
			except ValueError:
				continue

			if (lower is not None and choice < lower) or \
				(upper is not None and choice > upper) or \
				(valid is not None and choice not in valid) or \
				(isValid is not None and not isValid(choice)):
				continue

			return choice
	
	def saveLog(self, name: str, data: list):
		"""
		Save log data to text file in "logs" folder
		
		name: name of log
		data: data to write to log file
		"""
		path = "logs/" + name + ".txt"
		
		f = open(path, "w+")
		print("Writing log files to " + path)
		for pt in data:
			f.write(str(pt[0])+" "+str(pt[1])+"\n")
		f.close()

	def run(self):
		"""
		Run compression, handle saving image and logging data.
		"""
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

