#!/usr/bin/env python3

import board
import adafruit_dotstar as dotstar
import numpy as np
import time
import sys
from pprint import pprint

ARRAY_SIZE = 8
MATRIX_SIZE = 8
N_DOTS = MATRIX_SIZE**2
BRIGHTNESS = 0.2

color_dict = {
    'red': (255,0,0),
    'green': (0,255,0),
    'blue': (0,0,255),
    'white': (255,255,255)
    'off': (0,0,0)
}

def clearDots(dots):
    for i in range(len(dots)):
        dots[i] = (0,0,0)

def illuminate_all(dots):
    for i in range(len(seq)):
        dots[seq[i]] = color_dict[color]

def illuminate_grid(dots):
    grid = np.array([
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,1,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0]])
    for i in range(len(seq)):
        c = grid.flatten()[i]
        dots[seq[i]] = tuple(c * comp for comp in color_dict[color])

dots = dotstar.DotStar(
    board.SCK,
    board.MOSI,
    N_DOTS,
    brightness=BRIGHTNESS
)

A = np.arange(0,ARRAY_SIZE**2)
ledMatrix = A.reshape((ARRAY_SIZE,ARRAY_SIZE))
# ledMatrix = np.rot90(ledMatrix)
ledMatrix = np.flip(ledMatrix,axis=0)
subMatrix = ledMatrix[1:8,0:7]

seq = subMatrix.flatten()

clearDots(dots)


mode = sys.argv[1]
try:
    color = sys.argv[2]
except:
    color = 'off'

if mode == '':
    exit()
elif mode == 'all':
    illuminate_all(dots)
elif mode == 'grid':
    illuminate_grid(dots)
elif mode == 'off':
    clearDots(dots)
    dots.deinit()
else:
    exit()
