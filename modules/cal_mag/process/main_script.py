import numpy as np
from matplotlib import pyplot as plt
from matplotlib_scalebar.scalebar import ScaleBar
import sys
import os
import json


def inputData(type):
    data = {}
    print(f"Enter coordinates for {type}")
    print("=====================")
    if type == "roi":
        x0 = int(input("Upper left x coordinate: "))
        y0 = int(input("Upper left y coordinate: "))
        x1 = int(input("Lower right x coordinate: "))
        y1 = int(input("Lower right y coordinate: "))
        data = {
            'x0': x0, 'y0': y0,
            'x1': x1, 'y1': y1
        }
    elif type == "vbar":
        x = int(input("x coordinate: "))
        y0 = int(input("Upper y coordinate: "))
        y1 = int(input("Lower y coordinate: "))
        data = {
            'x': x,
            'y0': y0, 'y1': y1
        }
    return data

### START PROGRAM ###
if (len(sys.argv) == 1):
    print(f"USAGE: {sys.argv[0]} <dataset.npy>")
    exit()

file_path = sys.argv[1]
sample = np.load(file_path)

spsize = 1.12e-6

# pack the red pixels of the bayer array
[m,n] = sample.shape
packed = np.zeros((int(m/2),int(n/2)))
packed = sample[1::2,1::2]

fig,axs = plt.subplots(2,2)

scalebar = ScaleBar(spsize*2,color='red',frameon=False,location='lower right')

axs[0,0].title.set_text("Full FOV Image (RED Only)")
axs[0,0].imshow(packed)
axs[0,0].set_xticks(np.linspace(0,1500,4))
axs[0,0].set_yticks(np.linspace(0,1000,5))
axs[0,0].add_artist(scalebar)
plt.ion()
plt.show()

print("Looking for associated metadata for ROI coordinates...")
dataset_dir, dataset_name = os.path.split(file_path)
metadata_path = os.path.join(dataset_dir,'metadata.json')

# if path exists just read from the file
# if path exists but doesnt have what we need append
# if path doesnt exist create a new file and append

roi_coords = { }
metadata_file = None

try:
    metadata_file = open(metadata_path, 'r+')
    print("metadata successfully opened")
    metadata = json.load(metadata_file)
    if dataset_name in metadata.keys():
        print(f"{dataset_name} found")
        while True:
            update_roi = input("Would you like to update the region of interest (Y/N)?: ")
            if update_roi.upper() == "Y":
                roi_coords = inputData('roi')
                metadata[dataset_name]['roi'] = roi_coords
                metadata_file.seek(0)
                json.dump(metadata,metadata_file,indent=4)
                break
            elif update_roi.upper() == "N":
                roi_coords = metadata[dataset_name]['roi']
                break
            continue
    else:
        print(f"{dataset_name} not found")
        roi_coords = inputData('roi')
        metadata[dataset_name] = {
            "roi": roi_coords
        }
        metadata_file.seek(0)
        json.dump(metadata,metadata_file,indent=4)
except FileNotFoundError:
    print("metadata file dne, creating a new one...")
    metadata_file = open(metadata_path, 'w')
    roi_coords = inputData('roi')
    metadata = {
        dataset_name: {
            "roi": roi_coords
        }
    }
    json.dump(metadata,metadata_file,indent=4)

# Plot the ROI
roi = packed[roi_coords['y0']:roi_coords['y1'],
             roi_coords['x0']:roi_coords['x1']]

scalebar = ScaleBar(spsize*2,color='red',frameon=False,location='lower right')

axs[0,1].title.set_text("ROI")
axs[0,1].imshow(roi)
axs[0,1].set_xticks([])
axs[0,1].set_yticks([])
axs[0,1].add_artist(scalebar)

plt.show()

# Input threshold coords
if 'vbar' in metadata[dataset_name].keys():
    while True:
        update_vbar = input("Would you like to update the vertical bar (Y/N)?: ")
        if update_vbar.upper() == "Y":
            vbar_coords = inputData('vbar')
            metadata[dataset_name]['vbar'] = vbar_coords
            metadata_file.seek(0)
            json.dump(metadata,metadata_file,indent=4)
            break
        elif update_vbar.upper() == "N":
            vbar_coords = metadata[dataset_name]['vbar']
            break
        continue
else:
    vbar_coords = inputData('vbar')
    metadata[dataset_name]['vbar'] = vbar_coords
    metadata_file.seek(0)
    json.dump(metadata,metadata_file,indent=4)
metadata_file.close()

threshold = 400

# Threshold Line Coords

axs[0,1].plot([vbar_coords['x'],vbar_coords['x']],
              [vbar_coords['y0'],vbar_coords['y1']],
              color="red",linewidth=2)

v_line = roi[vbar_coords['y0']:vbar_coords['y1'],vbar_coords['x']]

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
plt.ioff()


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
try:
    total_width = fe_pixels[2] - re_pixels[0]
except Exception as e:
    print(e)
    total_width = 5
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
print(f"Resolution: {resolution}")

# one lp consists of two bars, thus the width of a bar should be equivalent to
# 1/(2*resolution)
actual_bar_width = (1/(2*resolution)) / 1000 # Let's put this in meters
captured_bar_width = avg_width * spsize * 2 # Remember the 2 here is due to the bayer array

magnification = captured_bar_width  / actual_bar_width
print(f"Actual bar width: {actual_bar_width}")
print(f"Captured_bar_width: {captured_bar_width}")
print(f'Magnification: {magnification}')

scalebar = ScaleBar(spsize*2,color='red',frameon=False,location='lower right')

plt.figure()
plt.imshow(roi)
plt.title("ROI")
plt.set_cmap('gray')
ax = plt.gca()
ax.set_xticks([])
ax.set_yticks([])
ax.add_artist(scalebar)

plt.show()
