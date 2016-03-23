#!/usr/bin/python
from Adafruit_Thermal import Adafruit_Thermal
from PIL import Image
import RPi.GPIO as GPIO

printer = Adafruit_Thermal(port="/dev/ttyAMA0", baudrate=19200,
                           heattime=255, dtr=18, timeout=5)
printer.reset()
printer.setDefault()
image = Image.open('gfx/smile_positive.png')
#image = image.point(lambda i: 0 if i < 230 else 255)
#image = image.convert('1',dither=None )

#bitmap = [0]  * (image.size[0] * image.size[1])
#i = 0
#for i in range(0,

printer.printImage(image)
#printer.feed(1)

#printer.printUpsideDown("Hello this is a longer text to test a printing ability of what happens with very long lines of text are printing in the upside down fashion")
