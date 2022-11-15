#! /usr/bin/env python3.7
# -*- coding: utf-8 -*-
from adafruit_servokit import ServoKit
import numpy as np
import time

kit = ServoKit(channels=16)
command = ""
while command != "end":
    command = input("enter speed:")
    
    kit.continuous_servo[2].throttle = float(command)
    except:
        command = "end"


kit.continuous_servo[2].throttle = 0

