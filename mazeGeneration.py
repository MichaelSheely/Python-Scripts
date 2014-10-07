import random
import msvcrt
import time
import graphics

cellSize = 15

class Maze:

    def __init__(self, columns, rows):
        self.openRows = rows
        self.openCols = columns
        self.rows = rows*2+1
        self.cols = columns*2+1
        self.data = self.initialize()

    def __repr__(self):
        string = ""
        for y in self.data:
            for x in y:
                if x.wall:
                    string += "X"
                elif x.special:
                    string += str(x.special)
                else:
                    string += " "
            string += "\n"
        return string

    def initialize(self):
        data = []
        for y in range(self.rows):
            aRow = []
            if y % 2 == 0:
                for x in range(self.cols):
                    aRow += [Cell(x,y,self,True)]
            else:
                for x in range(self.cols):
                    if x % 2 == 0:
                        aRow += [Cell(x,y,self,True)]
                    else:
                        aRow += [Cell(x, y, self)]
            data += [aRow]
        return data

    def getSquare(self, x, y):
        """returns the cell at x,y ignoring walls"""
        if x < 0 or y < 0:
            return "Too Small"
        elif x*2+2 > self.cols or y*2+2 > self.rows:
            return "Too Large"
        else:
            return self.data[y*2+1][x*2+1]

    def showSquare(self, x, y):
        """shows x, y in true coordinates"""
        if x < 0 or y < 0:
            return "Too Small"
        elif x > self.cols-1 or y > self.rows-1:
            return "Too Large"
        else:
            string = ''
            for row in self.data:
                for col in row:
                    if col.col == x and col.row == y:
                        string += '@'
                    elif col.wall:
                        string += 'X'
                    else:
                        string += ' '
                string += '\n'
        print(string)

    def chooseOpenCell(self, special=False):
        if not special:
            while True:
                cell = random.choice(random.choice(self.data))
                if not cell.wall:
                    return cell
        possibleOptions = []
        for y in range(1,len(self.data)-1):
            for x in range(1,len(self.data[0])-1):
                cell = self.data[y][x]
                if not cell.wall:
                    if cell.hasThreeWallsIntact():
                        if not cell.special:
                            return cell
        time.sleep(40)

    def makeCellsSpecial(self):
        goal = self.chooseOpenCell(True)
        goal.special = 'G'
        character = self.chooseOpenCell(True)       
        character.special = '@'
        return character

                        

class Cell:

    def __init__(self, col, row, maze, isWall=False):
        self.row = row
        self.col = col
        self.wall = isWall
        self.memberOf = maze
        self.visited = False
        self.inMaze = False
        self.special = False

    
    def __repr__(self):
        string = ''
        if self.wall:
            string += 'Wall'
        else:
            string += 'Open square'
        string +=' at col: '+str(self.col)+' and row: '+str(self.row)
        return string

    def getWallNeighbors(self):
        x = self.col
        y = self.row
        neighbors = []
        if x > 1:
            neighbors += [self.memberOf.data[y][x-1]]
        if y > 1:
            neighbors += [self.memberOf.data[y-1][x]]
        if x < self.memberOf.cols*2:
            neighbors += [self.memberOf.data[y][x+1]]
        if y < self.memberOf.rows*2:
            neighbors += [self.memberOf.data[y+1][x]]
        return neighbors

    def getCellNeighbors(self):
        x = self.col
        y = self.row
        neighbors = []
        if x > 2:
            neighbors += [self.memberOf.data[y][x-2]]
        if y > 2:
            neighbors += [self.memberOf.data[y-2][x]]
        if x < self.memberOf.cols - 2:
            neighbors += [self.memberOf.data[y][x+2]]
        if y < self.memberOf.rows - 2:
            neighbors += [self.memberOf.data[y+2][x]]
        return neighbors

    def hasThreeWallsIntact(self):
        x = self.col
        y = self.row
        walls = 0
        if self.memberOf.data[y][x-1].wall:
            walls += 1
        if self.memberOf.data[y][x+1].wall:
            walls += 1
        if self.memberOf.data[y-1][x].wall:
            walls += 1
        if self.memberOf.data[y+1][x].wall:
            walls += 1
        if walls == 3:
            return True
        else:
            return False

    def hasFourWallsIntact(self):
        x = self.col
        y = self.row
        if self.memberOf.data[y][x-1].wall:
            if self.memberOf.data[y][x+1].wall:
                if self.memberOf.data[y-1][x].wall:
                    if self.memberOf.data[y+1][x].wall:
                        return True
        return False

    def wallBetween(self, cell2):
        x1 = self.col
        x2 = cell2.col
        y1 = self.row
        y2 = cell2.row
        if x1 - x2 == 2:
            return self.memberOf.data[y1][x2 + 1]
        if x1 - x2 == -2:
            return self.memberOf.data[y1][x2 - 1]
        if y1 - y2 == 2:
            return self.memberOf.data[y2 + 1][x1]
        if y1 - y2 == -2:
            return self.memberOf.data[y2 - 1][x1]
    
            
