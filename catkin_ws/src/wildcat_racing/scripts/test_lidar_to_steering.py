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
        right_deg_arr = np.zeros(600)
        left_deg_arr = np.zeros(600)
        mid_deg_arr = np.zeros(600)
        #angle_count is how many ranges per degree of angle change.
        #average ranges per angle_count both for 'smoothing' sensor data and
        #for simplifying ranges indeces to coincide with integer degrees.
        deg_avg = 0
        deg_sum = 0
        for i in range(360,960): #Look at right side of LiDAR
            right_deg_arr[i-360] = ranges_arr[i]
        for i in range(1200,1800): #Look at left side of LiDAR
            left_deg_arr[i-1200] = ranges_arr[i]
        for i in range(960,1200): #Look at left side of LiDAR
            mid_deg_arr[i-960] = ranges_arr[i]

        #The index of the min range will be 90 degrees away from where we want
        #to steer the car
        try: #for only one minimum index
            right_min_range_index = np.argmin(right_deg_arr)
            left_min_range_index = np.argmin(left_deg_arr)
            mid_min_range_index = np.argmin(mid_deg_arr)
            auto_brake_steer_arr = np.extract(mid_deg_arr < 1, mid_deg_arr)

            #if right and left sides are within .1m (4 inches) default to
            #90 degrees
            right_left_range_diff = right_deg_arr[right_min_range_index] - left_deg_arr[left_min_range_index]
            #print("right_min_range_index: " + str(right_min_range_index))
            #print("left_min_range_index: " + str(left_min_range_index))
            #print("Difference: " + str(right_left_range_diff))
            #print("mid_min_range: " + str(mid_deg_arr[mid_min_range_index]))
            if np.abs(right_left_range_diff) < .1:
                new_angle = 90
            elif right_left_range_diff < 0: #turn left
                new_angle = (int((right_min_range_index + 360 + 720)/8)-45) #output(90,165)
                new_angle = ((new_angle - 90)*1.5) + 90
                print(str(right_min_range_index))
            elif right_left_range_diff > 0: #turn right
                print(str(left_min_range_index))
                new_angle = (int(((left_min_range_index + 1200 + 720)/8)-225)) #output(15,90)
                new_angle = ((new_angle - 90)*1.5) + 90
            else:
                new_angle = 90

            if new_angle > 180:
                new_angle = 180
            if new_angle < 0:
                new_angle = 0

        except: #for multiple minimum indeces, choose first minimum index
            right_min_range_index = np.argmin(right_deg_arr)[0]
            left_min_range_index = np.argmin(left_deg_arr)[0]
            #print("right_min_range_index: " + str(right_min_range_index))
            #print("left_min_range_index: " + str(left_min_range_index))
            #print("mid_min_range: " + str(mid_deg_arr[mid_min_range_index]))
            #if right and left sides are within .1m (4 inches) default to
            #90 degrees
            right_left_range_diff = right_deg_arr[right_min_range_index] - left_deg_arr[left_min_range_index]
            #print("Difference: " + str(right_left_range_diff))
            if np.abs(right_left_range_diff) < .1:
                new_angle = 90
            elif right_left_range_diff < 0: #turn left
                new_angle = (int((right_min_range_index + 360 + 720)/8)-45) #output(90,165)
                new_angle = ((new_angle - 90)*1.5) + 90
                print(str(right_min_range_index))
            elif right_left_range_diff > 0: #turn right
                print(str(left_min_range_index))
                new_angle = (int(((left_min_range_index + 1200 + 720)/8)-225)) #output(15,90)
                new_angle = ((new_angle - 90)*1.5) + 90
            else:
                new_angle = 90

            if new_angle > 180:
                new_angle = 180
            if new_angle < 0:
                new_angle = 0

        self.angle = new_angle
        self.pub.publish(new_angle)

if __name__ == '__main__':
    print("Running lidar_to_steering node.")
    rospy.init_node('lidar_to_steering')
    rate = rospy.Rate(30) # 30Hz, max for our LIDAR is 40Hz
    LIDARAngle()
    rospy.spin()

