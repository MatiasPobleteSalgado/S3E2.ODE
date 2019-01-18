import matplotlib.pyplot as plt
import requests as rq
import ctypes as ct
import json as js
import argparse
import utm

from scipy.spatial import Voronoi, voronoi_plot_2d
from sklearn.preprocessing import MinMaxScaler
from schoolData import *

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

comuneCode = args.comune
year = args.year

#- Get data on JSON format from web service
jsonData = js.loads(
	rq.get(
		"https://api.s3e2.cl/commune/" + comuneCode + "/" + year
	).text
)

file = open("schoolData.bin", "wb")

points = []
for school in jsonData:
	utmCoords = utm.from_latlon(school["LATITUD"], school["LONGITUD"])
	points.append(
		[utmCoords[0], utmCoords[1]]
	)


points.append([702451, 5715803])
points.append([715934, 5704934])
scaler = MinMaxScaler()
scaler.fit(points)

points = scaler.transform(points)
points = points[:-2]

indx = 0
for school in jsonData:
	s = SchoolData(points[indx][0], points[indx][1], schoolTypes[school["NOM_DEPE"]])
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