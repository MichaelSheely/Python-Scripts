Python Games
==============

Here we have a set of python games that I wrote over the summer of 2014
during research at Harvey Mudd.

These files were written to be compatible with Python 3 and Windows.

The 2048 file uses the msvcrt module which grabs keypresses from the
keyboard and is able to interpret the input without requiring the user
to press the enter key.  However, the msvcrt module does not work on
non-Windows manchines, since it is operating system dependent.

keypress.py is a file which tests the import of the msvcrt modules and
prints the result of a keypress without the user pressing enter

mazeGeneration employs a depth first search algorithm to create a maze and
then uses the msvcrt module to allow the player to solve the maze.

connectFour originated as a project in my CS 5 (introduction to computer science)
class in which we designed a basic AI to play against other AIs or against humans
(or to play two humans against one another).  I made a few improvements to the 
graphics and user input over the summer, so here it is.
