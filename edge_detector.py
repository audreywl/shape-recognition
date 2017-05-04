import cv2
import numpy as np
import math
import sys
def edge_detector(image):
	"""
	Given an input image file path, detects and returns the coordinates of each pixel detected as an edge.
	"""
	test_image = cv2.imread(image,-1)
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

			if x+1 < len(test_image[y]):
				right_pix = test_image[y][x+1]

			diff_down = 0
			diff_right = 0
			for c in range(len(curr_pix)):
				diff_down += abs(down_pix[c] - curr_pix[c])
				diff_right += abs(right_pix[c] - curr_pix[c])


			if diff_right >= tolerance or diff_down >= tolerance:
				pix_list.append([x,y])
	return find_contours(pix_list)


def create_image(pix_list,height,width):
	"""
	Given a list of lists of coordinates along with a width and height, creates a numpy array of pixels that represent the detected edges of an image"
	"""
	path = "temp.jpg"
	image = np.ones((height,width,1))
	image*=255
	for pix in pix_list:
		y = pix[1]
		x = pix[0]

		image[x][y] = [0]
	cv2.imwrite( path, image);
	return path


def coord_dist(point1,point2):
	"""
	Helper function for find_contours() designed to find the distance between two points
	Takes in two lists containing the x,y values for two points
	Returns the distance between the two points as a float
	"""

	x1 = float(point1[0])
	y1 = float(point1[1])
	x2 = float(point2[0])
	y2 = float(point2[1])
	
	dist = ((x2-x1)**2 + (y2-y1)**2)**(.5)
	return dist

#Unused
def find_contours(points):
	"""
	Program that takes in a numpy array of numpy arrays and determines which are close enough to be considered part of the same contour.
	Returns a list of lists containing coordinates along contours.
	"""
	contours = [[points[0]]]


	for p in range(1,len(points)):
		for x in range(len(contours)):
				dist1 = coord_dist(points[p],contours[x][0])
				dist2 = coord_dist(points[p],contours[x][-1])
				if dist1<2 or dist2<2:
					if points[p] not in contours:
						contours[x].append(points[p])
				else:
					contours.append([points[p]])
	return contours


if __name__ == '__main__':
	res = edge_detector("./square_base.png")
	print res
	# test_image = cv2.imread("./square_base.png",-1)
	# cv2.namedWindow( "Display window") # Create a window for display.
	# cv2.namedWindow( "Display window 2") # Create a window for display.
	
	# cv2.imshow("Display window",res)
	# cv2.imshow("Display window 2",test_image)
	# cv2.waitKey(0)
