#!/usr/bin/env python3
"""
Generating graphs
"""

import os
import matplotlib.pyplot as plt
import numpy as np

def validDir(path: str) -> bool:
	return os.path.isdir(path)

def validFile(path: str) -> bool:
	return os.path.isfile(path)

def getCurrent() -> str:
	return os.getcwd()

def getParent(path: str) -> str:
	return os.path.dirname(path)

def getChild(path: str, target: str) -> str:
	child = os.path.join(path, target)
	if validDir(child) or validFile(child):
		return child
	else:
		print(child)
		raise ValueError
	
def getFiles(path: str) -> str:
	return os.listdir(path)

def main():
	plt.style.use(["dark_background"])
	plt.rc("grid", linestyle="dashed", color="white", alpha=0.5)
	
	paths = {}

	try:
		paths["current"] = getCurrent()
		paths["root"] = getParent(paths["current"])
		paths["data"] = getChild(paths["root"], "data")
		paths["graphs"] = getChild(paths["root"], "graphs")
		paths["core"] = getChild(paths["root"], "core")
		paths["logs"] = getChild(paths["core"], "logs")

		paths["pca"] = getChild(paths["logs"], "example_pca")
		paths["svd"] = getChild(paths["logs"], "example_svd")
		

	except ValueError:
		print("Invalid file structure and data\nReturning...")
		return

	preppedData = {
		"pca": {
				"r": {"x": None, "y": None},
				"g": {"x": None, "y": None},
				"b": {"x": None, "y": None},
		},

		"svd": {
				"r": {"x": None, "y": None},
				"g": {"x": None, "y": None},
				"b": {"x": None, "y": None},
		},
	}

	for algorithm in ["pca", "svd"]:
		logs = getFiles(paths[algorithm])

		rPath = None
		bPath = None
		gPath = None
		aPath = None

		for log in logs:
			if "_R_" in log:
				rPath = log
			elif "_G_" in log:
				gPath = log
			elif "_B_" in log:
				bPath = log	
			elif "_A_" in log:
				aPath = log	

		files = {
			"r": open(getChild(paths["logs"], "example_"+algorithm+"/"+rPath), "r"),
			"g": open(getChild(paths["logs"], "example_"+algorithm+"/"+gPath), "r"),
			"b": open(getChild(paths["logs"], "example_"+algorithm+"/"+bPath), "r"),
		}

		content = {
			"r": files["r"].readlines(),
			"g": files["g"].readlines(),
			"b":files["b"].readlines(),
		}

		data = {
			"r": {"x": None, "y": None},
			"g": {"x": None, "y": None},
			"b": {"x": None, "y": None},
		}

		if aPath is not None:
			mode = "RGBA"
			files["a"] = open(getChild(paths["logs"], "example_"+algorithm+"/"+aPath), "r")
			content["a"] = files["a"].readlines()
			data["a"] =  {"x": None, "y": None}
		else:
			mode = "RGB"
	
		for file in files.values():
			file.close()

		for channel in data:
			xCoords, yCoords = zip(*[l.split() for l in content[channel]])
			data[channel]["x"] = [(float(x)/len(xCoords))*100 for x in xCoords]
			data[channel]["y"] = [float(y) for y in yCoords]

		for channel in data:
			preppedData[algorithm][channel]["x"] = np.array(data[channel]["x"])
			preppedData[algorithm][channel]["y"] = np.array(data[channel]["y"])
	
	colors = {
		"r": "red",
		"g": "green",
		"b": "blue",
	}

	fig, axes = plt.subplots(3, 2)
	
	fig.suptitle("Components vs Variation", fontsize=20)

	i = 0
	j = 0

	for algorithm in preppedData:
		for channel in preppedData[algorithm]:
			x = preppedData[algorithm][channel]["x"]
			y = preppedData[algorithm][channel]["y"]

			axes[i, j].set_title(str(algorithm).upper() +": "+colors[channel])
			axes[i, j].set(xlabel="% Components", ylabel="% Variation")
			axes[i, j].grid(True)
			axes[i, j].plot(x, y, linewidth=2, c=colors[channel])
			
			i += 1
			if i%3 == 0:
				i=0
		j += 1
		if j%2==0:
			j=0

	for ax in fig.get_axes():
		ax.label_outer()

	plt.tight_layout()
	plt.show()

if __name__ == "__main__":
	main()

