import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import matplotlib.pyplot as plt
import requests as rq
import ctypes as ct
import json as js
import pygame as pgm
import numpy as np
import math as mt
import argparse
import utm
from PIL import Image
import sys
from scipy.spatial import Voronoi, voronoi_plot_2d
from sklearn.preprocessing import MinMaxScaler, normalize
from schoolData import *

import smopy

import pygame_plot
import struct 
import pandas as pd
import json
from pandas.io.json import json_normalize

from pprint import pprint


pd.set_option("display.precision", 10)


min_coordinates = [-38.705326, -72.668784]
max_coordinates = [-38.761679, -72.528012]
max_coordinates = [-38.756572, -72.552991]


# - Escuela araucania -38.765716 -72.754132

"""

ESCUELA PARTICULAR ARAUCANIA -38.73762989 -72.57539476
ESCUELA PARTICULAR ARAUCANIA -38.76571646 -72.75413167

"""
#min_coordinates = [-38.705307, -72.650471]
#max_coordinates = [-38.761679, -72.528012]
#map = smopy.Map((min_coordinates[0], min_coordinates[1], max_coordinates[0], max_coordinates[1]), z=14)
#ax = map.show_mpl()

#plt.show()

"""
parser = argparse.ArgumentParser()
parser.add_argument(
	"comune",
	default = "09101", 
	help = "Comune code, see https://es.wikipedia.org/wiki/Anexo:Comunas_de_Chile"
)
parser.add_argument(
	"year",
	default = "2012", 
	help = "Year to see"
)
args = parser.parse_args()
"""
"""
API Example

https://api.s3e2.cl/commune/09101/2012

Temuco = 09101
"""

def scale(X, x_min, x_max):
    nom = (X-X.min(axis=0))*(x_max-x_min)
    denom = X.max(axis=0) - X.min(axis=0)
    denom[denom==0] = 1
    return x_min + nom/denom 

def normalize_rows(x: np.ndarray):
    """
    function that normalizes each row of the matrix x to have unit length.

    Args:
     ``x``: A numpy matrix of shape (n, m)

    Returns:
     ``x``: The normalized (by row) numpy matrix.
    """
    return x/np.linalg.norm(x, ord=2, axis=1, keepdims=True)

comuneCode = "09101" #args.comune
year = "2014" #args.year

#- Get data on JSON format from web service
json_data =	rq.get(
	f"https://api.s3e2.cl/commune/{comuneCode}/{year}"
).json()

file = open("schoolData.bin", "wb")


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
school_dataframe = pd.DataFrame.from_records(
	json_data,
	coerce_float=True
)
students = json_normalize(
	data = json_data
)

school_dataframe = pd.concat([school_dataframe, students], axis=1)
school_dataframe = school_dataframe.loc[:,~school_dataframe.columns.duplicated()]
school_dataframe["LATITUD"] = school_dataframe["LATITUD"].astype(float)
school_dataframe["LONGITUD"] = school_dataframe["LONGITUD"].astype(float)
school_dataframe["UTM_X"] = 0
school_dataframe["UTM_Y"] = 0
school_dataframe["RBD"] = school_dataframe["RBD"].astype(int)

for index, row in school_dataframe.iterrows():
	utm_coords =  utm.from_latlon(
		school_dataframe.at[index, "LATITUD"], 
		school_dataframe.at[index, "LONGITUD"]
	)
	"""
	if(school_dataframe.at[index, "NOM_RBD"] == "ESCUELA PARTICULAR ARAUCANIA"):
		print(row[["NOM_RBD", "UTM_X", "UTM_Y", "LATITUD", "LONGITUD"]])
		print(utm_coords)
	"""
	school_dataframe.at[index, "UTM_X"] = utm_coords[:2][0]
	school_dataframe.at[index, "UTM_Y"] = utm_coords[:2][1]



min_coordinates = utm.from_latlon(min_coordinates[0], min_coordinates[1])[:2]
max_coordinates = utm.from_latlon(max_coordinates[0], max_coordinates[1])[:2]

x_lenght = mt.fabs(max_coordinates[0] - min_coordinates[0])
y_lenght = mt.fabs(max_coordinates[1] - min_coordinates[1])

y_scaler = 1 * y_lenght / x_lenght  

print(y_scaler)

to_norm_data = np.concatenate(
	[
		school_dataframe[["UTM_X", "UTM_Y"]].values,
		[min_coordinates, max_coordinates]
	],
	axis=0
)

school_dataframe["UTM_X"] =  (school_dataframe["UTM_X"].values - min_coordinates[0]) / \
							   (max_coordinates[0] -  min_coordinates[0])

school_dataframe["UTM_Y"] = (school_dataframe["UTM_Y"].values - max_coordinates[1]) / \
							   (min_coordinates[1] -  max_coordinates[1])

#"""
school_dataframe[["UTM_X", "UTM_Y"]] = scale(
	to_norm_data,
	0, 1
)[:-2]
#"""

