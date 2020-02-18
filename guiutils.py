import cv2
import numpy as np

class EdgeFinder:
    def __init__(self, image, filter_size=1, threshold1=0, threshold2=0,hough_rho=1,hough_theta=1,hough_threshold=1,hough_min_line_length=1,hough_max_line_gap=1 ):
        self.image = image
        self._filter_size = filter_size
        self._threshold1 = threshold1
        self._threshold2 = threshold2
        self._hough_rho=hough_rho
        self._hough_theta=hough_theta
        self._hough_threshold=hough_threshold
        self._hough_min_line_length=hough_min_line_length
        self._hough_max_line_gap=hough_max_line_gap

        def onchangeThreshold1(pos):
            self._threshold1 = pos
            self._render()

        def onchangeThreshold2(pos):
            self._threshold2 = pos
            self._render()

        def onchangeFilterSize(pos):
            self._filter_size = pos
            self._filter_size += (self._filter_size + 1) % 2
            self._render()

        def onchangeHough_rho(pos):
            self._hough_rho=pos
            self._render()

        def onchangeHough_theta(pos):
            self._hough_theta=pos
            self._render()

        def onchangeHough_threshold(pos):
            self._hough_threshold=pos
            self._render()

        def onchangeHough_min_line_length(pos):
            self._hough_min_line_length=pos
            self._render()

        def onchangeHough_max_line_gap(pos):
            self._hough_max_line_gap=pos
            self._render()



        cv2.namedWindow('edges')

        cv2.createTrackbar('threshold1', 'edges', self._threshold1, 255, onchangeThreshold1)
        cv2.createTrackbar('threshold2', 'edges', self._threshold2, 255, onchangeThreshold2)
        cv2.createTrackbar('filter_size', 'edges', self._filter_size, 20, onchangeFilterSize)
        cv2.createTrackbar('Hough_rho', 'edges', self._hough_rho, 180, onchangeHough_rho)
        cv2.createTrackbar('Hough_theta', 'edges',self._hough_theta, 255, onchangeHough_theta)
        cv2.createTrackbar('Hough_threshold', 'edges',self._hough_threshold, 255, onchangeHough_threshold)
        cv2.createTrackbar('Hough_min_line_length', 'edges',self._hough_min_line_length, 255, onchangeHough_min_line_length)
        cv2.createTrackbar('Hough_max_line_gap', 'edges',self._hough_max_line_gap, 255, onchangeHough_max_line_gap)


        self._render()

        print ("Adjust the parameters as desired.  Hit any key to close.")

        cv2.waitKey(0)

        cv2.destroyWindow('edges')
        cv2.destroyWindow('smoothed')

    def threshold1(self):
        return self._threshold1

    def threshold2(self):
        return self._threshold2

    def filterSize(self):
        return self._filter_size

    def edgeImage(self):
        return self._edge_img

    def smoothedImage(self):
        return self._smoothed_img

    def houghImage(self):
        return self._hough_image

    def houghRho(self):
        return self._hough_rho

    def houghTheta(self):
        return self._hough_theta*(np.pi/180)

    def houghThreshold(self):
        return self._hough_threshold

    def houghMinLineLength(self):
        return self._hough_min_line_length

    def houghMaxLineGap(self):
        return self._hough_max_line_gap


    def _render(self):
        self._smoothed_img = cv2.GaussianBlur(self.image, (self._filter_size, self._filter_size), sigmaX=0, sigmaY=0)
        self._edge_img = cv2.Canny(self._smoothed_img, self._threshold1, self._threshold2)
        lines = cv2.HoughLinesP(self._edge_img,self._hough_rho,self._hough_theta*(np.pi/180),self._hough_threshold,np.array([]),self._hough_min_line_length,self._hough_max_line_gap)
        self._hough_image=np.copy(self.image)
        for line in lines:
            for x1,y1,x2,y2 in line:
                cv2.line(self._hough_image,(x1,y1),(x2,y2),(255,0,0),2)


        cv2.imshow('smoothed', self._smoothed_img)
        cv2.imshow('canny', self._edge_img)
        cv2.imshow('hough',self._hough_image)
