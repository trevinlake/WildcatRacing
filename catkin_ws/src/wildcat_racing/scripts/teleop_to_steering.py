#!/usr/bin/env python
import rospy
from std_msgs.msg import Empty
from std_msgs.msg import Float32
from geometry_msgs.msg import Twist
import numpy as np

pub = rospy.Publisher('/teleop_angle', Float32, queue_size=120)
rospy.init_node('teleop_to_steering', anonymous=True)
rate = rospy.Rate(120) # 120hz
angle = 90 #start out straight.
def teleop_to_steering(angle):
    while not rospy.is_shutdown():
        #Do cmd_vel conversion Code
        #angle =
        rospy.loginfo(angle)
        pub.publish(angle)
        rate.sleep()

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard: %s\n", data.data)
    #if data.data == null:
    #if linear_x != 0:
    #use forward_angle

    #if angular_z > 0:
    #use left_angle

    #if angular_z < 0:
    #use right_angle
    forward_angle = 1.04920586872571*np.log(linear_x) + 0.827254089734171
    left_angle = -94.4285281853136*np.log(angular_z) + 81
    right_angle = 94.4285281853136*np.log(angular_z) + 99
    
def teleop_listener():
    #already initiated teleop_to_steering node in main call.
    rospy.Subscriber('/cmd_vel', Twist, callback)
    while not rospy.is_shutdown():
        try:
            teleop_to_steering(angle)
        except rospy.ROSInterruptException:
            pass



if __name__ == '__main__':
    print "Running teleop_to_steering"
    teleop_listener()