"""
school_dataframe[["UTM_X", "UTM_Y"]] = normalize_rows(
	to_norm_data
)[:-2]
"""



indx = 0
for index, row in school_dataframe.iterrows():
	s = SchoolData(
		school_dataframe.at[index, "RBD"],
		school_dataframe.at[index, "UTM_X"], 
		school_dataframe.at[index, "UTM_Y"], 
		school_dataframe.at[index, "ALUMNOS.TOTAL"], 
		schoolTypes[school_dataframe.at[index, "NOM_DEPE"]]
	)
	file.write(s)
	indx += 1

file.close()
print("Saved %d schools" % indx)

#print(school_dataframe[school_dataframe["UTM_X"] == school_dataframe["UTM_X"].min()][["NOM_RBD", "UTM_X", "UTM_Y"]])
#print(school_dataframe[school_dataframe["UTM_Y"] == school_dataframe["UTM_Y"].min()][["NOM_RBD", "UTM_X", "UTM_Y"]])

"""
print(school_dataframe)

for school in json_data:
	utmCoords = utm.from_latlon(school["LATITUD"], school["LONGITUD"])
	points.append(
		[utmCoords[0], utmCoords[1]]
	)
	school["UTM"] = [utmCoords[0], utmCoords[1]]


min_coordinates = utm.from_latlon(min_coordinates[0], min_coordinates[1])
max_coordinates = utm.from_latlon(max_coordinates[0], max_coordinates[1])
points.append([min_coordinates[0], min_coordinates[1]])
points.append([max_coordinates[0], max_coordinates[1]])

scaler = MinMaxScaler()
scaler.fit(points)

points = scaler.transform(points)
#points = normalize(points)
points = points[:-2]

indx = 0
for school in json_data:
	s = SchoolData(
		int(school["RBD"]),
		points[indx][0], 
		points[indx][1], 
		json_data[indx]["ALUMNOS"]["TOTAL"], 
		schoolTypes[school["NOM_DEPE"]]
	)
	file.write(s)
	indx += 1

file.close()
print("Saved %d schools" % indx)
"""

if bool(int(sys.argv[1])):
	on = True
	fps = pgm.time.Clock()
	x_res, y_res = 1024, 1024
	temuco_map = Image.open("temuco_map.png")
	#temuco_map = temuco_map.resize((1024, 1024))
	max_width = 1024


	wpercent = (max_width/float(temuco_map.size[0]))
	hsize = int((float(temuco_map.size[1]) * float(wpercent)))
	temuco_map = temuco_map.resize((max_width, hsize), Image.ANTIALIAS)
	temuco_map.save("temuco_map.png")

	mode = temuco_map.mode
	size = temuco_map.size
	data = temuco_map.tobytes()
	scr = pgm.display.set_mode(size)
	print(size)

	school_colors = {
		"Municipal DAEM": [255, 0, 0],
		"Particular Subvencionado": [0, 255, 0],
		"Particular Pagado": [0, 0, 255]
	}

	

	this_image = pgm.image.fromstring(data, size, mode)
	while on:
		scr.blit(this_image, (0, 0))
		for e in pgm.event.get():
			if(e.type == pgm.QUIT):
				on = False
		x, y  = 0, 0

		for index, row in school_dataframe.iterrows():
			if pgm.rect.Rect(
				int(school_dataframe.at[index, "UTM_X"] * size[0]) - 5, 
				size[1] - int(school_dataframe.at[index, "UTM_Y"] * size[1]) - 5, 
				10, 
				10
			).collidepoint(pgm.mouse.get_pos()):
				print(school_dataframe.at[index, "NOM_RBD"])
			pgm.draw.circle(
				scr, 
				school_colors[school_dataframe.at[index, "NOM_DEPE"]], 
				(
					int(school_dataframe.at[index, "UTM_X"] * size[0]), 
					int(size[1] - school_dataframe.at[index, "UTM_Y"] * size[1])
				), 
				6, 
				0
			)
			fps.tick(60)
		pgm.display.update()

"""
#- Using voronoi teselation
#- Generate point vector
points = []
for school in jsonData:
	utmCoords = utm.from_latlon(school["LATITUD"], school["LONGITUD"])
	points.append(
		[utmCoords[0], utmCoords[1]]
	)

#- Normalize data to 0-1 range

scaler = MinMaxScaler()
scaler.fit(points)
points = scaler.transform(points)

#- Create Voronoi polygons
vor = Voronoi(points)
file = open("VertexData.dat", "wb")

indx = 0
for region in vor.regions:
	if(-1 in region):
		continue
	for point in region:
		vertex = VertexData(vor.vertices[point][0] * 1000, vor.vertices[point][1] * 1000, indx)
		file.write(vertex)
	indx += 1

#- Plot

voronoi_plot_2d(vor)
plt.show()
"""