
import time
import board
import busio
import digitalio
import time
from analogio import AnalogIn
import terminalio
import displayio

from adafruit_display_text import label
import adafruit_displayio_ssd1306

from digitalio import DigitalInOut, Direction, Pull
led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT

    
try:
    from i2cdisplaybus import I2CDisplayBus
except ImportError:
    from displayio import I2CDisplay as I2CDisplayBus
    
displayio.release_displays()
i2c = busio.I2C(board.P0_11, board.P1_04)
#i2c = board.I2C()
display_bus = I2CDisplayBus(i2c, device_address=0x3C)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)

splash = displayio.Group()
display.root_group = splash

text="hello"
ta = label.Label(terminalio.FONT, text=text, color=0xFFFF00, x=5, y=5)
splash.append(ta)

time.sleep(2)
# start LoRa

from sx1262 import SX1262

ta.text="import worked"
time.sleep(1)


try:
    
    sx = SX1262(spi_bus=1, clk=10, mosi=11, miso=12, cs=3, irq=20, rst=15, gpio=2)
    
    # LoRa
    sx.begin(freq=923, bw=500.0, sf=12, cr=8, syncWord=0x12,
             power=-5, currentLimit=60.0, preambleLength=8,
             implicit=False, implicitLen=0xFF,
             crcOn=True, txIq=False, rxIq=False,
             tcxoVoltage=1.7, useRegulatorLDO=False, blocking=True)
             
    text="lora worked"
except Exception as e:
    text=str(e)
    ta.text=text
    print(e)
    time.sleep(2)
    
ta.text=text


time.sleep(100)