def refine(maze):
    cellStack = []
    totalCells = maze.openRows*maze.openCols
    currentCell = maze.chooseOpenCell()
    visited = 1
    while visited < totalCells:
        surroundingCells = currentCell.getCellNeighbors()
        random.shuffle(surroundingCells)
        for cell in surroundingCells:
            if cell.hasFourWallsIntact():
                currentCell.wallBetween(cell).wall = False
                cellStack += [currentCell]
                currentCell = cell
                visited += 1
                break
            if surroundingCells.index(cell) == len(surroundingCells) - 1:
                currentCell = cellStack.pop()
    character = maze.makeCellsSpecial()
    return character


def playGame(maze, c):
    d = {}
    mazeWin = graphics.GraphWin("Maze", len(maze.data[0])*cellSize, len(maze.data)*cellSize)
    for y in range(len(maze.data)):
        for x in range(len(maze.data[y])):
            p1 = graphics.Point(cellSize*x, cellSize*y)
            p2 = graphics.Point(cellSize*(x+1), cellSize*(y+1))
            d[(x,y)] = graphics.Rectangle(p1, p2)
            rect = d[(x,y)]
            cell = maze.data[y][x]
            if cell.wall:
                rect.setFill("blue")
            elif cell.special == 'G':
                rect.setFill("red")
            elif cell.special == '@':
                rect.setFill("green")
            else:
                rect.setFill("white")
            rect.draw(mazeWin)
    while True:
        x = c.col
        y = c.row
        char = msvcrt.getwch()
        if char == 'a':
            if not maze.data[y][x-1].wall:
                c.special = False
                c = maze.data[y][x-1]
                d[(x,y)].setFill("white")
                d[(x-1,y)].setFill("green")
        if char == 's':
            if not maze.data[y+1][x].wall:
                c.special = False
                c = maze.data[y+1][x]
                d[(x,y)].setFill("white")
                d[(x,y+1)].setFill("green")
        if char == 'd':
            if not maze.data[y][x+1].wall:
                c.special = False
                c = maze.data[y][x+1]
                d[(x,y)].setFill("white")
                d[(x+1,y)].setFill("green")
        if char == 'w':
            if not maze.data[y-1][x].wall:
                c.special = False
                c = maze.data[y-1][x]
                d[(x,y)].setFill("white")
                d[(x,y-1)].setFill("green")
        if char == 'q':
            print("Bye!")
            time.sleep(1)
            return "QUIT"
        if c.special == 'G':
            c.special = '@'
            print("Congratulations! You've completed the maze!")
            time.sleep(1)
            mazeWin.close()
            return "Next Level"
        c.special = '@'


while True:
    x = input("Please pick a size for your maze.\n")
    try:
        x = int(x)
        if x > 1:
            break
        print("Please enter a valid input (s > 1).")
    except ValueError:
        print("Please enter a valid input (s > 1).")
        

level = 0
playAgain = "Next Level"
while playAgain == "Next Level":
    print("Level " + str(level))
    m = Maze(x, x)
    c = refine(m)
    x += random.choice([0,1])
    level += 1
    playAgain = playGame(m, c)
