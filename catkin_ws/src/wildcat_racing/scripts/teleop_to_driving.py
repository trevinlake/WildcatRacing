#!/usr/bin/env python
import rospy
from std_msgs.msg import Empty
from std_msgs.msg import Float32
from geometry_msgs.msg import Twist
import numpy as np

def teleop_to_driving(speed):
    while not rospy.is_shutdown():
        #Do cmd_vel conversion Code
        #angle =
        rospy.loginfo(speed)
        pub.publish(speed)
        rate.sleep()

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard: %s\n", data.data)
    linear_x = Twist.linear.x
    if linear_x < 1.1789 and linear_x > 0.4549:
        #Output in range(0-1)
        speed = 1.04920586872571*np.log(linear_x) + 0.827254089734171
        teleop_to_driving(speed)


def teleop_listener():
    #already initiated teleop_to_steering node in main call.
    rospy.Subscriber('/cmd_vel', Twist, callback)
    while not rospy.is_shutdown():
        try:
            teleop_to_driving(speed)
        except rospy.ROSInterruptException:
            pass

def main():
    pub = rospy.Publisher('/teleop_drive', Float32, queue_size=120)
    rospy.init_node('teleop_to_driving', anonymous=True)
    rate = rospy.Rate(120) # 120hz


if __name__ == '__main__':
    print "Running teleop_to_driving"
    main()
    teleop_listener()
