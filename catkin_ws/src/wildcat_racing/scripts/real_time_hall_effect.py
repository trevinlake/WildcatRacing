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
def animate(i, xs0, ys0, xs1, ys1, xs2, ys2, xs3, ys3):

    # Read voltage from i2c_bus
    voltage_0 = hall_0.voltage
    voltage_1 = hall_1.voltage
    voltage_2 = hall_2.voltage
    voltage_3 = hall_3.voltage

    # Add x and y to lists
    xs0.append(dt.datetime.now().strftime('%H:%M:%S.%f'))
    ys0.append(voltage_0)

    xs1.append(dt.datetime.now().strftime('%H:%M:%S.%f'))
    ys1.append(voltage_1)

    xs2.append(dt.datetime.now().strftime('%H:%M:%S.%f'))
    ys2.append(voltage_2)

    xs3.append(dt.datetime.now().strftime('%H:%M:%S.%f'))
    ys3.append(voltage_3)

    # Limit x and y lists to 20 items
    xs0 = xs0[-20:]
    ys0 = ys0[-20:]

    xs1 = xs1[-20:]
    ys1 = ys1[-20:]

    xs2 = xs2[-20:]
    ys2 = ys2[-20:]

    xs3 = xs3[-20:]
    ys3 = ys3[-20:]

    # Draw x and y lists
    ax[0][0].clear()
    ax[0][0].plot(xs3, ys3, 'g')
    ax[0][0].set_title("Front Left Suspension Sensor")
    ax[0][0].tick_params(labelrotation=45)


    ax[0][1].clear()
    ax[0][1].plot(xs2, ys2, 'k')
    ax[0][1].set_title("Front Right Suspension Sensor")
    ax[0][1].tick_params(labelrotation=45)

    ax[1][0].clear()
    ax[1][0].plot(xs1, ys1, 'orange')
    ax[1][0].set_title("Rear Left Suspension Sensor")
    ax[1][0].tick_params(labelrotation=45)

    ax[1][1].clear()
    ax[1][1].plot(xs0, ys0, 'm')
    ax[1][1].set_title("Rear Right Suspension Sensor")
    ax[1][1].tick_params(labelrotation=45)


    # Format plot
    plt.subplots_adjust(bottom=0.30)

    for a in ax.flat:
        a.set(xlabel='Time', ylabel='Voltage')
    plt.tight_layout()


sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
ADS1115_REG_CONFIG_PGA_6_144V        = 0x00 # 6.144V range = Gain 2/3
ADS1115_REG_CONFIG_PGA_4_096V        = 0x02 # 4.096V range = Gain 1
ADS1115_REG_CONFIG_PGA_2_048V        = 0x04 # 2.048V range = Gain 2 (default)
ADS1115_REG_CONFIG_PGA_1_024V        = 0x06 # 1.024V range = Gain 4
ADS1115_REG_CONFIG_PGA_0_512V        = 0x08 # 0.512V range = Gain 8
ADS1115_REG_CONFIG_PGA_0_256V        = 0x0A # 0.256V range = Gain 16
ads1115 = ADS.ADS1115(i2c)

hall_0 = AnalogIn(ads1115, ADS.P0)
hall_1 = AnalogIn(ads1115, ADS.P1)
hall_2 = AnalogIn(ads1115, ADS.P2)
hall_3 = AnalogIn(ads1115, ADS.P3)

# set x axis for time
hall_0_list = []
hall_1_list = []
hall_2_list = []
hall_3_list = []
time0_list = []
time1_list = []
time2_list = []
time3_list = []
# Create figure for plotting
fig, ax = plt.subplots(2,2)
xs0 = []
ys0 = []
xs1 = []
ys1 = []
xs2 = []
ys2 = []
xs3 = []
ys3 = []

while True:
    #Get the Digital Value of Analog of selected channel
    #print(hall0.value, hall0.voltage)
    hall_0_list.append(hall_0.voltage)
    time0_list.append(time.time())
    time.sleep(0.02)
    hall_1_list.append(hall_1.voltage)
    time1_list.append(time.time())
    time.sleep(0.02)
    hall_2_list.append(hall_2.voltage)
    time2_list.append(time.time())
    time.sleep(0.02)
    hall_3_list.append(hall_3.voltage)
    time3_list.append(time.time())
    #print("A0:%dmV A1:%dmV A2:%dmV A3:%dmV"%(adc0_list[i],adc1_list[i],adc2_list[i],adc3_list[i]))




    # Set up plot to call animate() function periodically
    ani = animation.FuncAnimation(fig, animate, fargs=(xs0, ys0, xs1, ys1, xs2, ys2, xs3, ys3), interval=100)
    #ani_1 = animation.FuncAnimation(fig, animate, fargs=(xs1, ys1), interval=1000)
    #ani_2 = animation.FuncAnimation(fig, animate, fargs=(xs2, ys2), interval=1000)
    #ani_3 = animation.FuncAnimation(fig, animate, fargs=(xs3, ys3), interval=1000)
    plt.tight_layout()
    plt.xticks(rotation=45, ha='right')
    plt.show()

