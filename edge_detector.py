import cv2
import numpy as np
import math
import sys
def edge_detector(image):
	"""
	Maybe detects edges using numpy.
	"""
	test_image = cv2.imread(image,-1)
	width = len(test_image[0])
	height = len(test_image)
	tolerance = 20 #amount of pixel variation allowed before edge is detected

	#keep track of the coordinates (x,y) of pixels where a dramatic change in coloration is detected
	down_pix = None
	right_pix = None
	pix_list = []
	for y in range(len(test_image[0:-2])):
		for x in range(len(test_image[0:-2])):
			curr_pix = test_image[y][x]
			if y+1 < len(test_image):
				down_pix = test_image[y+1][x]
			# else:
			# 	down_pix = None
			if x+1 < len(test_image[y]):
				right_pix = test_image[y][x+1]
			# else:
			# 	right_pix = None
			diff_down = 0
			diff_right = 0
			for c in range(len(curr_pix)):
				diff_down += abs(down_pix[c] - curr_pix[c])
				diff_right += abs(right_pix[c] - curr_pix[c])

			if diff_right >= tolerance or diff_down >= tolerance:
				pix_list.append([x,y])
	print pix_list





if __name__ == '__main__':
	edge_detector("./square_base.png")