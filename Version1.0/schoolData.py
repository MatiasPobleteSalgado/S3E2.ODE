import ctypes as ct

schoolTypes = {
	"Municipal": 1,
	"Particular Subvencionado": 2,
	"Particular Pagado": 3
}

class SchoolData(ct.Structure):
	_fields_ = [
		("x", ct.c_float),
		("y", ct.c_float),
		("capacity", ct.c_int),
		("type", ct.c_int)
	]
