import time
import numpy as np
import os

from datetime import datetime
from picamera2 import Picamera2, Preview, Metadata

EXP = 160000

cam = Picamera2()
format = "SBGGR10"

now = datetime.now()
dt_string = now.strftime("%Y%d%m_%H%M%S")
cwd = os.getcwd()
path = os.path.join(cwd,"capture_data")

if (os.path.exists(path) == False):
        os.mkdir(path)

#create still config
config = cam.create_still_configuration(
        raw={
            "size": cam.sensor_resolution,
            "format": format
            }
        )

cam.configure(config)
cam.set_controls({
            "ExposureTime": int(EXP),
            "AnalogueGain": 1,
            "ColourGains" : (1.0,1.0)
        })

cam.start()
time.sleep(1)

raw = cam.capture_array("raw")
casted_raw = raw.view(np.uint16) #cast from uint8 to uint16

np.save(os.path.join(path,f"RPI_{format}_{dt_string}"),casted_raw)

cam.stop()
cam.close()
