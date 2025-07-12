from sx1262 import SX1262
import time
import board
import busio
import digitalio
import time
from analogio import AnalogIn
import terminalio
import displayio
import adafruit_gps

from adafruit_display_text import label
import adafruit_displayio_ssd1306


SCREEN_WIDTH=10

uart_gps = busio.UART(board.P0_20, board.P0_22, baudrate=9600, timeout=10)

gps = adafruit_gps.GPS(uart_gps, debug=False)


sx = SX1262(spi_bus=1, clk=10, mosi=11, miso=12, cs=3, irq=20, rst=15, gpio=2)

# LoRa
sx.begin(freq=923, bw=500.0, sf=12, cr=8, syncWord=0x12,
         power=-5, currentLimit=60.0, preambleLength=8,
         implicit=False, implicitLen=0xFF,
         crcOn=True, txIq=False, rxIq=False,
         tcxoVoltage=1.7, useRegulatorLDO=False, blocking=True)

gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
gps.send_command(b"PMTK220,1000")

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

ta = label.Label(terminalio.FONT, text=text, color=0xFFFF00, x=5, y=20)
splash.append(ta)

gps_loc = label.Label(terminalio.FONT, text="[no gps fix]", color=0xFFFF00, x=5, y=5)
splash.append(gps_loc)

status = label.Label(terminalio.FONT, text="[ READY ]", color=0xFFFF00, x=5, y=60)
splash.append(status)

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
instr = []

ta.text='> '

last_print = time.monotonic()

while True:
    
    while not i2c.try_lock():
        pass
        
    i2c.readfrom_into(cardkb,b)
    i2c.unlock()
    
    
    
    c=b.decode()
    if (c == BACK and len(instr)>0):
        print("back!")
        try:
            instr.pop()
            print(''.join(instr))
            #print(''.join(instr))
            ta.text='> '+''.join(instr)
        except:
            print('error')
    elif (c != ESC and c != NUL and c !=LEFT):
        if (c == CR):
            #print('\nsending:',instr)
            status.text='[ SENDING ]'
            #ta.text='> '
            sendstring=''.join(instr)
            sx.send(sendstring.encode())
            time.sleep(1)
            status.text='[ SENT! ]'
            time.sleep(1)
            status.text='[ READY ]'
            #i2c.unlock()
            #send_message(sendee[1],instr.strip())
            #messages.append("me: "+instr.strip())
            #get_messages()
            instr=[]
            ta.text='> '+''.join(instr)
        else:
            print(c, end='')
            instr.append(str(c))
            #instr=instr+c
            #if(len(instr)>SCREEN_WIDTH):
            #    status.text='TOO LONG'
            #else:
            #    status.text='[ READY ]'
            time.sleep(.1)
            ta.text='> '+''.join(instr)
            #i2c.unlock()
    
         
    gps.update()
    current = time.monotonic()
    if current - last_print >= 1.0:
        last_print = current
        if not gps.has_fix:
            # Try again if we don't have a fix yet.
            print("Waiting for fix...")
            gps_loc.text='[no gps fix]'
            continue
        lat=gps.latitude
        lon=gps.longitude
        gps_loc.text=str(lat)+", "+str(lon)




