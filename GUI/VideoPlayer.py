import copy
import os
from tkinter import *
from tkinter import filedialog, ttk,messagebox

import cv2
import numpy as np
from PIL import Image, ImageTk
from Utility.image_procesing import resize_image_to_frame


class VideoPlayer(ttk.Frame):

    STD_DIMS = {
                "0.02MP": (160, 120),
                "0.06MP": (320, 180),
                "0.08MP": (320, 240),
                "0.1MP":  (424, 240),
                "0.2MP":  (640, 360),
                "0.3MP":  (640, 480),
                "0.4MP":  (848, 480),
                "0.5MP":  (960, 540),
                "0.9MP":  (1280, 720)
    }

    def __init__(self, parent: ttk.Frame=None, **prop: dict):

        setup = self.set_setup(prop)

        ttk.Frame.__init__(self, parent)

        # private

        self.__initialdir = "/"
        self.__initialdir_movie = "/"

        # protected
        self._frames_numbers = 0
        self._play = False
        self._record = False
        self._camera = False
        self._algo = False
        self._frame = np.zeros( self.STD_DIMS.get('0.3MP'),float)

        self._camera_port = 0
        self._cap = cv2.VideoCapture()
        self._source = 0

        self._out = object
        self._size = self.STD_DIMS.get('0.3MP')
        self._image_size = self.STD_DIMS.get('0.3MP')
        self._image_size_camera = self.STD_DIMS.get('0.3MP')
        self._image_ratio = 480/640
        self._command = []
        self._frame_rate = 24.0

        # public
      
        # build widget
        self._build_widget(parent, setup)

    @property
    def image_size_camera(self)->tuple:
        return self._image_size_camera

    @property
    def image_size(self)->tuple:
        height,width,*_= self._frame.shape
        self._image_size = (int(width), int(height))
        return self._image_size

    @property
    def image_ratio(self)->float:
        height,width,*_= self._frame.shape
        if width != 0:   
            self._image_ratio = height/width
        else:
            self._image_ratio = 0
        return self._image_ratio

    @property
    def play(self)->bool:

        if self._cap.isOpened():
            self._play = True
        else:
            self._play = False
        return self._play

    @property
    def record(self)->bool:
        return self._record

    @property
    def frame(self)->np.array:
        return self._frame

    @property
    def command(self):
        return self.__command

    @property
    def algo(self)->bool:
        return self._algo

    @property
    def camera(self):

        return self._camera

    @camera.setter
    def camera(self, capture: bool):

        if capture:
            if not self._cap.isOpened():
                self._cap = cv2.VideoCapture(self._camera_port, cv2.CAP_DSHOW)
                self._cap.set(3, self._image_size_camera[0])
                self._cap.set(4, self._image_size_camera[1])
            self._camera = True
        else:
            self._camera = False
            self._cap.release()

    @image_size_camera.setter
    def image_size_camera(self, res: str = '0.3MP'):
        if res in self.STD_DIMS.keys():
            self._image_size_camera = self.STD_DIMS.get(res)
        else:
            self._image_size_camera = self.STD_DIMS.get('0.3MP')

    @record.setter
    def record(self, record: bool):
        self._record = record
        self._record_view()

    @frame.setter
    def frame(self, frame: np.array):
        self._frame = frame

        if self.algo and callable(self._command):
            # convert image to numpy image
            matrix_image = np.array(self.frame)
            self._command(matrix_image)

    @command.setter
    def command(self, command):
        # check if the command is lambda expression
        if callable(command):

            self._command = command

    @algo.setter
    def algo(self, algo: bool):
        if isinstance(algo, bool):
            self._algo = algo

    # private
    def _build_widget(self, parent: ttk.Frame=None, setup: dict=dict):

        if parent is None:

            self.master.geometry("700x500+0+0")
            self.master.protocol( "WM_DELETE_WINDOW", self.on_closing)
            self.main_panel = Frame(self.master, relief=SUNKEN)
            self.main_panel.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)


        else:
            self.main_panel = parent

        # main panel
        self.main_panel.config(bg="black")

        icon_width = 45
        icon_height = 50
        canvas_progressbar_height = 2
        # frame_height = int(self.main_panel.cget('height')/10-icon_height-canvas_progressbar_height)

        self.canvas_image = Canvas(self.main_panel, bg="black", highlightthickness=0)
        self.canvas_image.pack(fill=BOTH, expand=True, side=TOP)
        self.canvas_image.bind("<Configure>", self._resize)
        self.canvas_image_height = int(self.canvas_image.config("height")[4])
        self.canvas_image_width  = int(self.canvas_image.config("width")[4])
        self.board = Label(self.canvas_image, bg="black", width=44, height=14)
        self.board.pack(fill=BOTH, expand=True)

        canvas_progressbar = Canvas(self.main_panel, relief=FLAT, height=canvas_progressbar_height, 
                                    bg="black", highlightthickness=0)
        canvas_progressbar.pack(fill=X, padx=10, pady=10)

        s = ttk.Style()
        s.theme_use('clam')
        s.configure("red.Horizontal.TProgressbar", foreground='red', background='red', thickness=3)
        self.progressbar = ttk.Progressbar(canvas_progressbar, style="red.Horizontal.TProgressbar", orient='horizontal',
                                           length=200, mode="determinate")

        self.progressbar.pack(fill=X, padx=10, pady=10, expand=True)

        # control panel
        self.control_frame = Frame(self.main_panel, bg="black", relief=SUNKEN)
        self.control_frame.pack(side=BOTTOM, fill=X, padx=20)

        icons_path = os.path.abspath(os.path.join(os.pardir, 'Icons' ))

        if setup['play']:
            # play video button button_live_video
            self.icon_play = PhotoImage(file=os.path.join(icons_path, 'play.PNG'))
            self.button_live_video = Button(self.control_frame, padx=10, pady=10, bd=8, fg="white", font=('arial', 12, 'bold'),
                                            text="> Load Video", bg='black', image=self.icon_play, height=icon_height,
                                            width=icon_width, command=lambda: self.load_movie())
            self.button_live_video.pack(side='left')

        # play camera
        if setup['camera']:
            self.icon_camera = PhotoImage(file=os.path.join(icons_path, 'camera.PNG'))
            self.button_camera = Button(self.control_frame, padx=10, pady=10, bd=8, fg="white", font=('arial', 12, 'bold'),
                                        text="camera", bg='black', image=self.icon_camera, height=icon_height,
                                        width=icon_width, command=lambda: self._camera_view())
            self.button_camera.pack(side='left')

        if setup['pause']:
            # pause video button button_live_video
            self.icon_pause = PhotoImage(file=os.path.join(icons_path, 'pause.PNG'))

            self.button_pause_video = Button(self.control_frame, padx=10, pady=10, bd=8, fg="white",
                                             font=('arial', 12, 'bold'),
                                             text="Pause", bg='black', image=self.icon_pause,
                                             height=icon_height, width=icon_width,
                                             command=lambda: self._pause_view())
            self.button_pause_video.pack(side='left')

        if setup['stop']:
            # stop video button button_live_video
            self.icon_stop = PhotoImage(file=os.path.join(icons_path, 'stop.PNG'))
            self.button_stop_video = Button(self.control_frame, padx=10, pady=10, bd=8, fg="white", font=('arial', 12, 'bold'),
                                            text="stop", bg='black', height=icon_height, width=icon_width,
                                            image=self.icon_stop,
                                            command=lambda: self.stop_player())
            self.button_stop_video.pack(side='left')

        if setup['record']:
            # record video
            self.icon_record_off = PhotoImage(file=os.path.join(icons_path, 'record_off.PNG'))
            self.icon_record_on = PhotoImage(file=os.path.join(icons_path, 'record_on.PNG'))

            self.button_record = Button(self.control_frame, padx=10, pady=10, bd=8, fg="white", font=('arial', 12, 'bold'),
                                        text="record", bg="black", height=icon_height, width=icon_width,
                                        image=self.icon_record_off,
                                        command=lambda: self._record_view())
            self.button_record.pack(side='left')

        if setup['image']:
            # load image button button_load_image
            self.icon_image = PhotoImage(file=os.path.join(icons_path, 'image.PNG'))
            self.button_image_load = Button(self.control_frame, padx=10, pady=10, bd=8, fg="white", font=('arial', 12, 'bold'),
                                            text="Load Image", bg="black", image=self.icon_image,
                                            height=icon_height, width=icon_width,
                                            command=lambda: self.load_image())
            self.button_image_load.pack(side='left')

        if setup['algo']:
            # load image button button_load_image
            # self.icon_algo = PhotoImage( file=os.path.join( icons_path, 'algo.PNG' ) )
            self.button_run_algo = Button(self.control_frame, padx=10, pady=10, bd=8, fg="white", font=('arial', 12, 'bold'),
                                          text="Run algo", bg="black", height=1, width=8,
                                          command=lambda: self._extract())
            self.button_run_algo.pack(side='left')

        # edit box
        self.frame_counter = Label(self.control_frame, height=2, width=15, padx=10, pady=10, bd=8,
                                   bg='black', fg="gray", font=('arial', 10, 'bold'))
        self.frame_counter.pack(side='left')

    def _camera_view(self):
        if not self.play:
            self.button_camera.config(bg='white', relief='sunken')
            self.camera_capture()
            self.button_camera.config(bg='black', relief='raised')

    def _pause_view(self):

        if self._cap.isOpened():
            if self._play:
                self.button_pause_video.config(relief='sunken')
                self._play = False
            else:
                self.button_pause_video.config(relief='raised')
                self._play = True
        else:
            self.button_pause_video.config(relief='raised')

    def _button_view_off(self):

        self.button_live_video.config(relief='raised')
        self.button_camera.config(bg='black', relief='raised')
        self.button_pause_video.config(relief='raised')
        self.button_stop_video.config(relief='raised')
        self.button_image_load.config(relief='raised')
        self.button_record.config(image=self.icon_record_off, relief='raised')

    def _record_view(self):
        
        self._record = not self._record

        if self._record and self.play:
            self.camera_recording()
            self.button_record.config(image=self.icon_record_on, relief='sunken')
        else:
            self.button_record.config(image=self.icon_record_off, relief='raised')

    def _update_progress(self, frame_pass: int = 0, frames_numbers: int = None):

        if frames_numbers is None:
            frames_numbers = self._frames_numbers

        self.frame_counter.configure(text=str(frame_pass) + " / " + str( frames_numbers ) )
        # update the progressbar
        self.progressbar["value"] = frame_pass
        self.progressbar.update()

    def _resize(self, event):

        self.canvas_image_width, self.canvas_image_height = event.width, event.height
   
        # resize image

        self.resize_image_show(self._frame)

    def _extract(self):
        if self.algo:

            self.algo = False
            self.button_run_algo.config(text="Run algo")
        else:
            self.algo = True
            self.button_run_algo.config(text="Stop algo")

    # public
    def set_setup(self, prop: dict) -> dict:

        default = {'play': True, 'camera': False, 'pause': True, 'stop': True, 'record': False, 'image': False,
                   'algo': False}
        setup = default.copy()
        setup.update( prop )
        self.algo = setup['algo']
        return setup

    def run_frames(self):
        frame_pass = 0
        try:
            while self._cap.isOpened():

                if self._play:
                    # update the frame number
                    ret, self.frame  = self._cap.read()
                    
                    if ret:
                        frame_pass += 1
                        self._update_progress( frame_pass )
                        if self._record:
                            self.save_frame( self._frame )

                        self.resize_image_show(self._frame)

                    elif not ret:
                        break

                # refresh image display
                self.board.update()
        except Exception as e:
            print( e )
        finally:
            self._cap.release()

            cv2.destroyAllWindows()
            self._button_view_off()

    def load_movie(self):
        if not self.play:
            self.button_live_video.config( relief='sunken' )
            movie_filename = filedialog.askopenfilename( initialdir=self.__initialdir_movie,
                                                         title="Select the movie to play",
                                                         filetypes=(("AVI files", "*.AVI"),
                                                                    ("MP4 files", "*.MP4"),
                                                                    ("all files", "*.*")) )
            if len( movie_filename ) != 0:
                self.__initialdir_movie = os.path.dirname( os.path.abspath( movie_filename ) )
                try:
                    self.play_movie( movie_filename )
                except Exception as e:
                    print( "Exception:", e )

                finally:
                    self.button_live_video.config( bg='black', relief='raised' )
            else:
                self.button_live_video.config( bg='black', relief='raised' )

    def play_movie(self, movie_filename: str):

        try:
            self._cap = cv2.VideoCapture( movie_filename )
            self._frames_numbers = int( self._cap.get( cv2.CAP_PROP_FRAME_COUNT ) )
            self._image_ratio = self._cap.get( cv2.CAP_PROP_FRAME_HEIGHT ) / self._cap.get( cv2.CAP_PROP_FRAME_WIDTH )
        except Exception as e:
            print( "Exception:", e )

        self.progressbar["maximum"] = self._frames_numbers
        self._play = True

        self.run_frames()

    def camera_capture(self):

        self._play = True
        self.camera = True
        self._frames_numbers = 1

        if self._play:
            self.run_frames()

    def pause_player(self):

        if self.play:
            self._play = False
        else:
            self._play = True

        self.pause_icon_view()

    def stop_player(self):

        # in the case the player is on stop the player
        if self.play:
            self._play = False
            self._cap.release()

            if self._record:
                # in the case the record in on - stop the recording
                self._out.release()
                self.record = False

            cv2.destroyAllWindows()
            self._update_progress(0, 0)

    def camera_recording(self, file: str = 'output.avi'):

        if self.play:
            self._source = cv2.VideoWriter_fourcc(*'XVID')
            self._out = cv2.VideoWriter(file, self._source, self._frame_rate, self.image_size, 0)

    def save_frame(self, frame):
        # convert two images to gray scale

        self._out.write(cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY))

    def load_image(self):

        filename = filedialog.askopenfilename(initialdir=self.__initialdir, title="Select the RGB image",
                                              filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
        self.__initialdir = os.path.dirname(os.path.abspath(filename))
        if len(filename) != 0:
            try:
                self.frame = Image.open(filename)
            except Exception as error:
                print( "Exception:", error)

            self.resize_image_show(self._frame)
    
    def resize_image_show(self,image):

        if Image.isImageType(image):
            self._size = resize_image_to_frame(image._size, (self.canvas_image_width, self.canvas_image_height) )
            image_view = copy.copy(image)
            self.show_image(image_view)
        elif isinstance(image, np.ndarray):
            if image.any():
               self._size = resize_image_to_frame((self._frame.shape[1],self._frame.shape[0]),(self.canvas_image_width, self.canvas_image_height))
               resize = cv2.resize(self._frame,  self._size, interpolation = cv2.INTER_AREA)
               image = self.matrix_to_pillow(resize)
               self.show_image(image)

    def show_image(self, image):
       
        # resize image
        image.thumbnail(self._size)
        self.photo = ImageTk.PhotoImage(image=image)
        # The Label widget is a standard Tkinter widget used to display a text or image on the screen.
        self.board.config(image=self.photo)
        self.board.image = self.photo
        # refresh image display
        self.board.update()

    @staticmethod
    def matrix_to_pillow(frame: np.array):

        # convert to BGR
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        # convert matrix image to pillow image object
        frame_pillow = Image.fromarray(frame_bgr)
        return frame_pillow

    def on_closing(self):
        if messagebox.askokcancel( "Quit", "Do you want to quit?" ):
            self.stop_player()
            self.master.destroy()





def main():
    vid = VideoPlayer(image=True, play=True, camera=True, record = True,algo = True)
    vid.command = lambda frame: extract_image(frame)
    vid.image_size_camera = '0.3MP'
    vid.mainloop()

# segment path
path = os.path.dirname( cv2.__file__ )
face_frontal = os.path.join( path, 'data', 'haarcascade_frontalface_default.xml' )

# cascade classifier
face_cascade = cv2.CascadeClassifier(face_frontal)


def extract_image(matrix_image: np.array):

    # apply algo

    # resize image
    resize_image = cv2.resize( matrix_image, dsize=(640, 480), interpolation=cv2.INTER_CUBIC )

    # Convert to gray scale
    gray = cv2.cvtColor( resize_image, cv2.COLOR_BGR2GRAY )

    # Detect the faces
    faces = face_cascade.detectMultiScale( gray, 1.1, 4 )
    # Draw the rectangle around each face
    for (x, y, w, h) in faces:
        cv2.rectangle( resize_image, (x, y), (x + w, y + h), (255, 0, 0), 2 )
    # Display
    cv2.imshow( 'img', resize_image )


if __name__ == "__main__":
    main()
