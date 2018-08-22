import threading as th
import pygame as pgm

class HeatSource(pgm.rect.Rect):
	#- Rect(x, y, width, height)
	sources = []
	n = None
	def __init__(self, pos = (0, 0), dim = (1, 1), temp = 0, num = 0):
		pgm.rect.Rect.__init__(self, pos, dim)
		self.source = False
		self.num = num
		self.on  = True
		self.pos = pos
		self.dim = dim
		self.temp = temp
		self.clock = pgm.time.Clock()
		self.updateThread = th.Thread(target = self.__update)
	
	def __str__(self):
		return str(self.num) + " " + str(self.temp)

	def getDTemp(self):
		if(self.num < HeatSource.n[0] + 1):
			if(self.num == 1):
				right  = HeatSource.sources[self.num - 1 + 1].temp
				bottom = HeatSource.sources[self.num - 1 + HeatSource.n[0]].temp
				dTemp  = (right - self.temp) / self.width ** 2 + (-self.temp + bottom) / self.height ** 2
				return dTemp
			if(self.num == HeatSource.n[0]):
				left   = HeatSource.sources[self.num - 1 - 1].temp
				bottom = HeatSource.sources[self.num - 1 + HeatSource.n[0]].temp
				dTemp = (-self.temp + left) / self.width ** 2 + (-self.temp + bottom) / self.height ** 2
				return dTemp
			right  = HeatSource.sources[self.num - 1 + 1].temp
			left   = HeatSource.sources[self.num - 1 - 1].temp
			bottom = HeatSource.sources[self.num - 1 + HeatSource.n[0]].temp
			dTemp  = (right - 2 * self.temp + left) / self.width ** 2 + (-self.temp + bottom) / self.height ** 2
			return dTemp
		if(self.num > (HeatSource.n[1] * HeatSource.n[0] - HeatSource.n[0])):
			if(self.num == (HeatSource.n[1] * HeatSource.n[0] - HeatSource.n[0] + 1)):
				right  = HeatSource.sources[self.num - 1 + 1].temp
				top    = HeatSource.sources[self.num - 1 - HeatSource.n[0]].temp
				dTemp = (right - self.temp) / self.width ** 2 + (top - self.temp) / self.height ** 2
				return dTemp
			if(self.num == (HeatSource.n[1] * HeatSource.n[0])):
				top    = HeatSource.sources[self.num - 1 - HeatSource.n[0]].temp
				left   = HeatSource.sources[self.num - 1 - 1].temp
				dTemp = (-self.temp + left) / self.width ** 2 + (top - self.temp) / self.height ** 2
				return dTemp
			top    = HeatSource.sources[self.num - 1 - HeatSource.n[0]].temp
			left   = HeatSource.sources[self.num - 1 - 1].temp
			right  = HeatSource.sources[self.num - 1 + 1].temp
			dTemp = (right - 2 * self.temp + left) / self.width ** 2 + (top - self.temp) / self.height ** 2
			return dTemp
		if(self.num % HeatSource.n[0] == 1):
			top    = HeatSource.sources[self.num - 1 - HeatSource.n[0]].temp
			right  = HeatSource.sources[self.num - 1 + 1].temp
			bottom = HeatSource.sources[self.num - 1 + HeatSource.n[0]].temp
			dTemp = (right - self.temp) / self.width ** 2 + (top - 2 * self.temp + bottom) / self.height ** 2
			return dTemp
		if(self.num % HeatSource.n[0] == 0):
			left   = HeatSource.sources[self.num - 1 - 1].temp
			top    = HeatSource.sources[self.num - 1 - HeatSource.n[0]].temp
			bottom = HeatSource.sources[self.num - 1 + HeatSource.n[0]].temp
			dTemp = (-self.temp + left) / self.width ** 2 + (top - 2 * self.temp + bottom) / self.height ** 2
			return dTemp
		right  = HeatSource.sources[self.num - 1 + 1].temp
		left   = HeatSource.sources[self.num - 1 - 1].temp
		top    = HeatSource.sources[self.num - 1 - HeatSource.n[0]].temp
		bottom = HeatSource.sources[self.num - 1 + HeatSource.n[0]].temp
		dTemp = (right - 2 * self.temp + left) / self.width ** 2 + (top - 2 * self.temp + bottom) / self.height ** 2
		return dTemp

	def __update(self):
		dTime = 10
		while(self.on):
			self.clock.tick(60)
			if(not self.source):
				self.temp = self.temp + self.getDTemp() * dTime

	def start(self):
		self.updateThread.start()

	def getHeat(self, dTemp, dTime):
		temp = self.temp + dTemp * dTime
		if(temp < 1000):
			self.temp = self.temp + dTemp * dTime

	def stop(self):
		self.on = False

	def draw(self, scr, fill = False):
		if(fill):
			pgm.draw.rect(scr, Color.red, self)
			return
		pgm.draw.rect(scr, [self.temp / 1000 * 250, 0, 0], self)
