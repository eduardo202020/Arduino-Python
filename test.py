import serial
import serial.tools.list_ports as prt 
import time

ports = prt.comports()

for p in ports:
    print(p)

arduino = serial.Serial(port='COM6', baudrate=921600 , timeout=.1)

def read_write(x=None):
    if(x is None):
        if(arduino.in_waiting):
            data = arduino.readline()
            data = data.decode()
            return data
    else:
        arduino.write(bytes(x,"utf-8"))


while True:
    #status = input("LED Status(on/anything for off)")
    #arduino.write(bytes(status,"utf-8"))
    #time.sleep(0.1)
    print(read_write())
  
