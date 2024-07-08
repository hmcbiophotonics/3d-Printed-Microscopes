### view the most recently capture bayer picture in matplotlib ###

import numpy as np
import os
from pprint import *
from matplotlib import pyplot as plt


format = "SBGGR10"
cwd = os.getcwd()
path = os.path.join(cwd,"capture_data")

files = os.listdir(path)
max = 0
recent_f = ""
for f in files:
    fnum = int(f.replace(f"RPI_{format}","").replace("_","").replace(".npy",""))
    if (fnum > max):
        max = fnum
        recent_f = f


data = np.load(os.path.join(path,recent_f))

rgb = np.zeros(data.shape+(3,), dtype=data.dtype)
rgb[0::2,0::2,2] = data[0::2,0::2] #B
rgb[0::2,1::2,1] = data[0::2,1::2] #G
rgb[1::2,0::2,1] = data[1::2,0::2] #G
rgb[1::2,1::2,0] = data[1::2,1::2] #R

plt.subplot(2,2,1)
plt.title("Raw Bayer Image in RGB mixed format")
plt.imshow(rgb)
ax = plt.gca()
ax.set_xticks([])
ax.set_yticks([])


plt.subplot(2,2,2)
r = rgb.copy()
r[:,:,[1,2]] = 0
plt.title("Red Component")
plt.imshow(r)
ax = plt.gca()
ax.set_xticks([])
ax.set_yticks([])

plt.subplot(2,2,3)
g = rgb.copy()
g[:,:,[0,2]] = 0
plt.title("Green Component")
plt.imshow(g)
ax = plt.gca()
ax.set_xticks([])
ax.set_yticks([])

plt.subplot(2,2,4)
b = rgb.copy()
b[:,:,[0,1]] = 0
plt.title("Blue Component")
plt.imshow(b)
ax = plt.gca()
ax.set_xticks([])
ax.set_yticks([])

plt.show()
