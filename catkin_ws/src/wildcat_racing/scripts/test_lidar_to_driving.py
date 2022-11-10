#! /usr/bin/env python3.7
# -*- coding: utf-8 -*-
import rospy
from std_msgs.msg import Empty
from std_msgs.msg import Float32
from sensor_msgs.msg import LaserScan
import numpy as np

class LIDARAngle:

    # LIDAR info:
    # The LIDAR can 'see' as close as 0.2 meters (about 0.65ft)
    # and as far away as 30 meters (about 98.5ft).

    def __init__(self):
        self.angle = 0
        self.pub = rospy.Publisher('/lidar_angle', Float32, queue_size=35)
        self.scan_subscriber = rospy.Subscriber('/scan', LaserScan, self.callback)

    def callback(self, LaserScan):
        rospy.loginfo(rospy.get_caller_id() + "Latest LiDAR scan time was: %s\n", LaserScan.scan_time)
        new_angle = Float32()
        ranges_arr = np.array(LaserScan.ranges)
        angle_count = 8
        deg_arr = np.zeros(int(len(ranges_arr)/angle_count))
        #angle_count is how many ranges per degree of angle change.
        #average ranges per angle_count both for 'smoothing' sensor data and
        #for simplifying ranges indeces to coincide with integer degrees.
        deg_avg = 0
        deg_sum = 0
        for i in range(45,225,angle_count): #Look at only the ranges within the semi circle.
            for j in range(angle_count):
                deg_sum += ranges_arr[i+j]
            deg_avg = deg_sum/angle_count
            deg_arr[i-45] = deg_avg #indeces 0-179
            deg_sum = 0

        #The index of the maximum range will coincide with degree angle
        #in deg_arr.
        new_angle = np.argmax(deg_arr)[0]

        self.angle = new_angle
        self.pub.publish(new_angle)

if __name__ == '__main__':
    print("Running lidar_to_steering node.")
    rospy.init_node('lidar_to_steering')
    rate = rospy.Rate(30) # 30Hz, max for our LIDAR is 40Hz
    LIDARAngle()
    rospy.spin()
