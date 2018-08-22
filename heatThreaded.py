import threading as th
import pygame as pgm
import random as rnd
from sys import argv
import time

class Color(object):
	white = (255, 255, 255)
	red   = (255, 0, 0)
	black = (0, 0, 0)

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

	def __update(self):

		while(self.on):
			self.clock.tick(60)
			if(not self.source):
				dTime = 10
				if(self.num < HeatSource.n[0] + 1):
					if(self.num == 1):
						right  = HeatSource.sources[self.num - 1 + 1].temp
						bottom = HeatSource.sources[self.num - 1 + HeatSource.n[0]].temp
						dTemp  = (right - self.temp) / self.width ** 2 + (-self.temp + bottom) / self.height ** 2
						self.temp = self.temp + dTemp * dTime 
						continue
					if(self.num == HeatSource.n[0]):
						left   = HeatSource.sources[self.num - 1 - 1].temp
						bottom = HeatSource.sources[self.num - 1 + HeatSource.n[0]].temp
						dTemp = (-self.temp + left) / self.width ** 2 + (-self.temp + bottom) / self.height ** 2
						self.temp = self.temp + dTemp * dTime 
						continue
					right  = HeatSource.sources[self.num - 1 + 1].temp
					left   = HeatSource.sources[self.num - 1 - 1].temp
					bottom = HeatSource.sources[self.num - 1 + HeatSource.n[0]].temp
					dTemp  = (right - 2 * self.temp + left) / self.width ** 2 + (-self.temp + bottom) / self.height ** 2
					self.temp = self.temp + dTemp * dTime 
					continue
				if(self.num > (HeatSource.n[1] * HeatSource.n[0] - HeatSource.n[0])):
					if(self.num == (HeatSource.n[1] * HeatSource.n[0] - HeatSource.n[0] + 1)):
						right  = HeatSource.sources[self.num - 1 + 1].temp
						top    = HeatSource.sources[self.num - 1 - HeatSource.n[0]].temp
						dTemp = (right - self.temp) / self.width ** 2 + (top - self.temp) / self.height ** 2
						self.temp = self.temp + dTemp * dTime 
						continue
					if(self.num == (HeatSource.n[1] * HeatSource.n[0])):
						top    = HeatSource.sources[self.num - 1 - HeatSource.n[0]].temp
						left   = HeatSource.sources[self.num - 1 - 1].temp
						dTemp = (-self.temp + left) / self.width ** 2 + (top - self.temp) / self.height ** 2
						self.temp = self.temp + dTemp * dTime 
						continue
					top    = HeatSource.sources[self.num - 1 - HeatSource.n[0]].temp
					left   = HeatSource.sources[self.num - 1 - 1].temp
					right  = HeatSource.sources[self.num - 1 + 1].temp
					dTemp = (right - 2 * self.temp + left) / self.width ** 2 + (top - self.temp) / self.height ** 2
					self.temp = self.temp + dTemp * dTime 
					continue
				if(self.num % HeatSource.n[0] == 1):
					top    = HeatSource.sources[self.num - 1 - HeatSource.n[0]].temp
					right  = HeatSource.sources[self.num - 1 + 1].temp
					bottom = HeatSource.sources[self.num - 1 + HeatSource.n[0]].temp
					dTemp = (right - self.temp) / self.width ** 2 + (top - 2 * self.temp + bottom) / self.height ** 2
					self.temp = self.temp + dTemp * dTime 
					continue
				if(self.num % HeatSource.n[0] == 0):
					left   = HeatSource.sources[self.num - 1 - 1].temp
					top    = HeatSource.sources[self.num - 1 - HeatSource.n[0]].temp
					bottom = HeatSource.sources[self.num - 1 + HeatSource.n[0]].temp
					dTemp = (-self.temp + left) / self.width ** 2 + (top - 2 * self.temp + bottom) / self.height ** 2
					self.temp = self.temp + dTemp * dTime 
					continue
				right  = HeatSource.sources[self.num - 1 + 1].temp
				left   = HeatSource.sources[self.num - 1 - 1].temp
				top    = HeatSource.sources[self.num - 1 - HeatSource.n[0]].temp
				bottom = HeatSource.sources[self.num - 1 + HeatSource.n[0]].temp
				dTemp = (right - 2 * self.temp + left) / self.width ** 2 + (top - 2 * self.temp + bottom) / self.height ** 2
				self.temp = self.temp + dTemp * dTime

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

class Main(object):
	@staticmethod
	def main(args):
		dim = (6, 3)
		nX, nY = (60, 30)
		HeatSource.n = nX, nY
		scale = 200
		num = 1
		for y in range(nY):
			for x in range(nX):
				hs = HeatSource(
					((dim[0] / nX) * x * scale, (dim[1] / nY) * y * scale), 
					(dim[0] / nX * scale, dim[1] / nY * scale), 
					100,
					num
				)
				HeatSource.sources.append(hs)
				num += 1
		
		HeatSource.sources[100].temp   = 1000
		HeatSource.sources[100].source = True

		on = True
		scr = pgm.display.set_mode((dim[0] * scale, dim[1] * scale))
		fps = pgm.time.Clock()

		for heatSource in HeatSource.sources:
			heatSource.start()

		while(on):
			scr.fill(Color.white)
			frameTime = fps.tick(60)

			for e in pgm.event.get():
				if(e.type == pgm.QUIT):
					on = False
				if(e.type == pgm.KEYDOWN):
					if(e.key == pgm.K_ESCAPE):
						on = False

			for heatSource in HeatSource.sources:
				heatSource.draw(scr)

				if(heatSource.collidepoint(pgm.mouse.get_pos())):
					heatSource.getHeat(10, frameTime)


			pgm.display.update()
			
		for heatSource in HeatSource.sources:
			heatSource.stop()

if(__name__ == "__main__"):
	Main.main(argv)