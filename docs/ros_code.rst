ROS Code
========================

RQT Graph
________________________
.. image:: images/RQT_graph.png
  :width: 800
  :alt: Alternative text

The above image is a graph of all ROS Nodes used within our vehicle and how they relate to each other. This RQT Graph should be referenced as the code below is examined. The ovals depict a ROS node and the rectangles depict a ROS topic.

ROS Node Data Characterization Example - Lidar to Steering Subscriber/Publisher Node
________________________
.. code-block:: python
  :linenos:
  :emphasize-lines: 1,17-18,33-38,55,57,61,68,73,102,107

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
          for i in range(960,1200): #Look straight ahead of LiDAR
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
      
Line 1 is the "shebang" which tells the Python interpreter which version of Python should be used to run the code. In line 17, we set this node to publish on a topic called lidar_angle. (In line 107, we can see it will be published at a rate of 30 Hz). Line 18 is where the node is set to subscribe to the /scan topic where our lidar data is published. In lines 33-38, we extract several subarrays from the total ranges_array provided from the ranges found in the /scan topic. One sub-array coincides with a snippet of ranges found on the right-hand side of the vehicle, another is a snippet of ranges found on the vehicle's left-hand side. Finally, the last snippet of ranges corresponds with ranges found directly ahead of the vehicle. Line 55 shows that if the minimum distance of both right and left sub-arrays differ by less than .1 meter, the vehicle defaults to 90 degrees which corresponds with the vehicle heading straight. Line 57 shows how the vehicle will make a left turn. Note: The vehicle uses the equation found in line 58 to determine the angle of the nearest obstacle in reference to the vehicle. Line 59 shows how the vehicle then offsets its heading by adjusting the steering 90 degrees away from the angle solved for in line 58. Lines 68-71 accounts for adjustments to the steering data characterization equations in how aggressive the steering response should be. For our vehicle, the steering response is static, however with dynamic steering response, it is possible to get invalid values returned from the characterization equations. These lines allow for a dynamic steering characterization while sanitizing the angles returned prior to publishing them to the lidar_angle topic. Line 73 is the except case for when there are multiple minimum indeces returned from lines 43-45. We chose to use the first minimum angle for this case. In line 102, we publish the characterized angle to the lidar_angle topic.

ROS Node Control Example - Steering Servo Subscriber Node
________________________
.. code-block:: python
  :linenos:
  :emphasize-lines: 1,9-10,12,19-21,23,28-29,33,37,39

    #! /usr/bin/env python3.7
    # -*- coding: utf-8 -*-
    import rospy
    from adafruit_servokit import ServoKit
    from std_msgs.msg import Float64
    from std_msgs.msg import Float32
    import numpy as np

    kit = ServoKit(channels=16)
    kit.servo[0].set_pulse_width_range(1400, 1825)

    class Servo:

        # Steering Servo info:
        # The steering servo as configured above will take range 0-180
        # where 0 is RHS and 180 is LHS.

        def __init__(self):
            self.angle = 0
            self.teleop_angle_subscriber = rospy.Subscriber('/teleop_angle', Float64, self.teleop_callback)
            self.lidar_angle_subscriber = rospy.Subscriber('/lidar_angle', Float32, self.lidar_callback)

        def teleop_callback(self, msg):
            rospy.loginfo(rospy.get_caller_id() + "Latest teleop_angle was: %s\n", msg)
            new_angle = Float64()
            if msg != 0:
                new_angle = round(msg.data)
                self.angle = msg
                kit.servo[0].angle = new_angle
            else:
                self.angle = 0

        def lidar_callback(self, msg):
            rospy.loginfo(rospy.get_caller_id() + "Latest lidar_angle was: %s\n", msg)
            new_angle = Float32()
            #Priority is given to teleop since self.angle is only updated by teleop.
            if self.angle == 0:
                new_angle = msg.data
                kit.servo[0].angle = new_angle

    if __name__ == '__main__':
        print("Running servo node.")
        rospy.init_node('servo')
        Servo()
        rospy.spin()

In Lines 9-10, we use the adafruit_servokit library to create a servo controller object that has 16 channels. This how the PCA9685 Servo Driver board is integrated in software. The pulse width chosen gives our car the full steering range of motion without locking up the servo. The values show in line 10 were found via trial and error. Line 12 is where we create a Servo class. We decided to make all Python ROS Nodes using object oriented architecture since Python's implementation of ROS in scripted architecture requires some 'tricks' and global variables to access and pass the variables even within the same Node. Lines 20-21 are where we tell this node to subscribe to both /teleop_angle and /lidar_angle topics. Line 23 is the teleop callback function which is called any time new data shows up on the /teleop_angle topic. In line 28, we can see that if a teleop message is not 0, we assign the nodes 'angle' attribute to be the value of the message. Then in line 29, we send the new angle to the steering servo over the PCA9685 control board at channel 0 using PWM via I2C protocol. Line 33 is the lidar callback function which is called every time new data appears on the /lidar_angle topic. Line 37 shows how we give priority to teleop since we are using teleop as an emergency override to stop autonomous driving using keyboard controls. Line 39 sends the latest lidar data to the steering servo via the PCA6985 servo control board.

Note: The teleop_callback is expected to be called at 120 Hz as the publisher node which publishes to the teleop_angle topic refreshes at 120 Hz. The lidar_callback is expected to be called at 30 Hz according to the lidar_angle topic's publish rate.
