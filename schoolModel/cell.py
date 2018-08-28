import threading as th
import pygame as pgm
from multiprocessing import Process

class StudentType(object):
	vulnerable = 3
	rich       = 4

class SchoolType(object):
	municipal = 0
	private = 2

class Cell(pgm.rect.Rect):
	#- Rect(x, y, width, height)
	cells = []
	n = None
	timeStep = 0
	threadPause = 60
	dTime = 0.1
	interactions = {
		SchoolType.municipal: {
			StudentType.vulnerable: 1,
			StudentType.rich : 1
		},

		SchoolType.private: {
			StudentType.vulnerable: 1,
			StudentType.rich : 1
		}
	}

	currentStudentType = None
	currentSchool = None
	def __init__(self, pos = (0, 0), dim = (1, 1), v = 0, u = 0, num = 0):
		pgm.rect.Rect.__init__(self, pos, dim)
		self.source = False
		self.num = num
		self.on  = True
		self.pos = pos
		self.dim = dim
		self.u   = u
		self.v   = v
		self.clock = pgm.time.Clock()
		self.updateThread = th.Thread(target = self.__update)
	
	def __str__(self):
		return str(self.num) + " " + str(self.v)

	def getDV(self):
		cT = 10
		if(self.num < Cell.n[0] + 1):
			if(self.num == 1):
				right  = Cell.cells[self.num - 1 + 1].v
				bottom = Cell.cells[self.num - 1 + Cell.n[0]].v
				dTemp  = cT * (right -2 * self.v) / self.width ** 2 + cT * (-2 * self.v + bottom) / self.height ** 2
				return dTemp
			if(self.num == Cell.n[0]):
				left   = Cell.cells[self.num - 1 - 1].v
				bottom = Cell.cells[self.num - 1 + Cell.n[0]].v
				dTemp = cT * (-2 * self.v + left) / self.width ** 2 + cT * (-2*self.v + bottom) / self.height ** 2
				return dTemp
			right  = Cell.cells[self.num - 1 + 1].v
			left   = Cell.cells[self.num - 1 - 1].v
			bottom = Cell.cells[self.num - 1 + Cell.n[0]].v
			dTemp  = cT * (right - 2 * self.v + left) / self.width ** 2 + cT * (- 2 * self.v + bottom) / self.height ** 2
			return dTemp
		if(self.num > (Cell.n[1] * Cell.n[0] - Cell.n[0])):
			if(self.num == (Cell.n[1] * Cell.n[0] - Cell.n[0] + 1)):
				right  = Cell.cells[self.num - 1 + 1].v
				top    = Cell.cells[self.num - 1 - Cell.n[0]].v
				dTemp = cT * (right - 2 * self.v) / self.width ** 2 + cT * (top - 2 * self.v) / self.height ** 2
				return dTemp
			if(self.num == (Cell.n[1] * Cell.n[0])):
				top    = Cell.cells[self.num - 1 - Cell.n[0]].v
				left   = Cell.cells[self.num - 1 - 1].v
				dTemp = cT * (-2 * self.v + left) / self.width ** 2 + cT * (top - 2 * self.v) / self.height ** 2
				return dTemp
			top    = Cell.cells[self.num - 1 - Cell.n[0]].v
			left   = Cell.cells[self.num - 1 - 1].v
			right  = Cell.cells[self.num - 1 + 1].v
			dTemp = cT * (right - 2 * self.v + left) / self.width ** 2 + cT * (top - 2 * self.v) / self.height ** 2
			return dTemp
		if(self.num % Cell.n[0] == 1):
			top    = Cell.cells[self.num - 1 - Cell.n[0]].v
			right  = Cell.cells[self.num - 1 + 1].v
			bottom = Cell.cells[self.num - 1 + Cell.n[0]].v
			dTemp = cT * (right - 2 * self.v) / self.width ** 2 + cT * (top - 2 * self.v + bottom) / self.height ** 2
			return dTemp
		if(self.num % Cell.n[0] == 0):
			left   = Cell.cells[self.num - 1 - 1].v
			top    = Cell.cells[self.num - 1 - Cell.n[0]].v
			bottom = Cell.cells[self.num - 1 + Cell.n[0]].v
			dTemp = cT * (- 2 * self.v + left) / self.width ** 2 + cT * (top - 2 * self.v + bottom) / self.height ** 2
			return dTemp
		right  = Cell.cells[self.num - 1 + 1].v
		left   = Cell.cells[self.num - 1 - 1].v
		top    = Cell.cells[self.num - 1 - Cell.n[0]].v
		bottom = Cell.cells[self.num - 1 + Cell.n[0]].v
		dTemp = cT * (right - 2 * self.v + left) / self.width ** 2 + cT * (top - 2 * self.v + bottom) / self.height ** 2
		return dTemp

	def getDU(self):
		c = Cell.interactions[Cell.currentSchool][Cell.currentStudentType]
		cT = 0
		if(self.num < Cell.n[0] + 1):
			if(self.num == 1):
				right  = Cell.cells[self.num - 1 + 1]
				bottom = Cell.cells[self.num - 1 + Cell.n[0]]
				dTemp  = cT * (right.u - self.u) / self.width ** 2 \
					+ cT * (-self.u + bottom.u) / self.height ** 2 \
					- c * (right.v - self.v) / self.width ** 2 \
					- c * (-self.v + bottom.v) / self.height ** 2
				return dTemp
			if(self.num == Cell.n[0]):
				left   = Cell.cells[self.num - 1 - 1]
				bottom = Cell.cells[self.num - 1 + Cell.n[0]]
				dTemp = cT * (-self.u + left.u) / self.width ** 2 + \
					cT * (-self.u + bottom.u) / self.height ** 2 -\
					c * (-self.v + left.v) / self.width ** 2 - \
					c * (-self.v + bottom.v) / self.height ** 2
				return dTemp
			right  = Cell.cells[self.num - 1 + 1]
			left   = Cell.cells[self.num - 1 - 1]
			bottom = Cell.cells[self.num - 1 + Cell.n[0]]
			dTemp  = cT * (right.u - 2 * self.u + left.u) / self.width ** 2 +\
				cT * (-self.u + bottom.u) / self.height ** 2 -\
				c * (right.v - 2 * self.v + left.v) / self.width ** 2 -\
				c * (-self.v + bottom.v) / self.height ** 2
			return dTemp
		if(self.num > (Cell.n[1] * Cell.n[0] - Cell.n[0])):
			if(self.num == (Cell.n[1] * Cell.n[0] - Cell.n[0] + 1)):
				right  = Cell.cells[self.num - 1 + 1]
				top    = Cell.cells[self.num - 1 - Cell.n[0]]
				dTemp = cT * (right.u - self.u) / self.width ** 2 + \
					cT * (top.u - self.u) / self.height ** 2 -\
					c * (right.v - self.v) / self.width ** 2 - \
					c * (top.v - self.v) / self.height ** 2
				return dTemp
			if(self.num == (Cell.n[1] * Cell.n[0])):
				top    = Cell.cells[self.num - 1 - Cell.n[0]]
				left   = Cell.cells[self.num - 1 - 1]
				dTemp = cT * (-self.u + left.u) / self.width ** 2 + \
					cT * (top.u - self.u) / self.height ** 2 -\
					c * (-self.v + left.v) / self.width ** 2 - \
					c * (top.v - self.v) / self.height ** 2
				return dTemp
			top    = Cell.cells[self.num - 1 - Cell.n[0]]
			left   = Cell.cells[self.num - 1 - 1]
			right  = Cell.cells[self.num - 1 + 1]
			dTemp = cT * (right.u - 2 * self.u + left.u) / self.width ** 2 + \
				cT * (top.u - self.u) / self.height ** 2 -\
				c * (right.v - 2 * self.v + left.v) / self.width ** 2 - \
				c * (top.v - self.v) / self.height ** 2 
			return dTemp
		if(self.num % Cell.n[0] == 1):
			top    = Cell.cells[self.num - 1 - Cell.n[0]]
			right  = Cell.cells[self.num - 1 + 1]
			bottom = Cell.cells[self.num - 1 + Cell.n[0]]
			dTemp = cT * (right.u - self.u) / self.width ** 2 + \
				cT * (top.u - 2 * self.u + bottom.u) / self.height ** 2 -\
				c * (right.v - self.v) / self.width ** 2 -\
				c * (top.v - 2 * self.v + bottom.v) / self.height ** 2
			return dTemp
		if(self.num % Cell.n[0] == 0):
			left   = Cell.cells[self.num - 1 - 1]
			top    = Cell.cells[self.num - 1 - Cell.n[0]]
			bottom = Cell.cells[self.num - 1 + Cell.n[0]]
			dTemp = cT * (-self.u + left.u) / self.width ** 2 +\
				cT * (top.u - 2 * self.u + bottom.u) / self.height ** 2 -\
				c * (-self.v + left.v) / self.width ** 2 -\
				c * (top.v - 2 * self.v + bottom.v) / self.height ** 2
			return dTemp
		right  = Cell.cells[self.num - 1 + 1]
		left   = Cell.cells[self.num - 1 - 1]
		top    = Cell.cells[self.num - 1 - Cell.n[0]]
		bottom = Cell.cells[self.num - 1 + Cell.n[0]]
		dTemp = cT * (right.u - 2 * self.u + left.u) / self.width ** 2 + \
			cT * (top.u - 2 * self.u + bottom.u) / self.height ** 2 -\
			c * (right.v - 2 * self.v + left.v) / self.width ** 2 - \
			c * (top.v - 2 * self.v + bottom.v) / self.height ** 2
		return dTemp

	def __update(self):
		while(self.on):
			self.clock.tick(Cell.threadPause)
			self.v = self.v + self.getDV() * Cell.dTime
			nU = self.u + self.getDU() * Cell.dTime
			if nU != self.u:
				print(self.u)
			if (nU < 0):
				self.u = 0
				continue
			self.u = nU
			

	def start(self):
		self.updateThread.start()

	def getHeat(self, dTemp, dTime):
		temp = self.v + dTemp * dTime
		if(temp < 1000):
			self.v = self.v + dTemp * dTime

	def stop(self):
		self.on = False

	def draw(self, scr, fill = False):
		if(fill):
			pgm.draw.rect(scr, Color.red, self)
			return
		try:
			pgm.draw.rect(scr, [self.v / 10000 * 250, 0, self.u / 10000 * 250], self)
		except:
			print(self.num, self.v, self.u)