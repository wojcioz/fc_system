# Runs in systemctl daemon mode as sudo

import board
import neopixel
pixels = neopixel.NeoPixel(board.D18, 30)
pixels[0] = (255, 0, 0)

pixels.fill((60, 60, 60))
while(True):
    pass

