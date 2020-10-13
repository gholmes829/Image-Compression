# PCA-Image-Compression
Runs lossy image compression on images with choice parameters.  
  
## Usage:
* `./__main__.py [SOURCE] [ALGORITHM] [MODE] [COMPRESSION] [TARGET] [PREVENT OVERFLOW]`  
* `./__main__.py [SOURCE] [ALGORITHM] [MODE] [COMPRESSION]`  
* `./__main__.py [SOURCE]`  

_Note: If the former is used, user will complete parameters through terminal_
    
## Source:
* Select file from "images" folder with valid extension:
  * .jpg
  * .jpeg
  * .png
  * .tif
  
## Algorithms:
* pca: Principal Component Analysis
* svd: Singular Value Decomposition
  
## Modes:
* v: Select a percentage of **variance** to keep  
* c: Select a number of **components** to keep
* q: Select **quality** from predefined settings
  
_Note: If using algorithm=svd, only mode=c is valid_  
  
## Compression:
Compression | Mode=v | Mode=c | Mode=q
------------|--------|--------|-------
**Type and Range** | float between 0 and 100 | int between zero and image height | low, medium, or high
**Valid for** | pca | pca, svd | pca
  
## Target:
* file name: name with valid extension which will be saved to "output" folder
  
_Note: If you would rather show the image but not save, omit this argument_
  
## Prevent Overflow:
* 0: False, values of pixels on one or more channels may overflow, resulting in cool noise
* 1: True, prevent cool noise but retain maximum image quality
  
## Examples:
*  `./__main__.py tiger.jpg pca 1 95 tiger_pca_v_95.tif 0`  
*  `./__main__.py flower.jpg svd 3 min`  
*  `./__main__.py knight.png>`  
