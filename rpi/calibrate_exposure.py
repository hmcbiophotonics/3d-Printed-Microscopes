#!/usr/bin/env python3
import time
import os
import numpy as np
import sys

from datetime import datetime
from picamera2 import Picamera2, Preview, Metadata

# Returns the exposuretime at which the image is saturated
def getSaturatedTime(cam,exposures):
    for exposure in exposures:
        arr = captureExposure(cam,exposure)
        print(np.max(arr))
        if (np.max(arr) == 1023):
            print(f"Saturated at {exposure} us",file=sys.stderr)
            np.save('saturated.npy',arr)
            return exposure

# Returns the array for a set exposuretime
def captureExposure(cam,exposure):
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
    # Setup file capture formatting
    now = datetime.now()
    dt_string = now.strftime("%Y%m%d_%H%M%S")

    cwd = os.getcwd()
    capture_path = os.path.join(cwd,"capture_data")

    if (os.path.exists(capture_path) == False):
        os.mkdir(capture_path)

    # Setup camera
    FORMAT = "SBGGR10"

    cam = Picamera2()

    cam_cfg = cam.create_still_configuration(
        raw={
            "size": cam.sensor_resolution,
            "format": FORMAT,
        }
    )
    cam.configure(cam_cfg)

    # Start experiment
    cam.start()
    exposures = np.arange(10000,200000,5000)
    saturatedTime = getSaturatedTime(cam,exposures)
    cam.close()


    # Once we get the saturated image let's take an image at an exposure time
    # before saturation


if __name__ == "__main__":
    main()
