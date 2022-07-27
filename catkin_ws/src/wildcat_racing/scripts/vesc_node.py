#!/usr/bin/env python
"""
Created on Wed Jul 27 12:16:37 2022

@author: trevin
"""

import os
import rospy
from std_msgs.msg import String

print("Opened vesc node")
os.system("rostopic echo /cmd_vel")



#def callback(data):
#    rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.data)
#
#def vesc():
#
#    # In ROS, nodes are uniquely named. If two nodes with the same
#    # name are launched, the previous one is kicked off. The
#    # anonymous=True flag means that rospy will choose a unique
#    # name for our 'listener' node so that multiple listeners can
#    # run simultaneously.
#    rospy.init_node('vesc', anonymous=True)
#
#    rospy.Subscriber('', String, callback)
#
#    # spin() simply keeps python from exiting until this node is stopped
#    rospy.spin()
#
#if __name__ == '__main__':
#    vesc()
