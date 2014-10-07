#
# hw10pr3
# Connect Four: AI
#
# Due: 11/18/2013

""" Includes an errorchecker function which makes it more difficult to break while entering moves """
import random
import time
from graphics import *

class Player:
    """ A player with a certain type of move token and can evaluate the board for future moves """
    def __init__(self, ox, tbt, ply):
        """ the constructor """
        self.ox = ox.upper()
        self.tbt = tbt
        self.ply = ply

    def __repr__( self ):
        """ creates an appropriate string """
        s = "Player for " + self.ox + "\n"
        s += "  with tiebreak type: " + self.tbt + "\n"
        s += "  and ply == " + str(self.ply) + "\n\n"
        return s
    
    def oppCh(self):
        """ returns the opposite token as the player calling this """
        if self.ox == 'O':
            return 'X'
        else: return 'O'

    def scoreBoard(self, b):
        """ returns a float value representing the score of the input b """
        if b.winsFor(self.ox):
            return 100.0
        elif b.winsFor(self.oppCh()):
            return 0.0
        else:
            return 50.0

    def tiebreakMove(self, scores):
        """ takes in a nonempty list of floating-point numbers.  Choses the highest score, returning its column number: breaks ties based on the tiebreaking type of the player calling the function"""
        possible_moves = []
        m = max(scores)
        for i in range(len(scores)):
            if scores[i] == m:
                possible_moves += [i]
        if self.tbt in ['random', 'Random', 'rdm', 'rand', 'RANDOM']:
            return random.choice(possible_moves)
        elif self.tbt in ['left', 'Left', 'LEFT']:
            return possible_moves[0]
        elif self.tbt in ['right', 'Right', 'RIGHT']:
            return possible_moves[-1]

    def scoresFor(self, b):
        """ Returns a list of scores, with the element of the list corresponding to the "goodness" of the input board after the number of moves represented by the index """
        scores = [50.0]*len(b.data[0])
        for col in range(len(b.data[0])):
            if b.data[0][col] != ' ':
                scores[col] = -1
            elif self.scoreBoard(b) != 50.0:
                scores[col] = self.scoreBoard(b)
            elif self.ply == 0:
                scores[col] = self.scoreBoard(b)
            else:
                b.addMove(col, self.ox, "noShow")
                if self.scoreBoard(b) == 100.0:
                    scores[col] = 100.0
                else:
                    p2 = Player(self.oppCh(), self.tbt, self.ply -1)
                    p2scores = p2.scoresFor(b)
                    if 100.0 in p2scores:
                        scores[col] = 0.0
                    elif 50.0 in p2scores:
                        scores[col] = 50.0
                    else:
                        scores[col] = 100.0
                b.delMove(col)
        return scores
            
    def nextMove(self,b):
        """ Takes in b, and object of type Board and returns an integer representing the column number that the player will next move to """
        possmoves = self.scoresFor(b)
        return self.tiebreakMove(possmoves)
                
