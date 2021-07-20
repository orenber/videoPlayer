import numpy as np
import cv2
import os
from Utility.file_location import *

# segment cv2 path
path = os.path.dirname(cv2.__file__)
face_frontal_path = os.path.join(path, 'data', 'haarcascade_frontalface_default.xml')
face_cascade = cv2.CascadeClassifier(face_frontal_path)
images_face_path = full_file(["Resources", "images", "faces", "face"])


cap = cv2.VideoCapture(0)

while(True):

    # capture frame by frame
    ret, frame = cap.read()
    # convert BGR image to gray
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # detect faces in the image
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
    # go over all the face and plot the rectangle around
    for(x, y, w, h) in faces:

        print(x, y, w, h)
        # detect ROI face
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        # crop the region of intrest ( faces in the images)
        cv2.imwrite(file_date(images_face_path, '.png'), roi_gray)
        # take the roi corrdinet x and y
        points_start = (x, y)
        points_end = (x+w, y+h)
        # draw rectangle around the faces
        cv2.rectangle(frame, points_start, points_end, (255,0,0), 3)



    # display image and plot
    cv2.imshow('frame', frame)
    # press quite to Exit the loop
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

# when everything done , realse the capture

cap.release()
cv2.destroyAllWindows()

