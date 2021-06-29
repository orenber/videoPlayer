import numpy as np
from PIL import Image


class FrameImg(object):

    def __init__(self, image):

        self._width = 640
        self._height = 480
        self._size = (self._width, self._height)
        self._image = np.zeros(self._size, float)

        self._ratio = self._height/self._width
        self._type = "RGB"
        self.image = image

    @property
    def image(self) -> np.array:
        return self._image

    @property
    def size(self) -> tuple:

        return self._size

    @property
    def ratio(self) -> float:

        return self._ratio

    @property
    def width(self) -> float:

        return self._width

    @property
    def height(self) -> float:

        return self._height

    @image.setter
    def image(self, image):

        if isinstance(image, np.ndarray):
            self._image = image
            self._size = (image.shape[1], image.shape[0])

        elif Image.isImageType(image):
            self._image = image
            self._size = (image.size[0], image.size[1])

        else:
            raise TypeError("Only image are allowed")
        self._width, self._height, *_ = self._size
        self._ratio = self._height/self._width
