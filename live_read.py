import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import serial

port = input('Which serial port would you like to connect to? (/dev/ttyACM0)\n>')
port = '/dev/ttyACM0'
ser = serial.Serial(port)

gas_vals = []
temp_vals = []

#fig = plt.figure()
#plt.ion()

#def animate(i):

while True:
    try:
        raw = ser.readline()
        name, val = raw.decode('ascii').split('=')
        if name == 'gasValueRaw':
            gas_vals.append(int(val))
            print(int(val))
        elif name == 'tempValueRaw':
            temp_vals.append(int(val))

    except Exception as e:
        print(e)
        pass
