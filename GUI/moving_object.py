import numpy as np
import cv2
import os
import copy
from time import sleep
from matplotlib import pyplot as plt
from skimage import morphology, measure, segmentation, io
# recording images   
pri_frame = np.zeros(( 480,640,1), np.uint8)
cap = cv2.VideoCapture(0)

fourcc = cv2.VideoWriter_fourcc(*'XVID')
movie_filename = 'output.avi'
out = cv2.VideoWriter(movie_filename, fourcc, 24.0, (480,640))

while(cap.isOpened()):
    ret, frame_rgb = cap.read()
    if ret==True:

        # convert two images to gray scale
        frame = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2GRAY)

        # remove nuice from to image 
        gausian_blurr = cv2.GaussianBlur(frame,(3,3),0)

        # subtract one image from another
        sub = cv2.absdiff(gausian_blurr, pri_frame )

        # convert the product image to binary image
        (thresh, blackAndWhiteImage) = cv2.threshold(sub, 30, 255, cv2.THRESH_BINARY)
        
        # make all pixels < threshold black
        #binarized = 1.0 * (blackAndWhiteImage > thresh)
        # save the last frame
        pri_frame = gausian_blurr
         
        # label image
        # Setup SimpleBlobDetector parameters.

        #noise2_label = morphology.label(binarized)
        #cc = measure.regionprops(noise2_label)

        #image_clear = morphology.remove_small_objects(noise2_label, min_size=200, connectivity=1,in_place=True)
       
        # check the number of blob in the image
        #number_objects1 = len(cc)
        #if number_objects1>27:
         
        #    area = max([n.area for n in cc])
        #   if area>3000:
        #    print(area)
            

        # remove noise
        # image_clear = morphology.remove_small_objects(noise2_label, min_size=200, connectivity=1)
        
        ### check the cuture of the binary image 
        ##contours ,_ = cv2.findContours(blackAndWhiteImage, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
     
   
        ##if len(contours) != 0:
        ###    # the contours are drawn here
        ##    cv2.drawContours(frame_rgb, contours, -1,(255, 0, 0), 3)

 
        # Output
        #cv2.imshow( 'sub', sub )
        cv2.imshow('blackandwhite',blackAndWhiteImage)
 

        cv2.imshow( 'frame', frame_rgb )


#        out.write(frame)
#
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
cap.release()
out.release()

cv2.destroyAllWindows()


# show two images 
# cap = cv2.VideoCapture(movie_filename)
# while(cap.isOpened()):
#     ret, frame = cap.read()
#     if ret==True:
#         frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
#         sub = cv2.absdiff(frame,pri_frame)
#
#         (thresh, blackAndWhiteImage) = cv2.threshold(sub, 127, 255, cv2.THRESH_BINARY)
#         cv2.imshow('frame',frame)
#         pri_frame = frame
#
#         # noise filter
#         image_clear = morphology.remove_small_objects(blackAndWhiteImage, min_size=500, connectivity=1)
#         #plt.imshow(image_clear)
#
#         cv2.imshow('sub',sub)
#         cv2.imshow('binary',image_clear)
#
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#     else:
#         break
# cap.release()
#
# cv2.destroyAllWindows()












# determain the 































