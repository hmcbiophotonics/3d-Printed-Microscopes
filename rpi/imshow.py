#!/usr/bin/env python3

from matplotlib import pyplot as plt
import numpy as np
import sys


vector = np.load(sys.argv[1])

red = vector[1::2,1::2]

plt.figure()
plt.imshow(red)
plt.show()
