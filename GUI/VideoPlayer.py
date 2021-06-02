import copy
import os
from tkinter import *
from tkinter import filedialog, ttk

import cv2
import numpy as np
from PIL import Image, ImageTk


class VideoPlayer(ttk.Frame):

    STD_DIMS = {"480p":   (640,480),
                "720p":   (1280,720),
                "1080p":  (1920,1080),
                "4K":     (3840,2160)}

    def __init__(self, parent: ttk.Frame=None, **prop: dict):

        setup = self.set_setup(prop)

        ttk.Frame.__init__(self, parent)

        # private
        self.__frames_numbers = 0
        self.__play = False
        self.__record = False
        self.__camera = False
        self.__algo = False
        self.__frame = np.array
        self.__initialdir = "/"
        self.__initialdir_movie = "/"
        self.__camera_port = 0

        # protected
        self._cap = cv2.VideoCapture()
        self._source = 0

        self._out = object
        self._size = self.STD_DIMS.get('480P')
        self._image_size = self.STD_DIMS.get('480P')
        self._image_size_camera = self.STD_DIMS.get('480p')
        self._image_ratio = 480/640
        self._command = []
        self._frame_rate = 24.0

        # public
        self.frame = np.array
        # build widget
        self._build_widget(parent, setup)

    @property
    def image_size_camera(self)->tuple:
        return self._image_size_camera

    @property
    def image_size(self)->tuple:
        self._image_size = (int(self._cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(self._cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        return self._image_size

    @property
    def play(self)->bool:

        if self._cap.isOpened():
            self.__play = True
        else:
            self.__play = False
        return self.__play

    @property
    def record(self)->bool:
        return self.__record

    @property
    def frame(self)->np.array:
        return self.__frame

    @property
    def command(self):
        return self.__command

    @property
    def algo(self)->bool:
        return self.__algo

    @property
    def camera(self):

        return self.__camera

    @camera.setter
    def camera(self, capture: bool):

        if capture:
            if not self._cap.isOpened():
                self._cap = cv2.VideoCapture(self.__camera_port, cv2.CAP_DSHOW)
                self._cap.set(3, self._image_size_camera[0])
                self._cap.set(4, self._image_size_camera[1])
            self.__camera = True
        else:
            self.__camera = False
            self._cap.release()

    @image_size_camera.setter
    def image_size_camera(self, res: str = '480P'):
        if res in self.STD_DIMS.keys():
            self._image_size_camera = self.STD_DIMS.get(res)
        else:
            self._image_size_camera = self.STD_DIMS.get('480P')

    @record.setter
    def record(self, record: bool):
        self.__record = record
        self._record_view()

    @frame.setter
    def frame(self, frame: np.array):
        self.__frame = frame

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
            self.__algo = algo

    def set_setup(self, prop: dict)->dict:

        default = {'play': True, 'camera': False, 'pause': True, 'stop': True, 'record': False, 'image': False, 'algo': False}
        setup = default.copy()
        setup.update(prop)
        self.algo = setup['algo']
        return setup

    def _build_widget(self, parent: ttk.Frame=None, setup: dict=dict):

        if parent is None:
            self.master.geometry("700x500+0+0")
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
        self.canvas_image.bind("<Configure>", self.resize)

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
                                       command=lambda: self.stop_movie())
            self.button_stop_video.pack(side='left')

        if setup['record']:
            # record video
            self.icon_record_off = PhotoImage( file=os.path.join(icons_path, 'record_off.PNG'))
            self.icon_record_on = PhotoImage( file=os.path.join(icons_path, 'record_on.PNG'))

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
                                          command=lambda: self.extract())
            self.button_run_algo.pack(side='left')

        # edit box
        self.frame_counter = Label(self.control_frame, height=2, width=15, padx=10, pady=10, bd=8,
                                   bg='black', fg="gray", font=('arial', 10, 'bold'))
        self.frame_counter.pack(side='left')

    def camera_recording(self, file: str = 'output.avi'):
        
        if self._cap.isOpened():
            if self.__play:
                self.__record = not self.__record
                if self.__record:

                    self._source = cv2.VideoWriter_fourcc(*'XVID')
                    self._out = cv2.VideoWriter(file, self._source, self._frame_rate,self.image_size,0)

    def _camera_view(self):

        self.button_camera.config(bg='white', relief='sunken')
        self.camera_capture()
        self.button_camera.config(bg='black', relief='raised')

    def _pause_view(self):

        if self._cap.isOpened():
            if self.__play:
                self.button_pause_video.config(relief='sunken')
                self.__play = False
            else:
                self.button_pause_video.config(relief='raised')
                self.__play = True
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
        
        self.camera_recording()

        if self.__record :
            self.button_record.config(image=self.icon_record_on,relief = 'sunken')
        else:
            self.button_record.config(image=self.icon_record_off,relief = 'raised')

    def save_frame(self, frame):
        # convert two images to gray scale

        self._out.write(cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY))

    def extract(self):
        if self.algo:

            self.algo = False
            self.button_run_algo.config(text="Run algo")
        else:
            self.algo = True
            self.button_run_algo.config(text="Stop algo")

    def resize(self, event):

        w, h = event.width, event.height

        width = h/self._image_ratio
        height = h

        if width > w:

            width = w
            height = w*self._image_ratio

        self._size = (int(width), int(height))
        if Image.isImageType(self.frame):
            image = copy.deepcopy(self.frame)
            self.show_image(image)

    def load_image(self):

        filename = filedialog.askopenfilename(initialdir=self.__initialdir, title="Select the RGB image",
                                              filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
        self.__initialdir = os.path.dirname(os.path.abspath(filename))
        if len(filename) != 0:
            self.frame = Image.open(filename)
            image = self.frame

            self.update_progress(1, 1)
            self.__image_ratio = image.height / image.width
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

    def load_movie(self):
        
        self.button_live_video.config(relief = 'sunken')
        movie_filename = filedialog.askopenfilename(initialdir=self.__initialdir_movie,
                                                    title="Select the movie to play",
                                                    filetypes=(("AVI files", "*.AVI"),
                                                               ("MP4 files", "*.MP4"),
                                                               ("all files", "*.*")))
        if len(movie_filename) != 0:
            self.__initialdir_movie = os.path.dirname(os.path.abspath(movie_filename))
            try:
                self.play_movie(movie_filename)
            except Exception as e:
                 print("Exception:", e)
              
        self.button_live_video.config(bg='black', relief='raised')

    def play_movie(self, movie_filename: str):
        
        try:
            self._cap = cv2.VideoCapture(movie_filename)
            self.__frames_numbers = int(self._cap.get(cv2.CAP_PROP_FRAME_COUNT))
            self._image_ratio = self._cap.get(cv2.CAP_PROP_FRAME_HEIGHT) / self._cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        except Exception as e:
            print("Exception:", e)

        self.progressbar["maximum"] = self.__frames_numbers
        self.__play = True

        self.run_frames()

    def camera_capture(self):

        self.__play = True
        self.camera = True
        self.__frames_numbers = 1
     
        if self.__play:
            self.run_frames()

    def run_frames(self):
        frame_pass = 0
        try:
            while self._cap.isOpened():

                if self.__play:
                    # update the frame number
                    ret, image_matrix = self._cap.read()
                    self.frame = image_matrix
                    if ret:
                        frame_pass += 1
                        self.update_progress(frame_pass)
                        if self.__record:
                            self.save_frame(image_matrix)

                        # convert matrix image to pillow image object
                        self.__frame = self.matrix_to_pillow(image_matrix)
                        self.show_image(self.__frame)

                    elif not ret:
                        break

                # refresh image display
                self.board.update()
        except Exception as e:
            print(e)
        finally:
            self._cap.release()

            cv2.destroyAllWindows()
            self._button_view_off()

    @staticmethod
    def matrix_to_pillow(frame: np.array):

        # convert to BGR
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        # convert matrix image to pillow image object
        frame_pillow = Image.fromarray(frame_bgr)
        return frame_pillow

    def stop_movie(self):
        
        # in the case the player is on stop the player 
        if self.play: 
            self.__play = False
            self._cap.release()

            if self.__record:
        # in the case the record in on - stop the recording 
                self._out.release()
                self.record = False

            cv2.destroyAllWindows()
            self.update_progress(0, 0)

    def pause_movie(self):

        if self.play:
            self.__play = False
        else:
             self.__play = True

        self.pause_icon_view()


    def update_progress(self, frame_pass: int=0, frames_numbers: int = None):

        if frames_numbers is None:
            frames_numbers = self.__frames_numbers

        self.frame_counter.configure(text=str(frame_pass) + " / " + str(frames_numbers))
        # update the progressbar
        self.progressbar["value"] = frame_pass
        self.progressbar.update()


def main():
    vid = VideoPlayer(image=True, play=True, camera=True, record = True,algo = True)
    vid.command = lambda frame: extract_image(frame)
    vid.image_size_camera = '480p'
    vid.mainloop()

# segment path
path = os.path.abspath(os.path.join(os.pardir, 'xml'))
face_frontal = os.path.join(path, 'haarcascade_frontalface_default.xml')

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
