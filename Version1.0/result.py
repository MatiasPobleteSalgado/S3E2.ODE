import pygame as pgm
import numpy as np
import ctypes as ct
import os
import pandas as pd

import matplotlib.pyplot as pp

def file_to_array(file_name):
	file = open(file_name, "rb")

	nX, nY = 1024, 1024
	n = nX * nY
	data = np.ndarray(shape=[n], dtype="float32")
	file.readinto(data)
	return data

def generate_dots(array):
	dots = []
	nX, nY = 1024, 1024
	n = nX * nY
	x, y  = 0, 0
	for i in range(n):
		if(x < (nX -1)):
			x +=1
		else:
			x = 0
			y += 1
		if(array[i] > 0):
			dots.append([array[i], x, y])
	return dots

def total_squared_difference(m1, m2):
	return np.sum(np.mean(m2 - m1))

school_colors = {
	"Municipal": [255, 0, 0],
	"Particular Subvencionado": [0, 255, 0],
	"Particular Pagado": [0, 0, 255]
}

n = 1024 * 1024
"""
red_iterations = [file_to_array(f"results/{i}") for i in os.listdir("results") if i[:2] == "m1"]
blue_iterations = [file_to_array(f"results/{i}") for i in os.listdir("results") if i[:2] == "m2"]

np.save("results/numpy_files/m1.npy", red_iterations)
np.save("results/numpy_files/m2.npy", blue_iterations)
"""

red_iterations = np.load("results/numpy_files/m1.npy")
blue_iterations = np.load("results/numpy_files/m2.npy")

total_iterations = len(red_iterations)

m1_differences = [total_squared_difference(red_iterations[i], red_iterations[i + 1]) for i in range(total_iterations - 1)]
m2_differences = [total_squared_difference(blue_iterations[i], blue_iterations[i + 1]) for i in range(total_iterations - 1)]

pp.plot(range(500, 10000, 500), m1_differences)
pp.plot(range(500, 10000, 500), m2_differences)
#pp.show()

df = pd.DataFrame([range(500, 10000, 500), m1_differences])
df.to_csv("khe.csv", index=False)
print(df)
"""
red_dots = [generate_dots(i) for i in red_iterations]
blue_dots = [generate_dots(i) for i in blue_iterations]

blue_max_num = max([max(i) for i in blue_iterations])
blue_min_num = min([min(i) for i in blue_iterations])


red_max_num = max([max(i) for i in red_iterations])
red_min_num = min([min(i) for i in red_iterations])

on = True
fps = pgm.time.Clock()
x_res, y_res = 1024, 1024
scr = pgm.display.set_mode([x_res, y_res])

while on:

	scr.fill((0, 0, 0))
	for e in pgm.event.get():
		if(e.type == pgm.QUIT):
			on = False
	for frame in red_dots:
		for i in frame:
			pgm.draw.circle(
				scr, 
				np.array((250, 0, 0)), 
				(i[1], i[2]),
				int(10 * ((i[0] - red_min_num) / (red_max_num - red_min_num))) + 1,
				1
			)
			pgm.display.update()

	for frame in blue_dots:
		for i in frame:
			pgm.draw.circle(
				scr, 
				np.array((0, 0, 255)), 
				(i[1], i[2]),
				int(10 * ((i[0] - blue_min_num) / (blue_max_num - blue_min_num))) + 1,
				1
			)
			pgm.display.update()

		
	fps.tick(60)
"""