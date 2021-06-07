import numpy as np
import cv2
import os
import copy
from time import sleep
from skimage import morphology, measure, segmentation

# recording images 
 
pri_frame = np.zeros((480,640,1), np.uint8)
cap = cv2.VideoCapture(0)

fourcc = cv2.VideoWriter_fourcc(*'XVID')
movie_filename = 'output.avi'
out = cv2.VideoWriter(movie_filename, fourcc, 24.0, (640,480),0)
record  = False
frame_take = 0
while(cap.isOpened()):
    ret, frame_rgb = cap.read()
    if ret==True:

        # convert two images to gray scale
        frame = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2GRAY)

        # subtract one image from another
        sub = cv2.absdiff(frame, pri_frame )

        # convert the product image to binary image
        (thresh, blackAndWhiteImage) = cv2.threshold(sub, 30, 255, cv2.THRESH_BINARY)

        # save the last frame
        pri_frame = frame

        # label image
        label_image = morphology.label(blackAndWhiteImage)

        # remove noise
        image_clear = morphology.remove_small_objects(label_image, min_size=100, connectivity=1)

        # check how much blob thar is in the image
        cc = measure.regionprops(image_clear)

        # in the case thar is blob above the threshold ->  trigger record function
        if len(cc)>1 and frame_take<150:

          print(frame_take)
          record  = True
          frame_take += 5

        if frame_take>0:
            out.write(frame)
            frame_take -= 1
            cv2.imshow('record',frame)

        # return to binary image
        binary_image = image_clear.astype(np.float)


        # Output
        cv2.imshow( 'sub', sub )

        cv2.imshow( 'binary', binary_image )

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































