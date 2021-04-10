from netifaces import interfaces, ifaddresses, AF_INET

def ip4_addresses():
    ip_list = []
    for interface in interfaces():
        for link in ifaddresses(interface)[AF_INET]:
            ip_list.append(link['addr'])
    return ip_list


import time
import busio
import board
from digitalio import DigitalInOut, Direction

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from adafruit_epd.epd import Adafruit_EPD
from adafruit_epd.ssd1675b import Adafruit_SSD1675B  # pylint: disable=unused-import
#from adafruit_epd.ssd1675 import Adafruit_SSD1675  # pylint: disable=unused-import

# create two buttons
switch1 = DigitalInOut(board.D6)
switch2 = DigitalInOut(board.D5)
switch1.direction = Direction.INPUT
switch2.direction = Direction.INPUT

# create the spi device and pins we will need
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
ecs = DigitalInOut(board.CE0)
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
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)

# Alternatively load a TTF font.  Make sure the .ttf font
# file is in the same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
# font = ImageFont.truetype('Minecraftia.ttf', 8)

# Write two lines of text.
draw.text((x, top), "Goodbye", font=font, fill=BLACK)
draw.text((x, top + 20), "World!", font=font, fill=BLACK)
draw.text((x, top + 40), ip4_addresses()[1], font=font, fill=BLACK)

#splash.line((x, bottom, x + 60 + shape_width, top), fill=WHITE, width=3)
splash.line((x, top+shape_width, x + shape_width, bottom), fill=WHITE, width=3)
x += shape_width + padding
splash.text((x, top), "Push!!", font=font, fill=WHITE)
splash.text((x, top + 20), "ME!!!!", font=font, fill=WHITE)
splash.text((x, top + 40), ip4_addresses()[1], font=font, fill=WHITE)

print("entering the loops")
display.image(splashimage)
display.display()
while True:
    if not switch1.value:
        print("Switch 1")
        display.image(image)
        display.display()
        while not switch1.value:
            time.sleep(0.01)
    if not switch2.value:
        print("Switch 2")
        display.image(splashimage)
        #display.fill(Adafruit_EPD.WHITE)
        display.display()
        while not switch2.value:
            time.sleep(0.01)
    time.sleep(0.01)
