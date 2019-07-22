import matplotlib.pyplot as plt
import requests as rq
import ctypes as ct
import json as js
import pygame as pgm
import numpy as np
import argparse
import utm

from scipy.spatial import Voronoi, voronoi_plot_2d
from sklearn.preprocessing import MinMaxScaler
from schoolData import *

import smopy

import pygame_plot
import struct 
import pandas as pd
import json
from pandas.io.json import json_normalize

from pprint import pprint
min_coordinates = [-38.705326, -72.668784]
max_coordinates = [-38.761679, -72.528012]
#map = smopy.Map((-38.705326, -72.668784, -38.761679, -72.528012), z=13)
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

https://api.s3e2.cl/commune/09111/2012

Temuco = 09101
"""

class VertexData(ct.Structure):
	_fields_ = [
		("x", ct.c_float),
		("y", ct.c_float),
		("polygonIndex", ct.c_int)
	]

comuneCode = "09101" #args.comune
year = "2012" #args.year

#- Get data on JSON format from web service
json_data =	rq.get(
	f"https://api.s3e2.cl/commune/{comuneCode}/{year}"
).json()

file = open("schoolData.bin", "wb")


json_data = list(
	[i for i in json_data if i["RURAL_RBD"] == 0]
)


school_dataframe = pd.DataFrame.from_records(json_data)
students = json_normalize(
	data = json_data
)
print(students["ALUMNOS.TOTAL"].sum(), students["ALUMNOS.NO_VULNERABLES"].sum())
print(students["ALUMNOS.TOTAL"].sum() - students["ALUMNOS.NO_VULNERABLES"].sum())
points = []
for school in json_data:
	utmCoords = utm.from_latlon(school["LATITUD"], school["LONGITUD"])
	points.append(
		[utmCoords[0], utmCoords[1]]
	)


min_coordinates = utm.from_latlon(min_coordinates[0], min_coordinates[1])
max_coordinates = utm.from_latlon(max_coordinates[0], max_coordinates[1])
points.append([min_coordinates[0], min_coordinates[1]])
points.append([max_coordinates[0], max_coordinates[1]])
scaler = MinMaxScaler()
scaler.fit(points)

print(scaler.get_params())
points = scaler.transform(points)
points = points[:-2]

indx = 0
for school in json_data:
	s = SchoolData(points[indx][0], points[indx][1], json_data[indx]["ALUMNOS"]["TOTAL"], schoolTypes[school["NOM_DEPE"]])
	file.write(s)
	indx += 1

file.close()
print("Saved %d schools" % indx)

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