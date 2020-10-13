# PCA-Image-Compression

Usage: ./\__main__.py [SOURCE] [ALGORITHM] [MODE] [COMPRESSION] [TARGET] [PREVENT OVERFLOW]

Run image compression on image with valid extension: {'.png', '.tif', '.jpeg', '.jpg'}

Algorithms:
	pca: Principal Component Analysis
	svd: Singular Value Decomposition

Modes:
	v: Select a percentage of variance to keep. Only valid if mode=pca.    
	c: Select a number of components to keep.
	q: Select compression level from predefined settings. Only valid if mode=pca.  

Compression:
	Mode:
		v -> float between 0 and 100
		c -> int
		q -> Either low, medium, or high quality

Target:
	file name: name with valid extension which will be saved to "output" folder
	Note: If you would rather show the image but not save, omit this argument

Prevent Overflow:
	0: False, values of pixels on one or more channels may overflow, resulting in cool noise
	1: True, prevent cool noise and retain maximum image quality

Examples:
	./\__main__.py tiger.jpg pca 1 95 tiger_var95_pca.tif 0
	./\__main__.py flower.jpg svd 3 min flower_qualMin_svd.jpg 1
