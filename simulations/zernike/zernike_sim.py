#!/usr/bin/env python3
from zernikepy import zernike_polynomials
from matplotlib import pyplot as plt
import numpy as np

p = zernike_polynomials(mode=4, size = 256) # mode 4 is defocus

plt.figure()
plt.imshow(p)
plt.show()
