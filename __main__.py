#!/usr/bin/env python3

"""
Author: Grant Holmes
Contact: g.holmes429@gmail.com
Date: 10/16/2020
"""

from driver import Driver
import sys

def main(argv, argc):
	driver = Driver(argv, argc)	
	driver.run()

if __name__ == "__main__":
	main(sys.argv, len(sys.argv))
