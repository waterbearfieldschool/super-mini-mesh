import time
import board
import busio
import displayio
import framebufferio
import sharpdisplay
import busio
import digitalio


messages = []

displayio.release_displays()

bus = board.SPI()
chip_select_pin = board.D7

framebuffer = sharpdisplay.SharpMemoryFramebuffer(bus, chip_select_pin, width=400, height=240)

display = framebufferio.FramebufferDisplay(framebuffer)

from adafruit_display_text.label import Label
from terminalio import FONT

label1 = Label(font=FONT, text="> ", x=0, y=5, scale=1, line_spacing=1.2)
label2 = Label(font=FONT, text="(waiting...)", x=0, y=35, scale=1, line_spacing=1.2)
label3 = Label(font=FONT, text="-------messages-------", x=0, y=20, scale=1, line_spacing=1.2)
#display.root_group = label

text_group = displayio.Group()
text_group.append(label1)
text_group.append(label2)
text_group.append(label3)

display.root_group=text_group
#display.show(text_group)

i2c = busio.I2C(board.SCL, board.SDA)

while not i2c.try_lock():
    pass
 
#cardkb = i2c.scan()[0]  # should return 95
i2c_devices = i2c.scan()
print(i2c_devices)
cardkb=i2c_devices[0]
if cardkb != 95:
    print("!!! Check I2C config: " + str(i2c))
    print("!!! CardKB not found. I2C device", cardkb,
          "found instead.")
    exit(1)
 
ESC = chr(27)
NUL = '\x00'
CR = "\r"
LF = "\n"
LEFT = bytearray(b'\xB4')
RIGHT = bytearray(b'\xB7')
DOWN = bytearray(b'\xB6')
UP = bytearray(b'\xB5')
c = ''
b = bytearray(1)

instr = ''
radio_instr = ''
uart = busio.UART(board.TX, board.RX, baudrate=38400,timeout=0)

msg_display_index=0

message_lines = 9

def show_messages(highlight):
    # highlight is the last message
    end_message=highlight
    start_message = (highlight-message_lines)%len(messages)
    print("highlight:",highlight)
    print("bounds:",start_message,end_message)
    outstr=''
    i = end_message
    count=0
    while (count < message_lines) and (count < len(messages)):
        outstr="<"+str(i)+"> "+messages[i]+'\n'+outstr
        i=(i-1)%len(messages)
        count=count+1
    label2.text=outstr

while True:

    i2c.readfrom_into(cardkb,b)
    if (b == LEFT):
        print("left!")
        continue
    if (b == RIGHT):
        print("right!")
        continue
    if (b == UP):
        print("up!")
        if(len(messages)>message_lines):
            msg_display_index=(msg_display_index-1)%len(messages)
            if(msg_display_index<(message_lines-1)):
                msg_display_index=message_lines-1
            print("index=",msg_display_index)
            show_messages(msg_display_index)
            #label2.text="<"+str(msg_display_index)+"> "+messages[msg_display_index]
        continue
    if (b == DOWN):
        print("down!")
        if(len(messages)>message_lines):
            #msg_display_index=(msg_display_index+1)%len(messages)
            msg_display_index=msg_display_index+1
            if(msg_display_index>len(messages)-1):
                msg_display_index=len(messages)-1
            print("index=",msg_display_index)
            show_messages(msg_display_index)
            #label2.text="<"+str(msg_display_index)+"> "+messages[msg_display_index]
        continue
    
    try:
        c=b.decode()
        if (c != ESC and c != NUL and c !=LEFT):
            if (c == CR):
                print('\nsending:',instr)
                label1.text='> '
                uart.write(bytes(instr, "ascii"))
                messages.append("me: "+instr.strip())
                msg_display_index=len(messages)-1
                show_messages(msg_display_index)
                instr=''
            else:
                print(c, end='')
                instr=instr+c
                label1.text='> '+instr
    except:
        print("error")
            
    data = uart.read(1)  # read up to 32 bytes
    if data is not None:
        this=''.join([chr(b) for b in data])
        if this == LF or this == CR:
            if this == CR:
                continue
            else:
                #print(data,this)
                print(radio_instr)
                if (len(radio_instr)>0):
                    messages.append(radio_instr.strip())
                    print('messages:',messages)
                    msg_display_index=len(messages)-1
                    #label2.text="<"+str(msg_display_index)+"> "+messages[msg_display_index]
                    show_messages(msg_display_index)
                radio_instr=''
                #radio_instr=radio_instr+'\n'
        else:
            radio_instr=radio_instr+this
 
# be nice, clean up
i2c.unlock()
