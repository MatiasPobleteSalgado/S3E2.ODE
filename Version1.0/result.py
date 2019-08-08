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
import seaborn as sb


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
	return np.mean(np.square(m2 - m1))



comuneCode = "09101" #args.comune
year = "2014" #args.year

#- Get data on JSON format from web service
json_data =	rq.get(
	f"https://api.s3e2.cl/commune/{comuneCode}/{year}"
).json()

json_data = list(
	[
		i for i in json_data if i["RURAL_RBD"] == 0 and 
		i["NOM_RBD"] not in [
			"ESCUELA EPU NEWEN", 
			"LICEO TECNICO PROF. CENTENARIO",
			"LICEO CUMBRES DE LABRANZA",
			"ESCUELA LABRANZA",
			"COLEGIO LOS ROBLES",
			"SUN FLOWER SCHOOL",
			"ESCUELA PARTICULAR ARAUCANIA",
			"ESCUELA BASICA PARTICULAR EMPRENDER"
		]
	]
)

points = []

ids = file_to_array("school_ids.bin", "int32")

non_zeros = np.nonzero(ids)[0]


school_dataframe = pd.DataFrame.from_records(json_data)
students = json_normalize(
	data = json_data
)

school_dataframe = pd.concat([school_dataframe, students], axis=1)
school_dataframe = school_dataframe.loc[:,~school_dataframe.columns.duplicated()]

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

num_iterations = len(red_iterations) * 1000

iterations = list(range(1000, num_iterations, 1000))
sb.set(style="darkgrid")

#pp.xscale("log")
pp.figure(figsize=(16,9))
pp.yscale("log")
pp.xticks(np.arange(1000, num_iterations + 1000, 1000), rotation='vertical')
pp.grid(linestyle='-')
pp.plot(iterations, m1_differences, linewidth=2, label="Alumnos no vulnerables", color="red")
pp.plot(iterations, m2_differences, linewidth=2, label="Alumnos vulnerables", color="blue")
pp.legend()
pp.xlabel("Iteraciones")
pp.ylabel("Diferencia de densidad promedio")

pp.savefig("cambio.pdf", dpi=300)
pp.savefig("cambio.png", dpi=300)
pp.clf()
#pp.show()



#dataframe = pd.DataFrame({"iterations": iterations, "m1": m1_differences, "m2": m2_differences})

#print(school_dataframe.columns)

red_mat_differences = []
cont = 0

school_dataframe["ALUMNOS.VULNERABLES"] = school_dataframe["ALUMNOS.TOTAL"] - \
										  school_dataframe["ALUMNOS.NO_VULNERABLES"]  
school_dataframe["MAT_VULNERABLES"] = 0
school_dataframe["MAT_VULNERABLES"] = school_dataframe["MAT_VULNERABLES"].astype(int)
school_dataframe["MAT_NO_VULNERABLES"] = 0
school_dataframe["MAT_NO_VULNERABLES"] = school_dataframe["MAT_NO_VULNERABLES"].astype(int)
school_dataframe["RBD"] = school_dataframe["RBD"].astype(int)
no_vulnerables = []
vulnerables = []
total = []


school_dataframe = school_dataframe.loc[:,~school_dataframe.columns.duplicated()]
for iteration in red_iterations:
	diferencias = []
	cont += 1
	for i in non_zeros:
		row_index = school_dataframe.index[school_dataframe["RBD"] == ids[i]]
		row = school_dataframe.iloc[row_index]

		diferencias.append(
			(
				int(row["ALUMNOS.NO_VULNERABLES"]) - 
				int(iteration[i] / 1000)  
			) ** 2
		)
		if(cont == len(red_iterations)):
			school_dataframe.at[row_index, 'MAT_NO_VULNERABLES'] = int(iteration[i] / 1000)
			no_vulnerables.append(int(iteration[i] / 1000))

	average = np.mean(np.array(diferencias, dtype=np.float32))
	red_mat_differences.append(average)

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
				int(row["ALUMNOS.VULNERABLES"]) -
				int(iteration[i] / 1000)  
			) ** 2
		)
		if(cont == len(blue_iterations)):
			school_dataframe.at[row_index, 'MAT_VULNERABLES'] = int(iteration[i] / 1000)
			vulnerables.append(int(iteration[i] / 1000))
	average = np.mean(np.array(diferencias))
	blue_mat_differences.append(average)


iterations = list(range(1000, num_iterations + 1000, 1000))
pp.xticks(np.arange(1000, num_iterations + 1000, 1000), rotation='vertical')
pp.grid(linestyle='-')



school_dataframe["MAT_TOTAL"] = school_dataframe["MAT_NO_VULNERABLES"] + school_dataframe["MAT_VULNERABLES"]
school_dataframe["DIFERENCIA_TOTAL"] = school_dataframe["ALUMNOS.TOTAL"] - school_dataframe["MAT_TOTAL"]
school_dataframe["DIFERENCIA_VULNERABLES"] = school_dataframe["ALUMNOS.VULNERABLES"] - school_dataframe["MAT_VULNERABLES"]
school_dataframe["DIFERENCIA_NO_VULNERABLES"] = school_dataframe["ALUMNOS.NO_VULNERABLES"] - school_dataframe["MAT_NO_VULNERABLES"]
school_dataframe["MAT_TOTAL"] = school_dataframe["MAT_TOTAL"].round()
school_dataframe["MAT_TOTAL"] = school_dataframe["MAT_TOTAL"].astype(int)

df = school_dataframe[[
	"NOM_RBD", 
	"NOM_DEPE", 
	"ALUMNOS.NO_VULNERABLES", 
	"ALUMNOS.VULNERABLES", 
	"MAT_NO_VULNERABLES", 
	"MAT_VULNERABLES",
	"DIFERENCIA_VULNERABLES",
	"DIFERENCIA_NO_VULNERABLES",
	"DIFERENCIA_TOTAL",
	"ALUMNOS.TOTAL",
	"MAT_TOTAL"
]]


#df["MAT_VULNERABLES"] = vulnerables
#df["MAT_NO_VULNERABLES"] = no_vulnerables

df.to_csv("final.csv", index=False)
dataframe = pd.DataFrame({"iterations": iterations, "m1": red_mat_differences, "m2": blue_mat_differences})
dataframe.to_csv("average_difference.csv", index=False)

pp.figure(figsize=(16,9))

#pp.xscale("log")
pp.yscale("log")

pp.plot(iterations, np.sqrt(np.array(red_mat_differences)), linewidth=2, label="Alumnos no vulnerables", color="red")
pp.plot(iterations, np.sqrt(np.array(blue_mat_differences)), linewidth=2, label="Alumnos vulnerables", color="blue")
pp.legend()
pp.xlabel("Iteraciones")
pp.ylabel("Diferencia de matricula promedio")
#pp.show()
pp.savefig("diferencia.pdf", dpi=300)
pp.savefig("diferencia.png", dpi=300)

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