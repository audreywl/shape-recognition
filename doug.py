#!/usr/bin/env python

"""ROS Node for executing the Douglas-Peucker algorithm."""

import math

def process_image(img):
	cv_image = None                        # the latest image from the camera
	binary_image = None

	hsv_lb = np.array([0, 0, 0])           # hsv lower bound
	hsv_ub = np.array([245, 245, 245])     # hsv upper bound

	cv2.namedWindow('video_window')
	cv2.namedWindow('threshold_image')
	cv2.createTrackbar('H lb', 'threshold_image', 0, 255, set_h_lb)
	cv2.createTrackbar('S lb', 'threshold_image', 0, 255, set_s_lb)
	cv2.createTrackbar('V lb', 'threshold_image', 0, 255, set_v_lb)

	cv2.createTrackbar('H ub', 'threshold_image', 245, 255, set_h_ub)
	cv2.createTrackbar('S ub', 'threshold_image', 245, 255, set_s_ub)
	cv2.createTrackbar('V ub', 'threshold_image', 245, 255, set_v_ub)

 #we do contours to make sure subsequent points are neighbors -
	# CV_RETR_EXTERNAL because we only want one contour, and CV_CHAIN_APPROX_NONE b/c we don't want to compress by finding extrema, we want all the pointsg



def distance(endpoints, point):
	"""computes the perpendicular distance between a point a line defined by two endpoints"""
	start = endpoints[0]
	end = endpoints[1]
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
		dist = distance((point_list[0],point_list[-1]), point_list[i])
		if dist>max_distance:
			max_distance = dist
			furthest_point = i
	if max_distance > epsilon:
		new_line_1 = point_list[0:i+1]
		new_line_2 = point_list[i:-1]
		result_list_1 = dp(new_line_1, epsilon)
		result_list_2 = dp(new_line_2, epsilon)
		return result_list_1[0:-1].append(result_list_2)
	else:
		return [point_list[0], point_list[-1]]

def update_img(img):
	binary_image = process_image(img)
	if not binary_image is None:
