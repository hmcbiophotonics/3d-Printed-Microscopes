import board
import adafruit_dotstar as dotstar
import time

ARRAYSIZE = 8
MATRIXSIZE = 7
N_DOTS = ARRAYSIZE**2
COLORS = {
        "WHITE" : (255,255,255),
        "RED"   : (255,0,0),
        "GREEN" : (0,255,0),
        "BLUE"  : (0,0,255)
        }

COLOR = COLORS["WHITE"]
BRIGHTNESS = 0.02
DELAY = 0.05


def make_spiral_seq(x,y,arraysize,matrixsize):
    """
    counterclockwise spiral sequence generator for led matrix where (0,0) is bottom left

    Args:
        x: center x position of spiral
        y: center y position of spiral
        arraysize: number of total leds
        matrixsize: number of used leds
    Returns:
        seq: sequence of the indexes of leds

    """
    idx = x + y*arraysize
    x = y = 0
    dx = -1
    dy = 0
    seq = []
    for i in range(matrixsize**2):
        if (-matrixsize/2 < x <= matrixsize/2) and (-matrixsize < y <= matrixsize/2):
            seq.append(idx)
        if x == -y or (y > 0 and x == y) or (y < 0 and y == x-1):
            dx, dy = -dy, dx
        idx = idx + dx
        idx = idx + arraysize*dy
        x = x + dx
        y = y + dy
    return seq

def make_linear_seq(x,y,arraysize,matrixsize):
    """
    linear sequence generator from top left to bottom right where (0,0) is bottom left

    Args:
        x: xshift
        y: yshift
        arraysize: number of total leds
        matrixsize: number of used leds
    """
    seq = []
    for i in range(matrixsize):
        for j in range(matrixsize):
            idx = arraysize*((matrixsize-1-i)+y)+(j+x)
            seq.append(idx)
    return seq


def clearDots():
    for i in range(N_DOTS):
        dots[i] = (0,0,0)

dots = dotstar.DotStar(board.SCK, board.MOSI, N_DOTS, brightness=BRIGHTNESS)

#seq = make_linear_seq(0,0,ARRAYSIZE, MATRIXSIZE)
seq = make_spiral_seq(3,3,ARRAYSIZE, MATRIXSIZE)


clearDots()
try:
    while True:
        for i in range(len(seq)):
            dots[seq[i]] = COLOR
            time.sleep(DELAY)
            clearDots()
            time.sleep(DELAY)

except KeyboardInterrupt:
    clearDots()


