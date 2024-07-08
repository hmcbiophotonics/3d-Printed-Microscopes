import board
import adafruit_dotstar as dotstar

ARRAYSIZE = 8
N_DOTS = ARRAYSIZE**2
COLORS = {
        "WHITE" : (255,255,255),
        "RED"   : (255,0,0),
        "GREEN" : (0,255,0),
        "BLUE"  : (0,0,255)
        }

COLOR = COLORS["WHITE"]
BRIGHTNESS = 0.02

CONDENSOR_SETUP = [
        [0,0,0,0,0,0,0,0],
        [1,1,1,1,1,1,1,0],
        [1,1,1,1,1,1,1,0],
        [1,1,1,1,1,1,1,0],
        [1,1,1,1,1,1,1,0],
        [1,1,1,1,1,1,1,0],
        [1,1,1,1,1,1,1,0],
        [1,1,1,1,1,1,1,0]
        ]

#BOTTOM LEFT IS (0,0)

#CONDENSOR_SETUP = [
#      y [0,0,0,0,0,0,0,0],
#      ^ [0,0,0,0,0,0,0,0],
#      | [0,0,0,0,0,0,0,0],
#      | [0,0,0,0,0,0,0,0],
#      | [0,0,0,1,0,0,0,0],
#      | [0,0,0,0,0,0,0,0],
#      | [0,0,0,0,0,0,0,0],
#      | [0,0,0,0,0,0,0,0]
#      .-----------------> x 
#        ]

def clearDots():
    for i in range(N_DOTS):
        dots[i] = (0,0,0)

dots = dotstar.DotStar(board.SCK, board.MOSI, N_DOTS, brightness=BRIGHTNESS)

try:
    while True:
        for i in range(ARRAYSIZE):
            for j in range(ARRAYSIZE):
                illumination = CONDENSOR_SETUP[ARRAYSIZE-1-i][j]
                dots[ARRAYSIZE*i+j] = ([illumination*rgb for rgb in COLOR])

except KeyboardInterrupt:
    clearDots()
