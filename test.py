import serial
import serial.tools.list_ports as prt 
import time

ports = prt.comports()

for p in ports:
    print(p)

arduino = serial.Serial('COM6', 9600,baudrate=921600 , timeout=.1)

while True:
    status = input("LED Status(on/anything for off)")
    arduino.write(bytes(status,"utf-8"))
    time.sleep(0.1)
  
