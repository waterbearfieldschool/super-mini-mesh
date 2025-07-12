from sx1262 import SX1262
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

sx = SX1262(spi_bus=1, clk=10, mosi=11, miso=12, cs=3, irq=20, rst=15, gpio=2)

# LoRa
sx.begin(freq=923, bw=500.0, sf=12, cr=8, syncWord=0x12,
         power=-5, currentLimit=60.0, preambleLength=8,
         implicit=False, implicitLen=0xFF,
         crcOn=True, txIq=False, rxIq=False,
         tcxoVoltage=1.7, useRegulatorLDO=False, blocking=True)

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

text="startup ..."
ta = label.Label(terminalio.FONT, text=text, color=0xFFFF00, x=5, y=5)
splash.append(ta)

#while not i2c.try_lock():
#    pass
    
#i2c_devices = i2c.scan()
#print(i2c_devices)
#i2c.unlock()

cardkb=95

ESC = chr(27)
NUL = '\x00'
CR = "\r"
LF = "\n"
TAB = bytearray(b'\x09')
LEFT = bytearray(b'\xB4')
RIGHT = bytearray(b'\xB7')
DOWN = bytearray(b'\xB6')
UP = bytearray(b'\xB5')
BACK = bytearray(b'\x08')
c = ''
b = bytearray(1)
instr = ''

ta.text='> (ready)'
while True:
    
    while not i2c.try_lock():
        pass
    i2c.readfrom_into(cardkb,b)
    i2c.unlock()
    
    c=b.decode()
    if (c == BACK) and len(instr)>0:
        instr=instr[:-1]
    if (c != ESC and c != NUL and c !=LEFT):
        if (c == CR):
            print('\nsending:',instr)
            ta.text='> (sending message)'
            sx.send(instr.encode())
            time.sleep(1)
            ta.text='> (sent!)'
            time.sleep(1)
            ta.text='> '
            #i2c.unlock()
            #send_message(sendee[1],instr.strip())
            #messages.append("me: "+instr.strip())
            #get_messages()
            instr=''
        else:
            print(c, end='')
            instr=instr+c
            time.sleep(.1)
            ta.text='> '+instr
            #i2c.unlock()
    
    




