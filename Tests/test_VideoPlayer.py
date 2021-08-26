from unittest import TestCase
from GUI.videoPlayer import VideoPlayer
import os
from PIL import Image
import cv2
from time import sleep
import tkinter
import numpy as np
import threading

import time


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
            self.assertTupleEqual(self.vid.image_size_camera, value, "Error set image size:"+res)

    def test_image_size(self):

        self.test__init__(image=True)
        # read image
        self.vid.frame = self.image_test
        image_size = self.vid.frame.size
        self.assertTupleEqual(self.image_test.size, image_size)
        pass

    def test_record(self):

        self.test__init__(play=True, record=True)
        self.vid.record = True
        self.assertFalse(self.vid.record)

        # open file
        self.vid._record = True
        self.vid.play_movie(self.move_test)
        self.assertTrue(self.vid.record)

        # play record
        movie_path = os.path.abspath(os.path.join(os.pardir, 'Test Function'))
        recorded_file = os.path.join(movie_path, 'output.avi')
        self.vid.play_movie(recorded_file)

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

    def test_load_movie(self):
        self.test__init__(play=True, pause=True, stop=True)

        self.vid.load_movie()
        #self.vid.after(5000, self.vid.destroy)
        pass

    def test_play_movie(self):
        self.test__init__(play=True, pause=True, stop=True)
        # open file
        self.vid.play_movie(self.move_test)

        pass

    def test_camera_capture(self):
        self.test__init__(play=True, camera=True)
        c = threading.Thread(target=lambda: self.close_window())
        t = threading.Thread(target=lambda: self.vid.camera_capture())
        t.start()
        c.start()
        c.join()
        t.join()

    def test_pause_player(self):
        self.test__init__(play=True, camera=True, pause=True)
        t = threading.Thread(target=lambda: self.assert_button_camera_press())
        c = threading.Thread(target=lambda: self.assert_button_pause_press())

        t.start()
        c.start()
        t.join()
        c.join(5)

    def assert_button_camera_press(self):
        self.assertRaises(tkinter.TclError, lambda: self.vid._camera_view())

    def assert_button_pause_press(self):
        self.assertRaises(tkinter.TclError, lambda: self.vid.pause_player())

    def test_stop_player(self):
        self.test__init__(play=True, stop=True)
        self.assertRaises( tkinter.TclError, lambda: self.vid.play_movie(self.move_test))
        self.vid.button_stop_video.after(15000, self.vid.stop_player)


        pass

    def test_camera_recording(self):
        self.test__init__(play=True, stop=True, record=True)
        self.button.re
        # open file
        self.assertRaises(tkinter.TclError, lambda: self.vid.play_movie(self.move_test))
        self.assertRaises(tkinter.TclError, lambda: self.vid._record_view())

    def test_save_frame(self):

        self.test__init__(image=True, play=False, stop=False, pause=False)
        self.vid.frame = np.array(self.image_test)
        self.vid.save_frame(self.vid.frame.image)

    def test_load_image(self):

        self.test__init__(image=True, play=False, stop=False, pause=False)
        self.assertRaises(tkinter.TclError, lambda: self.vid.load_image())

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

    def close_window(self):
        print('destroy')
        self.vid.destroy()



def extract_image(matrix_image):
    cv2.imshow('frame', matrix_image)
