#! /usr/bin/env python3.7
# -*- coding: utf-8 -*-
import rospy
from std_msgs.msg import Empty
from std_msgs.msg import Float32
from sensor_msgs.msg import LaserScan
import numpy as np

class LIDARSpeed:

    # LIDAR info:
    # The LIDAR can 'see' as close as 0.2 meters (about 0.65ft)
    # and as far away as 30 meters (about 98.5ft).

    def __init__(self):
        self.speed = 0
        self.pub = rospy.Publisher('/lidar_speed', Float32, queue_size=35)
        self.scan_subscriber = rospy.Subscriber('/scan', LaserScan, self.callback)

    def callback(self, LaserScan):
        rospy.loginfo(rospy.get_caller_id() + "Latest LiDAR scan time was: %s\n", LaserScan.scan_time)
        new_speed = Float32()
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
                deg_sum += ranges[i+j]
            deg_avg = deg_sum/angle_count #Average range within a degree of 8 measurements.
            deg_arr[i-45] = deg_avg #indeces 0-179
            deg_sum = 0

        auto_brake_arr = np.extract(deg_arr < 0.6, deg_arr)
        max_range = np.max(deg_arr)
        if len(auto_brake_arr) > 0:
            new_speed = 0
        elif max_range > 0.6 and max_range < 1:
            new_speed = 0.1 #Hardcoded slow speed for close range.
        elif max_range > 1 and max_range < 30:
            new_speed = .175 #Hardcoded slow speed for test mode.
        else:
            new_speed = 0

        self.angle = new_speed
        self.pub.publish(new_speed)

if __name__ == '__main__':
    print("Running lidar_to_driving node.")
    rospy.init_node('lidar_to_driving')
    rate = rospy.Rate(30) # 30Hz, max for our LIDAR is 40Hz
    LIDARSpeed()
    rospy.spin()
