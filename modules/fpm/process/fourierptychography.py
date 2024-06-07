import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation as animation
from decimal import Decimal, ROUND_HALF_UP
from argparse import Namespace
from scipy import integrate


DEFAULT_CONFIG = {
        "num_aperture" : .15,
        "wavelength"   : 623e-9,
        "spsize"       : 1.12e-6,
        "led_dist"     : 60e-3,
        "led_sep"      : 3.175e-3,
        "led_num"      : 8,
        "arraysize"    : 7,
}



class FourierPtychography():
    def __init__(self):
        """
        Fourier Ptychographic Imaging Algorithm Constructor

        Args:
        Returns:
            Nothing
        """
        try:
            self.create_configuration(DEFAULT_CONFIG)
        except Exception:
            print(Exception)

    def create_configuration(self, config={}):
        self.config = config
        return config


    @staticmethod
    def round_hu(number):
        """
        A better round function

        Args:
            number: a floating point number

        Returns:
            the number rounded to ones digit with half up
        """
        return int(Decimal(number).quantize(0, ROUND_HALF_UP)) 

    @staticmethod
    def get_LED_center(centerImage):
        """
        simple LED position finder in the image domain (only center LED should be on)

        Args:
            centerImage: image with center LED on

        Returns:
            xavg, yavg: center position of LED
        """
        [m,n] = centerImage.shape
        x = []
        for i in range(n):
            if ((centerImage[int(m/2),i]+centerImage[int(m/2)-1,i])/2 > 255/2):
                x.append(i)
        xavg = int((x[0] + x[len(x)-1])/2)
        y = []
        for i in range(m):
            if ((centerImage[i,xavg]+centerImage[i,xavg-1])/2 > 255/2):
                y.append(i)
        yavg = int((y[0] + y[len(y)-1])/2)
        return xavg,yavg

    @staticmethod
    def make_spiral_seq(x,y,arraysize):
        """
        counterclockwise spiral sequence generator for led matrix where (0,0) is bottom left
    
        Args:
            x: center x position of spiral
            y: center y position of spiral
            arraysize: number of used leds
            matrixsize: number of total leds
Returns:
            seq: sequence of the indexes of leds
    
        """
        idx = x + (arraysize-y-1)*arraysize
        x = y = 0
        dx = 0
        dy = -1
        seq = []
        for i in range(arraysize**2):
            if (-arraysize/2 < x <= arraysize/2) and (-arraysize < y <= arraysize/2):
                seq.append(idx)
            if x == y or (x < 0 and x == -y) or (x > 0 and y == 1-x):
                dx, dy = -dy, dx
            idx = idx + dx
            idx = idx + arraysize*dy
            x = x + dx
            y = y + dy
        return seq

    def create_vectors(self):
        """
        Create K vectors for FPM setup

        Args:
            Nothing

        Returns:
            kx,ky: numpy arrays for kx and ky vectors
        """
        arraysize = self.config["arraysize"]
        led_sep   = self.config["led_sep"]
        led_dist  = self.config["led_dist"]

        xlocation = np.zeros(arraysize**2)
        ylocation = np.zeros(arraysize**2)

        for i in range(arraysize):
            xlocation[i*arraysize:arraysize*(i+1)] = np.arange(-(arraysize-1)/2*led_sep,arraysize/2*led_sep,led_sep)
            ylocation[i*arraysize:arraysize*(i+1)] = ((arraysize-1)/2-i)*led_sep
        #kx = -np.sin(np.arctan(xlocation/led_dist))
        #ky = -np.sin(np.arctan(ylocation/led_dist))  
        kx = -xlocation/(np.sqrt(xlocation**2+ylocation**2+led_dist**2))
        ky = -ylocation/(np.sqrt(xlocation**2+ylocation**2+led_dist**2))
        return kx,ky

    def recover(self,seqlowres):
        """
        Recover the hi-res image
        
        Args:
            seqlowres: numpy array of sequential low resolution images

        Returns:
            recoveredObject: "Stitched" high resolution image

        """

        ### define seqlowres and upsampling ratio ###

        [numim,m1,n1] = seqlowres.shape
        pratio        = 4
        psize         = self.config["spsize"] / pratio
        m = m1 * pratio; n = n1 * pratio

        ### create k vectors ###
        k0      = 2 * np.pi / self.config["wavelength"]
        [kx,ky] = self.create_vectors()
        kx      = k0 * kx               ;  ky = k0 * ky
        dkx     = 2*np.pi / (psize * n) ; dky = 2*np.pi / (psize * m)

        #setup low pass filter 
        cutoffFrequency = self.config["num_aperture"] * k0
        kmax = np.pi/self.config["spsize"]
        kx2 = np.arange(-kmax,kmax+kmax/((n1-1)/2),kmax/((n1-1)/2))
        ky2 = np.arange(-kmax,kmax+kmax/((m1-1)/2),kmax/((m1-1)/2))

        if (kx2.size > n1) : kx2 = kx2[:-1]
        if (ky2.size > m1) : ky2 = ky2[:-1]

        [kxm,kym] = np.meshgrid(kx2,ky2)

        CTF = ((kxm**2 + kym**2) < cutoffFrequency**2) #Coherent Transfer Function Filter

        seq = self.make_spiral_seq(3,3,self.config["arraysize"])

        recoveredObject = np.ones((m,n))
        recoveredObjectFT = np.fft.fftshift(np.fft.fft2(recoveredObject))

        trackRecoveredFT = []
        pupils = []

        loop = 5
        pupil = 1
        for tt in range(loop):
            for i3 in range(numim):
                i2 = int(seq[i3])
                kxc = self.round_hu((n+1)/2+kx[i2]/dkx)
                kyc = self.round_hu((m+1)/2-ky[i2]/dky)
                kxl = self.round_hu(kxc-(n1-1)/2)
                kxh = self.round_hu(kxc+(n1-1)/2)
                kyl = self.round_hu(kyc-(m1-1)/2)
                kyh = self.round_hu(kyc+(m1-1)/2)

                lowResFT_1 = (m1/m)**2 * recoveredObjectFT[kyl:kyh+1,kxl:kxh+1] * CTF * pupil
                lowResIm = np.fft.ifft2(np.fft.ifftshift(lowResFT_1))
                lowResIm = (m/m1)**2 * seqlowres[i2,:,:] * np.exp(1j * np.angle(lowResIm))
                lowResFT_2 = np.fft.fftshift(np.fft.fft2(lowResIm)) * CTF * (1/pupil)
                recoveredObjectFT[kyl:kyh+1,kxl:kxh+1] = recoveredObjectFT[kyl:kyh+1,kxl:kxh+1] \
                    + np.conj(pupil) / (np.max(abs(pupil)**2)) \
                        * (lowResFT_2 - lowResFT_1)
                if (tt == 0 and i3 == 0):
                    # plt.figure()
                    # plt.subplot(1,3,1)
                    # plt.imshow(np.log(np.abs(recoveredObjectFT)))
                    # plt.subplot(1,3,2)
                    # plt.imshow(np.log(np.abs(np.conj(recoveredObjectFT[kyl:kyh+1,kxl:kxh+1]) / (np.max(abs(recoveredObjectFT[kyl:kyh+1,kxl:kxh+1])**2)))))
                    # plt.subplot(1,3,3)
                    # plt.imshow(np.log(np.abs(lowResFT_2 - lowResFT_1)))
                    x = np.conj(recoveredObjectFT[kyl:kyh+1,kxl:kxh+1]) / (np.max(abs(recoveredObjectFT[kyl:kyh+1,kxl:kxh+1])**2)) * (lowResFT_2 - lowResFT_1)
                    print(x[0,0], x[128,128])
                    x = x + 1
                    print(x[0,0], x[128,128])

                pupil = pupil + np.conj(recoveredObjectFT[kyl:kyh+1,kxl:kxh+1]) \
                    / (np.max(abs(recoveredObjectFT[kyl:kyh+1,kxl:kxh+1])**2)) \
                    * (lowResFT_2 - lowResFT_1)

                if (tt == 0):
                    trackRecoveredFT.append(recoveredObjectFT.copy())
                    pupils.append(pupil.copy())

        recoveredObject = np.fft.ifft2(np.fft.ifftshift(recoveredObjectFT))

        return recoveredObject, recoveredObjectFT, trackRecoveredFT
