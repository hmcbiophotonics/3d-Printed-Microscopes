#!/usr/bin/env python3

from picamera2 import Picamera2, Preview
import time

FORMAT = "SBGGR10"
EXPOSURE = 45000

cam = Picamera2()
config = cam.create_preview_configuration(
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
time.sleep(1)
cam.start_preview(Preview.QTGL)
time.sleep(1)
cam.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print('done')
cam.close()
