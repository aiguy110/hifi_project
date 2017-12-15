import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import serial
import time

port = input('Which serial port would you like to connect to? (/dev/ttyACM0)\n>')
port = '/dev/ttyACM0'
ser = serial.Serial(port)

bac_graph_points = [0]
temp_vals = [0]
times = [0]
look_back_secs = 20

bac_log_short = []
short_log_length = 200

bac_per_ppm = 0.0003404 * 2

V_source = 5
V_o = None

yellow_thress = 0.04
red_thress = 0.08

fig, ax = plt.subplots()
ax.set_ylim(0, 0.2)
line, = ax.plot([], [], lw=2)
ax.grid()

timer = 5
start_time = tic = time.time()
print(f'Grabbing reference reading in \n{timer}')

def run(data):
    global tic, timer, start_time
    global V_o
    global bac_log_short, short_log_length
    global yellow_thress, red_thress

    # Tic toc
    current_time = time.time()
    if current_time - tic > 1:
        tic = current_time
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
                #michaels_number = (V_source/V_o - 1)/(V_source/V_sensor - 1)
                #print(f'michaels_number={michaels_number}')
                bac = bac_per_ppm * ppm

                bac_graph_points.append(bac)
                times.append(current_time-start_time)

                bac_log_short.append(bac)
                if len(bac_log_short) > short_log_length:
                    bac_log_short.pop(0)
                display_bac = max(bac_log_short)
                led_color = 'g'
                if display_bac > red_thress:
                    led_color = 'r'
                elif display_bac > yellow_thress:
                    led_color = 'y'
                ser.write(led_color.encode('ascii'))

                print(f'bac={display_bac}       ', end='\r')

        elif name == 'tempValueRaw':
            temp_vals.append(int(val))

    except Exception as e:
        print(e)
        pass

    # Forget old data
    while len(times) > 1 and times[0] < current_time - start_time - look_back_secs:
        times.pop(0)
        bac_graph_points.pop(0)

    # Plotting stuff
    line.set_data(times, bac_graph_points)
    xmin, xmax = ax.get_xlim()
    #plt.plot([xmin, xmax], [yellow_thress, yellow_thress], 'y--')
    #plt.plot([xmin, xmax], [red_thress, red_thress], 'r--')
    if times[-1] >= xmax:
        ax.set_xlim(times[0], times[-1]+5)
        ax.figure.canvas.draw()

    return line,

ani = animation.FuncAnimation(fig, run, frames=None, blit=False, interval=10, repeat=False)
plt.show()
