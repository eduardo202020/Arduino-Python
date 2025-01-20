import serial
import serial.tools.list_ports as prt 

ports = prt.comports()

for p in ports:
    print(p)

arduino = serial.Serial('COM6', 9600,baudrate=921600 , timeout=.1)

while True:
    arduino.write(bytes("hi","utf-8"))
    time.sleep(0.1)
    if(arduino.in_waiting):
        packet = arduino.readline()
        packet = packet.decode('utf-8').strip()
        print(packet)
