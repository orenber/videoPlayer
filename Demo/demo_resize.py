import numpy as np        
import cv2

# inputs

# frame inputs
w_frame, h_frame = 350,160
frame_ratio = h_frame/w_frame

# image_inputs
image = np.zeros((700, 480), np.float)
w_image, h_image = image.shape
image_ratio = h_image/w_image


if frame_ratio < image_ratio:

    h_ratio = h_frame/h_image
    h = h_image*h_ratio
    w = w_image*h_ratio

elif frame_ratio > image_ratio:

    w_ratio = w_frame / w_image
    h = h_image * w_ratio
    w = w_image * w_ratio

elif frame_ratio == image_ratio:

    p = w_frame / w_image
    h = p*h_image
    w = p*w_image

new_image_size = (int(w), int(h))

print(new_image_size)