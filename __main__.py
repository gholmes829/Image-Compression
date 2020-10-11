#!/usr/bin/env python3
from driver import Driver
import sys

def main(argv):
	argc = len(argv)
	driver = Driver()
	if argc == 2:
		driver.run(fileName=argv[1])
	elif argc == 3:
		driver.run(fileName=argv[1], mode=argv[2])
	elif argc == 4:
		driver.run(fileName=argv[1], mode=argv[2], compression=argv[3])
	elif argc == 5:
		driver.run(fileName=argv[1], mode=argv[2], compression=argv[3], convertBW=argv[4])
	else:
		driver.run()

if __name__ == "__main__":
	main(sys.argv)
