
from GUI.videoPlayer import VideoPlayer
from GUI.frameImg import FrameImg
from GUI.dynamic_panel import DynamicPanel

import numpy as np
import cv2
from tkinter import *
from tkinter import ttk
from Utility.file_location import *
from Utility.logger_setup import setup_logger

import Pmw


class Factory(VideoPlayer):
    FILE_TYPE = {".AVI", 0,
                 ".MP4", 1}

    def __init__(self, parent: ttk.Frame = None, **kwargs):

        self.log = setup_logger( "Factory Camera" )

        super().__init__( image=True, play=True, camera=True, record=True )

        self.algo_stack = []
        self.frame_take = 0
        self.frame_number = 0
        self.set_gray_image = True
        self._resolution = '0.02MP'

        self._file_name_record = "record_video"
        self._output_path_record = full_file(['Resources', 'Record', self._file_name_record] )
        self._record_color = 1

        self.pri_frame = FrameImg( np.zeros( self.STD_DIMS.get(self._resolution  ), float ) )

    def _build_widget(self, parent: ttk.Frame = None, setup: dict = dict):

        self.hide()
        self.log.info( "start build widget" )

        self.master.geometry( "950x720+0+0" )
        self.master.protocol( "WM_DELETE_WINDOW", self.on_closing )

        # Title bar Title
        self.master.title( "FactoryCamera" )
        # Title Bar Icon
        self.icons_path = full_file(["Icons", "webcamera.ico"])
        self.master.iconbitmap(self.icons_path )

        # main panel

        self.main_frame = Frame( width=1000,
                                 height=720,
                                 bg="gray24",
                                 relief="raised",
                                 name="main_frame" )
        self.main_frame.pack( side=TOP )
        self.main_frame.place( relx=0, rely=0, relwidth=1, relheight=1 )

        super()._build_widget( self.main_frame, setup )

        self.canvas_image.unbind( "<Configure>" )

        # control panel
        matrix = {"row": [{"col": [0, 0]},{"col": [0, 0]}]}
        self.dynamic_panel = DynamicPanel( self.canvas_image, matrix )

        self.board.place_forget()
        self.board.destroy()
        self.board = self.dynamic_panel.current_label_image

        self.dynamic_panel.command = lambda: self._focus_label()
        [can.bind( "<Configure>", self._resize ) for can in self.dynamic_panel.canvas_image]

        # load image button button_load_image

        self.button_blue_object = Button(self.control_frame, padx=10, pady=10, bd=8,
                                                 fg="white",
                                                 font=('arial', 12, 'bold'),
                                                 bg="blue",
                                                 height=1,
                                                 width=2,
                                                 name="button_blue_object",
                                                 command=lambda: self._button_blue_object_view() )
        self.button_blue_object.pack( side='left' )
        button_blue_object_tooltip = Pmw.Balloon( self.control_frame )
        button_blue_object_tooltip.bind( self.button_blue_object, "blue  detection" )
        self.show()

    def _focus_label(self):

        self.board = self.dynamic_panel.current_label_image

    def _button_blue_object_view(self):

        if self.button_blue_object.cget( 'relief' ) == 'raised':
            self.algo_list( True, self.movement_detection )
            self.button_blue_object.config( bg='white', relief='sunken' )
            self.log.info( "Object detection is On" )

        elif self.button_blue_object.cget( 'relief' ) == 'sunken':
            self.algo_list( False, self.movement_detection )
            self.button_blue_object.config(bg='blue', relief='raised' )
            self.log.info( "Movement detection is Off" )


    def algo_list(self, add: bool = False, algo=None):

        if add:
            if algo not in self.algo_stack:
                self.algo_stack.append( algo )
        else:
            if algo is None:
                pass

            elif algo in self.algo_stack:
                self.algo_stack.remove( algo )

    def _pause_view(self):
        super()._pause_view()
        # condition for crop ROI

    def run_frames(self):

        self.log.info( "run frame by frame" )
        self.frame_number = 0
        self.frame_take = 0

        try:

            while self._cap.isOpened():

                if self._play:

                    # update the frame number
                    ret, image = self._cap.read()

                    if ret:

                        self.frame.image = image

                        self.frame_number += 1

                        self._update_progress( self.frame_number )
                        if self._record:
                            self.save_frame( image )

                        # take the image and sand it to the list of function to analyze process
                        algo_list = self.algo_stack
                        algo_nums = len( algo_list )

                        if algo_nums:

                            for n in range( 0, algo_nums ):
                                algo_list[n]( image )

                        # self.face_detection(frame_gray)
                        # convert matrix image to pillow image object
                        self.resize_image_show( self.frame )

                        # refresh image display
                    elif not ret:
                        break
                self.board.update()
        except Exception as error:
            self.log.exception( error )
        finally:
            self._cap.release()
            self._out.release()
            cv2.destroyAllWindows()
            self._button_view_off()

    def save_frame(self, frame: np.array):
        try:

            self._out.write( frame )
        except Exception as error:
            self.log.error(error)


def main():
    vid = Factory()
    vid.mainloop()


if __name__ == "__main__":
    main()
