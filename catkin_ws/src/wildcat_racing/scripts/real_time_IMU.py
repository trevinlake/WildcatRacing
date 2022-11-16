#!/usr/bin/env python3.7
import board
import busio
import digitalio
import array
import numpy as np
from adafruit_bus_device.spi_device import SPIDevice
import struct
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.ticker import FuncFormatter
import datetime as dt
import time

# This function is called periodically from FuncAnimation
def animate(i, xs, ys):

    # Add x and y to lists
    xs.append(dt.datetime.now().strftime('%H:%M:%S.%f'))
    ys.append(x_accel)

    # Limit x and y lists to 20 items
    xs = xs[-20:]
    ys = ys[-20:]

    # Draw x and y lists
    ax.clear()
    ax.plot(xs, ys)

    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('Acceleration Over Time')
    plt.ylabel("m/(s^2)")
    return


#Constants
X_GYRO_LOW = bytearray([0x04,0x05])
X_GYRO_OUT = bytearray([0x06, 0x07])
Y_GYRO_LOW = bytearray([0x08,0x09])
Y_GYRO_OUT = bytearray([0x0A, 0x0B])
Z_GYRO_LOW = bytearray([0x0C,0x0D])
Z_GYRO_OUT = bytearray([0x0E, 0x0F])
X_ACCEL_LOW = bytearray([0x10,0x11])
X_ACCEL_OUT = bytearray([0x12, 0x13])
Y_ACCEL_LOW = bytearray([0x14,0x15])
Y_ACCEL_OUT = bytearray([0x16, 0x17])
Z_ACCEL_LOW = bytearray([0x18,0x19])
Z_ACCEL_OUT = bytearray([0x1A, 0x1B])
TEMP_OUT = bytearray([0x1C, 0x1D])
TIME_STAMP = bytearray([0x1E, 0x1F])


#Setup spi bus
spi = busio.SPI(board.SCLK, MISO=board.MISO, MOSI = board.MOSI)
#Setup Chip Select
cs = digitalio.DigitalInOut(board.CE0_1)

#Create an instance of the SPIDevice class
device = SPIDevice(spi, cs, baudrate=4000, polarity=0, phase=0)


def spi_request_float32(request_low, request_out):
    result_low = bytearray(2)
    result_out = bytearray(2)
    result = bytearray(4)
    with device as spi:
        spi.write_readinto(request_low, result_low)
        spi.write_readinto(request_out, result_out)
    result_out.extend(result_low)
    result_float = struct.unpack('f', result_out)

    return result_float[0]

def spi_request_decimal(request):
    result = bytearray(2)
    with device as spi:
        spi.write_readinto(request, result)

    result_decimal = int.from_bytes(result, byteorder='big', signed=True)

    return result_decimal
time_stamp = 0
# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(2, 2, 1)
xs = []
ys = []
x_accel_list = []
x_gyro_list = []
time0_list = []
while True:
    x_accel = spi_request_float32(X_ACCEL_LOW, X_ACCEL_OUT)
    y_accel = spi_request_float32(Y_ACCEL_LOW, Y_ACCEL_OUT)
    z_accel = spi_request_float32(Z_ACCEL_LOW, Z_ACCEL_OUT)

    x_gyro = spi_request_float32(X_GYRO_LOW, X_GYRO_OUT)
    y_gyro = spi_request_float32(Y_GYRO_LOW, Y_GYRO_OUT)
    z_gyro = spi_request_float32(Z_GYRO_LOW, Z_GYRO_OUT)

    temp = spi_request_decimal(TEMP_OUT)/10
    time_stamp += spi_request_decimal(TIME_STAMP)
    print("x_acceleration: " + str(x_accel))
    print("x_gyro: " + str(x_gyro))
    print("Temperature: " + str(temp) + "\n")
    #first Hall effect sensor

    #Get the Digital Value of Analog of selected channel
    #x_accel_list.append(x_accel)
    #x_gyro_list.append(x_gyro)
    #time0_list.append(time.time())


    #plt.plot(time0_list,x_accel_list, label = "x_accel")
    #plt.plot(time0_list,x_gyro_list, label = "x_gyro")
    #plt.legend()
    #ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=1000)
    #plt.show()

