from unittest import TestCase
from PIL import Image
import numpy as np
from GUI.frameImg import FrameImg
import os


class TestFrameImg(TestCase):

    def setUp(self):

        images_path = os.path.abspath(os.path.join(os.pardir, 'Resources', 'images'))
        image_file = os.path.join(images_path, '301-F.jpg')
        self.image_test = Image.open(image_file)

        movie_path = os.path.abspath(os.path.join(os.pardir, 'Resources', 'movies'))
        movie_file = os.path.join(movie_path, 'kids_play.avi')
        self.move_test = movie_file

    def test__init__(self):
        self.frame = FrameImg(self.image_test)
        self.assertEquals(self.frame.image, self.image_test, "images are not the  same!")
        self.assertIsInstance(self.frame, FrameImg)

    def test_image(self):
        self.frame = FrameImg(np.zeros((400, 900), dtype=np.uint8))
        self.frame.image = self.image_test
        self.assertEquals(self.frame.image, self.image_test, "images are not the  same!")

    def test_size(self):

        self.frame = FrameImg(self.image_test)
        self.assertEqual(self.frame.size, self.image_test.size)

    def test_ratio(self):
        self.frame = FrameImg(self.image_test)
        width, height = self.image_test.size
        image_ratio = height/width
        self.assertEqual(self.frame.ratio,image_ratio)

    def test_width(self):
        self.frame = FrameImg(self.image_test)
        width, _ = self.image_test.size
        self.assertEqual(self.frame.width, width)

    def test_height(self):
        self.frame = FrameImg(self.image_test)
        _, height = self.image_test.size
        self.assertEqual(self.frame.height, height)
