import numpy as np
import cv2

from Utility.file_location import *
import pickle

# segment cv2 path
path = os.path.dirname(cv2.__file__)
face_frontal_path = os.path.join(path, 'data', 'haarcascade_frontalface_default.xml')
face_cascade = cv2.CascadeClassifier(face_frontal_path)
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainner.yml")

images_face_path = full_file(["Resources", "images", "faces"])

labels = {"person_name": 1}
font = cv2.FONT_HERSHEY_SIMPLEX
stroke = 2
color = (255, 255, 255)

with open("labels.pickle", 'rb') as f:
    og_labels = pickle.load(f)
    labels = {v: k for k, v in og_labels.items()}

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

        # detect ROI face
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

        # recognizer deep learned model predict keras tensorflow pytorch scikit learn
        id_, conf = recognizer.predict(roi_gray)

        if conf >= 47:

           name = labels[id_]
           cv2.putText(frame, name, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, color, stroke, cv2.LINE_AA)

        # crop the region of intrest ( faces in the images)
        # cv2.imwrite(file_date(images_face_path, '.png'), roi_gray)
        # take the roi corrdinet x and y
           points_start = (x, y)
           points_end = (x+w, y+h)
        # draw rectangle around the faces
           cv2.rectangle(frame, points_start, points_end, (255, 0, 0), 3)

    # display image and plot
    cv2.imshow('frame', frame)
    # press quite to Exit the loop
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

# when everything done , realse the capture

cap.release()
cv2.destroyAllWindows()

