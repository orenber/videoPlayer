from unittest import TestCase
from GUI.videoPlayer import VideoPlayer
import os
from PIL import Image
import cv2
from time import sleep
import tkinter
import numpy as np
import threading


class TestVideoPlayer( TestCase ):

    def test__init__(self, **atr):
        self.vid = VideoPlayer( **atr )
        self.vid.update()
        return

    def setUp(self):
        images_path = os.path.abspath( os.path.join( os.pardir, 'Resources', 'images' ) )
        self.image_file = os.path.join( images_path, '301-F.jpg' )
        self.image_test = Image.open(  self.image_file )

        movie_path = os.path.abspath( os.path.join( os.pardir, 'Resources', 'movies' ) )
        movie_file = os.path.join( movie_path, 'carplate30.mp4' )
        self.move_test = movie_file

    def test_frame_rate(self):
        self.test__init__( play=True, camera=True, record=True )
        print(self.vid.frame_rate)
        self.vid.frame_rate = 30
        self.assertEqual(self.vid.frame_rate,30,"frame rate did not change")

    def test_file_name_record(self):
        self.test__init__( play=True, camera=True, record=True )
        self.file_name = "test_file_name_record"
        self.vid.file_name_record = self.file_name
        self.assertEqual(self.vid.file_name_record , self.file_name , "file name  did not change")

    def test_size(self):
        self.test__init__(play=True, camera=True, record=True )
        self.assertEqual(self.vid.size, self.vid.STD_DIMS.get('0.3MP'),
                         "image size is not :"+str(self.vid.STD_DIMS.get('0.3MP')))

    def test_image_size_camera(self):
        self.test__init__( image=True, play=True, camera=True, record=True )
        for res, value in self.vid.STD_DIMS.items():
            self.vid.image_size_camera = res
            self.assertTupleEqual( self.vid.image_size_camera, value, "Error set image size:" + res )

    def test_play(self):

        self.test__init__( play=True, pause=True, stope=True )
        self.assertFalse(self.vid.play,"play wrong state = True ")
        self.vid.button_play_video.after(2500,
                                         lambda: self.assertTrue( self.vid.play, "play wrong state = False") )
        # play video
        self.vid.play_movie(self.move_test)
        self.assertFalse( self.vid.play,"play wrong state = True")

    def test_record(self):

        self.test__init__( play=True,record = True, pause=True, stope=True )
        self.assertFalse(self.vid.record, "record wrong state = True " )
        self.vid.button_record.after(1000,lambda:  self.recording(True))
        self.vid.button_record.after(1500,lambda: self.assertTrue(self.vid.record, "record wrong state  = False"))
        # play video
        # play video
        self.vid.play_movie( self.move_test )

        self.assertFalse(  self.vid.record , "record wrong state = True" )

    def recording(self,state: bool = True):
        self.vid.record = state
        print(str( self.vid.record ))
        self.assertEqual(self.vid.record,state)

    def test_frame(self):
        self.test__init__( play=True, image=True )
        self.vid.frame = self.image_test
        self.test_show_image()
        image = self.vid.frame
        self.assertEqual( image, self.vid.frame, 'test_frame :images not equal' )

        pass

    def test_command(self):
        #
        self.test__init__( algo=True )
        self.vid.command = lambda frame: extract_image( frame )

        # call show image method
        self.vid.show_image( self.image_test )
        self.vid._extract()

        self.vid.frame = self.image_test
        pass

    def test_algo(self):
        self.test__init__( algo=True )
        self.vid.command = lambda frame: extract_image( frame )

        # call show image method
        self.vid.show_image( self.image_test )
        self.vid._extract()
        self.assertTrue( self.vid.algo )

    def test_camera(self):
        self.test__init__( play=True, camera=True )
        self.vid.camera = True
        self.assertTrue( self.vid.camera )
        pass

    def test__build_widget(self):
        self.fail()

    def test__camera_view(self):
        self.test__init__( camera=True, pause=True,stop=True )
        self.vid.button_camera.after( 2000, self.vid._pause_view )
        self.vid.button_camera.after( 3000, self.vid._pause_view )
        self.vid.button_camera.after( 5500, self.vid.stop_player )
        self.vid._camera_view()

    def test__pause_view(self):
        self.test__init__( play=True, pause=True )
        self.vid.button_pause_video.after( 1000, self.vid._pause_view )
        self.vid.button_pause_video.after( 2000, self.vid._pause_view )
        self.vid.button_pause_video.after( 3000, self.vid._pause_view )
        self.vid.button_pause_video.after( 3500, self.vid._pause_view )

        # play video
        self.vid.play_movie( self.move_test )

    def test__button_view_off(self):
        self.fail()

    def test__record_view(self):
        self.test__init__( play=True,record = True, pause=True )
        self.vid.button_pause_video.after( 1000, self.vid._record_view )
        self.vid.button_pause_video.after( 2000, self.vid._pause_view )
        self.vid.button_pause_video.after( 3000, self.vid._pause_view )
        self.vid.button_pause_video.after( 5500, self.vid.stop_player )

        # play video
        self.vid.play_movie( self.move_test )

    def test__record_view_state(self):
        self.fail()

    def test__update_progress(self):
        self.fail()

    def test__resize(self):
        self.fail()

    def test__extract(self):
        self.fail()

    def test_set_setup(self):
        test_setup = {"play": True, "pause": True, "stop": True, "camera": False,
                      "record": False, "algo": False, "image": False}
        self.test__init__( **test_setup )
        self.assertDictEqual( self.vid.setup, test_setup )
        pass

    def test_run_frames(self):
        self.fail()

    def test_load_movie(self):
        self.test__init__( play=True, pause=True, stop=True )

        self.vid.load_movie( self.move_test )
        # self.vid.after(5000, self.vid.destroy)
        pass

    def test_play_movie(self):
        self.test__init__( play=True, pause=True, stop=True )
        # open file
        self.vid.play_movie( self.move_test )

        pass

    def test_camera_capture(self):
        self.test__init__( play=True, camera=True )
        c = threading.Thread( target=lambda: self.close_window() )
        t = threading.Thread( target=lambda: self.vid.camera_capture() )
        t.start()
        c.start()
        c.join()
        t.join()

    def test_pause_player(self):
        self.test__init__( play=True, camera=True, pause=True )

        self.vid.button_pause_video.after( 1000, lambda: self.vid.pause_player() )
        self.vid.play_movie( self.move_test )

    def assert_button_camera_press(self):
        self.assertRaises( tkinter.TclError, lambda: self.vid._camera_view() )



    def test_stop_player(self):
        self.test__init__( play=True, stop=True )
        self.vid.button_stop_video.after( 5000, self.vid.stop_player )
        self.vid.play_movie( self.move_test )

        pass

    def test_camera_recording(self):
        self.test__init__( play=True,camera =True, stop=True, record=True )

        self.vid.button_record.after( 2000, self.vid.camera_recording )
        self.vid.button_record.after(3000,  self.vid._record_view )
        self.vid.play_movie( self.move_test )
        # open file


    def test_save_frame(self):
        self.fail()

    def test_save_frame(self):
        self.test__init__(image=True, play=False, stop=False, pause=False )
        self.vid.frame = np.array( self.image_test )
        self.vid.save_frame( self.vid.frame.image )

    def test_load_image(self):
        self.test__init__( image=True, play=False, stop=False, pause=False )
        self.vid.load_image(self.image_file)
        self.vid.update()

        pass

    def test_resize_image_show(self):
        self.fail()

    def test_show_image(self):
        self.test__init__( image=True )
        # read image
        # call show image method
        self.vid.show_image( self.image_test )
        pass

    def test_matrix_to_pillow(self):
        self.test__init__( image=True )
        matrix_image = np.array( self.image_test )
        pillow_image = self.vid.matrix_to_pillow( matrix_image )
        self.assertTrue( Image.isImageType( pillow_image ) )
        pass

    def test_on_closing(self):
        self.test__init__()
        self.vid.after( 1000,  self.vid.destroy)
        self.vid.on_closing()



    def test_image_size(self):
        self.test__init__( image=True )
        # read image
        self.vid.frame = self.image_test
        image_size = self.vid.frame.size
        self.assertTupleEqual( self.image_test.size, image_size )
        pass



    def close_window(self):
        print( 'destroy' )
        self.vid.destroy()


def extract_image(matrix_image):
    cv2.imshow( 'frame', matrix_image )





 
 
