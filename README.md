# PCA-Image-Compression
  
IMAGE COMPRESSOR!!!
  
Usage:  
* ./\__main__.py [SOURCE] [ALGORITHM] [MODE] [COMPRESSION] [TARGET] [PREVENT OVERFLOW]  
* ./\__main__.py [SOURCE]  

Note: If the former is used, user will complete parameters through terminal

Run image compression on image with valid extension: ('.jpg', '.jpeg', '.png', '.tif')

Algorithms:
* pca: Principal Component Analysis
* svd: Singular Value Decomposition

Modes:
* v: Select a percentage of variance to keep. Only valid if mode=pca.    
* c: Select a number of components to keep.
* q: Select compression level from predefined settings. Only valid if mode=pca.  

Compression ranges:
	Given mode...
		v -> float between 0 and 100
		c -> int
		q -> Either low, medium, or high quality

Target:
	file name: name with valid extension which will be saved to "output" folder
	
	Note: If you would rather show the image but not save, omit this argument

Prevent Overflow:
	0: False, values of pixels on one or more channels may overflow, resulting in cool noise
	1: True, prevent cool noise but retain maximum image quality

Examples:
> ./\__main__.py tiger.jpg pca 1 95 tiger_pca_v_95.tif 0
> ./\__main__.py flower.jpg svd 3 min
> ./\__main__.py knight.png
