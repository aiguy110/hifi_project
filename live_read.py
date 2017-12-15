import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import serial
import time

port = input('Which serial port would you like to connect to? (/dev/ttyACM0)\n>')
port = '/dev/ttyACM0'
ser = serial.Serial(port)

gas_vals = []
temp_vals = []

bac_per_ppm = 0.0003404

V_source = 5
V_o = None

#fig = plt.figure()
#plt.ion()

#def animate(i):

bac_log = []
log_length = 100

timer = 5
tic = time.time()
print(f'Grabbing reference reading in \n{timer}')
while True:
    # Tic toc
    if time.time() - tic > 1:
        tic = time.time()
        timer -= 1
        if timer > 0:
            print(timer)

    try:
        raw = ser.readline()
        name, val = raw.decode('ascii').split('=')
        if name == 'gasValueRaw':
            V_sensor = float(val) / 1024 * V_source

            if timer == 0 and V_o is None:
                V_o = V_sensor
                print('Reference set!')
                print(f'V_o={V_o}')

            if V_o is not None:
                ppm = np.exp(-14.7*((V_source/V_o - 1)/(V_source/V_sensor - 1) - 0.45))
                bac = bac_per_ppm * ppm
                bac_log.append(bac)
                if bac_log > log_length:
                    bac_log.pop(0)
                print(f'bac={max(bac_log)}       ', end='\r')

        elif name == 'tempValueRaw':
            temp_vals.append(int(val))

    except Exception as e:
        print(e)
        pass
