from schoolModel.cell import Cell
import threading as th

class StudentType(object):
	vulnerable = 3
	rich       = 4

class Student(Cell):
	def __init__(self, position, type, num = 0):
		#- def __init__(self, pos = (0, 0), dim = (1, 1), temp = 0, num = 0):
		self.position = position
		self.type = type
		HeatSource.__init__(self, self.position, (20, 20), 0, num)
		self.updateThread = th.Thread(target = self.__update)

	def g(self, x, y):
		if(self.num == 101):
			return 100
		return 0

	def __update(self):
		dTime = 10
		while (self.on):
			self.clock.tick(60)
			self.temp = dTime * self.getDTemp() + dTime * self.g(self.left, self.top)
