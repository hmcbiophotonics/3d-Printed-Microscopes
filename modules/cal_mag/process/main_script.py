import numpy as np
from matplotlib import pyplot as plt
from matplotlib_scalebar.scalebar import ScaleBar
import sys

### START PROGRAM ###
if (len(sys.argv) == 1):
    print(f"USAGE: {sys.argv[0]} <dataset.npy>")
    exit()

sample = np.load(sys.argv[1])

spsize = 1.12e-6

# pack the red pixels of the bayer array
[m,n] = sample.shape
packed = np.zeros((int(m/2),int(n/2)))
packed = sample[1::2,1::2]

fig,axs = plt.subplots(2,2)
axs[0,0].title.set_text("Full FOV Image (RED Only)")
axs[0,0].imshow(packed)
axs[0,0].set_xticks(np.linspace(0,1500,4))
axs[0,0].set_yticks(np.linspace(0,1000,5))

# These values are for a different dataset
# x = [136,136]
# y = [110,211]

x = [170,170]
y = [132,260]

# Same here
# roi = packed[345:934,550:1147]
roi = packed[141:867,460:1186]
threshold = 700

axs[0,1].title.set_text("ROI")
axs[0,1].plot(x,y,color="red",linewidth=2)
axs[0,1].imshow(roi)
axs[0,1].set_xticks([])
axs[0,1].set_yticks([])

v_line = roi[y[0]:y[1],x[0]]

axs[1,0].axhline(y=threshold,color="red",linewidth=2)
axs[1,0].plot(v_line)
axs[1,0].title.set_text("Line Plot")
axs[1,0].set_xlabel('Pixel Number')
axs[1,0].set_ylabel('Pixel Intensity [a.u.]')
axs[1,0].set_yticks(np.linspace(0,1024,5))

filt = (v_line<=threshold)

axs[1,1].title.set_text("Threshold Line Plot")
axs[1,1].plot(filt)
axs[1,1].set_xlabel('Pixel Number')
axs[1,1].set_ylabel('Normalized Pixel Intensity [a.u.]')


# Now let's actually calculate the magnification

# Let's first compute the "width of each bar"

widths = []
pixel = 0
pixel_count = 0
re_pixels = []
fe_pixels = []
while (pixel < filt.size - 1):
    if (filt[pixel] == False and filt[pixel+1] == True):
        re_pixels.append(pixel)
    if (filt[pixel] == True and filt[pixel+1] == False):
        fe_pixels.append(pixel)
    pixel = pixel + 1
widths = np.array(re_pixels) - np.array(fe_pixels)
total_width = fe_pixels[2] - re_pixels[0]
print(f"Raw pixel widths for each bar: {widths}")
print(f"Raw rising-edge pixels: {re_pixels}")
print(f"Raw falling-edge pixels: {fe_pixels}")
print(f"Raw total width pixels: {total_width}")
avg_width = np.round(total_width/5)
print(f"Avg bar width pixels: {avg_width}")

# Since we are dealing with Group #4 Element #2
# Resolution = 2^(Group Number + (Element Number - 1)/6)
group = 4
element = 2
resolution = 2**(group + (element - 1)/6) # (lp/mm)

# one lp consists of two bars, thus the width of a bar should be equivalent to
# 1/(2*resolution)
actual_bar_width = (1/(2*resolution)) / 1000 # Let's put this in meters
captured_bar_width = avg_width * spsize * 2 # Remember the 2 here is due to the bayer array

magnification = captured_bar_width  / actual_bar_width
print(f"Actual bar width: {actual_bar_width}")
print(f"Captured_bar_width: {captured_bar_width}")
print(f'Magnification: {magnification}')

plt.figure()
plt.imshow(roi)
plt.title("ROI")
plt.set_cmap('gray')
ax = plt.gca()
ax.set_xticks([])
ax.set_yticks([])

plt.show()
