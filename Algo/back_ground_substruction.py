import cv2 as cv
import numpy as np

cap = cv.VideoCapture(0)
fgbg = cv.createBackgroundSubtractorMOG2(detectShadows=True,history=100,varThreshold=40)
#fgbg = cv.createBackgroundSubtractorKNN(detectShadows=True)


while True:
    ret, frame = cap.read()
    if frame is None:
        break
    fgmask = fgbg.apply(frame)

    cv.imshow('Frame', frame)
    cv.imshow('FG MASK Frame', fgmask)

    keyboard = cv.waitKey(30)
    if keyboard == 'q' or keyboard == 27:
        break
cap.release()
cv.destroyAllWindows()
