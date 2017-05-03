#!/usr/bin/env python

# import rospy
# from sensor_msgs.msg import Image
# from cv_bridge import CvBridge
import cv2
import numpy as np
import math
import sys



# def distance(endpoints, point):
#     """
#     Computes the perpendicular distance between a point and a line defined by two endpoints.
#     Accepts a tuple of lists depicting x and y coordinates for the endpoints parameter and a list
#     containing the x and y coordinates of the desired point to compare to the line.
#     """
#     P1 = endpoints[0][0]
#     P2 = endpoints[1][0]
#     y0 = point[1]
#     x0 = point[0]
#     y1 = P1[1]
#     x1 = P1[0]
#     y2 = P2[1]
#     x2 = P2[0]

#     dist = abs((y2-y1)*x0-(x2-x1)*y0+x2*y1-y2*x1)/math.sqrt((y2-y1)**(2)+(x2-x1)**(2)) 
#     return dist

def distance(endpoints, point): # x3,y3 is the point
    
    P1 = endpoints[0][0]
    P2 = endpoints[1][0]
    y3 = point[1]
    x3 = point[0]
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

    # Note: If the actual distance does not matter,
    # if you only want to compare what this function
    # returns to other results of this function, you
    # can just return the squared distance instead
    # (i.e. remove the sqrt) to gain a little performance

    dist = math.sqrt(dx*dx + dy*dy)

    return dist

def dp(point_list, epsilon):
    max_distance = 0
    # print len(point_list)
    furthest_point = None
    result_list = []
    for i in range(len(point_list[1:-1])):
        # print i[0][0]
        #print(i,len(point_list))
        # print i
        # print point_list[0][0]
        # print point_list[-1][0]
        # print point_list[i][0]
        #print point_list[i]
        dist = distance((point_list[0],point_list[-1]), point_list[i][0])
        if dist < max_distance:
            print dist

        if dist>max_distance: #try adding a 'fudge factor' extra value to be sure its worth splitting for
            max_distance = dist
            furthest_point = i 
    #print point_list[0],point_list[-1]
    print point_list[furthest_point][0]
    #print 'max_distance', max_distance
    if max_distance > epsilon:
        new_line_1 = point_list[0:i+1]
        new_line_2 = point_list[i:]
        print 'split'
        result_list.extend(dp(new_line_1, epsilon))
        result_list.extend(dp(new_line_2, epsilon))
        return result_list
        # print result_list_1
        # print result_list_2

    else:
        # print point_list[0], point_list[-1]
        # result_list.append((point_list[0][0]))
        # result_list.append(point_list[-1][0])
        
        # print result_list
        # return result_list
        print 'end'
        print 'endpoints', point_list[0],point_list[-1]
        print furthest_point
        #print 'furthest point', point_list[furthest_point][0]
        print 'max_distance', max_distance
        return [point_list[0][0]]
        

        # if result_list_1 != None:
        #     # print "hey"
        #     # thing = result_list_1[0].append(result_list_2[0])
        #     thing = [np.append(result_list_1[0],result_list_2[0])]
            
        #     # print thing
        #     #print 'split', new_line_1, new_line_2
        #     return thing
        # else:
        #     print "listen"
        #     return result_list_2


def shape_trainer(trainImage):
    minVal = 50
    maxVal = 87
    test_image = cv2.imread(trainImage,-1)
    # test_image = cv2.medianBlur(test_image,5)
    edge_detected = cv2.Canny(test_image,minVal,maxVal)
    if cv2.__version__.startswith('3.'):
         _, contours, contour_hierarchy  = cv2.findContours(edge_detected, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    else:
        contours, contour_hierarchy  = cv2.findContours(edge_detected, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contour_image = cv2.drawContours(test_image, contours, -1, (0,255,0), 3)
    # print contour_image
    # print contours
    # print edge_detected
    #cv2.imshow('video_window', test_image)
    
    # cv2.imshow('video_window2', edge_detected)
    # cv2.imshow('video_window3', contour_image)
    res = []
    vals = []
    # print contours[0]
    #print len(contours)
    for i in range(len(contours)):
        #print contours
        temp = dp(contours[i], 5)
        #print type(temp)
        #print type(temp[0])
        #print temp
        for i in range(0,len(temp)-1,2):
            #print len(temp[0])
            #print i
            #print temp[i]
            cv2.line(test_image, (temp[i][0],temp[i][1]),(temp[i+1][0], temp[i+1][1]), (0,0,255), 5)
            cv2.imshow('video_window', test_image)
            cv2.waitKey(0)
        # if temp:
        # print len(temp[0])
        # res.append(temp)
        print temp[0]
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
    print shape_trainer("./square_base.png") #works best at 177.9
    #print shape_trainer("./squares_base.png")
    # print shape_trainer("./pentagon_base.png")