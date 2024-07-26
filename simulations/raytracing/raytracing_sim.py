import numpy as np
import matplotlib.pyplot as plt
from raytracing import *


"""
A raytracing simulation for the raspberry pi camera module v2 in the microscope
Determines NA, Magnification, FOV, ImgHeight, and ImageDistance from raytracing parameters
"""

# all units are in mm except f_stop
f1                = 3.04      #focal length of lens
f_stop            = 2         #f stop for lens
working_distance  = 4.06         #-0.5
lens_diameter     = 5         #lens diameter
aperture_diameter = f1/f_stop #diameter of the front aperture in front of lens
front_stop_sep    = 1         #separation between lens and front aperture
obj_h             = 3         #object height
camera_sensor_x   = 3.68      #width of sensor image
camera_sensor_y   = 2.76      #height of sensor image


camera_sensor_diagonal_diameter = np.sqrt((camera_sensor_x)**2+(camera_sensor_y)**2)
print(f'Aperture diameter = {aperture_diameter}')
print(f'Camera sensor diagonal diameter = {camera_sensor_diagonal_diameter}')


path = ImagingPath()
rays = ObjectRays(diameter = obj_h, halfAngle=0.18, H=3, T=5)
path.objectHeight = obj_h


path.append(Space(d=working_distance))
path.append(Aperture(diameter=aperture_diameter))
path.append(Space(d=front_stop_sep))
path.append(Lens(f=f1, diameter=lens_diameter))
path.append(Space(d=path.intermediateConjugates()[-1][0]-working_distance-front_stop_sep))
path.append(Aperture(diameter=camera_sensor_diagonal_diameter))

axialRay = path.axialRay()
print(axialRay.theta)


path.display(rays=rays, removeBlocked=False)
print(f"Object height is: {path.objectHeight}")
print(f"Image height is: {path.imageSize(useObject=True)}")
print(f"Lateral magnification is {path.imageSize(useObject=True)/obj_h}")
print(f"The intermediate conjugates are located at {path.intermediateConjugates()}")
print(f"The system lateral magnification is {path.magnification()[0]}")
print(f"The system NA is {path.NA()}")
print(f"Image distance {path.intermediateConjugates()[-1][0]-working_distance-front_stop_sep}")
print(f"Field of view is {path.fieldOfView()}")

