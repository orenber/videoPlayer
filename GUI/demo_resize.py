import numpy as np        

# inputs

w_frame, h_frame = 640,480
image = np.zeros((700,480),np.float)
frame_ratio = h_frame/w_frame

self._image_ratio = self.image_ratio
h_image = self._cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
w_image = self._cap.get(cv2.CAP_PROP_FRAME_WIDTH)

if frame_ratio < self._image_ratio:

    h_ratio = h_frame/h_image
    h = h_frame*h_ratio
    w = w_frame*h_ratio
elif self._image_ratio == 0:
    pass
elif frame_ratio > self._image_ratio:

    w_ratio = w_frame / w_image
    h = h_frame * w_ratio
    w = w_frame * w_ratio

elif frame_ratio == self._image_ratio:

    p = frame_ratio / self._image_ratio
    h = p*h_image
    w = p*w_image

self._size = (int(w), int(h))