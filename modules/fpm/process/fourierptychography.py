import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation as animation
from decimal import Decimal, ROUND_HALF_UP
from argparse import Namespace
from numpy.fft import ifftshift
from scipy import integrate
import cv2


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
    def ft2(m):
        return np.fft.fftshift(np.fft.fft2(m))

    @staticmethod
    def ift2(m):
        return np.fft.ifft2(np.fft.ifftshift(m))

    @staticmethod
    def round(number):
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
    def make_spiral_seq(arraysize):
        #x = arraysize // 2
        #y = arraysize // 2
        x = 0
        y = 0
        dy = 1
        dx = 0
        matrix = np.arange(arraysize**2)
        matrix = np.reshape(matrix,(arraysize,arraysize))
        seq = []
        for i in range(arraysize**2):
            seq.append(matrix[arraysize//2-y,x+arraysize//2])
            x = x + dx
            y = y + dy
            if (y==-x) or (y < 0 and y == x) or (y > 0 and y == x + 1):
                dx,dy = -dy,dx
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
        kx = -xlocation/(np.sqrt(xlocation**2+ylocation**2+led_dist**2))
        ky = -ylocation/(np.sqrt(xlocation**2+ylocation**2+led_dist**2))
        plt.figure()
        plt.plot(kx,ky,'bo')
        plt.show()
        return kx,ky

    def recover(self,seqlowres,loop,pupil):
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

        seq = self.make_spiral_seq(self.config["arraysize"])

        recoveredObject = np.mean(seqlowres,axis=0)
        recoveredObject = cv2.resize(recoveredObject,[m,n],interpolation=cv2.INTER_CUBIC)
        recoveredObjectFT = self.ft2(recoveredObject)

        trackRecoveredFT = []

        pupil = CTF

        for tt in range(loop):
            for i3 in range(numim):
                i2 = int(seq[i3])

                kxc = self.round((n+1)/2+kx[i2]/dkx)
                kyc = self.round((m+1)/2-ky[i2]/dky)
                kxl = self.round(kxc-(n1-1)/2); kxh = self.round(kxc+(n1-1)/2)
                kyl = self.round(kyc-(m1-1)/2); kyh = self.round(kyc+(m1-1)/2)
                lowResFT_1 = (m1/m)**2 * recoveredObjectFT[kyl-1:kyh,kxl-1:kxh] * pupil
                lowResIm = self.ift2(lowResFT_1)
                lowResIm = (m/m1)**2 * seqlowres[i2,:,:] * lowResIm / np.abs(lowResIm)
                lowResFT_2 = self.ft2(lowResIm)

                recoveredObjectFT[kyl-1:kyh,kxl-1:kxh] = recoveredObjectFT[kyl-1:kyh,kxl-1:kxh] \
                    + np.conj(pupil) / (np.max(np.abs(pupil)**2)) \
                    * (lowResFT_2 - lowResFT_1)

                pupil = pupil + np.conj(recoveredObjectFT[kyl-1:kyh,kxl-1:kxh]) \
                    / (np.max(np.abs(recoveredObjectFT[kyl-1:kyh,kxl-1:kxh])**2)) \
                    * (lowResFT_2 - lowResFT_1)
                pupil = pupil * CTF
                trackRecoveredFT.append(recoveredObjectFT.copy())

        recoveredObject = self.ift2(recoveredObjectFT)
        # clean the pupil function
        pupil = np.where(np.abs(pupil) == 0, 0+0j, pupil)

        return recoveredObject, recoveredObjectFT, trackRecoveredFT, pupil
