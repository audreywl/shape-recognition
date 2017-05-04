#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np
import math

class ShapeRecognizer(object):
    """ This robot should recognize shapes """


    def __init__(self):
        """ Initialize the street sign reocgnizer """
        rospy.init_node('shape_recognizer')
        self.cv_image = np.zeros((480,640))                        # the latest image from the camera
        self.hsv_image = np.zeros((480,640))
        self.bridge = CvBridge()                    # used to convert ROS messages to OpenCV
        cv2.namedWindow('video_window')
        cv2.moveWindow('video_window', 600, 600)
        rospy.Subscriber("/camera/image_raw", Image, self.process_image)
        self.edge_detected = np.zeros((480,640))
        self.contour_image = np.zeros((480,640))
        self.minVal = 50
        self.maxVal = 87
        self.res = []
        self.test_image = cv2.imread("./square_base.png",-1)



    def distance(self, endpoints, point):
        """computes the perpendicular distance between a point a line defined by two endpoints"""
        P1 = endpoints[0][0]
        P2 = endpoints[1][0]

        y3 = point[0][1]
        x3 = point[0][0]
        y1 = P1[1]
        x1 = P1[0]
        y2 = P2[1]
        x2 = P2[0]

        px = x2-x1
        py = y2-y1

        something = px*px + py*py

        u =  ((x3 - x1) * px + (y3 - y1) * py) / float(something)

        if u > 1:
            u = 1
        elif u < 0:
            u = 0

        x = x1 + u * px
        y = y1 + u * py

        dx = x - x3
        dy = y - y3

        dist = math.sqrt(dx*dx + dy*dy)

        return dist



    def dp(self, M, epsilon):
        """
        Recursively simplifies an array of points using the RDP algorithm.
        M: an array
        epsilon: epsilon in the rdp algorithm
        dist: distance function
        """
        dmax = 0.0
        index = -1

        for i in xrange(1, M.shape[0]):
            d = self.distance((M[0],M[-1]),M[i])

            if d > dmax:
                index = i
                dmax = d

        if dmax > epsilon:
            r1 = self.dp(M[:index + 1], epsilon)
            r2 = self.dp(M[index:], epsilon)

            return np.vstack((r1[:-1], r2))
        else:
            return np.vstack((M[0], M[-1]))

    def process_image(self, msg):
        """ Process image messages from ROS and stash them in an attribute
            called cv_image for subsequent processing """
        self.cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
        self.edge_detected = cv2.Canny(self.cv_image,self.minVal,self.maxVal)
        if cv2.__version__.startswith('3.'):
             _, self.contours,_  = cv2.findContours(self.edge_detected, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        else:
            self.contours,_  = cv2.findContours(self.edge_detected, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        self.contour_image = cv2.drawContours(self.cv_image, self.contours, -1, (0,255,0), 3)
        for i in range(len(self.contours)):
            temp = self.dp(self.contours[i], 20)
            self.res.append(len(temp))
            if len(temp) == 7:
                for i in range(0,len(temp)-1,2):
                    cv2.line(self.contour_image, (temp[i][0],temp[i][1]),(temp[i+1][0], temp[i+1][1]), (0,0,255), 5)
            if len(temp) == 5:
                for i in range(0,len(temp)-1,2):
                    cv2.line(self.contour_image, (temp[i][0],temp[i][1]),(temp[i+1][0], temp[i+1][1]), (255,0,0), 5)


    def set_minVal(self, val):
        """ set hue lower bound """
        self.minVal = val

    def set_maxVal(self, val):
        """ set saturation lower bound """
        self.maxVal = val




    def run(self):
        """ The main run loop"""
        r = rospy.Rate(10)
        while not rospy.is_shutdown():

            if not self.cv_image is None:
                #cv2.imshow('video_window', self.cv_image)
                cv2.imshow('video_window2', self.contour_image)
                cv2.waitKey(10)
            r.sleep()

if __name__ == '__main__':
    node = ShapeRecognizer()
    node.run()