from unittest import TestCase
import os
from PIL import Image
from GUI.surveillance import Surveillance


class TestSurveillance( TestCase ):

    def test__init__(self):
        self.vid = Surveillance()
        self.vid.update()
        pass

    def setUp(self) -> None:
        images_path = os.path.abspath( os.path.join( os.pardir, 'Resources', 'images' ) )
        image_file = os.path.join( images_path, '301-F.jpg' )
        self.image_test = Image.open( image_file )

        movie_path = os.path.abspath( os.path.join( os.pardir, 'Resources', 'movies' ) )
        movie_file = os.path.join( movie_path, 'kids_play.avi' )
        self.move_test = movie_file

    def test_algo_list(self):
        self.test__init__()
        test_list = [self.vid.profile_detection, self.vid.face_detection, self.vid.movement_detection]
        for i, fun in enumerate( test_list ):
            self.vid.algo_list( True, fun )
            self.assertListEqual( self.vid.algo_stack[:i], test_list[:i],
                                  "Error: List methods are not the same" )

        for i, fun in enumerate( test_list ):
            self.vid.algo_list( False, fun )
            self.assertListEqual( self.vid.algo_stack[:], test_list[i + 1:],
                                  "Error: List methods are not the same" )

    def test_movement_detection(self):
        self.test__init__()
        # push on the button
        self.vid._button_movement_detection_view()
        # load move
        # open file
        self.vid.play_movie( self.move_test )

    def test_face_detection(self):
        self.test__init__()
        # push on the button
        self.vid._button_face_detection_view()
        # load move
        # open file
        self.vid.play_movie( self.move_test )

    def test__build_widget(self):
        self.fail()

    def test__focus_label(self):
        self.fail()

    def test__button_movement_detection_view(self):
        self.fail()

    def test__button_face_detection_view(self):
        self.fail()

    def test__button_face_recognition_view(self):
        self.fail()

    def test__pause_view(self):
        self.fail()

    def test_lable_image(self):
        self.fail()

    def test_run_frames(self):
        self.fail()

    def test_face_recognition(self):
        self.fail()

    def test_record_movement(self):
        self.fail()

    def test_save_frame(self):
        self.fail()
