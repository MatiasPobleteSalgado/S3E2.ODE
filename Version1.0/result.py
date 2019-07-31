import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame as pgm
import numpy as np
import ctypes as ct
import pandas as pd
import requests as rq
import math as mt
import utm
from pandas.io.json import json_normalize

from scipy.spatial import Voronoi, voronoi_plot_2d
from sklearn.preprocessing import MinMaxScaler, normalize
import matplotlib.pyplot as pp


min_coordinates = [-38.705326, -72.668784]
max_coordinates = [-38.761679, -72.528012]

#min_coordinates = [-38.705307, -72.650471]
#max_coordinates = [-38.761679, -72.528012]

def file_to_array(file_name, dtype="float32"):
	file = open(file_name, "rb")

	nX, nY = 1024, 1024
	n = nX * nY
	data = np.ndarray(shape=[n], dtype=dtype)
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

def average_difference(m1, m2):
	return np.mean(np.sqrt(np.square(m2 - m1)))



comuneCode = "09101" #args.comune
year = "2014" #args.year

#- Get data on JSON format from web service
json_data =	rq.get(
	f"https://api.s3e2.cl/commune/{comuneCode}/{year}"
).json()

json_data = list(
	[i for i in json_data if i["RURAL_RBD"] == 0]
)

points = []

ids = file_to_array("school_ids.bin", "int32")

non_zeros = np.nonzero(ids)[0]

for school in json_data:
	utmCoords = utm.from_latlon(school["LATITUD"], school["LONGITUD"])
	points.append(
		[utmCoords[0], utmCoords[1]]
	)
	school["UTM"] = [utmCoords[0], utmCoords[1]]

school_dataframe = pd.DataFrame.from_records(json_data)
students = json_normalize(
	data = json_data
)

points = list(school_dataframe["UTM"])
min_coordinates = utm.from_latlon(min_coordinates[0], min_coordinates[1])
max_coordinates = utm.from_latlon(max_coordinates[0], max_coordinates[1])
points.append([min_coordinates[0], min_coordinates[1]])
points.append([max_coordinates[0], max_coordinates[1]])

scaler = MinMaxScaler()
scaler.fit(points)

points = scaler.transform(points)
points = points[:-2]


points = points * 1024
points = points.astype(int)

normalized_dataframe = pd.DataFrame(points, columns=["normalized_x", "normalized_y"], dtype=int)
school_dataframe = pd.concat([school_dataframe, normalized_dataframe], axis=1)
school_dataframe = pd.concat([school_dataframe, students], axis=1)



school_colors = {
	"Municipal": [255, 0, 0],
	"Particular Subvencionado": [0, 255, 0],
	"Particular Pagado": [0, 0, 255]
}

n = 1024 * 1024
file_list = os.listdir("results")

file_list = sorted(file_list, key=lambda x: int(x.split("_")[1].split(".")[0]))
#"""
red_iterations = [file_to_array(f"results/{i}") for i in file_list if i[:2] == "m1"]
blue_iterations = [file_to_array(f"results/{i}") for i in file_list if i[:2] == "m2"]

#np.save("results/numpy_files/m1.npy", red_iterations)
#np.save("results/numpy_files/m2.npy", blue_iterations)
#"""

#red_iterations = np.load("results/numpy_files/m1.npy")
#blue_iterations = np.load("results/numpy_files/m2.npy")

total_iterations = len(red_iterations)

m1_differences = [average_difference(red_iterations[i], red_iterations[i + 1]) for i in range(total_iterations - 1)]
m2_differences = [average_difference(blue_iterations[i], blue_iterations[i + 1]) for i in range(total_iterations - 1)]

num_iterations = 10000

iterations = list(range(1000, num_iterations, 1000))
pp.xticks(np.arange(1000, num_iterations + 1000, 1000), rotation='vertical')
pp.grid(linestyle='-')
pp.plot(iterations, m1_differences, linewidth=2, label="Alumnos no vulnerables", color="red")
pp.plot(iterations, m2_differences, linewidth=2, label="Alumnos vulnerables", color="blue")
pp.legend()
pp.xlabel("Iteraciones")
pp.ylabel("Diferencia de densidad promedio")
#"""
pp.show()



#dataframe = pd.DataFrame({"iterations": iterations, "m1": m1_differences, "m2": m2_differences})

