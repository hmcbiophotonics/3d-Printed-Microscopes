#!/usr/bin/python3
from fourierptychography import FourierPtychography as FP
from plot import Plot
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider
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
object_dist        = (1 + magnification) / magnification * focal_length
image_dist         = magnification * object_dist
num_aperture       = np.sin(np.arctan(0.5 * aperture_diameter / (object_dist -
                                                                 front_stop_sep)))
num_aperture       = 0.11
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

size = 128
cropped = packed[:,cy-size:cy+size,cx-size:cx+size]

recovered, recoveredFT, trackRecoveredFT = FPM.recover(cropped)

PLOT = Plot(cropped, recoveredFT, trackRecoveredFT)
