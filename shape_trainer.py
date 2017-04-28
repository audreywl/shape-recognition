#!/usr/bin/env python

# import rospy
# from sensor_msgs.msg import Image
# from cv_bridge import CvBridge
import cv2
import numpy as np
import math
import sys

def distance(endpoints, point):
    """
    Computes the perpendicular distance between a point and a line defined by two endpoints.
    Accepts a tuple of lists depicting x and y coordinates for the endpoints parameter and a list
    containing the x and y coordinates of the desired point to compare to the line.
    """
    P1 = endpoints[0][0]
    P2 = endpoints[1][0]
    y0 = point[1]
    x0 = point[0]
    y1 = P1[1]
    x1 = P1[0]
    y2 = P2[1]
    x2 = P2[0]

    dist = abs((y2-y1)*x0-(x2-x1)*y0+x2*y1-y2*x1)/((y2-y1)**(2)+(x2-x1)**(2))**(0.5) 
    return dist


def dp(point_list, epsilon):
    max_distance = 0
    # print len(point_list)
    furthest_point = None
    for i in range(len(point_list[1:-1])):
        # print i[0][0]
        # print(i,len(point_list))
        # print point_list
        dist = distance((point_list[0],point_list[-1]), point_list[i][0])
        if dist>max_distance: #try adding a 'fudge factor' extra value to be sure its worth splitting for
            max_distance = dist
            furthest_point = i
    if max_distance > epsilon:
        new_line_1 = point_list[0:i+1]
        new_line_2 = point_list[i:-1]
        result_list_1 = dp(new_line_1, epsilon)
        result_list_2 = dp(new_line_2, epsilon)
        # print result_list_1
        # print result_list_2
        if result_list_1 != None:
            # print "hey"
            # thing = result_list_1[0].append(result_list_2[0])
            thing = [np.append(result_list_1[0],result_list_2[0])]
            # print thing
            return thing
        else:
            # print "listen"
            return result_list_2
    else:
        return [point_list[0], point_list[-1]]


def shape_trainer(trainImage):
    minVal = 50
    maxVal = 87
    test_image = cv2.imread(trainImage,-1)
    # test_image = cv2.medianBlur(test_image,5)
    edge_detected = cv2.Canny(test_image,minVal,maxVal)
    contours, contour_hierarchy  = cv2.findContours(edge_detected, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contour_image = cv2.drawContours(test_image, contours, -1, (0,255,0), 3)
    # print contour_image
    # print contours
    # print edge_detected
    # cv2.imshow('video_window', test_image)
    # cv2.imshow('video_window2', edge_detected)
    # cv2.imshow('video_window3', contour_image)
    res = []
    vals = []
    # print contours[0]
    print len(contours)
    for i in range(len(contours)):
        temp = dp(contours[i], 40)
        # if temp:
        # print len(temp[0])
        # res.append(temp)
        res.append(len(temp[0]))
    # print res
    # return len(res[0][0])/2
    return res
    # for x in res:
        # vals.appe


if __name__ == '__main__':
    sys.setrecursionlimit(2000)
    # print shape_trainer("./circle_base.png")
    # print shape_trainer("./multi_image.png")
    # print shape_trainer("./square_base.png") #works best at 177.9
    print shape_trainer("./squares_base.png")
    # print shape_trainer("./pentagon_base.png")