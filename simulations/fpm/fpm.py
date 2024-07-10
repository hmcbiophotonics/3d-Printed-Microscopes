#!/usr/bin/env python3
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable # For nice colorbars
from decimal import Decimal, ROUND_HALF_UP
from zernikepy import zernike_polynomials

def fft2(x):
    return np.fft.fft2(x)

def fftshift(x):
    return np.fft.fftshift(x)

def ifft2(x):
    return np.fft.ifft2(x)

def ifftshift(x):
    return np.fft.ifftshift(x)

def round(x):
    return int(Decimal(x).quantize(0,ROUND_HALF_UP))

def gseq(arraysize):
    n             = (arraysize+1)/2
    sequence      = np.zeros((2,arraysize**2))
    sequence[0,0] = n
    sequence[1,0] = n
    dx            = +1
    dy            = -1
    stepx         = +1
    stepy         = -1
    direction     = +1
    counter       = 0
    for i in range(1,arraysize**2):
        counter += 1
        if (direction == +1):
            sequence[0,i] = sequence[0,i-1]+dx
            sequence[1,i] = sequence[1,i-1]
            if (counter == np.abs(stepx)):
                counter   = 0
                direction = direction * -1
                dx        = dx * -1
                stepx     = stepx*-1
                stepx     = stepx + 1 if (stepx > 0) else stepx-1
        else:
            sequence[0,i] = sequence[0,i-1]
            sequence[1,i] = sequence[1,i-1]+dy
            if (counter == np.abs(stepy)):
                counter   = 0
                direction = direction * -1
                dy        = dy*-1
                stepy     = stepy*-1
                stepy     = stepy+1 if (stepy > 0) else stepy-1
    seq = (sequence[0,:]-1)*arraysize+sequence[1,:] - 1
    return seq

amplitude = np.asarray(Image.open('../figures/monkey_gray.png'),dtype=np.float64)
phase = np.asarray(Image.open('../figures/landscape_gray.png'),dtype=np.float64)
phase = np.pi * phase / np.max(phase)
object = amplitude * np.exp(1j * phase)

plt.figure()
plt.imshow(abs(object),cmap='gray')
plt.title('Initial Complex Object Amplitude')

arraysize = 15
xlocation = np.zeros(arraysize**2)
ylocation = np.zeros(arraysize**2)
LEDgap = 3.05e-3
LEDheight = 60e-3

for i in range(arraysize):
    xlocation[i*arraysize:arraysize*(i+1)] = np.arange(-(arraysize-1)/2*LEDgap,arraysize/2*LEDgap,LEDgap)
    ylocation[i*arraysize:arraysize*(i+1)] = ((arraysize-1)/2-i)*LEDgap

kx_relative = -np.sin(np.arctan(xlocation/LEDheight))
ky_relative = -np.sin(np.arctan(ylocation/LEDheight))

wavelength = 623e-9
k0 = 2*np.pi/wavelength;
spsize = 1.12e-6 * 2/1.5;
psize = spsize/4;
NA = .18;
[m,n] = object.shape

m1 = int(m/(spsize/psize))
n1 = int(n/(spsize/psize))

imSeqLowRes = np.zeros((m1,n1,arraysize**2))
kx = k0 * kx_relative
ky = k0 * ky_relative
dkx = 2*np.pi/(psize*n)
dky = 2*np.pi/(psize*m)
cutoffFrequency = NA * k0
kmax = np.pi/spsize
[kxm,kym] = np.meshgrid(
        np.arange(-kmax,kmax+kmax/((n1-1)/2),kmax/((n1-1)/2)), 
        np.arange(-kmax,kmax+kmax/((n1-1)/2),kmax/((n1-1)/2))
        )
CTF = ((kxm**2 + kym**2) < cutoffFrequency**2)
zernike_p = zernike_polynomials(mode=5, size = 128) # mode 4 is defocus

PUPIL = CTF * np.exp(1j * zernike_p)

plt.figure()
plt.imshow(np.angle(PUPIL))
plt.title('Pupil Function Phase')

