import threading as th

from sys import argv
import time
import pygame as pgm
import random as rnd

class Color(object):
	white = (255, 255, 255)
	red   = (255, 0, 0)
	black = (0, 0, 0)

class HeatSource(pgm.rect.Rect):
	#- Rect(x, y, width, height)
	sources = []
	s2 = []
	n = None
	def __init__(self, pos = (0, 0), dim = (1, 1), temp = 0, num = 0):
		pgm.rect.Rect.__init__(self, pos, dim)
		self.num = num
		self.on  = True
		self.pos = pos
		self.dim = dim
		self.temp = temp
		self.neighbors = []
		self.clock = pgm.time.Clock()
		self.updateThread = th.Thread(target = self.__update)

	def __update(self):
		while(self.on):
			self.clock.tick(100)
			dTime = 1
			if(self.num < HeatSource.n[0] + 1):
				if(self.num == 1):
					right  = HeatSource.s2[self.num - 1 + 1].temp
					bottom = HeatSource.s2[self.num - 1 + HeatSource.n[0]].temp
					dTemp  = (right - self.temp) / self.width ** 2 + (-self.temp + bottom) / self.height ** 2
					self.temp = self.temp + dTemp * dTime 
					break
				if(self.num == HeatSource.n[0]):
					left   = HeatSource.s2[self.num - 1 - 1].temp
					bottom = HeatSource.s2[self.num - 1 + HeatSource.n[0]].temp
					dTemp = (-self.temp + left) / self.width ** 2 + (-self.temp + bottom) / self.height ** 2
					self.temp = self.temp + dTemp * dTime 
					break
				right  = HeatSource.s2[self.num - 1 + 1].temp
				left   = HeatSource.s2[self.num - 1 - 1].temp
				bottom = HeatSource.s2[self.num - 1 + HeatSource.n[0]].temp
				dTemp  = (right - 2 * self.temp + left) / self.width ** 2 + (-self.temp + bottom) / self.height ** 2
				self.temp = self.temp + dTemp * dTime 
				break
			if(self.num > (HeatSource.n[1] * HeatSource.n[0] - HeatSource.n[0])):
				if(self.num == (HeatSource.n[1] * HeatSource.n[0] - HeatSource.n[0] + 1)):
					right  = HeatSource.s2[self.num - 1 + 1].temp
					top    = HeatSource.s2[self.num - 1 - HeatSource.n[0]].temp
					dTemp = (right - self.temp) / self.width ** 2 + (top - self.temp) / self.height ** 2
					self.temp = self.temp + dTemp * dTime 
					break
				if(self.num == (HeatSource.n[1] * HeatSource.n[0])):
					top    = HeatSource.s2[self.num - 1 - HeatSource.n[0]].temp
					left   = HeatSource.s2[self.num - 1 - 1].temp
					dTemp = (-self.temp + left) / self.width ** 2 + (top - self.temp) / self.height ** 2
					self.temp = self.temp + dTemp * dTime 
					break

				top    = HeatSource.s2[self.num - 1 - HeatSource.n[0]].temp
				left   = HeatSource.s2[self.num - 1 - 1].temp
				right  = HeatSource.s2[self.num - 1 + 1].temp
				dTemp = (right - 2 * self.temp + left) / self.width ** 2 + (top - self.temp) / self.height ** 2
				self.temp = self.temp + dTemp * dTime 
				break
			if(self.num % HeatSource.n[0] == 1):
				top    = HeatSource.s2[self.num - 1 - HeatSource.n[0]].temp
				right  = HeatSource.s2[self.num - 1 + 1].temp
				bottom = HeatSource.s2[self.num - 1 + HeatSource.n[0]].temp
				dTemp = (right - self.temp) / self.width ** 2 + (top - 2 * self.temp + bottom) / self.height ** 2
				self.temp = self.temp + dTemp * dTime 
				break
			
			if(self.num % HeatSource.n[0] == 0):
				left   = HeatSource.s2[self.num - 1 - 1].temp
				top    = HeatSource.s2[self.num - 1 - HeatSource.n[0]].temp
				bottom = HeatSource.s2[self.num - 1 + HeatSource.n[0]].temp
				dTemp = (-self.temp + left) / self.width ** 2 + (top - 2 * self.temp + bottom) / self.height ** 2
				self.temp = self.temp + dTemp * dTime 
				break

			right  = HeatSource.s2[self.num - 1 + 1].temp
			left   = HeatSource.s2[self.num - 1 - 1].temp
			top    = HeatSource.s2[self.num - 1 - HeatSource.n[0]].temp
			bottom = HeatSource.s2[self.num - 1 + HeatSource.n[0]].temp
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
		dim = (5, 2)
		nX, nY = (50, 20)
		HeatSource.n = nX, nY
		scale = 200
		num = 1
		for y in range(nY):
			arr = []
			for x in range(nX):
				hs = HeatSource(
					((dim[0] / nX) * x * scale, (dim[1] / nY) * y * scale), 
					(dim[0] / nX * scale, dim[1] / nY * scale), 
					100,
					num
				)
				arr.append(
					hs
				)
				HeatSource.s2.append(hs)
				num += 1
			HeatSource.sources.append(arr)
		
		for i in range(len(HeatSource.sources) - 1):
			for j in range(len(HeatSource.sources[i]) - 1):
				HeatSource.sources[i][j].neighbors.append(HeatSource.sources[i + 1][j])
				HeatSource.sources[i + 1][j].neighbors.append(HeatSource.sources[i][j])

		for j in range(len(HeatSource.sources[0]) - 1):
			HeatSource.sources[len(HeatSource.sources) - 1][j].neighbors.append(HeatSource.sources[len(HeatSource.sources) - 1][j + 1])
			HeatSource.sources[len(HeatSource.sources) - 1][j + 1].neighbors.append(HeatSource.sources[len(HeatSource.sources) - 1][j])

		for j in range(len(HeatSource.sources[i]) - 1):
			for i in range(len(HeatSource.sources) - 1):
				HeatSource.sources[i][j].neighbors.append(HeatSource.sources[i][j + 1])
				HeatSource.sources[i][j + 1].neighbors.append(HeatSource.sources[i][j])

		for i in range(len(HeatSource.sources) - 1):
			HeatSource.sources[i][len(HeatSource.sources[i]) - 1].neighbors.append(HeatSource.sources[i + 1][len(HeatSource.sources[i]) - 1])
			HeatSource.sources[i + 1][len(HeatSource.sources[i]) - 1].neighbors.append(HeatSource.sources[i][len(HeatSource.sources[i]) - 1])

		on = True
		scr = pgm.display.set_mode((1280, 720))
		fps = pgm.time.Clock()

		for heatSource in HeatSource.s2:
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

			for heatGen in HeatSource.sources:
				for h in heatGen:
					h.draw(scr)

			for heatGen in HeatSource.sources:
				for h in heatGen:
					if(h.collidepoint(pgm.mouse.get_pos())):
						pgm.display.set_caption(str(h.num))
						h.getHeat(1, frameTime)
						for n in h.neighbors:
							n.draw(scr, True)

			pgm.display.update()

		for heatSource in HeatSource.sources:
			for h in heatSource:
				h.stop()

if(__name__ == "__main__"):
	Main.main(argv)