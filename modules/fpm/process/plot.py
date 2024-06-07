from matplotlib import pyplot as plt
from matplotlib.widgets import Slider
from matplotlib.animation import FuncAnimation
from matplotlib_scalebar.scalebar import ScaleBar
import matplotlib.patches as patches
from fourierptychography import FourierPtychography as FP
import numpy as np

class Plot():
    def __init__(self,vector,cropped,recoveredFT,trackRecoveredFT):
        self.seq = FP.make_spiral_seq(3,3,7)
        self.vector = vector

        self.cropped = cropped

        self.recoveredFT = recoveredFT
        self.recovered = np.fft.ifft2(np.fft.ifftshift(self.recoveredFT))
        
        self.trackRecoveredFT = trackRecoveredFT

        self.trackRecovered = []
        for i in range(len(trackRecoveredFT)):
            self.trackRecovered.append(np.fft.ifft2(np.fft.ifftshift(trackRecoveredFT[i])))

        self.image_idx = 0
        self.fig,self.axs   = plt.subplots(3,3)
        plt.set_cmap('gray')

        for ax_row in self.axs:
            for ax in ax_row:
                ax.set_yticks([])
                ax.set_xticks([])

        self.fig.text(0.06, 0.75, 'Intensity', ha='center', va='center', fontsize=12)
        self.fig.text(0.06, 0.50, 'F.T.', ha='center', va='center', fontsize=12)
        self.fig.text(0.06, 0.25, 'Phase', ha='center', va='center', fontsize=12)

        #plot original vector
        self.axs[0,0].set_title("Original FOV")
        self.v1 = self.axs[0,0].imshow(self.vector[self.seq[self.image_idx]])
        self.v2 = self.axs[1,0].imshow(np.log(abs(np.fft.fftshift(np.fft.fft2(self.vector[self.seq[self.image_idx]])))))
        self.axs[2,0].remove()

        roi_rect = patches.Rectangle(
            (842-128,551-128),256,256,
            edgecolor='r',
            facecolor='none'
        )
        self.axs[0,0].add_patch(roi_rect)
        self.axs[0,0].text(842-128,551-128,'ROI',color='red')

        scalebar = ScaleBar(1.12e-6*2,color='red',frameon=False)
        self.axs[0,0].add_artist(scalebar)

        self.axs[0,1].set_title("ROI")
        self.u1 = self.axs[0,1].imshow(self.cropped[self.seq[self.image_idx]])
        self.u2 = self.axs[1,1].imshow(np.log(abs(np.fft.fftshift(np.fft.fft2(self.cropped[self.seq[self.image_idx]])))))
        self.axs[2,1].remove()

        scalebar = ScaleBar(1.12e-6*2,color='red',frameon=False)
        self.axs[0,1].add_artist(scalebar)

        self.axs[0,2].set_title("Recovered Progression")
        self.t1 = self.axs[0,2].imshow(self.normalize(np.abs(self.trackRecovered[self.image_idx])))
        self.t2 = self.axs[1,2].imshow(np.log(abs(self.trackRecoveredFT[self.image_idx])))
        self.t3 = self.axs[2,2].imshow(np.angle(self.trackRecovered[self.image_idx]))

        scalebar = ScaleBar(1.12e-6/4*2,color='red',frameon=False)
        self.axs[0,2].add_artist(scalebar)


        self.ax_slider = plt.axes([0.1, 0.1, 0.8, 0.03])
        self.slider = Slider(
            self.ax_slider,
            'LED Position',
            0,
            len(self.vector) - 1,
            valinit=self.image_idx,
            valstep=1
        )
        self.slider.on_changed(self.update)
        self.fig.canvas.mpl_connect('key_press_event',self.on_key_press)

        self.anim = FuncAnimation(self.fig, self.animate, frames=len(self.vector), interval=200, repeat=True)

        plt.figure()
        plt.title("ROI With Center LED On")
        plt.imshow(self.cropped[self.seq[0]])
        ax = plt.gca()
        ax.set_xticks([])
        ax.set_yticks([])
        scalebar = ScaleBar(1.12e-6*2,
                            color='red',
                            frameon=False,
                            font_properties={'size':16}
                            )
        ax.add_artist(scalebar)
        plt.savefig('figure2.png')

        fig2,axs2 = plt.subplots(3,1)
        axs2[0].set_title("Final Recovered")
        axs2[0].imshow((abs(self.recovered)/np.max(abs(self.recovered))))
        axs2[1].imshow(np.log(abs(self.recoveredFT)))
        axs2[2].imshow(np.angle(self.recovered))
    
        plt.figure()
        plt.title("Final Recovered Amplitude")
        plt.imshow((abs(self.recovered)/np.max(abs(self.recovered))))
        ax = plt.gca()
        ax.set_xticks([])
        ax.set_yticks([])
        scalebar = ScaleBar(1.12e-6*2/4,
                            color='red',
                            frameon=False,
                            font_properties={'size':16}
                            )
        ax.add_artist(scalebar)
        plt.savefig('figure3.png')

        plt.show()

    def update(self,val):
        self.image_idx = int(self.slider.val)
        self.v1.set_data(self.vector[self.seq[self.image_idx]])
        self.v2.set_data(np.log(abs(np.fft.fftshift(np.fft.fft2(self.vector[self.seq[self.image_idx]])))))

        self.u1.set_data(self.cropped[self.seq[self.image_idx]])
        self.u2.set_data(np.log(abs(np.fft.fftshift(np.fft.fft2(self.cropped[self.seq[self.image_idx]])))))

        self.t1.set_data(self.normalize(abs(self.trackRecovered[self.image_idx])))
        self.t2.set_data(np.log(abs(self.trackRecoveredFT[self.image_idx])))
        self.t3.set_data(np.angle(self.trackRecovered[self.image_idx]))

        self.fig.canvas.draw_idle()

    def normalize(self, image):
        """ Normalize image to range [0, 1] """
        norm_image = (image - np.min(image)) / (np.max(image) - np.min(image))
        return norm_image

    def on_key_press(self,event):
        if event.key == 'left':
            self.image_idx = (self.image_idx - 1) % len(self.vector)
        if event.key == 'right':
            self.image_idx = (self.image_idx + 1) % len(self.vector)
        self.slider.set_val(self.image_idx)

    def animate(self, frame):
        self.slider.set_val(frame)
