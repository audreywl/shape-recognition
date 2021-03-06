#!/usr/bin/env python

import cv2
import numpy as np
import math
import sys
from edge_detector import edge_detector


def distance(endpoints, point): 
    """
    Takes in the endpoints of a line as a list of lists and a point as a list of x,y coordinates.
    Returns the distance between the line and the point as a float
    """
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

def dp(M, epsilon):
    """
    A recursive implementation of the Rieker Douglas Peuker algorithm
    Takes an array M containing the points the algorithm should analyze and streamline along with the epsilon, which is the tolerance for cutting off points.
    Returns a new array of points that have been reduced to their most important values.
    ie: if there are points along the same line, only the beginning and end points of the line will be kept.
    """
    dmax = 0.0
    index = -1

    for i in xrange(1, M.shape[0]):
        d = distance((M[0],M[-1]),M[i])

        if d > dmax:
            index = i
            dmax = d

    if dmax > epsilon:
        r1 = dp(M[:index + 1], epsilon)
        r2 = dp(M[index:], epsilon)

        return np.vstack((r1[:-1], r2))
    else:
        return np.vstack((M[0], M[-1]))

def shape_trainer(trainImage):
    """
    Diagnostic function responsible for figuring out the number of key points in a given shape. This is designed to be used in tandem with the shape_recognizer
    function.
    Takes in the path to an image
    Returns the number of key points in each contour of the image as a list
    """
    minVal = 50
    maxVal = 87
    test_image = cv2.imread(trainImage,-1)
    edge_detected = cv2.Canny(test_image,minVal,maxVal)
    #where the code differs if we could use our self-designed functions
    # edge_path = edge_detector(trainImage)
    # edge_detected = cv2.imread(edge_path,0)
    if cv2.__version__.startswith('3.'):
         _, contours, contour_hierarchy  = cv2.findContours(edge_detected, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    else:
        contours, contour_hierarchy  = cv2.findContours(edge_detected, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contour_image = cv2.drawContours(test_image, contours, -1, (0,255,0), 3)
    res = []
    vals = []
    for i in range(len(contours)):
        temp = dp(contours[i], 5)
        for i in range(0,len(temp)-1,2):
            cv2.line(test_image, (temp[i][0],temp[i][1]),(temp[i+1][0], temp[i+1][1]), (0,0,255), 5)
            cv2.imshow('video_window', test_image)
            cv2.waitKey(0)
        
        res.append(len(temp))
        
    return res


if __name__ == '__main__':
    sys.setrecursionlimit(2000)
    # print shape_trainer("./circle_base.png")
    # print shape_trainer("./multi_image.png")
    print shape_trainer("./square_base.png") #works best at 177.9
    # print shape_trainer("./squares_base.png")
    # print shape_trainer("./pentagon_base.png")

    """
    Brief Estimate: 
    - circle: 42 (only tested once)
    - square: 5 (consistent)
    - triangle: 7(only tested once)
    """