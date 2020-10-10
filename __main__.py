#!/usr/bin/env python3
from driver import Driver
import sys

def main(argv):
	driver = Driver()
	if len(argv) == 2:
		driver.run(fileName=argv[1])
	elif len(argv) == 3:
		driver.run(fileName=argv[1], convertBW=argv[2])
	elif len(argv) == 4:
		driver.run(fileName=argv[1], convertBW=argv[2], accuracy=argv[3])
	else:
		driver.run()

if __name__ == "__main__":
	main(sys.argv)
