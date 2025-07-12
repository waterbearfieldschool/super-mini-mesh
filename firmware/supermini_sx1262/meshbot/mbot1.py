import time
import board
import busio
import digitalio
#import supervisor
#supervisor.runtime.autoreload = False

uart = busio.UART(board.P0_06, board.P0_08, baudrate=115200,timeout=10)


#uart.write('hello\r\n')

CR = "\r"
LF = "\n"

messages=[]
incoming=''

while True:

    data = uart.read(1)  # read up to 32 bytes
    if data is not None:
        this=''.join([chr(b) for b in data])
        if this == LF or this == CR:
            if this == CR:
                continue
            else:
                #print(data,this)
                print(incoming)
                try:
                    print("8:",incoming.decode('utf-8'))
                except:
                    print("8 bad")
                try:
                    print("16:",incoming.decode('utf-16'))
                except:
                    print("16 bad")
                try:
                    print("ascii:",incoming.decode('ascii'))
                except:
                    print('ascii bad')
                if (len(incoming)>0):
                    messages.append(incoming.strip())
                    print('messages:',messages)
                    #msg_display_index=len(messages)-1
                    #label2.text="<"+str(msg_display_index)+"> "+messages[msg_display_index]
                    #show_messages(msg_display_index)
                incoming=''
                #radio_instr=radio_instr+'\n'
        else:
            incoming=incoming+this