class Board:
    """ A board with an arbitrary certain height and width and data representing tokens filling the connect four slots"""

    def __init__(self, width, height):
        """ constructs Board type objects """
        self.width = width
        self.height = height
        W = self.width
        H = self.height
        self.data = [[' ']*W for row in range(H)]
        self.win = GraphWin("Connect_Four", 60*(width), 60*(height+1))
        self.graphical_data = []
        for row in range(height+1):
            new_row = []
            for col in range(width):
                if row < height:
                    #the center is a Point (pixel col, pixel row)
                    center = Point(50 + 50*col, 50 + 50*row)
                    c = Circle(center, 10)
                    c.draw(self.win)
                    new_row += [c]
                else:
                    center = Point(50 + 50*col, 50 + 50*row)
                    c = Text(center, col%10)
                    c.draw(self.win)
                    new_row += [c]
            self.graphical_data += [new_row]
            

    def __repr__(self):
        """ Prints a viusal representation of a board """
        H = self.height
        W = self.width
        s = '' #the string to return
        for row in range(0,H):
            s += '|'
            for col in range(0,W):
                s += self.data[row][col] + '|'
            s += '\n'
        s += (2*W+1)*'-' #bottom of board
        n = ' ' #sets first character to a space
        for num in range(W):
            n += str(num%10) + ' ' #adds the next cardinal digit
        s += '\n' + n
        return s

    def addMove(self, col, ox, display = "show"):
        """Places the given character into the given column"""
        H = self.height
        for vert in range(H-1,-1,-1):
            if self.data[vert][col] == ' ':
                self.data[vert][col] = ox
                break
        if display == "noShow":
            return
        for row in range(self.height):
            for width in range(self.width):
                if self.data[row][width] == "X":
                    color = 'red'
                    self.graphical_data[row][width].setFill(color)
                elif self.data[row][width] == "O":
                    color = 'black'
                    self.graphical_data[row][width].setFill(color)
                else:
                    color = 'white'
                    self.graphical_data[row][width].setFill(color)

    def clear(self):
        """ Clears the board that called it """
        for x in range(len(self.data)):
            for i in range(len(self.data[x])):
                self.data[x][i] = ' '
        for row in range(self.height):
            for width in range(self.width):
                if self.data[row][width] == "X":
                    color = 'red'
                    self.graphical_data[row][width].setFill(color)
                elif self.data[row][width] == "O":
                    color = 'black'
                    self.graphical_data[row][width].setFill(color)
                else:
                    color = 'white'
                    self.graphical_data[row][width].setFill(color)
        return

    def setBoard(self, moveString):
        """ takes in a string of columns and places alternating checkers in those columns, starting with 'X'            
            For example, call b.setBoard('012345') to see 'X's and 'O's alternate on the bottom row, or b.setBoard('000000') to see them alternate in the left column.
            moveString must be a string of integers """
        nextCh = 'X'
        for colString in moveString:
            col = int(colString)
            if 0 <= col <= self.width:
                self.addMove(col, nextCh)
            if nextCh == 'X': nextCh = 'O'
            else: nextCh = 'X'

    def allowsMove(self, c):
        """ Checks if a given move is legal, if so returns True, else returns False """
        if c < 0 or c >= self.width:
            return False
        if self.data[0][c] != ' ':
            return False
        return True

    def isFull(self):
        """ Checks if the top row is completely full, if so, return True, if not, return False """
        for col in range(self.width):
            if self.allowsMove(col): #If you can drop a token in anywhere, then the board isn't full (assuming gravity, and we haven't hacked the system and made tokens float along the top.  If he had done that, we could always just check each element of each list of the "data" list, much as we did in the self.clear() function.
                return False
        return True

    def delMove(self, c):
        """ Deltetes the topmost token from column c.  If column c is empty, nothing happens """
        for row in range(self.height):
            if self.data[row][c] != ' ':
                self.data[row][c] = ' '
                return

    def winsFor(self, ox):
        """ Returns true if there are four checkers of a given type ox in a row, column, or diagonal of the board """
        if self.four_in_row(ox) or self.four_in_col(ox) or self.four_in_diag(ox):
            return True
        return False

    def four_in_row(self, ox):
        """ Returns true if there are four checkers of a given type ox in a row of the board """
        for row in range(len(self.data)):
            for col in range(len(self.data[0])-3):
                if self.data[row][col] == ox:
                    if self.data[row][col+1] == ox:
                        if self.data[row][col+2] == ox:
                            if self.data[row][col+3] == ox:
                                return True
        return False
        
    def four_in_col(self, ox):
        """ Returns true if there are four checkers of a given type ox in a column of the board """
        for col in range(len(self.data[0])):
            for row in range(len(self.data) - 3):
                if self.data[row][col] == ox:
                    if self.data[row+1][col] == ox:
                        if self.data[row+2][col] == ox:
                            if self.data[row+3][col] == ox:
                                return True
        return False
                
            
    def four_in_diag(self, ox):
        """ Returns true if there are four checkers of a given type ox in a diagonal of the board """
        for col in range(len(self.data[0])-3):  #checks for a negative victory for ox
            for row in range(len(self.data) - 3):
                if self.data[row][col] == ox:
                    if self.data[row+1][col+1] == ox:
                        if self.data[row+2][col+2] == ox:
                            if self.data[row+3][col+3] == ox:
                                return True
        for col in range(len(self.data[0])-3):
            for row in range(3,len(self.data)):
                if self.data[row][col] == ox:
                    if self.data[row-1][col+1] == ox:
                        if self.data[row-2][col+2] == ox:
                            if self.data[row-3][col+3] == ox:
                                return True
        return False
        # diagonal positive victory for x: b.setBoard('01122323343')
        # diagonal negative victory for x: b.setBoard('43322121101')
        # row victory for x: b.setBoard('01232435415')
        # column victory for x: b.setBoard('1212131')



    def playGame(self, px, po):
        """ Hosts a game of connect four, calling on the nextMove method for px and po, which will be objects of type player """
        while True:
            print("Welcome to Connect Four!")
            print(self)
            print()
            turn = 'X'
            player = 'Player 1'
            while True:
                if (turn == 'X' and px == 'human') or (turn=='O' and po == 'human'):
                    col = errorchecker(player)
                    if self.allowsMove(col):
                        self.addMove(col, turn)
                        if self.winsFor(turn):
                            print(self)
                            print('Good game '+player+'!')
                            time.sleep(1.5)
                            break
                        elif self.isFull():
                            print(self)
                            print('Board is full, game over!')
                            break
                        elif turn == 'X':
                            turn = 'O'
                            player = 'Player 2'
                        else:
                            turn = 'X'
                            player = 'Player 1'
                        print(self)
                        print()
                    else:
                        print("That is not a valid move, please choose again.")
                else:
                    if turn == 'X':
                        move = px.nextMove(self)
                    else:
                        move = po.nextMove(self)
                    self.addMove(move, turn)
                    if self.winsFor(turn):
                        print(self)
                        print('Good game '+player+'!')
                        time.sleep(1.5)
                        break
                    elif self.isFull():
                        print(self)
                        print('Board is full, game over!')
                        break
                    elif turn == 'X':
                        turn = 'O'
                        player = 'Player 2'
                    else:
                        turn = 'X'
                        player = 'Player 1'
                    print(self)
                    print()
                    
            self.clear()
            while True:
                x = errorchecker_playagain()
                if x == True:
                    break
                elif x == False:
                    print("Goodbye")
                    return
                else:
                    print("I don't recognize that input.")

