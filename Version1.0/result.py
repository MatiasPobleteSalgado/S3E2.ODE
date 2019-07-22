import pygame as pgm
import numpy as np
import ctypes as ct
import os

def file_to_arrau(file_name):
	file = open(file_name, "rb")

	nX, nY = 1024, 1024
	n = nX * nY
	data = np.ndarray(shape=[n], dtype="float32")
	file1.readinto(data)
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

on = True
fps = pgm.time.Clock()
x_res, y_res = 1024, 1024
scr = pgm.display.set_mode([x_res, y_res])

school_colors = {
	"Municipal": [255, 0, 0],
	"Particular Subvencionado": [0, 255, 0],
	"Particular Pagado": [0, 0, 255]
}

n = 1024 * 1024

red_iterations = [file_to_array(f"{i}") for i in os.listdir("results") if i[:2] == "m1"]
blue_iterations = [file_to_array(f"{i}") for i in os.listdir("results") if i[:2] == "m2"]

red_dots = [generate_dots(i) for i in red_iterations]
blue_dots = [generate_dots(i) for i in blue_iterations]


print(red_iterations)
nX, nY = 1024, 1024
#red_data = np.fromfile(file, dtype="float32") 
cellIndx = nX * nY
red_data = ct.c_float * n
red_data = np.ndarray(shape=[n], dtype="float32")
file1.readinto(red_data)

red_max_num = max(red_data)
red_min_num = min(red_data)

red_dots = []
x, y  = 0, 0
for i in range(cellIndx):
	if(x < (nX -1)):
		x +=1
	else:
		x = 0
		y += 1
	if(red_data[i] > 0):
		red_dots.append([red_data[i], x, y])

blue_data = ct.c_float * n
blue_data = np.ndarray(shape=[n], dtype="float32")
file2.readinto(blue_data)

blue_max_num = max(blue_data)
blue_min_num = min(blue_data)

blue_dots = []
x, y  = 0, 0
for i in range(cellIndx):
	if(x < (nX -1)):
		x +=1
	else:
		x = 0
		y += 1
	if(blue_data[i] > 0):
		blue_dots.append([blue_data[i], x, y])


while on:
	#scr.blit((0, 0), map.img)
	scr.fill((0, 0, 0))
	for e in pgm.event.get():
		if(e.type == pgm.QUIT):
			on = False
	for i in red_dots:
		pgm.draw.circle(
			scr, 
			np.array((250, 0, 0)), 
			(i[1], i[2]),
			int(10 * ((i[0] - red_min_num) / (red_max_num - red_min_num))),
			0
		)
	for i in blue_dots:
		pgm.draw.circle(
			scr, 
			np.array((0, 0, 255)), 
			(i[1], i[2]),
			int(10 * ((i[0] - blue_min_num) / (blue_max_num - blue_min_num))),
			0
		)
		
	"""
	for school in json_red_data:
		pgm.draw.circle(
			scr, 
			school_colors[school["NOM_DEPE"]], 
			(
				int(points[indx][0] * x_res), 
				y_res - int(points[indx][1] * y_res)
			), 
			1, 
			1
		)
		indx += 1
	"""
	fps.tick(60)
	pgm.display.update()