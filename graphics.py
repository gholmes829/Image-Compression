#!/usr/bin/env python3
"""
Generating graphs
"""

import os
import matplotlib.pyplot as plt
import numpy as np

# wrappers for convenience
def validDir(path: str) -> bool:
	return os.path.isdir(path)

def validFile(path: str) -> bool:
	return os.path.isfile(path)

def getSize(path: str) -> float:
	return os.path.getsize(path)

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
	plt.rc("grid", linestyle="dashed", color="white", alpha=0.25)
	
	paths = {}

	try:
		paths["current"] = getCurrent()
		paths["root"] = getParent(paths["current"])
		paths["data"] = getChild(paths["root"], "data")
		
		paths["graphs"] = getChild(paths["root"], "graphs")
		paths["core"] = getChild(paths["root"], "core")
		paths["logs"] = getChild(paths["core"], "logs")

		paths["pcaLog"] = getChild(paths["logs"], "example_pca")
		paths["svdLog"] = getChild(paths["logs"], "example_svd")
		
		paths["pcaImg"] = getChild(paths["data"], "flower_pca_c_1")
		paths["svdImg"] = getChild(paths["data"], "flower_svd_c_1")

	except ValueError:
		print("Invalid file structure and data\nReturning...")
		return

	logData = {
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

	imgData = {
		"pca" : {"x": [], "y": []},
		"svd" : {"x": [], "y": []},
	}

	maxSize = {
		"pca": getSize(getChild(paths["pcaImg"], "flower_1920.jpg")),
		"svd": getSize(getChild(paths["svdImg"], "flower_1080.jpg")),
	}

	maxComponents = {
		"pca": 1920,
		"svd": 1080,
	}

	for algorithm in ["pca", "svd"]:
		# graphs for images
		imgs = getFiles(paths[algorithm+"Img"])

		for img in imgs:
			# get components
			components = ""
			for i in range(len(img)):
				if img[i] == "_":
					for j in range(i+1, len(img)):
						if img[j] != ".":
							components += img[j]
						else:
							break
					break
			# add component to x
			imgData[algorithm]["x"].append((int(components)/maxComponents[algorithm])*100)
			imgData[algorithm]["y"].append((getSize(getChild(paths[algorithm+"Img"], img))/maxSize[algorithm])*100)

		# graphs for logs
		logs = getFiles(paths[algorithm+"Log"])

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

		logFiles = {
			"r": open(getChild(paths["logs"], "example_"+algorithm+"/"+rPath), "r"),
			"g": open(getChild(paths["logs"], "example_"+algorithm+"/"+gPath), "r"),
			"b": open(getChild(paths["logs"], "example_"+algorithm+"/"+bPath), "r"),
		}

		content = {
			"r": logFiles["r"].readlines(),
			"g": logFiles["g"].readlines(),
			"b": logFiles["b"].readlines(),
		}

		data = {
			"r": {"x": None, "y": None},
			"g": {"x": None, "y": None},
			"b": {"x": None, "y": None},
		}

		if aPath is not None:
			mode = "RGBA"
			logFiles["a"] = open(getChild(paths["logs"], "example_"+algorithm+"/"+aPath), "r")
			content["a"] = logFiles["a"].readlines()
			data["a"] =  {"x": None, "y": None}
		else:
			mode = "RGB"
	
		for file in logFiles.values():
			file.close()

		for channel in data:
			xCoords, yCoords = zip(*[l.split() for l in content[channel]])
			data[channel]["x"] = [(float(x)/len(xCoords))*100 for x in xCoords]
			data[channel]["y"] = [float(y) for y in yCoords]

		for channel in data:
			logData[algorithm][channel]["x"] = np.array(data[channel]["x"])
			logData[algorithm][channel]["y"] = np.array(data[channel]["y"])

	colors = {
		"r": "red",
		"g": "green",
		"b": "blue",
	}

	fig, axes = plt.subplots(3, 2)
	
	# fig.suptitle("Components vs Variance", fontsize=20)

	i = 0
	j = 0

	for algorithm in logData:
		for channel in logData[algorithm]:
			x = logData[algorithm][channel]["x"]
			y = logData[algorithm][channel]["y"]

			axes[i, j].set_title(str(algorithm).upper() +": "+colors[channel].capitalize())
			axes[i, j].set(xlabel="% Components", ylabel="% Variance")
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

	fig = plt.figure()
	
	i = 0
	for algorithm in logData:
		plt.subplot(2, 1, 1+i)
		plt.title(algorithm.upper())
		plt.xlabel("% Components")
		plt.ylabel("% Raw")
		plt.grid(True)

		x = imgData[algorithm]["x"]
		y = imgData[algorithm]["y"]
		coords = zip(x, y)
		sortedCoords = sorted(coords, key=lambda k: [k[0], k[1]])
		x, y = np.array(list(zip(*sortedCoords)))
		plt.plot(x, y, c="orange", linewidth=2, linestyle="-.", label="File Size", zorder=4)

		for channel in logData[algorithm]:
			x = logData[algorithm][channel]["x"]
			y = logData[algorithm][channel]["y"]
			plt.plot(x, y, c=colors[channel], linewidth=2, linestyle="-", label=(colors[channel].capitalize()+" Variance"))
		
		# fig.suptitle("Components vs File Size", fontsize=20)
		plt.legend(loc="right")
		i += 1
	
	for ax in fig.get_axes():
		ax.label_outer()

	plt.tight_layout()
	plt.show()



if __name__ == "__main__":
	main()

