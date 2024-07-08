from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation as animation
from pprint import *
from decimal import Decimal, ROUND_HALF_UP
import os

#spiral function
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

inputObject = np.asarray(Image.open("figures/monkey_gray.gif"))
objectAmplitude = np.double(inputObject)

phase = np.asarray(Image.open("figures/landscape_gray.gif"))
phase = np.pi * phase / np.max(np.max(phase))

#create complex object
object = objectAmplitude * np.exp(1j*phase)

arraysize = 7
LEDgap = 3.175 #3.175 mm between adjacent LEDS
LEDheight = 60 #60 mm between LEDarray and sample

xlocation = np.zeros(arraysize**2)
ylocation = np.zeros(arraysize**2)

#create kvectors from top left to bottom right
for i in range(arraysize):
    xlocation[i*arraysize:arraysize*(i+1)] = np.arange(-(arraysize-1)/2*LEDgap,arraysize/2*LEDgap,LEDgap)
    ylocation[i*arraysize:arraysize*(i+1)] = ((arraysize-1)/2-i)*LEDgap

kx_relative = -np.sin(np.arctan(xlocation/LEDheight))
ky_relative = -np.sin(np.arctan(ylocation/LEDheight))

waveLength = 623e-9
k0 = 2*np.pi/waveLength
spsize = 1.12e-6
psize = spsize / 4
NA = .1

[m,n] = objectAmplitude.shape
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
objectFT = np.fft.fftshift(np.fft.fft2(object))

#generate sequential low res images
for i in range(arraysize**2):
    kxc = int(Decimal((n+1)/2+kx[i]/dkx).quantize(0, ROUND_HALF_UP))
    kyc = int(Decimal((m+1)/2+ky[i]/dky).quantize(0, ROUND_HALF_UP))
    kxl = int(Decimal(kxc-(n1-1)/2).quantize(0,ROUND_HALF_UP))
    kxh = int(Decimal(kxc+(n1-1)/2).quantize(0,ROUND_HALF_UP))
    kyl = int(Decimal(kyc-(m1-1)/2).quantize(0,ROUND_HALF_UP))
    kyh = int(Decimal(kyc+(m1-1)/2).quantize(0,ROUND_HALF_UP))

    imSeqLowFT = (m1/m)**2 * objectFT[kyl:kyh+1,kxl:kxh+1] * CTF
    imSeqLowRes[:,:,i] = np.abs(np.fft.ifft2(np.fft.ifftshift(imSeqLowFT)))

seq = gseq(arraysize)

#lists of sequentially stitched Fourier Transform, Phase, & Image as algorithm proceeds
list_FT = []
list_PH = []
list_IM = []

objectRecover = np.ones((m,n))
objectRecoverFT = np.fft.fftshift(np.fft.fft2(objectRecover))


#main stitching algorithm
loop = 5
for tt in range(loop):
    for i3 in range(arraysize**2):
        i2  = int(seq[i3])
        kxc = int(Decimal((n+1)/2+kx[i2]/dkx).quantize(0, ROUND_HALF_UP))
        kyc = int(Decimal((m+1)/2+ky[i2]/dky).quantize(0, ROUND_HALF_UP))
        kxl = int(Decimal(kxc-(n1-1)/2).quantize(0,ROUND_HALF_UP))
        kxh = int(Decimal(kxc+(n1-1)/2).quantize(0,ROUND_HALF_UP))
        kyl = int(Decimal(kyc-(m1-1)/2).quantize(0,ROUND_HALF_UP))
        kyh = int(Decimal(kyc+(m1-1)/2).quantize(0,ROUND_HALF_UP))

        lowResFT = (m1/m)**2 * objectRecoverFT[kyl:kyh+1,kxl:kxh+1] * CTF
        im_lowRes = np.fft.ifft2(np.fft.ifftshift(lowResFT))
        im_lowRes = (m/m1)**2 * imSeqLowRes[:,:,i2] * np.exp(1j * np.angle(im_lowRes))
        lowResFT = np.fft.fftshift(np.fft.fft2(im_lowRes)) * CTF
        objectRecoverFT[kyl:kyh+1,kxl:kxh+1] = (1-CTF) * objectRecoverFT[kyl:kyh+1,kxl:kxh+1] + lowResFT
        if (tt == 0):
            list_FT.append(np.log(np.abs(objectRecoverFT)))
            list_PH.append(np.angle(np.fft.ifft2(np.fft.ifftshift(objectRecoverFT))))
            list_IM.append(abs(np.fft.ifft2(np.fft.ifftshift(objectRecoverFT))))


objectRecover = np.fft.ifft2(np.fft.ifftshift(objectRecoverFT))


plt.figure()
plt.set_cmap("gray")
plt.imshow(objectAmplitude)
cbar = plt.colorbar(fraction = 0.047*(objectAmplitude.shape[0]/objectAmplitude.shape[1]))
cbar.set_label("Amplitude [a.u.]")
plt.title("Input amplitude")
ax = plt.gca()
ax.set_xticks([])
ax.set_yticks([])

plt.figure()
plt.imshow(phase)
plt.title("Input phase")
ax = plt.gca()
ax.set_xticks([])
ax.set_yticks([])


plt.figure()
plt.imshow(abs(objectRecover))
cbar = plt.colorbar(fraction = 0.047*(objectRecover.shape[0]/objectRecover.shape[1]))
cbar.set_label("Amplitude [a.u.]")
plt.title("Recovered amplitude")
ax = plt.gca()
ax.set_xticks([])
ax.set_yticks([])


plt.figure()
plt.imshow(np.angle(objectRecover))
plt.title("Recovered phase")
ax = plt.gca()
ax.set_xticks([])
ax.set_yticks([])


plt.figure()
plt.imshow(np.log(abs(objectRecoverFT)))
plt.title("Recovered FT")
ax = plt.gca()
ax.set_xticks([])
ax.set_yticks([])


fig, ax = plt.subplots()
ims = []
for i in range(49):
    im = ax.imshow(list_PH[i], animated = True)
    ims.append([im])

plt.title("Recoverd Phase Animation")
ax = plt.gca()
ax.set_xticks([])
ax.set_yticks([])
ani = animation.ArtistAnimation(fig,ims, interval=500, blit=True, repeat_delay = 0)

plt.figure()
plt.title("Phase After 1st LED")
ax = plt.gca()
ax.set_xticks([])
ax.set_yticks([])
plt.imshow(list_PH[0])

plt.figure()
plt.title("Phase After 2nd Sequential LED")
ax = plt.gca()
ax.set_xticks([])
ax.set_yticks([])
plt.imshow(list_PH[1])

plt.figure()
plt.title("Initial Low Resolution Image With Center LED On")
ax = plt.gca()
ax.set_xticks([])
ax.set_yticks([])
plt.imshow(imSeqLowRes[:,:,24])

plt.show()




