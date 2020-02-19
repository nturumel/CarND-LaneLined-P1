# **Finding Lane Lines on the Road** 

[image1]: ./write_up_images/grey.jpg 
[image2]: ./write_up_images/blur_grey.jpg  
[image3]: ./write_up_images/edges.jpg  
[image4]: ./write_up_images/masked_image.jpg  
[image5]: ./write_up_images/hough_line.jpg  
[image6]: ./write_up_images/final.jpg  


---

### Reflection

### 1. Describe your pipeline. As part of the description, explain how you modified the draw_lines() function.

My Pipeline consists of 6 steps:
1. Read input image and convert to greyscale:
I used the command cv2.cvtColor(img,cv2.COLOR_BGR2GRAY), converting to greyscale helps reduce the noise.
![alt text][image1]

2. Blur the image to reduce noise:
I reduced the noise of the image by using cv2.GaussianBlur(img,(kernel_size,kernel_size),0).
![alt text][image2]

3. Use canny edge detection to demarket the edges in the image
I used edges=ncv.Canny(blur_grey,low,high)
![alt text][image3]

4. Create a region of interest:
I created a roi for working on lan detection, you start with a blank np array and then use cv fill poly to mark an edge with a color, then perform a & operation with your canny, to get canny for roi
![alt text][image4]

5. Perform Hough Transform:
Perform the hough transform using cv2.HoughLinesP(img,rho,theta,threshold,np.array([]),min_line_length,max_line_gap)
and then draw the lines obtained over your image
![alt text][image5]

6. Improve Line drwaing:
The lines obtained by hough are not solid, in order to draw solid lines, forst seperate left lines and right lines, I tried the following approaches
1. Using the slope of the lines, -ve being righ lane and +ve the left, this appraoch did not work well, possibly being due to the fact the slope is very small and some left and right lines got mixed
2. Divide your roi into two parts, this approach worked better but is cruse, also the lines I got were shaky

Once you get the lines, run it through a polyfit method, and then get your x, y points for plotting.
I used order one polyfit as it worked best for me.
Also since I could not get cv.polyline to work, I had to stick with 4 points. The y coordinates were 300 and 540, the extremes of my roi.
![alt text][image6]

7. Extra work: I mproved a gui tool for tuning parameters to incorporate Hough lines. This enabled me to get the best possible parameters.

### 2. Identify potential shortcomings with your current pipeline
 The potential shortcomings are:
 1. I cannot identify curves properly as I am using an order one polyfit.
 2. I have very few points in my final lane draw lines.
 3. My roi is static, it should be more dynamic.
 


### 3. Suggest possible improvements to your pipeline

Use a better method to sperate lane lines from Hough and use a higher order approximation for polyfit