#!/usr/bin/env python3

import board
import time
import sys

import adafruit_dotstar as dotstar
import numpy as np
from picamera2 import Picamera2, Preview

FORMAT = "SBGGR10"
EXPOSURES = np.array([45000,55000,55000,55000])
EXPOSURE = 85000
BRIGHTNESS=0.2
color = 'red'
color_dict = {
    'red': (255,0,0),
    'green': (0,255,0),
    'blue': (0,0,255),
    'white': (255,255,255)
}


def clear_dots(dots):
    for i in range(len(dots)):
        dots[i] = (0,0,0)

def init_dots(N_DOTS,BRIGHTNESS):
    dots = dotstar.DotStar(
        board.SCK,
        board.MOSI,
        N_DOTS,
        brightness=BRIGHTNESS
    )
    return dots

def matrix_setup(ARRAY_SIZE = 8):
    A = np.arange(0,ARRAY_SIZE**2)
    A = A.reshape((ARRAY_SIZE,ARRAY_SIZE))

    ledMatrix = np.flip(A,axis=0)
    subMatrix = ledMatrix[1:8,0:7]

    seq = subMatrix.flatten()
    return seq


def init_camera():
    cam = Picamera2()
    config = cam.create_still_configuration(
        raw={
            "size": cam.sensor_resolution,
            "format": FORMAT
        }
    )
    cam.configure(config)
    cam.set_controls({
        "ExposureTime": EXPOSURE,
        "AnalogueGain": 1.0,
        "ColourGains": (1.0,1.0)
        })
    cam.start()
    print("Camera has started",file=sys.stderr)
    return cam

def capture_array(cam):
    request = cam.capture_request()
    metadata = request.get_metadata()
    result = request.make_array("raw").view(np.uint16)
    request.release()
    return result

def capture_exposure(cam,exposure):
    exposure = int(exposure)
    print(f"Capturing for {exposure} us ",file=sys.stderr,end='')
    cam.set_controls({
        "ExposureTime": exposure,
        "AnalogueGain": 1.0,
        "ColourGains" : (1.0,1.0)
    })
    # Seems like after 3 frames is when the exposure does not vary. Metadata
    # exposure does not converge that accurately for lower exposure < 10000
    for i in range(3):
        request = cam.capture_request()
        metadata = request.get_metadata()
        request.release()
    request = cam.capture_request()
    metadata = request.get_metadata()
    received_exp = metadata['ExposureTime']
    print(f'Received Exposure for {received_exp} us',file=sys.stderr)
    result = request.make_array("raw").view(np.uint16)
    request.release()
    return result

def main():
    ARRAY_SIZE = 8
    MATRIX_SIZE = 8
    # These params are to transform 4, 8x8 matrices to a single 16x16 matrix
    exp_idx = 0
    indices = np.indices((7,7))
    exp_grid = np.maximum(np.abs(indices[0] - 7 // 2),np.abs(indices[1] - 7 // 2))
    exp_indices = exp_grid.flatten()

    cam = init_camera()

    seq = matrix_setup(ARRAY_SIZE=ARRAY_SIZE)
    dots = init_dots(N_DOTS=MATRIX_SIZE**2,BRIGHTNESS=BRIGHTNESS)
    clear_dots(dots)

    for i in range(len(seq)):
        j = seq[i]
        dots[j] = color_dict[color]
        time.sleep(0.1)
        vector = capture_exposure(cam,EXPOSURES[exp_indices[i]])
        np.save(f'/home/hmcbiophotonics/1x1/vector_{i:03d}.npy', vector)
        dots[j] = (0,0,0)
        time.sleep(0.1)
            # wait some time here before iterating to the next LED s.t. LEDs do
            # not overlap

    dots.deinit()
    cam.close()

if __name__ == '__main__':
    main()
