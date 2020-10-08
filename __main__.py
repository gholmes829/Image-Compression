#!/usr/bin/env python3
from driver import Driver
import sys

def main(argv):
	driver = Driver()
	driver.run(argv[1])

if __name__ == "__main__":
	if len(sys.argv) == 2:
		main(sys.argv)
	else:
		print("Incorrect arguments:")
		print("\t- Need to put valid image in \"images\" folder")
		print("\t- Run as ./__main__ <image file name>")
