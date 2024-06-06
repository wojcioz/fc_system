# Runs in systemctl daemon mode as sudo

# import board
# import neopixel
from pipes import Pipe
# pixels = neopixel.NeoPixel(board.D18, 30)
# pixels[0] = (255, 0, 0)

# pixels.fill((60, 60, 60))

pipe = Pipe("distance")
pipe.create_pipe()

while(True):
    pipe.read_from_pipe()
