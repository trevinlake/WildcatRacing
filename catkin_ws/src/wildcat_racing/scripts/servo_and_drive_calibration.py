from adafruit_servokit import ServoKit
import numpy as np
import time

kit = ServoKit(channels=16)

"""
#Use this code to set pulse width min and max.
kit.servo[0].set_pulse_width_range(1000, 2000)
"""

"""
#Use this code to set drive motor throttle; 0 is stopped,
0.5 is half speed, 1 is full speed.
kit.continuous_servo[1].throttle = 0
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

#Drive Constants
DRIVE_THROTTLE_MIN = 0
DRIVE_THROTTLE_MAX = 0.25
DRIVE_STEP = 0.01
DRIVE_STEP_LIST = np.arange(DRIVE_THROTTLE_MIN, DRIVE_THROTTLE_MAX, DRIVE_STEP)


#Sweep the steering servo within its entire range.
for step in STEERING_STEP_LIST:
    kit.servo[0].angle = step
    print(step)
    time.sleep(.1)

#Slowly increase throttle on drive motor within its entire range.
for step in DRIVE_STEP_LIST:
    kit.continuous_servo[1].throttle = step
    print(step)
