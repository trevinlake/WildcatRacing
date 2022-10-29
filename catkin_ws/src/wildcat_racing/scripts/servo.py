#! /usr/bin/env python3
import rospy
from adafruit_servokit import ServoKit
from std_msgs.msg import Float64
from std_msgs.msg import Float32
import numpy as np

kit = ServoKit(channels=16)
kit.servo[0].set_pulse_width_range(1400, 1825)

class Servo:

    # Steering Servo info:
    # The steering servo as configured above will take range 0-180
    # where 0 is RHS and 180 is LHS.

    def __init__(self):
        self.angle = 0
        self.teleop_angle_subscriber = rospy.Subscriber('/teleop_angle', Float64, self.teleop_callback)
        self.lidar_angle_subscriber = rospy.Subscriber('/lidar_angle', Float32, self.lidar_callback)

    def teleop_callback(self, msg):
        rospy.loginfo(rospy.get_caller_id() + "Latest teleop_angle was: %s\n", msg)
        new_angle = Float64()
        if msg != 0:
            new_angle = msg
            self.angle = msg
            kit.servo[0].angle = new_angle
        else:
            self.angle = 0

    def lidar_callback(self, msg):
        rospy.loginfo(rospy.get_caller_id() + "Latest lidar_angle was: %s\n", msg)
        new_angle = Float32()
        #Priority is given to teleop since self.angle is only updated by teleop.
        if self.angle == 0:
            new_angle = msg
            kit.servo[0].angle = new_angle

if __name__ == '__main__':
    print("Running servo node.")
    rospy.init_node('servo')
    Servo()
    rospy.spin()
