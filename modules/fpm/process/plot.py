from matplotlib import pyplot as plt
from matplotlib.widgets import Slider
from matplotlib.animation import FuncAnimation
from matplotlib_scalebar.scalebar import ScaleBar
from mpl_toolkits.axes_grid1 import make_axes_locatable # For nice colorbars
import matplotlib.patches as patches
from fourierptychography import FourierPtychography as FP
import numpy as np



class Plot():
    def __init__(self,vector,cropped,recoveredFT,trackRecoveredFT,pupil = None,numim = 49):
        self.seq = FP.make_spiral_seq(int(np.sqrt(numim)))
        self.vector = vector

        self.cropped = cropped

        self.recoveredFT = recoveredFT
        self.recovered = np.fft.ifft2(np.fft.ifftshift(self.recoveredFT))
        
        self.trackRecoveredFT = trackRecoveredFT

        self.trackRecovered = []
        for i in range(len(trackRecoveredFT)):
            self.trackRecovered.append(np.fft.ifft2(np.fft.ifftshift(trackRecoveredFT[i])))

        self.image_idx = 0
        self.fig,self.axs = plt.subplots(3,3,figsize=(12,12))
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

        cx = 850
        cy = 560
        size = 128

        roi_rect = patches.Rectangle(
            (cx-size//2,cy-size//2),size,size,
            edgecolor='r',
            facecolor='none'
        )
        self.axs[0,0].add_patch(roi_rect)
        self.axs[0,0].text(cx-size//2,cy-size//2,'ROI',color='red')

        scalebar = ScaleBar(1.12e-6*2,color='red',frameon=False,location='lower right')
        self.axs[0,0].add_artist(scalebar)

        self.axs[0,1].set_title("ROI")
        self.u1 = self.axs[0,1].imshow(self.cropped[self.seq[self.image_idx]])
        self.u2 = self.axs[1,1].imshow(np.log(abs(np.fft.fftshift(np.fft.fft2(self.cropped[self.seq[self.image_idx]])))))
        self.axs[2,1].remove()

        scalebar = ScaleBar(1.12e-6*2,color='red',frameon=False,location='lower right')
        self.axs[0,1].add_artist(scalebar)

        self.axs[0,2].set_title("Recovered Progression")
        self.t1 = self.axs[0,2].imshow(abs(self.trackRecovered[self.image_idx])/np.max(abs(self.trackRecovered[self.image_idx])))
        self.t2 = self.axs[1,2].imshow(np.log(abs(self.trackRecoveredFT[self.image_idx])))
        self.t3 = self.axs[2,2].imshow(np.angle(self.trackRecovered[self.image_idx]))

        scalebar = ScaleBar(1.12e-6/4*2,color='red',frameon=False,location='lower right')
        self.axs[0,2].add_artist(scalebar)

        self.add_kvector(self.v2,self.axs[1,0])
        self.add_kvector(self.u2,self.axs[1,1])
        self.add_kvector(self.t2,self.axs[1,2])


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

        # self.anim = FuncAnimation(self.fig, self.animate, frames=len(self.vector), interval=200, repeat=True)

        plt.figure()
        plt.title("Initial Low-Res Image")
        plt.imshow(self.cropped[self.seq[0]])
        ax = plt.gca()
        ax.set_xticks([])
        ax.set_yticks([])
        scalebar = ScaleBar(1.12e-6*2,
                            color='red',
                            frameon=False,
                            font_properties={'size':16},
                            location='lower right'
                            )
        ax.add_artist(scalebar)
    
        plt.figure()
        plt.title("Final Recovered Amplitude")
        plt.imshow((abs(self.recovered)/np.max(abs(self.recovered))))

        ax = plt.gca()
        ax.set_xticks([])
        ax.set_yticks([])
        scalebar = ScaleBar(1.12e-6*2/4,
                            color='red',
                            frameon=False,
                            font_properties={'size':16},
                            location='lower right'
                            )
        ax.add_artist(scalebar)

        fig,ax = plt.subplots()
        ax.set_title("Final Recovered Spectrum")
        im = ax.imshow(np.log(np.abs(self.recoveredFT)))
        ax.set_xticks([])
        ax.set_yticks([])
        self.add_kvector(im,ax)

        fig,ax = plt.subplots()
        ax.set_title("Final Recovered Phase")
        
        im = ax.imshow(np.angle(self.recovered))
        ax.set_xticks([])
        ax.set_yticks([])
        self.add_colorbar(im,ax,'rad')

        if pupil is not None:
            fig,ax = plt.subplots()
            ax.set_title("Recovered Pupil")
            im = ax.imshow(np.angle(pupil),cmap='rainbow')
            ax.set_xticks([])
            ax.set_yticks([])
            self.add_colorbar(im,ax,'rad')

            fix,ax = plt.subplots()
            ax.set_title("Recovered Pupil Spectrum")
            im = ax.imshow(np.abs(pupil))
            ax.set_xticks([])
            ax.set_yticks([])
            self.add_kvector(im,ax)



        plt.show()

    def update(self,val):
        self.image_idx = int(self.slider.val)
        self.v1.set_data(self.vector[self.seq[self.image_idx]])
        self.v2.set_data(np.log(abs(np.fft.fftshift(np.fft.fft2(self.vector[self.seq[self.image_idx]])))))

        self.u1.set_data(self.cropped[self.seq[self.image_idx]])
        self.u2.set_data(np.log(abs(np.fft.fftshift(np.fft.fft2(self.cropped[self.seq[self.image_idx]])))))

        self.t1.set_data(abs(self.trackRecovered[self.image_idx])/np.max(abs(self.trackRecovered[self.image_idx])))
        self.t2.set_data(np.log(abs(self.trackRecoveredFT[self.image_idx])))
        self.t3.set_data(np.angle(self.trackRecovered[self.image_idx]))

        self.fig.canvas.draw_idle()

    def on_key_press(self,event):
        if event.key == 'left':
            self.image_idx = (self.image_idx - 1) % len(self.vector)
        if event.key == 'right':
            self.image_idx = (self.image_idx + 1) % len(self.vector)
        self.slider.set_val(self.image_idx)

    def animate(self, frame):
        self.slider.set_val(frame)

    def add_kvector(self,him,ax):
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

    def add_colorbar(self,him, ax, cbar_title=""):
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        cbar = self.fig.colorbar(him, cax=cax)
        cbar.set_label(cbar_title, rotation=270, labelpad=15)

