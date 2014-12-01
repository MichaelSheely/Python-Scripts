import graphics
import time

VoffSet = 80
HoffSet = 40
cellSize = 40

class Maze:

    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.cells = [] #2D array of cell objects
        self.Vwalls = [] #2D array of all possible vertical walls
        self.Hwalls = [] #2D array of all possible horizontal walls
        self.win = graphics.GraphWin("Maze",2*HoffSet+cellSize*columns,2*VoffSet+cellSize*rows)
        self.win.setBackground("black")
        self.initialize()

    def __repr__(self):
        return str(self.cells)

    def initialize(self):
        for r in range(self.rows):
            self.cells += [[]]
            for c in range(self.columns):
                self.cells[r] += [Cell(r,c)]
                self.cells[r][c].cellGraphic.draw(self.win)
        for r in range(self.rows):
            self.Vwalls += [[]]
            for c in range(self.columns+1):
                if c == 0:
                    self.Vwalls[r] += [Wall(r,c,'W',True,'v')]
                elif c == self.columns:
                    self.Vwalls[r] += [Wall(r,c,'E',True,'v')]
                else:
                    self.Vwalls[r] += [Wall(r,c,False,True,'v')]
                self.Vwalls[r][c].wallGraphic.draw(self.win)
        for r in range(self.rows+1):
            self.Hwalls += [[]]
            for c in range(self.columns):
                if r == 0:
                    self.Hwalls[r] += [Wall(r,c,'N',True,'h')]
                elif r == self.rows:
                    self.Hwalls[r] += [Wall(r,c,'S',True,'h')]
                else:
                    self.Hwalls[r] += [Wall(r,c,False,True,'h')]
                self.Hwalls[r][c].wallGraphic.draw(self.win)

    def insertObj(self, row, column, obj):
        """draws the given object in the maze any objects must
        have a createFigure() member function that provides a
        drawable .figure data member and take .maze data member
        that stores the maze in which the object exists"""
        obj.row = row
        obj.column = column
        obj.maze = self #this sets the object to know what maze it is in
        anchorPt = self.cells[row][column].cellGraphic.getCenter()
        obj.createFigure(anchorPt)
        obj.figure.draw(self.win)

    def getWall(self, cell, direction):
        """returns the wall in the given direction from
        the given cell"""
        return self.getWall(cell.row, cell.column, direction)

    def getWall(self, row, column, direction):
        """returns the wall in the given direction from
        the given cell"""
        if direction == 'N':
            return self.Hwalls[row][column]
        elif direction == 'W':
            return self.Vwalls[row][column]
        elif direction == 'E':
            return self.Vwalls[row][column+1]
        elif direction == 'S':
            return self.Hwalls[row+1][column]
        
    def setWall(self, row, column, orientation, solid):
        if orientation == 'v':
            self.Vwalls[row][column].setWall(solid)
        else:
            self.Hwalls[row][column].setWall(solid)
    
    def close(self):
        self.win.close()
  
class Cell:

    def __init__(self, row, column):
        self.row = row
        self.column = column
        self.obj = None
        p1 = graphics.Point(HoffSet+cellSize*column,VoffSet+cellSize*row)
        p2 = graphics.Point(HoffSet+cellSize*(column+1),VoffSet+cellSize*(row+1))
        self.cellGraphic = graphics.Rectangle(p1, p2)
        self.cellGraphic.setOutline("black")

    def __repr__(self):
        return str((self.row, self.column))

    def setColor(self, color):
        self.cellGraphic.setFill(color)
        

class Wall:

    def __init__(self, row, column, edge, solid, orientation):
        self.row = row
        self.column = column
        self.solid = solid
        self.edge = edge
        self.orientation = orientation
        if orientation == 'v':
            p1 = graphics.Point(HoffSet+column*cellSize,VoffSet+row*cellSize)
            p2 = graphics.Point(HoffSet+column*cellSize,VoffSet+(row+1)*cellSize)
        else:
            p1 = graphics.Point(HoffSet+column*cellSize,VoffSet+row*cellSize)
            p2 = graphics.Point(HoffSet+(column+1)*cellSize,VoffSet+row*cellSize)
        self.wallGraphic = graphics.Line(p1, p2)
        self.refreshWall()


    def __repr__(self):
        if self.edge != False:
            return str(self.edge)+" edge of the maze"
        if self.orientation == 'v':
            s = "Vertical wall between "
            s += str((self.row, self.column))
            s += " and "
            s += str((self.row+1, self.column))
        else:
            s = "Horizontal wall between "
            s += str((self.row, self.column))
            s += " and "
            s += str((self.row, self.column+1))
        return s

    def setWall(self, solid):
        self.solid = solid
        self.refreshWall()

    def refreshWall(self):
        if self.solid and self.edge == False:
            self.wallGraphic.setOutline("white")
        elif self.solid:
            self.wallGraphic.setOutline("red")
        else:
            self.wallGraphic.setOutline("black")

