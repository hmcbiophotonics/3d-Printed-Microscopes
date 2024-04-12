import numpy as np
import board
import adafruit_dotstar as dotstar
import time
from picamera2 import Picamera2, Preview, Metadata

N_DOTS = 8*8
ARRAYSIZE = 7
MATRIXSIZE = 8

def make_spiral_seq(x,y,arraysize,matrixsize):
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
    idx = x + y*matrixsize
    x = y = 0
    dx = -1
    dy = 0
    seq = []
    for i in range(arraysize**2):
        if (-arraysize/2 < x <= arraysize/2) and (-arraysize < y <= arraysize/2):
            seq.append(idx)
        if x == -y or (y > 0 and x == y) or (y < 0 and y == x-1):
            dx, dy = -dy, dx
        idx = idx + dx
        idx = idx + matrixsize*dy
        x = x + dx
        y = y + dy
    return seq

def make_linear_seq(x,y,arraysize,matrixsize):
    """
    linear sequence generator from top left to bottom right where (0,0) is bottom left

    Args:
        x: xshift
        y: yshift
        arraysize: number of used leds
        matrixsize: number of total leds
    """
    seq = []
    for i in range(arraysize):
        for j in range(arraysize):
            idx = matrixsize*((arraysize-1-i)+y)+(j+x)
            seq.append(idx)
    return seq

def clearDots():
    for i in range(N_DOTS):
        dots[i] = (0,0,0)




#init board
dots = dotstar.DotStar(board.SCK, board.MOSI, N_DOTS, brightness=0.055)

#init cam
cam = Picamera2()
format = "SBGGR10"

#create still config
config = cam.create_still_configuration(
        raw={
            "size": cam.sensor_resolution,
             "format": format
             }
        )

cam.configure(config)
cam.set_controls({"AnalogueGain":1, "ColourGains":(1.0,1.0)})

cam.start()
clearDots()

captured_vectors = []

#seq = make_spiral_seq(3,3,7,8)
seq = make_linear_seq(0,0,ARRAYSIZE,MATRIXSIZE)

for i in range(len(seq)):
    dots[seq[i]] = (255,0,0)
    time.sleep(0.1)
    raw = cam.capture_array("raw")
    casted_raw = raw.view(np.uint16) #cast from uint8 to uint16
    captured_vectors.append(casted_raw)
    time.sleep(0.1)
    clearDots()
    time.sleep(0.1)

clearDots()
np.save("captured_vectors",captured_vectors)
cam.stop()
cam.close()
