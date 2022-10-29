#! /usr/bin/env python
import rospy
from std_msgs.msg import Empty
from std_msgs.msg import Float64
from geometry_msgs.msg import Twist
import numpy as np

class TeleopAngle:

    def __init__(self):
        self.angle = 0
        self.pub = rospy.Publisher('/teleop_angle', Float64, queue_size=120)
        self.cmd_vel_subscriber = rospy.Subscriber('/cmd_vel', Twist, self.callback)

    def callback(self, Twist):
        rospy.loginfo(rospy.get_caller_id() + "I heard: %s\n", Twist.angular.z)
        new_angle = Float64()
        angular_z = Twist.angular.z
        if angular_z == 0:
            new_angle = 90
        elif angular_z < 0 and angular_z > -2.3579 and angular_z < -.91:
        #use left_angle(output is in range (90,180])
            new_angle = 94.4285281853136*np.log(-1*angular_z) + 99
        elif angular_z > .91 and angular_z < 2.3579:
        #use right_angle(output is in range [0,90))
            new_angle = -94.4285281853136*np.log(angular_z) + 81
        else:
            new_angle = 90

        self.angle = new_angle
        self.pub.publish(new_angle)

if __name__ == '__main__':
    print("Running teleop_to_steering node.")
    rospy.init_node('teleop_to_steering')
    rate = rospy.Rate(120) # 120hz
    TeleopAngle()
    rospy.spin()
