from unittest import TestCase
from GUI.VideoPlayer import VideoPlayer
import os
from PIL import Image as pil
import cv2


class TestVideoPlayer(TestCase):

    def test___init__(self,**atr):
        self.vid = VideoPlayer(**atr)
        self.vid.update()


        return


    def test_load_image(self):
        self.test___init__(image= True)

        self.vid.load_image()
        pass

    def test_show_image(self):
        self.test___init__( image=True)
        # read image
        images_path = os.path.abspath(os.path.join(os.pardir, 'Resources', 'images'))
        image_file = os.path.join(images_path, '301-F.jpg')
        image = pil.open(image_file)

        # call show image method
        self.vid.show_image(image)

        pass

    def test_frame(self):

        self.test_show_image()
        image = self.vid.frame
        assert isinstance( image, pil.Image)
        pass


    def test_camera_capture(self):

        self.test___init__(play=True)
        self.vid.camera_capture()


    def test_load_movie(self):
        self.test___init__( play=True, pause=True, stop=True )

        self.vid.load_movie()
        pass

    def test_play_movie(self):
        self.test___init__( play=True, pause=True, stop=True )
        # open file
        movie_path = os.path.abspath(os.path.join(os.pardir, 'Resources', 'movies'))
        movie_file = os.path.join(movie_path, 'carplate30.mp4')

        self.vid.play_movie(movie_file)
        pass

    def test_command(self):

        #
        self.test___init__(camera=True, image=True)
        self.vid.command = lambda frame: extract_image(frame)

        images_path = os.path.abspath( os.path.join( os.pardir, 'Resources', 'images' ) )
        image_file = os.path.join( images_path, '301-F.jpg' )
        image = pil.open( image_file )

        # call show image method
        self.vid.show_image( image )


def extract_image(matrix_image):


            cv2.imshow( 'frame', matrix_image )


