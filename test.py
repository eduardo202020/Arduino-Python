import serial
import serial.tools.list_ports as prt 
import time

ports = prt.comports()

for p in ports:
    print(p)

arduino = serial.Serial(port='COM6', baudrate=921600 , timeout=.1)

def read_write(x):
    arduino.write(bytes(x,"utf-8"))
    time.sleep(0.1)
    data = arduino.readline()
    data = data.decode("utf-8")
    print(data)


while True:
    status = input("LED status (on/anything for off): ")
    read_write(status)
