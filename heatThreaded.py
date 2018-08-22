import threading as th
import pygame as pgm
from sys import argv
from schoolModel.heatSource import HeatSource
from schoolModel.school import School
from schoolModel.school import SchoolType
import time

class Color(object):
	white = (255, 255, 255)
	red   = (255, 0, 0)
	black = (0, 0, 0)

class Main(object):
	@staticmethod
	def main(args):
		dim = (5, 2)
		nX, nY = (50, 20)
		HeatSource.n = nX, nY
		scale = 200
		num = 1
		for y in range(nY):
			for x in range(nX):
				hs = HeatSource(
					((dim[0] / nX) * x * scale, (dim[1] / nY) * y * scale), 
					(dim[0] / nX * scale, dim[1] / nY * scale), 
					0,
					num
				)
				HeatSource.sources.append(hs)
				num += 1
		HeatSource.sources[100] = School(100, 30, (HeatSource.sources[100].left, HeatSource.sources[100].top), SchoolType.private, 101)
		#HeatSource.sources[256] = School(100, 30, (HeatSource.sources[256].left, HeatSource.sources[256].top), SchoolType.private, 257)
		#HeatSource.sources[500] = School(100, 30, (HeatSource.sources[500].left, HeatSource.sources[500].top), SchoolType.private, 501)
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
				"""
				if(heatSource.collidepoint(pgm.mouse.get_pos())):
					heatSource.getHeat(10, frameTime)
				"""
			pgm.display.update()
			
		for heatSource in HeatSource.sources:
			heatSource.stop()

if(__name__ == "__main__"):
	Main.main(argv)