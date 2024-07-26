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
magnification      = 1.5
object_dist        = ((1 + magnification) / magnification) * focal_length
image_dist         = magnification * object_dist
num_aperture       = 0.15
wavelength         = 623e-9
sensor_pixel_size  = 1.12e-6 * 2 / magnification
led_dist_to_sample = 60e-3
led_separation     = 3.05e-3
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

sample = np.sqrt(np.load(sys.argv[1]))

###
print(f"aperture_diameter: {aperture_diameter}")
print(f"NA: {num_aperture}")
print(f"iD: {image_dist}")
print(f"oD: {object_dist}")
print(f"nyquist resolution limit: {wavelength/(2*num_aperture)}")
print(f"sensor_pixel_size: {sensor_pixel_size}")

FPM = FP()
FPM.create_configuration(config)


[numim,m,n] = sample.shape

loop = 5
pupil = 1
recovered, recoveredFT, trackRecoveredFT, pupil = FPM.recover(sample,loop,pupil)
print(sample.shape)

def add_kvector(him,ax):
    offset_percent = 0.05
    img = him.get_array()
    height,width = img.shape
    text_offset = 0.15 * (height + width)/2
    origin = np.array([width*offset_percent,height*(1-offset_percent)])
    kx = np.array([1,0])
    ky = np.array([0,1])
    ax.quiver(*origin,*kx,color='r',scale=10)
    ax.quiver(*origin,*ky,color='r',scale=10)
    ax.text(*(origin+text_offset*kx),'$k_x$',color='r',ha='center',va='center')
    ax.text(*(origin-text_offset*ky),'$k_y$',color='r',ha='center',va='center')

def add_colorbar(him, ax, cbar_title=""):
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    cbar = fig.colorbar(him, cax=cax)
    cbar.set_label(cbar_title, rotation=270, labelpad=15)

fig, axs = plt.subplots(3,2,figsize=(10,10))
ims = np.empty(axs.shape,dtype=object)
plt.suptitle(f'{loop} loops')
ims[0,0] = axs[0,0].imshow(abs(recovered),cmap='gray')
axs[0,0].set_title("Recovered Object", va='center', rotation='vertical',x=-0.1,y=0.5)

ims[0,1] = axs[0,1].imshow(abs(pupil),cmap='gray')
axs[0,1].set_title("Recovered Pupil (Fourier Spectrum)", va='center',rotation='vertical',x=-0.1,y=0.5)
add_kvector(ims[0,1],axs[0,1])

ims[1,1] = axs[1,1].imshow(np.angle(pupil))
axs[1,1].set_title("Recovered Pupil (Phase)", va='center',rotation='vertical',x=-0.1,y=0.5)

ims[1,0] = axs[1,0].imshow(np.angle(recovered),cmap='gray')

ims[2,0] = axs[2,0].imshow(np.log(abs(recoveredFT)),cmap='gray')

add_kvector(ims[2,0],axs[2,0])
for i in np.ndindex(axs.shape):
    add_colorbar(ims[i],axs[i])
    axs[i].set_xticks([])
    axs[i].set_yticks([])
plt.show()


PLOT = Plot(sample,sample,recoveredFT, trackRecoveredFT, pupil=pupil,numim=numim)
