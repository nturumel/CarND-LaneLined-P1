import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2
import open_cv_helper as ncv
from shapely.geometry import Point,Polygon

# step 1 read in image and convert to grayscale
filename = r"C:\Users\Nihar\Documents\CarND-LaneLines-P1\test_images\solidWhiteRight.jpg"
image=mpimg.imread(filename)
print("hello")
#plt.imshow(image)

#1. Convert to greyscale
grey=ncv.Grey(image)
#plt.imshow(grey)
cv2.imshow('grey',grey)

#2. smooth the image with a guassian blur
kernel_size=13
blur_grey=ncv.Gaussian(grey,kernel_size)
#plt.imshow(blur_grey)
cv2.imshow('blur_grey',blur_grey)

#3. canny to do edge detection
low=72
high=161
#edges=cv2.Canny(blur_grey, low,high)
edges=ncv.Canny(blur_grey,low,high)
#plt.imshow(edges)
cv2.imshow('edges',edges)

#4. create a mask for a region of interest simultaneously
mask=np.zeros_like(edges)

red=255
roi=np.array([[(0,540),(400,300),(520,300),(960,540)]],dtype=np.int32)
cv2.fillPoly(mask,roi,red)
#plt.imshow(mask)
cv2.imshow('mask',mask)

#5. create an image which only has the road markings and the edge obtained from canny
masked_edges=cv2.bitwise_and(edges,mask)
#plt.imshow(masked_edges)
cv2.imshow('masked_edges',masked_edges)
#6. do the hough transform on the masked_edges obtained
rho=2
theta=np.pi/180
threshold=30
min_line_length=2
max_line_gap=20
lines=ncv.Hough(masked_edges,rho,theta,threshold,min_line_length,max_line_gap)
line_image=np.copy(image)
for line in lines:
    for x1,y1,x2,y2 in line:
        cv2.line(line_image,(x1,y1),(x2,y2),(255,0,0),5)
#plt.imshow(line_image)
cv2.imshow('line_image',line_image)

#7. improving line drawing
xleft=[]
yleft=[]
xright=[]
yright=[]

coords=[(460,540),(460,300),(520,300),(960,540)]
poly=Polygon(coords)
yboth=np.linspace(540,350,num=4,endpoint=True)

for line in lines:
    for x1,y1,x2,y2 in line:
        #cv2.line(line_image,(x1,y1),(x2,y2),(255,0,0),10)
        p1=Point(x1,y1)
        if(p1.within(poly)):
            xright.append(x1)
            xright.append(x2)
            yright.append(y1)
            yright.append(y2)
        else:
            xleft.append(x1)
            xleft.append(x2)
            yleft.append(y1)
            yleft.append(y2)

xleft=np.asarray(xleft)
yleft=np.asarray(yleft)
zleft=np.polyfit(yleft,xleft,2)
pleft=np.poly1d(zleft);
xleft=pleft(yboth)


xright=np.asarray(xright)
yright=np.asarray(yright)
zright=np.polyfit(yright,xright,2)
pright=np.poly1d(zright);
xright=pright(yboth)

yboth=yboth.astype(int)
xleft=xleft.astype(int)
xright=xright.astype(int)

final_image=np.copy(image)
cv2.line(final_image,(xleft[0],yboth[0]),(xleft[1],yboth[1]),(255,0,0),5)
cv2.line(final_image,(xleft[1],yboth[1]),(xleft[2],yboth[2]),(255,0,0),5)
cv2.line(final_image,(xleft[2],yboth[2]),(xleft[3],yboth[3]),(255,0,0),5)

cv2.line(final_image,(xright[0],yboth[0]),(xright[1],yboth[1]),(255,0,0),5)
cv2.line(final_image,(xright[1],yboth[1]),(xright[2],yboth[2]),(255,0,0),5)
cv2.line(final_image,(xright[2],yboth[2]),(xright[3],yboth[3]),(255,0,0),5)

#plt.imshow(final_image)
cv2.imshow('final_image',final_image)

'''
final_image_2=np.copy(image)
npleft=np.array([xleft,yboth])
npleft=npleft.reshape((-1,1,2))

cv2.polylines(final_image_2,npleft,True,(255,0,0),thickness=5)
plt.imshow(final_image_2)
'''
#cv2.show()
cv2.waitKey(0)

plt.show()
