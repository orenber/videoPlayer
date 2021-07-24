import numpy as np
import cv2

from Utility.file_location import *
import pickle


images_face_path = full_file(["Resources", "images", "301-F.jpg"])
# Read the image
img = cv2.imread(images_face_path)
# initialize counter
i = 0
# Display the image
cv2.imshow( 'a', img )
while True:
    # Display the image

    # wait for keypress
    k = cv2.waitKey()
    # specify the font and draw the key using puttext
    font = cv2.FONT_HERSHEY_SIMPLEX
    text = chr(k)
    if text == '\b':
        print(k)
    print(text)
    cv2.putText(img, text, (140+i, 250), font, .5, (0, 210, 0), 2, cv2.LINE_AA)
    i += 10
    if k == ord('q'):
        break
cv2.destroyAllWindows()