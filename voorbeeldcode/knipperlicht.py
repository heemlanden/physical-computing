from machine import Pin, I2C
import neopixel
import time

# Deze code test of je chip werkt door een paars licht te laten knipperen.
# Vervang deze code door je eigen code.
np = neopixel.NeoPixel(Pin(7),1)
for i in range(10):
    np[0]= (255,0,255)
    np.write()
    time.sleep(0.5)
    np[0] = (0,0,0)
    np.write()
    time.sleep(0.5)
