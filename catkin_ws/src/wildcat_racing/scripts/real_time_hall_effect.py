#!/usr/bin/env python3.7
import matplotlib.pyplot as plt
import numpy as np
import time
import adafruit_ads1x15.ads1115 as ADS
import board
import busio
import os
i2c = busio.I2C(board.SCL_1, board.SDA_1)
import sys
sys.path.append('../')
import time
from adafruit_ads1x15.analog_in import AnalogIn
import matplotlib.animation as animation
from matplotlib.ticker import FuncFormatter
import datetime as dt

def init():
    line.set_ydata([np.nan] * len(x))
    return line,

# This function is called periodically from FuncAnimation
def animate(i, xs, ys):

    # Read temperature (Celsius) from TMP102
    voltage = hall0.voltage

    # Add x and y to lists
    xs.append(dt.datetime.now().strftime('%H:%M:%S.%f'))
    ys.append(voltage)

    # Limit x and y lists to 20 items
    xs = xs[-20:]
    ys = ys[-20:]

    # Draw x and y lists
    ax.clear()
    ax.plot(xs, ys)

    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('Hall Effect 0 Over Time')
    plt.ylabel('Voltage')


sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
ADS1115_REG_CONFIG_PGA_6_144V        = 0x00 # 6.144V range = Gain 2/3
ADS1115_REG_CONFIG_PGA_4_096V        = 0x02 # 4.096V range = Gain 1
ADS1115_REG_CONFIG_PGA_2_048V        = 0x04 # 2.048V range = Gain 2 (default)
ADS1115_REG_CONFIG_PGA_1_024V        = 0x06 # 1.024V range = Gain 4
ADS1115_REG_CONFIG_PGA_0_512V        = 0x08 # 0.512V range = Gain 8
ADS1115_REG_CONFIG_PGA_0_256V        = 0x0A # 0.256V range = Gain 16
ads1115 = ADS.ADS1115(i2c)
hall0 = AnalogIn(ads1115, ADS.P0)

# set x axis for time
adc0_list = []
adc1_list = []
adc2_list = []
adc3_list = []
time0_list = []
time1_list = []
time2_list = []
time3_list = []
# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(2, 2, 1)
xs = []
ys = []
while True:
    #Get the Digital Value of Analog of selected channel
    #print(hall0.value, hall0.voltage)
    adc0_list.append(hall0.voltage)
    time0_list.append(time.time())
    #time.sleep(0.2)
    #adc1_list.append(hall1.voltage)
    #time1_list.append(time.time())
    #time.sleep(0.2)
    #adc2_list.append(hall2.voltage)
    #time2_list.append(time.time())
    #time.sleep(0.2)
    #adc3_list.append(hall3.voltage)
    #time3_list.append(time.time())
    #print("A0:%dmV A1:%dmV A2:%dmV A3:%dmV"%(adc0_list[i],adc1_list[i],adc2_list[i],adc3_list[i]))


    #first Hall effect sensor
    plt.subplot(2, 2, 1)
    line = (time.time(), hall0.voltage)
    plt.plot(time0_list,adc0_list)
    #plt.title("Hall Effect Sensor 2")
    #plt.subplot(2, 2, 2)
    #plt.plot(adc1, time1)

    #plt.title("Hall Effect Sensor 3")
    #plt.subplot(2, 2, 3)
    #plt.plot(adc2, time2)

    #plt.title("Hall Effect Sensor 4")
    #plt.subplot(2, 2, 4)
    #plt.plot(adc3, time3)

    # Set up plot to call animate() function periodically
    ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=1000)
    plt.show()

