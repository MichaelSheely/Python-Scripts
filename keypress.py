import msvcrt
import time
import graphics
import random

while True:
    char = msvcrt.getwch()
    if char == 'a':
        print("Left")
    if char == 's':
        print("Down")
    if char == 'd':
        print("Right")
    if char == 'w':
        print("Up")
    if char == 'q':
        break




