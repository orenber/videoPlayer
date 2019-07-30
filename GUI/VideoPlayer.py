from tkinter import*
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
import numpy as np
import cv2
import os


class VideoPlayer(ttk.Frame):

    def __init__(self, parent=None,**prop):

        setup = self.set_setup(prop)

        ttk.Frame.__init__(self,parent)



        self.cap = object
        self.size = (640, 480)

        self.image_ratio = 480/640
        self.play = False
        self._command = []
        self.frame = []


        # build widget
        self._build_widget(parent,setup)

    @property
    def frame(self):
        return self.__frame

    @property
    def command(self):
        return self.__command

    @property
    def algo(self):
        return self.__algo

    @frame.setter
    def frame(self, frame):
        self.__frame = frame

        if self.algo and callable(self._command):
            # convert image to numpay image
            matrix_image = np.array(self.frame)
            self._command(matrix_image)

    @command.setter
    def command(self,command):
        # check if the command is lambda expression
        if callable(command):

            self._command = command

    @algo.setter
    def algo(self, algo):
        assert isinstance(algo,bool)
        self.__algo = algo

    def bind_to(self, callback):
        print('bound')
        self._command.append(callback)


    def set_setup(self,prop):

        default = {'play':  True,'camera': False, 'pause': True, 'stop': True, 'image': False,'algo': False}
        setup = default.copy()
        setup.update(prop)
        self.algo = setup['algo']
        return setup

    def _build_widget(self, parent,setup):

        if parent is None:
            self.master.geometry("700x500+0+0")
            self.main_panel = Frame(self.master,relief=SUNKEN)
            self.main_panel.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)
        else:
            self.main_panel = parent

        # main panel
        self.main_panel.config(bg="black")

        icon_height = 1
        icon_width = 8
        canvas_progressbar_height = 1
        frame_height = int(self.main_panel.cget('height')/10-icon_height-canvas_progressbar_height)

        self.canvas_image = Canvas( self.main_panel, bg="black", highlightthickness=0)
        self.canvas_image.pack(fill=BOTH, expand=True,side=TOP)
        self.canvas_image.bind("<Configure>", self.resize)

        self.board = Label(self.canvas_image,bg="black",width=44, height=14)
        self.board.pack(fill=BOTH, expand=True)
        #image_label.bind( "<Configure>", self.resize )

        canvas_progressbar = Canvas(self.main_panel, relief = FLAT, height = canvas_progressbar_height,bg="black"
                                    ,highlightthickness=0)
        canvas_progressbar.pack( fill=X, padx=10, pady=10 )


        s = ttk.Style()
        s.theme_use( 'clam' )
        s.configure( "red.Horizontal.TProgressbar", foreground='red', background='red',thickness=3)
        self.progressbar = ttk.Progressbar(canvas_progressbar,style="red.Horizontal.TProgressbar", orient='horizontal',
                                           length=200,mode="determinate")

        self.progressbar.pack(fill=X, padx=10, pady = 10, expand=True)

        # control panel
        control_frame = Frame(self.main_panel, bg="black", relief=SUNKEN)
        control_frame.pack(side=BOTTOM,fill=X, padx=20)

        icons_path = os.path.abspath(os.path.join(os.pardir, 'GUI', 'Icons'))
        if setup['play']:
            # play video button button_live_video
          #  self.icon_play = PhotoImage(file = os.path.join(icons_path,'play2.PNG'))
            button_live_video = Button(control_frame, padx=10, pady=10, bd=8, fg="white", font=('arial', 12, 'bold'),
                                       text="> Load Video", bg='black',height=icon_height, width=icon_width,
                                       command=lambda: self.load_movie())
            button_live_video.pack(side='left')

        # play webcam
        if setup['camera']:
          #  self.icon_webcam = PhotoImage(file = os.path.join(icons_path,'camera.PNG'))
            button_webcam = Button(control_frame, padx=10, pady=10, bd=8, fg="white", font=('arial', 12, 'bold'),
                                         text="camera", bg='black',height=icon_height, width=icon_width,
                                         command=lambda: self.camera_capture())
            button_webcam.pack(side='left')

        if setup['pause']:
            # pause video button button_live_video
            #self.icon_pause = PhotoImage(file = os.path.join(icons_path,'pause2.PNG'))

            self.button_pause_video = Button( control_frame, padx=10, pady=10, bd=8, fg="white", font=('arial', 12, 'bold'),
                                        text="Pause", bg='black',height=icon_height, width=icon_width,
                                        command=lambda: self.pause_movie() )
            self.button_pause_video.pack( side='left' )

        if setup['stop']:
            # stop video button button_live_video
            #self.icon_stop = PhotoImage(file =os.path.join(icons_path,'stop.PNG'))
            button_stop_video = Button( control_frame, padx=10, pady=10, bd=8, fg="white", font=('arial', 12, 'bold'),
                                        text="stop", bg='black',height=icon_height, width=icon_width,
                                        command=lambda: self.stop_movie())
            button_stop_video.pack(side='left')

        if setup['image']:
            # load image button button_load_image
            #self.icon_image = PhotoImage(file =os.path.join(icons_path,'image.PNG'))
            button_load_image = Button(control_frame, padx=10, pady=10, bd=8, fg="white", font=('arial', 12, 'bold'),
                                       text="Load Image", bg="black",height=icon_height, width=icon_width,
                                       command=lambda: self.load_image())
            button_load_image.pack(side='left')

        if setup['algo']:
            # load image button button_load_image
            #self.icon_algo = PhotoImage( file=os.path.join( icons_path, 'algo.PNG' ) )
            self.button_run_algo = Button( control_frame, padx=10, pady=10, bd=8, fg="white", font=('arial', 12, 'bold'),
                                        text="Run algo", bg="black", height=1,
                                        width=8,
                                        command= lambda:self.extract())
            self.button_run_algo.pack( side='left' )



        # edit box
        self.frame_counter = Label(control_frame, height=2, width=15, padx=10, pady=10, bd=8,
                             bg='black',fg="gray", font=('arial', 10, 'bold'))
        self.frame_counter.pack(side='left')

    def extract(self):
      if self.algo:

          self.algo = False
          self.button_run_algo.config(text="Run algo")
      else :

          self.algo = True
          self.button_run_algo.config(text="Stop algo")

    def resize(self, event):

        w, h = event.width, event.height

        width = h/self.image_ratio
        height = h

        if width > w:

            width = w
            height = w*self.image_ratio

        self.size = (width,height)

    def load_image(self):

        filename = filedialog.askopenfilename(initialdir="/", title="Select the RGB image",
                                              filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

        if len(filename) != 0:
            image = Image.open(filename)

            self.image_ratio = image.height / image.width

            self.show_image(image)

    def show_image(self, image):

        self.frame = image
        self.frame.thumbnail(self.size)
        photo = ImageTk.PhotoImage(self.frame)
        # The Label widget is a standard Tkinter widget used to display a text or image on the screen.
        self.board.config(image=photo,height=-1)
        # run locate plate - find the plate in the image

        self.main_panel.mainloop()

    def load_movie(self):
        movie_filename = filedialog.askopenfilename(initialdir="/", title="Select the movie to play",
                                                    filetypes=(("AVI files", "*.AVI"),
                                                               ("MP4 files", "*.MP4"),
                                                               ("all files", "*.*")))
        self.play_movie(movie_filename)

        pass

    def play_movie(self, movie_filename):

        self.cap = cv2.VideoCapture(movie_filename)
        self.frames_numbers = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.image_ratio = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT) / self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        frame_pass = 0

        self.progressbar["maximum"] = self.frames_numbers
        self.play = True

        while self.cap.isOpened():

            if self.play:
                # update the frame number

                frame_pass += 1
                self.update_progress(frame_pass)

                ret, self.frame = self.cap.read()

                # convert to BGR
                frame_bgr = cv2.cvtColor(self.frame, cv2.COLOR_RGB2BGR)
                # convert matrix image to pillow image object
                frame = Image.fromarray(frame_bgr)
                # resize image
                frame.thumbnail(self.size)
                # The Label widget is a standard Tkinter widget used to display a text or image on the screen.
                photo = ImageTk.PhotoImage(image=frame)
                # The Label widget is a standard Tkinter widget used to display a text or image on the screen.

                self.board.configure(image=photo)

                # refresh image display
            self.master.update()

        self.cap.release()


        cv2.destroyAllWindows()

    def update_progress(self, frame_pass):

        self.frame_counter.configure( text=str(frame_pass) + " / " + str(self.frames_numbers))
         # update the progressbat
        self.progressbar["value"] = frame_pass
        self.progressbar.update()

    def camera_capture(self):

        self.cap = cv2.VideoCapture(0)
        self.play = not self.play

        while self.play:

            _, frame = self.cap.read()
            self.display_image(frame)

            k = cv2.waitKey(5) & 0xFF

            if k == 27:
                break

        cv2.destroyAllWindows()
        self.cap.release()

    def display_image(self, image):
        self.frame = image
        # convert to BGR
        frame_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        # convert matrix image to pillow image object
        self.frame = Image.fromarray( frame_bgr )
        # resize image
        self.frame.thumbnail(self.size)

        # The Label widget is a standard Tkinter widget used to display a text or image on the screen.
        photo = ImageTk.PhotoImage( image = self.frame )
        # The Label widget is a standard Tkinter widget used to display a text or image on the screen.
        self.board.config(image=photo)
        # refresh image display
        self.master.update()

    def stop_movie(self):

        self.pause_movie()
        self.cap.release()

        cv2.destroyAllWindows()
        self.update_progress(0)

    def pause_movie(self):

        if self.cap.isOpened():
            self.play = not self.play

        else:
            self.play = False

        if self.play:
            self.button_pause_video.config(text='pause')
        elif not self.play:
            self.button_pause_video.config(text = 'play')





def main():
    vid = VideoPlayer(algo=True,camera=True, image=True)
    vid.command = lambda frame: extract_image(frame)
    vid.mainloop()

def extract_image(matrix_image):
    #apply algo
    resize_image = cv2.resize( matrix_image, dsize=(640, 480), interpolation=cv2.INTER_CUBIC )
    cv2.imshow( 'frame', resize_image )


if __name__ == "__main__":
    main()
