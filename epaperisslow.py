#---------------------------------------------------------------epaperisslow.py
# playing around with 2.13" HD mono pi hat.
#
# screen drawing takes 9-10 seconds per update.


from datetime import datetime

def TimeString ():
    return datetime.now().strftime("%H:%M")
    
import time
import busio
import board
from digitalio import DigitalInOut, Direction

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from adafruit_epd.epd import Adafruit_EPD
from adafruit_epd.ssd1675b import Adafruit_SSD1675B  # pylint: disable=unused-import#from adafruit_epd.ssd1675 import Adafruit_SSD1675  # pylint: disable=unused-import
import math
import random


# create two buttons
switch1 = DigitalInOut(board.D6)
switch2 = DigitalInOut(board.D5)
switch1.direction = Direction.INPUT
switch2.direction = Direction.INPUT

# create the spi device and pins we will need
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
ecs = DigitalInOut(board.CE0) ## check back on this
dc = DigitalInOut(board.D22)
rst = DigitalInOut(board.D27)
busy = DigitalInOut(board.D17)

# give them all to our driver
display = Adafruit_SSD1675B(
    122,
    250,
    spi,  # 2.13" HD mono display (rev B)
    cs_pin=ecs,
    dc_pin=dc,
    sramcs_pin=None,
    rst_pin=rst,
    busy_pin=busy,
)
display.rotation = 1

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = display.width
height = display.height
image = Image.new("RGB", (width, height))
splashimage = Image.new("RGB", (width, height))

WHITE = (0xFF, 0xFF, 0xFF)
BLACK = (0x00, 0x00, 0x00)
print("clearing display")
# clear the buffer
display.fill(Adafruit_EPD.WHITE)
# clear it out
display.display()

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)
splash = ImageDraw.Draw(splashimage)
# empty it
draw.rectangle((0, 0, width, height), fill=WHITE)
splash.rectangle((0, 0, width, height), fill=BLACK)
print("drawing box")

# Draw an outline box
draw.rectangle((1, 1, width - 2, height - 2), outline=BLACK, fill=WHITE)
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = 5
shape_width = 30
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = padding

# Load default font.

font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 80)

text_origin=(7,top+15)
draw.text(text_origin, TimeString(), font=font, fill=BLACK)
splash.text(text_origin, TimeString(), font=font, fill=WHITE)

print("entering the loops")

#display.image(splashimage)
#display.display()

old_ticks = time.monotonic() - 50.0
image2display=splashimage

while True:
    
    ticks = time.monotonic()
    
    if not switch1.value:
        print("Switch 1")
        image2display=image
        display.image(image2display)
        display.display()
        while not switch1.value:
            time.sleep(0.01)
            
    if not switch2.value:
        print("Switch 2")
        image2display=splashimage
        display.image(image2display)
        display.display()
        while not switch2.value:
            time.sleep(0.01)
            
    # print( ticks - old_ticks)
    
    if(( ticks  - old_ticks) >= 50.0):
        #current_time=datetime.now().strftime("%H:%M  ")
        print("updating "+TimeString())
        draw.rectangle((0, 0, width, height), fill=WHITE)
        splash.rectangle((0, 0, width, height), fill=BLACK)
        draw.rectangle((1, 1, width - 2, height - 2), outline=BLACK, fill=WHITE)
        draw.text(text_origin,TimeString(),font=font, fill=BLACK)
        splash.text(text_origin,TimeString(), font=font, fill=WHITE)
        display.image(image2display)
        display.display()
        old_ticks=time.monotonic()
        