def errorchecker(player):
    """ Tries to convert x into a number, if unable, prompts for another input without crashing """
    while True:
        try:
            x = input(player+" make your move: ")
            x = int(round(float(x)))
            return x
        except (ValueError,TypeError,NameError,IOError):  #I found these types of errors on a python site: http://docs.python.org/2/tutorial/errors.html
            print("Oops! That was not a valid number.  Try again...")

def errorchecker_playagain():
    """ Tries to make sense of what the user wants to do """
    again = input('Would you like to play again? ')
    while True:
        try:
            if again in ['1', 'yes', 'Yes', 'okay', 'Alright', 'alright', 'y', 'Y', 'absolutely', 'Absolutely']:
                return True
            elif again in ['0', 'no', 'No', 'nope', 'Nope', 'n', 'N', 'NO', 'NOPE', 'never', 'Never', 'NEVER', 'NEVAR']:
                    return False
            else: return 'Wat?'
        except (ValueError,TypeError,NameError,IOError):
            print("I don't recognize that input.")


p1 = input("Player 1: Human or AI?\n")
if p1.lower() in ['human', 'h', 'person']:
    p1 = 'human'
elif p1.lower() in ['ai', 'a', 'artificialinteligence', 'artificial inteligence']:
    ply = int(input("Player 1 ply?\n"))
    p1 = Player('O', 'random', ply)
else:
    print('Did not recognize that command!')
    time.sleep(1)
    quit()
p2 = input("Player 2: Human or AI?\n")
if p2.lower() in ['human', 'h', 'person']:
    p2 = 'human'
elif p2.lower() in ['ai', 'a', 'artificialinteligence', 'artificial inteligence']:
    print("made it!")
    ply = int(input("Player 2 ply?\n"))
    p2 = Player('X', 'random', ply)
else:
    print('Did not recognize that command!')
    time.sleep(1)
    quit()
b = Board(int(input("Number of columns?\n")),int(input("Number of rows?\n")))
b.playGame(p1, p2)




            
