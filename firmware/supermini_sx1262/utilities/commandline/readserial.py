import serial
import sys

ser = serial.Serial("/dev/ttyACM0",115200)
while True:
    try:
        bs=ser.readline().decode()
        data=bs.strip().split(',')
        mesg=data[0].strip().split(':')[1]
        #print(bs.strip().split(',')) 
        #print("mesg=",mesg)
        lat=data[1].strip().split(':')[1]
        lon=data[2].strip().split(':')[1]
        rssi=data[3].strip().split(':')[1]
        outstring=mesg+","+lat+","+lon+","+rssi
        print(outstring)
        with open("out.csv", "a") as f:
            f.write(outstring+'\n')
    except Exception as e:
    # Handle the exception
        exc_type, exc_obj, exc_tb = sys.exc_info()
        line_number = exc_tb.tb_lineno
        print(f"Error: {e}, Type: {type(e).__name__}, Line: {line_number}")
