import cv2
import numpy as np
import math
import sys
def edge_detector(image):
	"""
	Given an input image file path, detects and returns the coordinates of each pixel detected as an edge.
	"""
	test_image = cv2.imread(image,-1)
	# print test_image
	width = len(test_image[0])
	height = len(test_image)
	tolerance = 762 #amount of pixel variation allowed before edge is detected #762 for black and white

	#keep track of the coordinates (x,y) of pixels where a dramatic change in coloration is detected
	down_pix = None
	right_pix = None
	pix_list = []
	for y in range(len(test_image[0:-2])):
		for x in range(len(test_image[0][0:-2])):
			curr_pix = test_image[y][x]
			if y+1 < len(test_image):
				down_pix = test_image[y+1][x]
			# else:
			# 	down_pix = None
			if x+1 < len(test_image[y]):
				right_pix = test_image[y][x+1]
			# else:
			# 	right_pix = None
			# diff_down = abs(down_pix-curr_pix)
			# diff_right = abs(right_pix-curr_pix)
			diff_down = 0
			diff_right = 0
			for c in range(len(curr_pix)):

				diff_down += abs(down_pix[c] - curr_pix[c])
				diff_right += abs(right_pix[c] - curr_pix[c])


			if diff_right >= tolerance or diff_down >= tolerance:
				pix_list.append([x,y])
	# return find_contours(create_image(pix_list,height,width))
	return find_contours(pix_list)
	# return pix_list


def create_image(pix_list,height,width):
	"""
	Given a list of lists of coordinates, creates a numpy array of pixels that represent the detected edges of an image"
	"""
	# image = np.zeros((height,width))
	path = "temp.jpg"
	image = np.ones((height,width,1))
	image*=255
	# print image
	# image.fill([255,255,255])
	# image.fill([])

	# for y in range(len(image)):
		# for x in range(len(image[0])):
			# image[y][x] = [255,255,255]
			# np.append(image[y][x],[255,255,255])
			# np.put(image,[y,x],[255,255,255])

	# print image
	for pix in pix_list:
		y = pix[1]
		x = pix[0]

		image[x][y] = [0]
		# np.put(image,[y,x],[0,0,0])
	# print image
	cv2.imwrite( path, image);
	return path


def coord_dist(point1,point2):
	# print(point1,point2)

	x1 = float(point1[0])
	y1 = float(point1[1])
	x2 = float(point2[0])
	y2 = float(point2[1])
	
	dist = ((x2-x1)**2 + (y2-y1)**2)**(.5)
	# print dist
	return dist


def find_contours(points):
	contours = [[points[0]]]
	print "length original:"
	print len(points)
	# potential = []
	# for p in range(1:len(points)):
	# 	for x in points[p+1:]:
	# 		dist = coord_dist(points[p],x)
	# 		if dist < 2:
	# 			if x not in contours:


	for p in range(1,len(points)):
		for x in range(len(contours)):
			# for y in contours[x]:
				dist1 = coord_dist(points[p],contours[x][0])
				dist2 = coord_dist(points[p],contours[x][-1])
				if dist1<2 or dist2<2:

					# print "this gets called"
					if points[p] not in contours:
						# print "gets here"
						contours[x].append(points[p])
						# print contours[x]
				else:
					# print "ever fails"
					contours.append([points[p]])
	print "length final:"
	print len(contours[0])
	return contours




	# test_image = cv2.imread(image,0)
	# width = len(test_image[0])
	# height = len(test_image)
	# tolerance = 762 #amount of pixel variation allowed before edge is detected #762 for black and white

	# #keep track of the coordinates (x,y) of pixels where a dramatic change in coloration is detected
	# down_pix = None
	# right_pix = None
	# up_pix = None
	# left_pix = None
	# previous_pix = None
	# pix_list = []
	# for y in range(len(test_image[0:-2])):
	# 	for x in range(len(test_image[0][0:-2])):
	# 		curr_pix = test_image[y][x]
	# 		if y+1 < len(test_image):
	# 			down_pix = test_image[y+1][x]
	# 		# else:
	# 		# 	down_pix = None
	# 		if x+1 < len(test_image[y]):
	# 			right_pix = test_image[y][x+1]
	# 		# else:
	# 		# 	right_pix = None
	# 		# diff_down = abs(down_pix-curr_pix)
	# 		# diff_right = abs(right_pix-curr_pix)
	# 		diff_down = 0
	# 		diff_right = 0
	# 		for c in range(len(curr_pix)):

	# 			diff_down += abs(down_pix[c] - curr_pix[c])
	# 			diff_right += abs(right_pix[c] - curr_pix[c])


	# 		if diff_right >= tolerance or diff_down >= tolerance:
	# 			pix_list.append([x,y])


if __name__ == '__main__':
	res = edge_detector("./square_base.png")
	print res
	# test_image = cv2.imread("./square_base.png",-1)
	# cv2.namedWindow( "Display window") # Create a window for display.
	# cv2.namedWindow( "Display window 2") # Create a window for display.
	
	# cv2.imshow("Display window",res)
	# cv2.imshow("Display window 2",test_image)
	# cv2.waitKey(0)
