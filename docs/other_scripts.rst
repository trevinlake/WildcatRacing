Fix-It Scripts
=====================

"Blinky" drive_motor_endpoint.py
_____________________

This refers to a state that the Electronic Speed Controller gets stuck in a mode where it waits for calibration input from a remote controller. This is due to it being traditionally used in an RC setting. Since our vehicle does not utilize that funcionality, we wrote a script to send data directly to the ESC to knock it out of this calibration mode before launching our race modes.

.. code-insert:: python
  :linenos:
  
  #! /usr/bin/env python3.7
  # -*- coding: utf-8 -*-
  from adafruit_servokit import ServoKit
  import numpy as np
  import time

  kit = ServoKit(channels=16)
  command = ""
  while command != "end":
      command = input("enter speed:")
      try:
        kit.continuous_servo[2].throttle = float(command)
      except:
          command = "end"
          
  kit.continuous_servo[2].throttle = 0
  
servo_and_drive_calbration.py
___________________________

This code was used to initially interface with the servo and drive motor directly rather than through a ROS node. It was used to iterate through and identify values which we could use to properly set the steering servo PWM pulse width to make the full range 0-180 degrees match the full range of steering where 0 degrees is a full right turn and 180 degrees is a full left turn and 90 degrees is straight ahead. The drive motor is treated as a continuous servo with values ranging from -1,1 where 0 is full coast, -1 is full brake, and 1 is full throttle. 

.. code-insert:: python
  :linenos:
  
  #! /usr/bin/env python3.7
  # -*- coding: utf-8 -*-
  from adafruit_servokit import ServoKit
  import numpy as np
  import time

  kit = ServoKit(channels=16)

  kit.servo[0].set_pulse_width_range(1400, 1825)

  """
  #Use this code to set pulse width min and max.
  kit.servo[0].set_pulse_width_range(1000, 2000)
  """

  """
  #Use this code to set drive motor throttle; 0 is stopped,
  0.5 is half speed, 1 is full speed.
  kit.continuous_servo[2].throttle = 0
  """

  """
  #Use this code to set the steering servo's angle.
  kit.servo[0].angle = 180
  """

  """
  #Use this code to set the steering servo's actuation range.
  kit.servo[0].actuation_range = 180
  """

  #Steering Constants
  STEERING_MIN_ANGLE = 0
  STEERING_MAX_ANGLE = 180
  STEERING_STEP = 0.2
  STEERING_STEP_LIST = np.arange(STEERING_MIN_ANGLE, STEERING_MAX_ANGLE, STEERING_STEP)
  INVERSE_STEERING_STEP_LIST = np.arange(STEERING_MAX_ANGLE, STEERING_MIN_ANGLE, STEERING_STEP)

  #Drive Constants
  DRIVE_THROTTLE_MIN = 0
  DRIVE_THROTTLE_MAX = 0.05
  DRIVE_STEP = 0.001
  DRIVE_STEP_LIST = np.arange(DRIVE_THROTTLE_MIN, DRIVE_THROTTLE_MAX, DRIVE_STEP)


  #Sweep the steering servo within its entire range.
  for step in STEERING_STEP_LIST:
      kit.servo[0].angle = step
      print(step)
      time.sleep(.01)

  time.sleep(5)

  #Slowly increase throttle on drive motor within its entire range.
  for step in DRIVE_STEP_LIST:
      kit.continuous_servo[2].throttle = step
      time.sleep(.1)
      print(step)



  kit.continuous_servo[2].throttle = 0

  kit.servo[0].angle = 90
  
real_time_hall_effect.py
____________________________
This code is the real-time graphing of the suspension sensor data using matplotlib's animate function.

.. code-insert:: python
  :linenos:
  
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

real_time_IMU.py
_____________________________
This code is the self-written driver code for accessing data stored on the ADIS16470 IMU's registers. Note: The baud rate is likely incorrect as we could not readily find the proper one to use.

.. code-insert:: python
  :linenos:
  
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
      
lidar_ethernet_setup.py
________________________
This code configure's the Jetson Nano's Ethernet port for the Lidar data rather than being used for network information.

.. code-insert:: python
  :linenos:
  
  #! /usr/bin/env python3.7
  # -*- coding: utf-8 -*-

  import os
  import rospy

  os.system("sudo ip addr add 192.168.0.15/24 broadcast 192.168.0.255 dev eth0")
  os.system("rosrun urg_node urg_node _ip_address:=192.168.0.10")

  print("LIDAR Ethernet port has been configured")