class Player:

    def __init__(self, number):
        self.number = number
        self.row = None
        self.maze = None
        self.column = None
        self.figure = None
        self.heading = None
        self.standing = True
        self.alive = True

    def __repr__(self):
        return "Player " + str(self.number)

    def createFigure(self, anchor):
        if self.heading == None:
            self.figure = graphics.Circle(anchor,cellSize/2.5)
            self.figure.setOutline("yellow")
        else:
            if self.heading == 'N':
                p1x = anchor.getX() 
                p1y = anchor.getY() - cellSize/3.0 
                p2x = anchor.getX() - cellSize/5.0
                p2y = anchor.getY() + cellSize/3.0
                p3x = anchor.getX() + cellSize/5.0
                p3y = anchor.getY() + cellSize/3.0
            elif self.heading == 'S':
                p1x = anchor.getX() 
                p1y = anchor.getY() + cellSize/3.0 
                p2x = anchor.getX() - cellSize/5.0
                p2y = anchor.getY() - cellSize/3.0
                p3x = anchor.getX() + cellSize/5.0
                p3y = anchor.getY() - cellSize/3.0
            elif self.heading == 'E':
                p1x = anchor.getX() + cellSize/3.0 
                p1y = anchor.getY()
                p2x = anchor.getX() - cellSize/3.0
                p2y = anchor.getY() - cellSize/5.0
                p3x = anchor.getX() - cellSize/3.0
                p3y = anchor.getY() + cellSize/5.0
            elif self.heading == 'W':
                p1x = anchor.getX() - cellSize/3.0 
                p1y = anchor.getY()
                p2x = anchor.getX() + cellSize/3.0
                p2y = anchor.getY() - cellSize/5.0
                p3x = anchor.getX() + cellSize/3.0
                p3y = anchor.getY() + cellSize/5.0
            p1 = graphics.Point(p1x, p1y)
            p2 = graphics.Point(p2x, p2y)
            p3 = graphics.Point(p3x, p3y)
            self.figure = graphics.Polygon(p1, p2, p3)
            self.figure.setOutline("yellow")

    def move(self, direction, newHeading):
        """this function attempts to move the player
        in the desired direction, and gives them a new
        heading, it also assumes they are already inserted
        into the maze"""
        self.figure.undraw()
        self.heading = newHeading
        r = self.row
        c = self.column
        if direction == 'N' and not self.maze.Hwalls[r][c].solid:
            nextPt = self.getAnchor(r-1, c)
            self.row -= 1
        elif direction == 'S' and not self.maze.Hwalls[r+1][c].solid:
            nextPt = self.getAnchor(r+1, c)
            self.row += 1
        elif direction == 'W' and not self.maze.Vwalls[r][c].solid:
            nextPt = self.getAnchor(r, c-1)
            self.column -= 1
        elif direction == 'E' and not self.maze.Vwalls[r][c+1].solid:
            nextPt = self.getAnchor(r, c+1)
            self.column += 1
        else:
            nextPt = self.getAnchor(r, c)
        self.createFigure(nextPt)
        self.figure.draw(self.maze.win)

    def shoot(self, direction):
        """shoots in a direction, marking the death squares
        red as the shot moves"""
        r = self.row
        c = self.column
        wallCount = 0
        while True: #not at the end!
            if direction == 'N':
                if self.maze.getWall(r,c,'N').solid: wallCount += 1
                if wallCount > 1: break
                r -= 1
                self.maze.cells[r][c].cellGraphic.setFill('red')
            elif direction == 'W':
                if self.maze.getWall(r,c,'W').solid: wallCount += 1
                if wallCount > 1: break
                c -= 1
                self.maze.cells[r][c].cellGraphic.setFill('red')
            elif direction == 'E':
                if self.maze.getWall(r,c,'E').solid: wallCount += 1
                if wallCount > 1: break
                c += 1
                self.maze.cells[r][c].cellGraphic.setFill('red')
            elif direction == 'S':
                if self.maze.getWall(r,c,'S').solid: wallCount += 1
                if wallCount > 1: break
                r += 1
                self.maze.cells[r][c].cellGraphic.setFill('red')
            time.sleep(0.5)
            

    def getAnchor(self, row, column):
        return self.maze.cells[row][column].cellGraphic.getCenter()
                           

n = "N"
e = "E"
w = "W"
s = "S"
N = n
E = e
W = w
S = s 

m = Maze(7,8)
p = Player(1)
m.insertObj(2,3,p)
m.setWall(2,3,'v',False)
m.setWall(2,5,'v',False)
m.setWall(3,4,'h',False)
m.setWall(2,1,'v',False)
m.setWall(1,0,'h',False)
m.setWall(2,1,'v',False)
m.setWall(2,3,'v',False)
m.setWall(2,2,'v',False)
m.setWall(3,4,'v',False)
m.setWall(2,0,'h',False)
m.setWall(3,3,'h',False)

