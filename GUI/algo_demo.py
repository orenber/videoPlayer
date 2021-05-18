import numpy as np
import cv2
import os
import copy
from time import sleep
from skimage import morphology, measure, segmentation

# recording images 
 

#cap = cv2.VideoCapture(0)

#fourcc = cv2.VideoWriter_fourcc(*'XVID')
movie_filename = 'output.avi'
#out = cv2.VideoWriter(movie_filename, fourcc, 20.0, (640,480))

#while(cap.isOpened()):
#    ret, frame = cap.read()
#    if ret==True:

#        out.write(frame)

#        cv2.imshow('frame',frame)
#        if cv2.waitKey(1) & 0xFF == ord('q'):
#            break
#    else:
#        break
#cap.release()
#out.release()

#cv2.destroyAllWindows()


# show two images 
pri_frame = np.zeros((480,640,1), np.uint8)
cap = cv2.VideoCapture(movie_filename)
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        sub = cv2.absdiff(frame,pri_frame)

        (thresh, blackAndWhiteImage) = cv2.threshold(sub, 127, 255, cv2.THRESH_BINARY)
        cv2.imshow('frame',frame)
        pri_frame = frame 
       
       
        # noise filter
        image_clear = morphology.remove_small_objects(blackAndWhiteImage, min_size=500,connectivity=1)
        #plt.imshow(image_clear)
        
        cv2.imshow('sub',sub)
        cv2.imshow('binary',image_clear)
     
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
cap.release()

cv2.destroyAllWindows()


# convert two images to gray scale


# substruct one image from another 

# convert the product image to binary image 

# remove noise 


# determain the 































