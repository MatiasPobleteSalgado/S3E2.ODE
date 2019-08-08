import pandas as pd
import math as mt


test_1 = pd.read_csv("final.csv")


school_types = [
	"Municipal DAEM",
	"Particular Subvencionado",
	"Particular Pagado",
]



selected = 8
for i in school_types:
	print(i)
	print(test_1.loc[test_1["NOM_DEPE"] == i]["DIFERENCIA_VULNERABLES"].describe())
	#print(data_frames[selected].loc[data_frames[selected]["NOM_DEPE"] == i]["DIFERENCIA_NO_VULNERABLES"].describe())
	print()