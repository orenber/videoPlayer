from tkinter import*
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
import numpy as np
import cv2
import os
import copy


class VideoPlayer(ttk.Frame):

    def __init__(self, parent: ttk.Frame=None, **prop: dict):

        setup = self.set_setup(prop)

        ttk.Frame.__init__(self, parent)

        # private
        self.__cap = object
        self.__size = (640, 480)
        self.__image_ratio = 480/640
        self.__frames_numbers = 0
        self.__play = False
        self.__algo = False
        self.__frame = np.array
        self.__initialdir = "/"
        self.__initialdir_movie = "/"

        # protected
        self._command = []

        # public
        self.frame = np.array
        # build widget
        self._build_widget(parent, setup)

    @property
    def frame(self)->np.array:
        return self.__frame

    @property
    def command(self):
        return self.__command

    @property
    def algo(self)->bool:
        return self.__algo

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

        default = {'play':  True, 'camera': False, 'pause': True, 'stop': True, 'image': False, 'algo': False}
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
        control_frame = Frame(self.main_panel, bg="black", relief=SUNKEN)
        control_frame.pack(side=BOTTOM, fill=X, padx=20)

        icons_path = os.path.abspath(os.path.join(os.pardir, 'Icons'))
        if setup['play']:
            # play video button button_live_video
            self.icon_play = PhotoImage(file=os.path.join(icons_path, 'play2.PNG'))
            button_live_video = Button(control_frame, padx=10, pady=10, bd=8, fg="white", font=('arial', 12, 'bold'),
                                       text="> Load Video", bg='black', image=self.icon_play, height=icon_height,
                                       width=icon_width, command=lambda: self.load_movie())
            button_live_video.pack(side='left')

        # play camera
        if setup['camera']:
            self.icon_camera = PhotoImage(file=os.path.join(icons_path, 'camera.PNG'))
            button_camera = Button(control_frame, padx=10, pady=10, bd=8, fg="white", font=('arial', 12, 'bold'),
                                   text="camera", bg='black', image=self.icon_camera, height=icon_height,
                                   width=icon_width, command=lambda: self.camera_capture())
            button_camera.pack(side='left')

        if setup['pause']:
            # pause video button button_live_video
            self.icon_pause = PhotoImage(file=os.path.join(icons_path, 'pause2.PNG'))

            self.button_pause_video = Button(control_frame, padx=10, pady=10, bd=8, fg="white",
                                             font=('arial', 12, 'bold'),
                                             text="Pause", bg='black', image=self.icon_pause,
                                             height=icon_height, width=icon_width,
                                             command=lambda: self.pause_movie())
            self.button_pause_video.pack(side='left')

        if setup['stop']:
            # stop video button button_live_video
            self.icon_stop = PhotoImage(file=os.path.join(icons_path, 'stop.PNG'))
            button_stop_video = Button(control_frame, padx=10, pady=10, bd=8, fg="white", font=('arial', 12, 'bold'),
                                       text="stop", bg='black', height=icon_height, width=icon_width,
                                       image=self.icon_stop,
                                       command=lambda: self.stop_movie())
            button_stop_video.pack(side='left')

        if setup['image']:
            # load image button button_load_image
            self.icon_image = PhotoImage(file=os.path.join(icons_path, 'image.PNG'))
            button_load_image = Button(control_frame, padx=10, pady=10, bd=8, fg="white", font=('arial', 12, 'bold'),
                                       text="Load Image", bg="black", image=self.icon_image,
                                       height=icon_height, width=icon_width,
                                       command=lambda: self.load_image())
            button_load_image.pack(side='left')

        if setup['algo']:
            # load image button button_load_image
            # self.icon_algo = PhotoImage( file=os.path.join( icons_path, 'algo.PNG' ) )
            self.button_run_algo = Button(control_frame, padx=10, pady=10, bd=8, fg="white", font=('arial', 12, 'bold'),
                                          text="Run algo", bg="black", height=1, width=8,
                                          command=lambda: self.extract())
            self.button_run_algo.pack(side='left')

        # edit box
        self.frame_counter = Label(control_frame, height=2, width=15, padx=10, pady=10, bd=8,
                                   bg='black', fg="gray", font=('arial', 10, 'bold'))
        self.frame_counter.pack(side='left')

    def extract(self):
        if self.algo:

            self.algo = False
            self.button_run_algo.config(text="Run algo")
        else:
            self.algo = True
            self.button_run_algo.config(text="Stop algo")

    def resize(self, event):

        w, h = event.width, event.height

        width = h/self.__image_ratio
        height = h

        if width > w:

            width = w
            height = w*self.__image_ratio

        self.__size = (int(width), int(height))
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
        image.thumbnail(self.__size)
        #
        self.photo = ImageTk.PhotoImage(image=image)
        # The Label widget is a standard Tkinter widget used to display a text or image on the screen.
        self.board.config(image=self.photo)
        self.board.image = self.photo
        # refresh image display
        self.board.update()

    def load_movie(self):
        
        movie_filename = filedialog.askopenfilename(initialdir=self.__initialdir_movie,
                                                    title="Select the movie to play",
                                                    filetypes=(("AVI files", "*.AVI"),
                                                               ("MP4 files", "*.MP4"),
                                                               ("all files", "*.*")))
        if len(movie_filename) != 0:
            self.__initialdir_movie = os.path.dirname(os.path.abspath(movie_filename))
            self.play_movie(movie_filename)

        pass

    def play_movie(self, movie_filename: str):

        self.__cap = cv2.VideoCapture(movie_filename)
        self.__frames_numbers = int(self.__cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.__image_ratio = self.__cap.get(cv2.CAP_PROP_FRAME_HEIGHT) / self.__cap.get(cv2.CAP_PROP_FRAME_WIDTH)

        self.progressbar["maximum"] = self.__frames_numbers
        self.__play = True

        self.run_frames()

    def camera_capture(self):

        self.__cap = cv2.VideoCapture(0)
        self.__frames_numbers = 1
        self.__play = not self.__play
        self.run_frames()

    def run_frames(self):
        frame_pass = 0

        while self.__cap.isOpened():

            if self.__play:
                # update the frame number
                ret, image_matrix = self.__cap.read()
                # self.frame = image_matrix
                if ret:
                    frame_pass += 1
                    self.update_progress(frame_pass)

                    # convert matrix image to pillow image object
                    self.frame = self.matrix_to_pillow(image_matrix)
                    self.show_image(self.frame)

                # refresh image display
            self.board.update()

        self.__cap.release()

        cv2.destroyAllWindows()

    @staticmethod
    def matrix_to_pillow(frame: np.array):

        # convert to BGR
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        # convert matrix image to pillow image object
        frame_pillow = Image.fromarray(frame_bgr)
        return frame_pillow

    def stop_movie(self):

        self.pause_movie()
        self.__cap.release()

        cv2.destroyAllWindows()
        self.update_progress(0, 0)

    def pause_movie(self):

        if self.__cap.isOpened():
            self.__play = not self.__play

        else:
            self.__play = False

        if self.__play:
            self.button_pause_video.config(image=self.icon_pause)
        elif not self.__play:
            self.button_pause_video.config(image=self.icon_play)

    def update_progress(self, frame_pass: int=0, frames_numbers: int = None):

        if frames_numbers is None:
            frames_numbers = self.__frames_numbers

        self.frame_counter.configure(text=str(frame_pass) + " / " + str(frames_numbers))
        # update the progressbar
        self.progressbar["value"] = frame_pass
        self.progressbar.update()


def main():
    vid = VideoPlayer(image=True, play=True, camera=True, algo=True)
    vid.command = lambda frame: extract_image(frame)
    vid.mainloop()


def extract_image(matrix_image: np.array):

    # apply algo
    resize_image = cv2.resize(matrix_image, dsize=(640, 480), interpolation=cv2.INTER_CUBIC)
    cv2.imshow('frame', resize_image)


if __name__ == "__main__":
    main()
