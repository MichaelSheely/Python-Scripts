#### python 2048 ####
import math
import random
import graphics
import msvcrt
import time

cellSize = 50

class Board:

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.board = {}
        for col in range(cols):
            for row in range(rows):
                self.board[(col, row)] = Block(col, row, 0)

    def __repr__(self):
        string = ''
        for y in range(self.rows):
            arow = ''
            for x in range(self.cols):
                arow += str(self.board[(x,y)].number)
            string += arow + '\n'
        return string

    def generateNewBlock(self):
        for attempt in range(self.cols*self.rows):
            x = random.choice(range(self.cols))
            y = random.choice(range(self.rows))
            choice = self.board[(x,y)]
            if choice.number == 0:
                choice.number = random.choice([2]*5+[4])
                return False
        for i in self.board:
            if self.board[i].number == 0:
                self.board[i].number = random.choice([2]*5+[4])
                return False
        for i in self.board:
            print(self.board[i].number)
            return True


    def push(self, direction):
        if direction == 'up':
            for y in range(1, self.rows):
                for x in range(self.cols): 
                    self.board[(x,y)].getPushed(direction, self)
        if direction == 'down':
            for y in range(self.rows-1, -1, -1):
                for x in range(self.cols):
                    self.board[(x,y)].getPushed(direction, self)
        if direction == 'left':
            for x in range(1, self.cols):
                for y in range(self.rows):
                    self.board[(x,y)].getPushed(direction, self)
        else:
            for x in range(self.cols-1, -1, -1):
                for y in range(self.rows):
                    self.board[(x,y)].getPushed(direction, self)
        

class Block:

    def __init__(self, x, y, number, color = "white"):
        self.x = x
        self.y = y
        self.number = number
        self.color = color
        p1 = graphics.Point(cellSize*x, cellSize*y)
        p2 = graphics.Point(cellSize*(x+1), cellSize*(y+1))
        self.visual = graphics.Rectangle(p1,p2)
        self.text = graphics.Text(graphics.Point(cellSize*(x+0.5), cellSize*(y+0.5)), str(self.number))
        

    def __repr__(self):
        return str(number) + " located at x = " + str(x) + ", y = " + str(y)

    def checkDestination(self, direction, board):
        try:
            if direction == 'up':
                dest = board.board[(self.x, self.y-1)]
            elif direction == 'down':
                dest = board.board[(self.x, self.y+1)]
            elif direction == 'left':
                dest = board.board[(self.x-1, self.y)]
            else:
                dest = board.board[(self.x+1, self.y)]
            if dest.number == 0:
                return 'destinationEmpty'
            else:
                return dest
        except KeyError:
            return None

    def getPushed(self, direction, board):
        if self.number == 0:
            return
        destination = self.checkDestination(direction, board)
        if destination == None: #the block is at the edge
            return
        if destination == 'destinationEmpty':
            newPosition = self.move(direction, board)
            newPosition.getPushed(direction, board)
        elif self.canConbine(destination):
            self.combine(destination)
            return

    def move(self, direction, board):
        newTile = None
        if direction == 'up':
            newTile = board.board[self.x, self.y-1]
            newTile.number = self.number
            newTile.color = self.color
        elif direction == 'down':
            newTile = board.board[self.x, self.y+1]
            newTile.number = self.number
            newTile.color = self.color
        elif direction == 'left':
            newTile = board.board[self.x-1, self.y]
            newTile.number = self.number
            newTile.color = self.color
        else:
            newTile = board.board[self.x+1, self.y]
            newTile.number = self.number
            newTile.color = self.color
        self.number = 0
        self.setColor()
        return newTile
    
            
    def canConbine(self, other):
        """checks if two blocks can combine"""
        if self.number == other.number:
            if self.number != 0:
                vdist = math.fabs(self.y - other.y)
                hdist = math.fabs(self.x - other.x)
                if (vdist == 1 or hdist == 1) and not (vdist == 1 and hdist == 1):
                    return True
        else:
            return False

    def combine(self, other):
        other.number *= 2
        other.setColor()
        self.number = 0
        self.setColor()

    
    def setColor(self):
        if self.number == 2:
            self.color = 'yellow'
        elif self.number == 4:
            self.color = 'orange'
        elif self.number == 8:
            self.color = 'purple'
        elif self.number == 16:
            self.color = 'green'
        elif self.number == 32:
            self.color = 'medium aquamarine'
        elif self.number == 64:
            self.color = 'DarkKhaki'
        elif self.number == 128:
            self.color = 'red'
        elif self.number == 256:
            self.color = 'light cyan'
        elif self.number == 512:
            self.color = 'blue'
        elif self.number == 1024:
            self.color = 'grey'
        elif self.number == 2048:
            self.color = 'gold'
        else:
            self.color = 'white'
        self.visual.setFill(self.color)


def main():
    size = input("Choose the size of your board.\n")
    b = Board(int(size),int(size))
    b.generateNewBlock()
    win = graphics.GraphWin("TheBoard", b.cols*cellSize, b.rows*cellSize)
    gameOver = False
    for i in b.board:
        b.board[i].visual.draw(win)
        b.board[i].text.draw(win)
    while not gameOver:
        for i in b.board:
            b.board[i].setColor()
            if b.board[i].number != 0:
                b.board[i].text.setText(str(b.board[i].number))
            else:
                b.board[i].text.setText("")
        char = msvcrt.getwch()
        move = None
        if char == 'a':
            move = 'left'
        if char == 's':
            move = 'down'
        if char == 'd':
            move = 'right'
        if char == 'w':
            move = 'up'
        if char == 'q':
            print("Bye!")
            time.sleep(1)
            return
        if type(move) == type(''):
            b.push(move)
            gameOver = b.generateNewBlock()
    return "GAME OVER"

main()
