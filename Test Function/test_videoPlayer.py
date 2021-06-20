from unittest import TestCase
from GUI.VideoPlayer import VideoPlayer
import os
from PIL import Image
import cv2
from time import sleep
import tkinter
import numpy as np


class TestVideoPlayer(TestCase):

    def test__init__(self, **atr):
        self.vid = VideoPlayer(**atr)
        self.vid.update()
        sleep(1)

        return

    def setUp(self):
        images_path = os.path.abspath(os.path.join(os.pardir, 'Resources', 'images'))
        image_file = os.path.join(images_path, '301-F.jpg')
        self.image_test = Image.open(image_file)

        movie_path = os.path.abspath(os.path.join(os.pardir, 'Resources', 'movies'))
        movie_file = os.path.join(movie_path, 'carplate30.mp4')
        self.move_test = movie_file

    def test_image_size_camera(self):
        self.test__init__(image=True, play=True, camera=True, record=True)
        for res, value in self.vid.STD_DIMS.items():
            self.vid.image_size_camera = res
            self.assertTupleEqual(self.vid.image_size_camere, value, "Error set image size:"+res)

    def test_image_size(self):

        self.test__init__(image=True)
        # read image
        self.vid.frame = self.image_test
        image_size = self.vid.image_size()
        self.assertTupleEqual(self.image_test._size, image_size)
        pass

    def test_record(self):
        self.test__init__(play=True, record=True)
        self.vid.record = True
        self.assertFalse(self.vid.record)
        # open file
        self.vid._record = True
        self.vid.play_movie(self.move_test)
        self.assertFalse(self.vid.record)

        pass

    def test_algo(self):
        self.test__init__(algo=True)
        self.vid.command = lambda frame: extract_image(frame)

        # call show image method
        self.vid.show_image(self.image_test)
        self.vid._extract()
        self.assertTrue(self.vid.algo)

    def test_camera(self):
        self.test__init__(play=True, camera=True)
        self.vid.camera = True
        self.assertTrue(self.vid.camera)
        pass

    def test_frame(self):
        self.test__init__(play=True, image=True)
        self.vid.frame = self.image_test
        self.test_show_image()
        image = self.vid.frame
        self.assertEqual(image,  self.vid.frame, 'test_frame :images not equal')

        pass

    def test_set_setup(self):
        test_setup = {"play": True, "pause": True, "stop": True, "camera": False,
                      "record": False, "algo": False, "image": False}
        self.test__init__(**test_setup)
        self.assertDictEqual(self.vid.setup, test_setup)
        pass

    def run_frame(self):
        self.fail()

    def test_load_movie(self):
        self.test__init__(play=True, pause=True, stop=True)

        self.vid.load_movie()
        pass

    def test_play_movie(self):
        self.test__init__(play=True, pause=True, stop=True)
        # open file
        self.vid.play_movie(self.move_test)

        pass

    def test_camera_capture(self):
        self.test__init__(play=True)

        self.vid.camera_capture()
        self.vid.destroy()

    def test_pause_player(self):
        self.test__init__(play=True, camera=True, pause=True)
        self.assertRaises(tkinter.TclError, lambda: self.vid._camera_view())
        self.assertRaises(tkinter.TclError, lambda: self.vid.pause_player())

    def test_stop_player(self):
        self.fail()

    def test_camera_recording(self):
        self.fail()

    def test_save_frame(self):
        self.fail()

    def test_load_image(self):
        self.test__init__(image=True)

        self.vid.load_image()
        pass

    def test_show_image(self):
        self.test__init__(image=True)
        # read image
        # call show image method
        self.vid.show_image(self.image_test)
        pass

    def test_matrix_to_pillow(self):
        self.test__init__(image=True)
        matrix_image = np.array(self.image_test)
        pillow_image = self.vid.matrix_to_pillow(matrix_image)
        self.assertTrue(Image.isImageType(pillow_image))
        pass

    def test_command(self):
        #
        self.test__init__(algo=True)
        self.vid.command = lambda frame: extract_image(frame)

        # call show image method
        self.vid.show_image(self.image_test)
        self.vid._extract()

        self.vid.frame = self.image_test
        pass


def extract_image(matrix_image):
    cv2.imshow('frame', matrix_image)
