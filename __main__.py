#!/usr/bin/env python3
from driver import Driver
import sys

def main(argv, argc):
	driver = Driver(argv, argc)	
	driver.run()

if __name__ == "__main__":
	main(sys.argv, len(sys.argv))
