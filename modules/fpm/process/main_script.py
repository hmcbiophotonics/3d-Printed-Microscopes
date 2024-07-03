from fourierptychography import FourierPtychography as FP
from plot import Plot
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider
from mpl_toolkits.axes_grid1 import make_axes_locatable # For nice colorbars
import numpy as np
import os
import sys

### Experimental Setup Params ###

### For raspberry pi camera module v2 ###
focal_length       = 3.04e-3
f_stop             = 2.0
aperture_diameter  = focal_length / f_stop
front_stop_sep     = 1e-3
magnification      = 1.5049504950495052
magnification = 1.5
object_dist        = ((1 + magnification) / magnification) * focal_length
image_dist         = magnification * object_dist
#num_aperture       = np.sin(np.arctan(0.5 * aperture_diameter / (object_dist - front_stop_sep)))
num_aperture       = 0.18
wavelength         = 623e-9
sensor_pixel_size  = 1.12e-6 * 2 / magnification
led_dist_to_sample = 60e-3
led_separation     = 3.175e-3
led_number         = 8
led_number_used    = 7


config = {
        "num_aperture" : num_aperture,
        "wavelength"   : wavelength,
        "spsize"       : sensor_pixel_size,
        "led_dist"     : led_dist_to_sample,
        "led_sep"      : led_separation,
        "led_num"      : led_number,
        "arraysize"    : led_number_used,
        }

### START PROGRAM ###

if (len(sys.argv) == 1):
    print(f"USAGE: {sys.argv[0]} <dataset.npy>")
    exit()

sample = np.load(sys.argv[1])


###
print(f"aperture_diameter: {aperture_diameter}")
print(f"NA: {num_aperture}")
print(f"iD: {image_dist}")
print(f"oD: {object_dist}")
print(f"nyquist resolution limit: {wavelength/(2*num_aperture)}")
print(f"sensor_pixel_size: {sensor_pixel_size}")

FPM = FP()
FPM.create_configuration(config)


#FPM.recover(cropped)
[numim,m,n] = sample.shape
packed = np.zeros((numim,int(m/2),int(n/2)))
packed = sample[:,1::2,1::2]
[cx,cy] = FP.get_LED_center(packed[24].copy())
[cx,cy] = [880,520]

size = 64
cropped = packed[:,cy-size:cy+size,cx-size:cx+size]

loop = 5
pupil = 1
recovered, recoveredFT, trackRecoveredFT, pupil = FPM.recover(cropped,loop,pupil)


def add_colorbar(him, ax, cbar_title=""):
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    cbar = fig.colorbar(him, cax=cax)
    cbar.set_label(cbar_title, rotation=270, labelpad=15)

ims = [0,0,0]
fig, axs = plt.subplots(3,1,figsize=(4,10))
plt.suptitle(f'{loop} loops')
ims[0] = axs[0].imshow(abs(recovered),cmap='gray')
axs[0].set_title("Recovered Object", va='center', rotation='vertical',x=-0.1,y=0.5)
ims[1] = axs[1].imshow(abs(pupil),cmap='gray')
axs[1].set_title("Recovered Pupil (Fourier Spectrum)", va='center',rotation='vertical',x=-0.1,y=0.5)
origin = np.array([0+10,127-10])
kx = np.array([1,0])
ky = np.array([0,1])
axs[1].quiver(*origin,*kx,color='r',scale=10)
axs[1].quiver(*origin,*ky,color='r',scale=10)
axs[1].text(*(origin+17.5*kx),'$k_x$',color='r',ha='center',va='center')
axs[1].text(*(origin-17.5*ky),'$k_y$',color='r',ha='center',va='center')
ims[2] = axs[2].imshow(np.angle(pupil),cmap='gray')
axs[2].set_title("Recovered Pupil (Phase)", va='center',rotation='vertical',x=-0.1,y=0.5)
for i in range(len(axs)):
    add_colorbar(ims[i],axs[i])
    axs[i].set_xticks([])
    axs[i].set_yticks([])
plt.show()


#PLOT = Plot(packed,cropped,recoveredFT, trackRecoveredFT)
