import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2

def Canny(img,low,high):
    return(cv2.Canny(img, low,high))

def Gaussian(img,kernel_size):
    return cv2.GaussianBlur(img,(kernel_size,kernel_size),0)

def Grey(img):
    return cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

def Hough(img,rho,theta,threshold,min_line_length,max_line_gap):
    return cv2.HoughLinesP(img,rho,theta,threshold,np.array([]),min_line_length,max_line_gap)
