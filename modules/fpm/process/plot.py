from matplotlib import pyplot as plt
from matplotlib.widgets import Slider
from fourierptychography import FourierPtychography as FP
import numpy as np

class Plot():
    def __init__(self,vector,recoveredFT,trackRecoveredFT):
        self.seq = FP.make_spiral_seq(3,3,7)
        self.vector = vector

        self.recoveredFT = recoveredFT
        self.recovered = np.fft.ifft2(np.fft.ifftshift(self.recoveredFT))
        
        self.trackRecoveredFT = trackRecoveredFT
        self.trackRecovered = [np.fft.ifft2(np.fft.ifftshift(tRFT)) for tRFT in self.trackRecoveredFT]

        self.image_idx = 0
        self.fig,self.axs   = plt.subplots(3,3)
        plt.set_cmap('gray')

        #plot original vector
        self.v1 = self.axs[0,0].imshow(self.vector[self.seq[self.image_idx]])
        self.v2 = self.axs[1,0].imshow(np.log(abs(np.fft.fftshift(np.fft.fft2(self.vector[self.seq[self.image_idx]])))))
        self.axs[2,0].remove()

        self.t1 = self.axs[0,1].imshow(abs(self.trackRecovered[self.image_idx]))
        self.t2 = self.axs[1,1].imshow(np.log(abs(self.trackRecoveredFT[self.image_idx])))
        self.t3 = self.axs[2,1].imshow(np.angle(self.trackRecovered[self.image_idx]))


        #plot recovered
        self.axs[0,2].imshow((abs(self.recovered)/np.max(abs(self.recovered))))
        self.axs[1,2].imshow(np.log(abs(self.recoveredFT)))
        self.axs[2,2].imshow(np.angle(self.recovered))

        self.ax_slider = plt.axes([0.1, 0.1, 0.8, 0.03])
        self.slider = Slider(
            self.ax_slider,
            'frame',
            0,
            len(self.vector) - 1,
            valinit=self.image_idx,
            valstep=1
        )
        self.slider.on_changed(self.update)
        self.fig.canvas.mpl_connect('key_press_event',self.on_key_press)


        plt.figure()
        plt.imshow(np.log(abs(np.fft.fftshift(np.fft.fft2(self.vector[self.seq[15]])))))
        plt.title("Frame 15 (x,y)=()")

        plt.show()

    def update(self,val):
        self.image_idx = int(self.slider.val)
        self.v1.set_data(self.vector[self.seq[self.image_idx]])
        self.v2.set_data(np.log(abs(np.fft.fftshift(np.fft.fft2(self.vector[self.seq[self.image_idx]])))))

        #self.trackRecovered[self.image_idx] = np.fft.ifft2(np.fft.ifftshift(self.trackRecoveredFT[self.image_idx]))

        self.t1.set_data(abs(self.trackRecovered[self.image_idx]))
        self.t2.set_data(np.log(abs(self.trackRecoveredFT[self.image_idx])))
        self.t3.set_data(np.angle(self.trackRecovered[self.image_idx]))

        self.fig.canvas.draw_idle()

    def on_key_press(self,event):
        if event.key == 'left':
            self.image_idx = (self.image_idx - 1) % len(self.vector)
        if event.key == 'right':
            self.image_idx = (self.image_idx + 1) % len(self.vector)
        self.slider.set_val(self.image_idx)
