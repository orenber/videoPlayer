from unittest import TestCase
from Utility.image_procesing import *


class Test(TestCase):

    def test_resize_image_to_frame(self):
        image_size = (640, 480)
        frame_size = (640, 480)
        frame_same_size_as_image = resize_image_to_frame(image_size, frame_size)
        self.assertTupleEqual(frame_same_size_as_image, image_size, "Error :resize_image_to_frame")
        frame_bigger = (1280, 720)
        resize_enlarge = resize_image_to_frame(image_size, frame_bigger)
        self.assertTupleEqual(resize_enlarge, (960, 720), "Error :resize_image_to_frame frame>image")
        frame_smaller = (120, 160)
        resize_smaller = resize_image_to_frame(image_size, frame_smaller)
        self.assertTupleEqual(resize_smaller, (120, 90), "Error :resize_image_to smaller frame")



