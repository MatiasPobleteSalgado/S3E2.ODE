from schoolModel.cell import Cell
from schoolModel.cell import SchoolType
import threading as th

class School(Cell):
	def __init__(self, capacity, numStudents, position, typeSchool, num = 0):
		#- def __init__(self, pos = (0, 0), dim = (1, 1), temp = 0, num = 0):
		self.capacity = capacity
		self.position = position
		self.numStudents = numStudents
		self.type = typeSchool
		Cell.__init__(self, self.position, (20, 20), 700, 0, num)
		self.updateThread = th.Thread(target = self.__update)
		#self.source = True

	def g(self, x, y):
		if((self.num == 124) or (self.num == 125) or (self.num == 126)):
			return 70000
		return 0

	def __update(self):
		while (self.on):
			self.clock.tick(Cell.threadPause)
			self.v = Cell.dTime * (self.getDV() + self.g(self.left, self.top))

