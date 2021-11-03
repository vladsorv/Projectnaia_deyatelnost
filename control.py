import keyboard
import serial
import json
import time

ser = serial.Serial('COM2', 9600)
x_ang = y_ang = z_ang = 0

while True:
    time.sleep(0.2)
    if keyboard.is_pressed('w'):
        x_ang += 0.1
    if keyboard.is_pressed('s'):
        x_ang -= 0.1

    if keyboard.is_pressed('d'):
        y_ang -= 0.1
    if keyboard.is_pressed('a'):
        y_ang += 0.1

    if keyboard.is_pressed('z'):
        z_ang -= 0.1
    if keyboard.is_pressed('x'):
        z_ang += 0.1

    data = [x_ang,y_ang,z_ang]

    bytes_data = json.dumps(data).encode('utf-8')
    ser.write(bytes_data)
    print(bytes_data)
