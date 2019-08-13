import pandas as pd
import math as mt


test_1 = pd.read_csv("test_1.csv")
test_2 = pd.read_csv("test_2.csv")
test_3 = pd.read_csv("test_3.csv")
test_4 = pd.read_csv("test_4.csv")
test_5 = pd.read_csv("test_5.csv")
test_6 = pd.read_csv("test_6.csv")
test_7 = pd.read_csv("test_7.csv")
test_8 = pd.read_csv("test_8.csv")
test_9 = pd.read_csv("test_9.csv")

school_types = [
	"Municipal DAEM",
	"Particular Subvencionado",
	"Particular Pagado",
]

data_frames = [
	test_1,
	test_2,
	test_3,
	test_4,
	test_5,
	test_6,
	test_7,
	test_8,
	test_9
]


selected = 8
for i in school_types:
	print(i)
	print(data_frames[selected].loc[data_frames[selected]["NOM_DEPE"] == i]["DIFERENCIA_VULNERABLES"].describe())
	#print(data_frames[selected].loc[data_frames[selected]["NOM_DEPE"] == i]["DIFERENCIA_NO_VULNERABLES"].describe())
	print()