import cv2
import os

path = os.path.abspath(os.path.join(os.getcwd(), 'xml'))
full_body = os.path.join(path,"haarcascade_fullbody.xml")
body_cascade = cv2.CascadeClassifier(full_body)
# To capture video from webcam.
vid = cv2.cv2.VideoCapture(0, cv2.CAP_DSHOW)
vid.set(3,480)
vid.set(4,640)
while True:
    response , color_image = vid.read()
    if response == False:
        break
    grey_image = cv2.cvtColor(color_image , cv2.COLOR_BGR2GRAY)
    body = body_cascade.detectMultiScale(grey_image , 1.1 , 2)
    for (x , y, w , h) in body:
        cv2.rectangle(color_image , (x , y) , (x+w , y + h) , (0 , 255 , 255) , 2)
        cv2.imshow('Detector' , color_image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
       break
vid.release()
cv2.destroyAllWindows()




















