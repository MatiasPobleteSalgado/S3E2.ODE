from schoolModel.cell import Cell
from schoolModel.cell import StudentType
from schoolModel.school import School

import threading as th

class Student(Cell):
	def __init__(self, position, type, num = 0):
		#- def __init__(self, pos = (0, 0), dim = (1, 1), temp = 0, num = 0):
		self.position = position
		self.type = type
		Cell.__init__(self, self.position, (20, 20), 0, 700, num)
		self.updateThread = th.Thread(target = self.__update)

	def g(self, x, y):
		if(self.num == 526):
			return 70000
		return 0

	def __update(self):
		while (self.on):
			self.clock.tick(Cell.threadPause)
			self.v = self.v + self.getDV() * Cell.dTime
			self.u = Cell.dTime * (self.getDU() + self.g(self.left, self.top))
