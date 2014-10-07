#### python 2048 ####
import math
import random
import graphics
import msvcrt
import time

cellSize = 5

def createTable(maxDoors):
    """creates the table of probabilities
    of success by switching"""
    table = graphics.GraphWin("table", (cellSize+1)*maxDoors, (cellSize+1)*maxDoors)
    if maxDoors < 3:
        return
    for n in range (3, maxDoors+1):
        for i in range(n-1):
            value = float(n-1)/(n**2 - n*i - n)
            p1 = graphics.Point(n*cellSize, i*cellSize)
            p2 = graphics.Point((n+1)*cellSize, (i+1)*cellSize)
            sqr = graphics.Rectangle(p1, p2)
            sqr.setFill(graphics.color_rgb(0,0,value*255))
            sqr.draw(table)
    return table

t = createTable(50)

def c():
    t.close()
