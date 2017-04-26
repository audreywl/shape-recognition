#!/usr/bin/env python

# import rospy
# from sensor_msgs.msg import Image
# from cv_bridge import CvBridge
import cv2
import numpy as np
import math

def distance(endpoints, point):
    """computes the perpendicular distance between a point a line defined by two endpoints"""
    # print endpoints
    start = endpoints[0][0]
    end = endpoints[1][0]
    # print start
    # print end
    dist_to_start = math.sqrt((point[0]-start[0])**2 + (point[1]-start[1])**2)
    angle_of_big_line = math.atan2((end[1]-start[1]),(end[0]-start[0]))
    angle_to_point = math.atan2((start[1]-point[1]),(start[0]-point[0]))
    start_angle = angle_of_big_line-angle_to_point
    perp_distance = dist_to_start*math.sin(start_angle)
    return perp_distance


def dp(point_list, epsilon):
    max_distance = 0

    furthest_point = None
    for i in range(len(point_list[1:-1])):
    	# print i[0][0]
    	# print(i,len(point_list))
        dist = distance((point_list[0],point_list[-1]), point_list[i][0])
        if dist>max_distance:
            max_distance = dist
            furthest_point = i
    if max_distance > epsilon:
        new_line_1 = point_list[0:i+1]
        new_line_2 = point_list[i:-1]
        result_list_1 = dp(new_line_1, epsilon)
        result_list_2 = dp(new_line_2, epsilon)
        # print result_list_1
        # print result_list_2
        if result_list_1:
        	return result_list_1[0:-1].append(result_list_2)
        else:
        	return result_list_2
    else:
        return [point_list[0], point_list[-1]]


def shape_trainer(trainImage):
	minVal = 50
	maxVal = 87
	test_image = cv2.imread(trainImage,-1)
	test_image = cv2.medianBlur(test_image,5)
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
	for i in range(len(contours)):
		temp = dp(contours[i], 100)
		# if temp:
		# print temp
		if temp:
			res.append(temp)
	return len(res)
	# for x in res:
		# vals.appe


if __name__ == '__main__':
	print shape_trainer("./circle_base.png")
	# print shape_trainer("./multi_image.png")
	print shape_trainer("./square_base.png")
	print shape_trainer("./pentagon_base.png")