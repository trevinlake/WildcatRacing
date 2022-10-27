#! /usr/bin/env python
import rospy
from std_msgs.msg import Empty
from std_msgs.msg import Float64
from geometry_msgs.msg import Twist
import numpy as np

class TeleopSpeed:

    def __init__(self):
        self.speed = 0
        self.pub = rospy.Publisher('/teleop_speed', Float64, queue_size=120)
        self.cmd_vel_subscriber = rospy.Subscriber('/cmd_vel', Twist, self.callback)

    def callback(self, Twist):
        rospy.loginfo(rospy.get_caller_id() + "I heard: %s\n", Twist.linear.x)
        new_speed = Float64()
        linear_x = Twist.linear.x
        if linear_x == 0:
            #set speed to 0 AKA teleop killswitch
            new_speed = 0
        elif linear_x < 1.1789 and linear_x > 0.4549:
            #Output in range(0-1)
            new_speed = 1.04920586872571*np.log(linear_x) + 0.827254089734171
        else:
            speed = 0

        self.speed = new_speed
        self.pub.publish(new_speed)

if __name__ == '__main__':
    print("Running teleop_to_driving node.")
    rospy.init_node('teleop_to_driving')
    rate = rospy.Rate(120) # 120hz
    TeleopSpeed()
    rospy.spin()

