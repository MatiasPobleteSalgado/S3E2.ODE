from schoolModel.heatSource import HeatSource
import threading as th

class SchoolType(object):
	municipal = 0
	private = 2

class School(HeatSource):
	def __init__(self, capacity, numStudents, position, typeSchool, num = 0):
		#- def __init__(self, pos = (0, 0), dim = (1, 1), temp = 0, num = 0):
		self.capacity = capacity
		self.position = position
		self.numStudents = numStudents
		self.type = typeSchool
		HeatSource.__init__(self, self.position, (20, 20), 700, num)
		self.updateThread = th.Thread(target = self.__update)
		#self.source = True

	def g(self, x, y):
		if(self.num == 101):
			return 100
		return 0

	def __update(self):
		dTime = 10
		while (self.on):
			self.clock.tick(60)
			self.temp = dTime * self.getDTemp() + dTime * self.g(self.left, self.top)