#print(school_dataframe.columns)

red_mat_differences = []
cont = 0

school_dataframe["VULNERABLES"] = 0
school_dataframe["MAT_VULNERABLES"] = 0
school_dataframe["MAT_VULNERABLES"] = school_dataframe["MAT_VULNERABLES"].astype(int)
school_dataframe["MAT_NO_VULNERABLES"] = 0
school_dataframe["MAT_NO_VULNERABLES"] = school_dataframe["MAT_NO_VULNERABLES"].astype(int)
school_dataframe["RBD"] = school_dataframe["RBD"].astype(int)
no_vulnerables = []
vulnerables = []


school_dataframe = school_dataframe.loc[:,~school_dataframe.columns.duplicated()]
for iteration in red_iterations:
	diferencias = []
	cont += 1
	for i in non_zeros:
		print(ids[i])
		row_index = school_dataframe.index[school_dataframe["RBD"] == ids[i]]
		row = school_dataframe.iloc[row_index]
		diferencias.append(
			(
				int(row["ALUMNOS.NO_VULNERABLES"]) - int(iteration[i] / 1000)  
			) ** 2
		)
		if(cont == len(red_iterations) -1):
			school_dataframe.at[row_index, 'MAT_NO_VULNERABLES'] = int(iteration[i] / 1000)

			no_vulnerables.append(int(iteration[i] / 1000))


	average = np.average(np.array(diferencias, dtype=np.float32))
	red_mat_differences.append(average)

print(len(diferencias), len(non_zeros))
blue_mat_differences = []
cont = 0

for iteration in blue_iterations:
	diferencias = []
	cont += 1
	for i in non_zeros:
		row_index = school_dataframe.index[school_dataframe["RBD"] == ids[i]]
		row = school_dataframe.iloc[row_index] 
		diferencias.append(
			(
				int(row["ALUMNOS.TOTAL"]) -
				int(row["ALUMNOS.NO_VULNERABLES"]) - 
				int(iteration[i] / 1000)  
			) ** 2
		)
		if(cont == len(blue_iterations) -1):
			school_dataframe.at[row_index, 'MAT_VULNERABLES'] = int(iteration[i] / 1000)
			vulnerables.append(int(iteration[i] / 1000))
	average = np.average(np.array(diferencias))
	blue_mat_differences.append(average)


iterations = list(range(1000, num_iterations + 1000, 1000))
pp.xticks(np.arange(1000, num_iterations + 1000, 1000), rotation='vertical')
pp.grid(linestyle='-')
pp.plot(iterations, np.sqrt(np.array(red_mat_differences)), linewidth=2, label="Alumnos no vulnerables", color="red")
pp.plot(iterations, np.sqrt(np.array(blue_mat_differences)), linewidth=2, label="Alumnos vulnerables", color="blue")
pp.legend()
pp.xlabel("Iteraciones")
pp.ylabel("Diferencia de matricula promedio")
pp.show()


df = school_dataframe[[
	"NOM_RBD", 
	"NOM_DEPE", 
	"ALUMNOS.NO_VULNERABLES", 
	"VULNERABLES", 
	"MAT_NO_VULNERABLES", 
	"MAT_VULNERABLES",
	"ALUMNOS.TOTAL"
]]
df["VULNERABLES"] = df["ALUMNOS.TOTAL"] - df["ALUMNOS.NO_VULNERABLES"]
df["MAT_TOTAL"]   = df["MAT_NO_VULNERABLES"] + df["MAT_VULNERABLES"]

#df["MAT_VULNERABLES"] = vulnerables
#df["MAT_NO_VULNERABLES"] = no_vulnerables

df.to_csv("final.csv", index=False)
dataframe = pd.DataFrame({"iterations": iterations, "m1": red_mat_differences, "m2": blue_mat_differences})
dataframe.to_csv("average_difference.csv", index=False)

"""
red_dots = [generate_dots(i) for i in red_iterations]
blue_dots = [generate_dots(i) for i in blue_iterations]

blue_max_num = max([max(i) for i in blue_iterations])
blue_min_num = min([min(i) for i in blue_iterations])


red_max_num = max([max(i) for i in red_iterations])
red_min_num = min([min(i) for i in red_iterations])

on = FalseW
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