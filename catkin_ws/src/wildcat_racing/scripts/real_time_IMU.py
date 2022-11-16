#!/usr/bin/env python3.7
import board
import busio
import digitalio
import array
import numpy as np
from adafruit_bus_device.spi_device import SPIDevice

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
spi = busio.SPI(board.SCK, MISO=board.MISO)
#Setup Chip Select
cs = digitalio.DigitalInOut(board.D2)

#Create an instance of the SPIDevice class
device = SPIDevice(spi, cs, baudrate=4000, polarity=0, phase=0)

def spi_request_float32(request_low, request_out):
    result_low = bytearray(2)
    result_out = bytearray(2)
    result = bytearray(4)
    with device as spi:
        spi.write_then_readinto(request_low, result_low)
        spi.write_then_readinto(request_out, result_out)
    result = result_out.append(result_low)
    result_bytes = np.array(result, dtype = np.uint8)
    result_float = result_bytes.view(dtype = np.float32)

    return result_float

def spi_request_decimal(request):
    result = bytearray(2)
    with device as spi:
        spi.write_then_readinto(request, result)
    result_bytes = np.array(result, dtype = np.uint8)
    result_decimal = int.from_bytes(result_bytes, byteorder='big', signed=True)

    return result_decimal

while True:
    x_accel = spi_request_float32(X_ACCEL_LOW, X_ACCEL_OUT)
    y_accel = spi_request_float32(Y_ACCEL_LOW, Y_ACCEL_OUT)
    z_accel = spi_request_float32(Z_ACCEL_LOW, Z_ACCEL_OUT)

    x_gyro = spi_request_float32(X_GYRO_LOW, X_GYRO_OUT)
    y_gyro = spi_request_float32(Y_GYRO_LOW, Y_GYRO_OUT)
    z_gyro = spi_request_float32(Z_GYRO_LOW, Z_GYRO_OUT)

    temp = spi_request_decimal(TEMP_OUT)/100
    time += spi_request_decimal(TIME_STAMP)
    print("X_ACCEL = " + x_accel + "\n")
    print("X_GYRO = " + x_gyro + "\n")
    print("Temperature = " + temp + " degrees Celsius")

