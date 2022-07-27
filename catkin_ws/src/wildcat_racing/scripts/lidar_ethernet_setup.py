#!/usr/bin/env python
"""
Spyder Editor

This is a temporary script file.
"""
import os
import rospy

os.system("sudo ip addr add 192.168.0.15/24 broadcast 192.168.0.255 dev eth0")
os.system("rosrun urg_node urg_node _ip_address:=192.168.0.10")

print("LIDAR Ethernet port has been configured")

