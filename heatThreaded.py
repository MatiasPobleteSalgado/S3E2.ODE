import threading as th
import pygame as pgm
from sys import argv
from schoolModel.cell import Cell
from schoolModel.school import School
from schoolModel.school import SchoolType
from schoolModel.student import Student
from schoolModel.student import StudentType
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
		Cell.n = nX, nY
		scale = 200
		num = 1
		for y in range(nY):
			for x in range(nX):
				hs = Cell(
					((dim[0] / nX) * x * scale, (dim[1] / nY) * y * scale), 
					(dim[0] / nX * scale, dim[1] / nY * scale), 
					0,
					num
				)
				Cell.cells.append(hs)
				num += 1
		Cell.cells[100] = School(100, 30, (Cell.cells[100].left, Cell.cells[100].top), SchoolType.private, 101)
		#Cell.cells[256] = School(100, 30, (Cell.cells[256].left, Cell.cells[256].top), SchoolType.private, 257)
		#Cell.cells[500] = School(100, 30, (Cell.cells[500].left, Cell.cells[500].top), SchoolType.private, 501)
		on = True
		scr = pgm.display.set_mode((dim[0] * scale, dim[1] * scale))
		fps = pgm.time.Clock()
		for cell in Cell.cells:
			cell.start()
		while(on):
			scr.fill(Color.white)
			frameTime = fps.tick(60)
			for e in pgm.event.get():
				if(e.type == pgm.QUIT):
					on = False
				if(e.type == pgm.KEYDOWN):
					if(e.key == pgm.K_ESCAPE):
						on = False
			for cell in Cell.cells:
				cell.draw(scr)
				"""
				if(Cell.collidepoint(pgm.mouse.get_pos())):
					Cell.getHeat(10, frameTime)
				"""
			pgm.display.update()
			
		for cell in Cell.cells:
			cell.stop()

if(__name__ == "__main__"):
	Main.main(argv)