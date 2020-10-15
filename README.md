# PCA-Image-Compression
Runs lossy image compression on images with choice parameters.  
  
## Usage:
* `./__main__.py [SOURCE] [ALGORITHM] [MODE] [COMPRESSION] [OVERFLOW] [LOG DATA] [TARGET]`
* `./__main__.py [SOURCE] [ALGORITHM] [MODE] [COMPRESSION] [OVERFLOW] [LOG DATA]`
* `./__main__.py [SOURCE] [ALGORITHM] [MODE] [COMPRESSION] [OVERFLOW]`
* `./__main__.py [SOURCE] [ALGORITHM] [MODE] [COMPRESSION]`
* `./__main__.py [SOURCE]`  

_Note: If arguments incomplete, user will complete parameters through terminal_
    
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
  
## Overflow:
* 1: True, values of pixels on one or more channels may overflow, resulting in cool noise
* 0: False, prevent cool noise but retain maximum image quality
* Optional
  
## LOG:
* 1: Log data from algorithm to logs/
* 0: Do not log data from algorithm to logs/
* Optional

## Target:
* file name: name with valid extension which will be saved to "output" folder
* Optional
  
## Examples:
*  `./__main__.py tiger.jpg pca 1 95 0 1 tiger_pca_v_95.tif` 
*  `./__main__.py flower.jpg svd 3 min`  
*  `./__main__.py knight.png`  
