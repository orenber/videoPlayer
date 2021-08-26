import cv2
import os
import time
import numpy as np
import multiprocessing

# segment path

path = os.path.dirname(cv2.__file__)
face_frontal = os.path.join(path,'data','haarcascade_frontalface_default.xml')
upper_body = os.path.join(path,'data',"haarcascade_upperbody.xml")
# cascade classifier
face_cascade = cv2.CascadeClassifier(face_frontal)
body_cascade = cv2.CascadeClassifier(upper_body)
#
# To capture video from webcam.
cap = cv2.VideoCapture(0)
# To use a video file as input
# cap = cv2.VideoCapture('filename.mp4')
color_image = np.zeros((480,640,3),  dtype=np.double)

def body_detection( gray_image, color_image):
    body = body_cascade.detectMultiScale(gray_image , 1.1 , 2)
    for (x , y, w , h) in body:
        cv2.rectangle(color_image , (x , y) , (x+w , y + h) , (0 , 255 , 255) , 2)


def face_detection(gray_image, color_image):
    # Detect the faces
    faces = face_cascade.detectMultiScale(gray_image, 1.1, 4)
    # Draw the rectangle around each face
    for (x, y, w, h) in faces:
        cv2.rectangle(color_image, (x, y), (x+w, y+h), (255, 0, 0), 2)


# pass in thread function 
algo_thread  = []


while True:
    # Read the frame
    _, color_image = cap.read()
    # Convert to grayscale
    gray = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)
    start = time.perf_counter()
    # detect body 
    # image_body_face = body_detection(gray,image_body_face)
    # detect face 
    # image_body_face = face_detection(gray,image_body_face)
    
    t  = multiprocessing.Process(target = body_detection, args = (gray,color_image,))
    t2 = multiprocessing.Process(target = face_detection, args = (gray,color_image,))
   
    algo_thread.append(t)
    algo_thread.append(t2)
    t.start()
    t2.start()
    
    for n in range(0,len(algo_thread)):
        algo_thread[n].join()
    # display image 
    cv2.imshow("body&face",color_image)
    finish = time.perf_counter()
    print('Finished in ', {round(finish - start,2)} ,'seconds(s)')
    # Stop if escape key is pressed
    k = cv2.waitKey(30) & 0xff
    if k==27:
        break
# Release the VideoCapture object
cap.release()



















