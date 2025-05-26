from sx1262 import SX1262
import time
import sys

sx = SX1262(spi_bus=1, clk=10, mosi=11, miso=12, cs=3, irq=20, rst=15, gpio=2)

# LoRa
sx.begin(freq=923, bw=500.0, sf=12, cr=8, syncWord=0x12,
         power=-5, currentLimit=60.0, preambleLength=8,
         implicit=False, implicitLen=0xFF,
         crcOn=True, txIq=False, rxIq=False,
         tcxoVoltage=1.7, useRegulatorLDO=False, blocking=True)

errors=0
while True:
    #print("listening...")
    msg, err = sx.recv()
    if len(msg) > 0:
        error = SX1262.STATUS[err]
        try:
            decoded_msg=msg.decode()
            print("--> "+msg.decode()+", rssi:"+str(sx.getRSSI()))
        except:
            errors=errors+1
        
