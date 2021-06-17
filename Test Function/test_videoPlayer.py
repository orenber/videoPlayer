from unittest import TestCase
from GUI.VideoPlayer import VideoPlayer
import os
from PIL import Image as pil
import cv2
from time import sleep


class TestVideoPlayer( TestCase ):

    def test__init__(self, **atr):
        self.vid = VideoPlayer( **atr )
        self.vid.update()
        sleep(1)

        return

    def setUp(self):
        images_path = os.path.abspath( os.path.join(os.pardir, 'Resources', 'images'))
        image_file = os.path.join(images_path, '301-F.jpg')
        self.image_test = pil.open(image_file)

    def test_image_size_camera(self):
        self.test__init__(image=True, play=True, camera=True, record=True )
        for res, value in self.vid.STD_DIMS.items():
            self.vid.image_size_camera = res
            self.assertEqual(self.vid.image_size_camera, value, "Error set image size:"+res)

    def test_image_size(self):

        self.test__init__(image=True)
        # read image
        self.vid.frame = self.image_test
        image_size = self.vid.image_size
        self.assertTupleEqual(self.image_test._size, image_size)
        pass

    def test_record(self):
        self.test__init__(play=True, record=True)
        self.vid.record = True
        self.assertFalse(self.vid.record)
        # open file
        movie_path = os.path.abspath(os.path.join(os.pardir, 'Resources', 'movies' ) )
        movie_file = os.path.join(movie_path, 'carplate30.mp4' )

        self.vid._record = True
        self.vid.play_movie(movie_file)
        self.assertFalse(self.vid.record)

        pass

    def test_command(self):
        self.fail()

    def test_algo(self):
        self.fail()

    def test_camera(self):
        self.test__init__( play=True, camera=True )
        self.vid.camera = True
        self.assertTrue(self.vid.camera)
        pass

    def test_frame(self):
        self.test_show_image()
        image = self.vid.frame
        assert isinstance(image, pil.Image)

        pass

    def test_set_setup(self):
        self.fail()

    def run_frame(self):
        self.fail()

    def test_load_movie(self):
        self.test__init__( play=True, pause=True, stop=True )

        self.vid.load_movie()
        pass

    def test_play_movie(self):
        self.test__init__( play=True, pause=True, stop=True )
        # open file
        movie_path = os.path.abspath( os.path.join( os.pardir, 'Resources', 'movies' ) )
        movie_file = os.path.join( movie_path, 'carplate30.mp4' )

        self.vid.play_movie( movie_file )

        pass

    def test_camera_capture(self):
        self.test__init__( play=True )

        self.vid.camera_capture()
        self.vid.close()

    def test_pause_player(self):
        self.fail()

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
        sleep(1)
        pass

    def test_matrix_to_pillow(self):
        self.fail()

    def test_command(self):
        #
        self.test__init__(camera=True, image=True)
        self.vid.command = lambda frame: extract_image(frame)

        images_path = os.path.abspath( os.path.join(os.pardir, 'Resources', 'images'))
        image_file = os.path.join(images_path, '301-F.jpg')
        image = pil.open(image_file)

        # call show image method
        self.vid.show_image( image )


def extract_image(matrix_image):
    cv2.imshow( 'frame', matrix_image )

