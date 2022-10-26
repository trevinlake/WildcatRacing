#!/usr/bin/env python
import rospy
from std_msgs.msg import Empty
from std_msgs.msg import Float32
from geometry_msgs.msg import Twist
import numpy as np

def teleop_to_steering(angle):
    while not rospy.is_shutdown():
        rospy.loginfo(angle)
        pub.publish(angle)
        rate.sleep()

def callback(Twist):
    rospy.loginfo(rospy.get_caller_id() + "I heard: %s\n", data.data)
    angular_z = Twist.angular.z
    if angular_z == 0:
        angle = 90
    elif angular_z < 0 and angular_z > -2.3579 and angular_z < -.91:
    #use left_angle(output is in range 0-90)
        angle = -94.4285281853136*np.log(-1*angular_z) + 81
    elif angular_z < 0 and angular_z > .91 and angular_z < 2.3579:
    #use right_angle(output is in range 90-180)
        angle = 94.4285281853136*np.log(angular_z) + 99
    else:
        angle = 90

    #publish new angle
    teleop_to_steering(angle)

def teleop_listener():
    #already initiated teleop_to_steering node in main call.
    rospy.Subscriber('/cmd_vel', Twist, callback)
    while not rospy.is_shutdown():
        try:
            teleop_to_steering(angle)
        except rospy.ROSInterruptException:
            pass

def main():
    pub = rospy.Publisher('/teleop_angle', Float32, queue_size=120)
    rospy.init_node('teleop_to_steering', anonymous=True)
    rate = rospy.Rate(120) # 120hz


if __name__ == '__main__':
    print "Running teleop_to_steering"
    main()
    teleop_listener()