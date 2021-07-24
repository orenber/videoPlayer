import cv2
cam = cv2.VideoCapture(0)
w = cam.get(cv2.CV_CAP_PROP_FRAME_WIDTH)
h = cam.get(cv2.CV_CAP_PROP_FRAME_HEIGHT)
print (w,h)
while cam.isOpened():
    err,img = cam.read()
    cv2.imshow("lalala", img)
    k = cv2.waitKey(10) & 0xff
    if k==27:
        break