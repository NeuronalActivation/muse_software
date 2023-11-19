import serial
import time


ser = serial.Serial('COM5')
time.sleep(2)
ser.write(b'blue\n')
#ser.close()