objectFT = fftshift(fft2(object))
for tt in range(arraysize**2):
    kxc = round((n+1)/2+kx[tt]/dkx)
    kyc = round((m+1)/2+ky[tt]/dky)
    kyl = round(kyc-(m1-1)/2); kyh = round(kyc+(m1-1)/2)
    kxl = round(kxc-(n1-1)/2); kxh = round(kxc+(n1-1)/2)
    imSeqLowFT = (m1/m)**2 * objectFT[kyl-1:kyh,kxl-1:kxh] * PUPIL
    imSeqLowRes[:,:,tt] = np.abs(ifft2(ifftshift(imSeqLowFT)))

plt.figure()
plt.imshow(imSeqLowRes[:,:,0],cmap='gray')
plt.title('0th Low Res Image')

seq = gseq(arraysize)

objectRecover = np.ones((m,n))
objectRecoverFT = fftshift(fft2(objectRecover))
loop = 5
pupil = 1
for tt in range(loop):
    for i3 in range(arraysize**2):
        i2 = int(seq[i3])

        kxc = round((n+1)/2+kx[i2]/dkx)
        kyc = round((m+1)/2+ky[i2]/dky)
        kyl = round(kyc-(m1-1)/2); kyh = round(kyc+(m1-1)/2)
        kxl = round(kxc-(n1-1)/2); kxh = round(kxc+(n1-1)/2)

        lowResFT_1 = (m1/m)**2 * objectRecoverFT[kyl-1:kyh,kxl-1:kxh]*CTF*pupil
        im_lowRes = ifft2(ifftshift(lowResFT_1))
        im_lowRes = (m/m1)**2 * imSeqLowRes[:,:,i2]*np.exp(1j*np.angle(im_lowRes))
        lowResFT_2 = fftshift(fft2(im_lowRes))*CTF*(1/pupil)

        objectRecoverFT[kyl-1:kyh,kxl-1:kxh]=objectRecoverFT[kyl-1:kyh,kxl-1:kxh] \
                + np.conj(pupil) / (np.max(np.abs(pupil)**2)) \
                * (lowResFT_2 - lowResFT_1)

        pupil = pupil + np.conj(objectRecoverFT[kyl-1:kyh,kxl-1:kxh]) \
                / (np.max(np.abs(objectRecoverFT[kyl-1:kyh,kxl-1:kxh])**2)) \
                * (lowResFT_2 - lowResFT_1)

objectRecover = ifft2(ifftshift(objectRecoverFT))


def add_colorbar(him, ax, cbar_title=""):
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    cbar = fig.colorbar(him, cax=cax)
    cbar.set_label(cbar_title, rotation=270, labelpad=15)

ims = [0,0,0]
fig, axs = plt.subplots(3,1,figsize=(4,10))
plt.suptitle(f'{loop} loops')
ims[0] = axs[0].imshow(abs(objectRecover),cmap='gray')
axs[0].set_title("Recovered Object", va='center', rotation='vertical',x=-0.1,y=0.5)
ims[1] = axs[1].imshow(abs(pupil))
axs[1].set_title("Recovered Pupil (Fourier Spectrum)", va='center',rotation='vertical',x=-0.1,y=0.5)

origin = np.array([0+10,127-10])
kx = np.array([1,0])
ky = np.array([0,1])

axs[1].quiver(*origin,*kx,color='r',scale=10)
axs[1].quiver(*origin,*ky,color='r',scale=10)
axs[1].text(*(origin+17.5*kx),'$k_x$',color='r',ha='center',va='center')
axs[1].text(*(origin-17.5*ky),'$k_y$',color='r',ha='center',va='center')
ims[2] = axs[2].imshow(np.angle(pupil))
axs[2].set_title("Recovered Pupil (Phase)", va='center',rotation='vertical',x=-0.1,y=0.5)
for i in range(len(axs)):
    add_colorbar(ims[i],axs[i])
    axs[i].set_xticks([])
    axs[i].set_yticks([])
plt.show()

