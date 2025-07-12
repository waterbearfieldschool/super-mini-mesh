import time
import board
import busio
import digitalio
#import supervisor
#supervisor.runtime.autoreload = False

uart = busio.UART(board.P0_06, board.P0_08, baudrate=115200,timeout=10)


#uart.write('hello\r\n')
            
while True:
    #data=uart.read(uart.in_waiting)
    data=uart.readline()
    #data=uart.read(32)
    if data:
    #if data is not None:
        print("data:",data)
        #string_data = data.decode("utf-8", errors="replace")
        #print("string_data=",string_data)
        #print(data.split(':'))
        #try:
        print("string:",str(data))
        instr=str(data).strip('\r\n')
        sp=instr.split(':')
        if len(sp)>1:
            print("split:",sp)
            name=sp[0]
            message=str(sp[1])
            message=message[:-5]
            print("name:",name)
            print("message:",message)
            #print("split:",instr.split(":"))
            
            m=str(message).strip()
            #message=message.strip('\n')
            print("stripped",m)
            if ("@meshbot" in m):
                print("ack back!")
                uart.write("meshbot received: \""+m.replace("@meshbot","")+"\"\r\n")
                #uart.write('hello\r\n')
            #m=name.decode()
            #print("decoded:",bytes(m)
            
            #m=m.strip('\r')
            #m=m.strip('\n')
            #m=m.strip()
            #ms=m.split(':')
            #print("name:",ms[0])
            #print("msg:",ms[1])
                
        
