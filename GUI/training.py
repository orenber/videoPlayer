
from GUI.dynamic_panel import DynamicPanel
from GUI.videoPlayer import VideoPlayer
from Algo.face_trainer import FaceTrainer
from tkinter import *
from tkinter import ttk, filedialog
from Utility.file_location import *
from Utility.logger_setup import setup_logger
from Utility.display_widget import center_widget
import cv2
import Pmw


class Trainer(VideoPlayer):

    def __init__(self, parent: ttk.Frame = None, **kwargs):
        self.log = setup_logger('TrainerGUI')
        self.setup = self.set_setup(kwargs)
        super().__init__(parent, play=True, camera=True)

        self.face = FaceTrainer()

        self.set_gray_image = True

        self.faces_names = []
        self.algo_stack = []

    @property
    def training(self) -> bool:
        return self._training

    @training.setter
    def training(self, train: bool = False):
        self._training = train

    @property
    def confident(self) -> int:
        return self._confident

    @confident.setter
    def confident(self, conf: int = 45) -> None:
        self._confident = conf

    @staticmethod
    def set_setup(prop: dict) -> dict:

        default = {'play': True, 'camera': True}
        setup = default.copy()
        setup.update(prop)
        return setup

    def _build_widget(self, parent: ttk.Frame = None, setup: dict = dict):

        if parent == None:

            self.master.geometry(center_widget(self.master,950,720))
            # create Main Frame
            self._main_frame = Frame(self.master, relief='sunken',
                                     width=1000,
                                     height=720,
                                     bg="gray24",
                                     name="main_frame" )
            self._main_frame.pack( side=TOP )
            self._main_frame.place( relx=0, rely=0, relwidth=1, relheight=1 )
        else:
            self._main_frame = parent

        self._icons_path = full_file(["Icons"])

        # control Frame
        self._frame_control = Frame(self._main_frame, bg="gray70", width=100)
        self._frame_control.pack(side=RIGHT, fill=Y, expand=0)

        self._frame_control_x = Frame( self._main_frame, bg="gray70")
        self._frame_control_x.pack( side=BOTTOM, fill=X, expand=0 )

        if self.setup['play']:
            # play video button button_live_video
            self.icon_play = PhotoImage( file=os.path.join( self._icons_path, 'play.PNG' ) )
            self.button_play_video = Button( self._frame_control,
                                             text="Load Video",
                                             image=self.icon_play,
                                             command=lambda: self.load_movie() )
            self.button_play_video.pack(side=TOP)
            button_camera_tooltip = Pmw.Balloon( self._frame_control )
            button_camera_tooltip.bind( self.button_play_video, "Load video and play" )

            # play camera
        if self.setup['camera']:
            self.icon_camera = PhotoImage( file=os.path.join( self._icons_path, 'camera.PNG' ) )
            self.button_camera = Button( self._frame_control,
                                         text="camera",
                                         image=self.icon_camera,
                                         command=lambda: self._camera_view())
            self.button_camera.pack( side=TOP )
            button_camera_tooltip = Pmw.Balloon( self._frame_control)
            button_camera_tooltip.bind( self.button_camera, "Camera player")

            # load image button_face_detect
        self.icon_face_detect = PhotoImage(file=os.path.join(self._icons_path, 'face_detection.PNG'))
        self.button_face_detection = Button(self._frame_control,
                                            text="face",
                                            image=self.icon_face_detect,
                                            name="button_face_detection",
                                            command=lambda: self._view_button_face_detection())
        self.button_face_detection.pack(side=TOP)
        button_face_detection_tooltip = Pmw.Balloon(self._frame_control)
        button_face_detection_tooltip.bind(self.button_face_detection, "Face detection")



        # botton train algo
        # icon open images folders
        self._icon_train = PhotoImage(file=os.path.join(self._icons_path, 'ai.PNG'))
        self._button_train = Button(self._frame_control,
                                    text="Train",
                                    image=self._icon_train,
                                    command=lambda: self._view_train_face_detection())
        self._button_train.pack(side=TOP)
        button_train_tooltip = Pmw.Balloon(self._frame_control)
        button_train_tooltip.bind(self._button_train, "Training data Mode")

        # botton show images
        # icon open images folders
        self._icons_open = PhotoImage(file=os.path.join(self._icons_path, 'folder_open.PNG'))
        self._button_open_images = Button(self._frame_control,
                                          text="Open",
                                          image=self._icons_open,
                                          command=lambda: self.open_folders(),
                                          relief='raised')
        self._button_open_images.pack(side=TOP)
        button_open_tooltip = Pmw.Balloon(self._frame_control)
        button_open_tooltip.bind(self._button_open_images, "Open images main folders")

        # botton run
        # icon open images folders
        self._icon_facial_recognition = PhotoImage(file=os.path.join(self._icons_path, 'face_recognition.PNG'))
        self._button_face_recognition = Button(self._frame_control,
                                               text="Run Test",
                                               image=self._icon_facial_recognition,
                                               command=lambda: self._view_button_face_recognition())
        self._button_face_recognition.pack(side=TOP)
        self._button_face_recognition["state"] = "disabled"
        button_face_recognition_tooltip = Pmw.Balloon(self._frame_control)
        button_face_recognition_tooltip.bind(self._button_face_recognition, "Run live video face recognition")


        # button mask live detection
        self._icon_mask = PhotoImage(file=os.path.join(self._icons_path, 'mask.PNG'))
        self._button_mask_detection = Button(self._frame_control,
                                         text="Mask Video",
                                         image=self._icon_mask,
                                         command=lambda: self._view_button_mask_detection())
        self._button_mask_detection.pack(side=TOP)

        button_mask_video_tooltip = Pmw.Balloon(self._frame_control)
        button_mask_video_tooltip.bind(self._button_mask_detection, "Run face mask detection live video")




        # create canvas
        self._canvas = Canvas(self._main_frame,
                              bg="gray24")
        self._canvas.pack(side=LEFT,
                          fill=BOTH,
                          expand=1)
        # add scrollbar to the canvas
        self._scroll_bar_y = ttk.Scrollbar(self._main_frame,
                                           orient=VERTICAL,
                                           command=self._canvas.yview)
        self._scroll_bar_y.pack(side=RIGHT, fill=Y)
        scroll_bar_y_tooltip = Pmw.Balloon(self._frame_control)
        scroll_bar_y_tooltip.bind(self._scroll_bar_y, "Scroll images in y direction")

        # add scrollbar in the x direction
        self._scroll_bar_x = ttk.Scrollbar(self._frame_control_x,
                                           orient=HORIZONTAL,
                                           command=self._canvas.xview)
        self._scroll_bar_x.pack(side=TOP, fill=X, expand=0)
        scroll_bar_x_tooltip = Pmw.Balloon(self._frame_control_x)
        scroll_bar_x_tooltip.bind(self._scroll_bar_x, "Scroll images in x direction")


        # Configure the canvas
        self._canvas.configure(yscrollcommand=self._scroll_bar_y,
                               xscrollcommand=self._scroll_bar_x)
        self._canvas.bind('<Configure>', lambda e: self._canvas.configure(scrollregion=self._canvas.bbox("all")))

        # create another frame inside the canvas
        self._frame_display = Frame(self._canvas)
        # image gallery
        matrix = {"col": [{"nrow": 0*[0]}]}

        self._image_gallery = DynamicPanel(self._frame_display, matrix)
        # Add that new frame to aWindow in The Canvas
        self._canvas.create_window((0, 0), window=self._frame_display, anchor="nw")

    def algo_list(self, add: bool = False, algo=None):

        if add:
            if algo not in self.algo_stack:
                self.algo_stack.append(algo)
        else:
            if algo is None:
                pass

            elif algo in self.algo_stack:
                self.algo_stack.remove(algo)

    def _view_button_face_detection(self):

        if self.button_face_detection.cget('relief') == 'raised':

            # self.algo_list(True, self.face_detection)
            self.algo_list(True, self.face.face_detection)
            self.button_face_detection.config(bg='white', relief='sunken')
            self.log.info("Face detection is on")

        elif self.button_face_detection.cget('relief') == 'sunken':

            # self.algo_list(False, self.face_detection)
            self.algo_list(False, self.face.face_detection)
            self.button_face_detection.config(bg='black', relief='raised')
            self.log.info("Face detection is Off")

    def _view_train_face_detection(self):
        if self._button_train.cget('relief') == 'raised':
            self.face.training = True
            self._button_train.config(relief=SUNKEN)
        elif self._button_train.cget('relief') == SUNKEN:
            self.face.training = False
            self._button_train.config(relief=RAISED)

    def _view_button_face_recognition(self):
        if self._button_face_recognition.cget('relief') == RAISED:
            self.faces_names = self.face.load_labels()
            self.algo_list(True, self.face.face_recognition)

            self._button_face_recognition.config(relief=SUNKEN)
            self.log.info("Face recognition is on")

        elif self._button_face_recognition.cget('relief') == SUNKEN:

            self.algo_list(False, self.face.face_recognition)

            self._button_face_recognition.config(relief=RAISED)
            self.log.info("Face recognition is off")

    def _view_button_mask_detection(self):
        if self._button_mask_detection.cget('relief') == RAISED:
            self.set_gray_image = False
            self.algo_list(True, self.face.mask_detection)

            self._button_mask_detection.config(relief=SUNKEN)
            self.log.info("Mask detection is on")

        elif self._button_mask_detection.cget('relief') == SUNKEN:
            self.algo_list(False, self.face.mask_detection)
            self.set_gray_image = True
            self._button_mask_detection.config(relief=RAISED)
            self.log.info("Mask detection is off")

    def show_images(self, label_images: dict):

        # get label n        um

        # get images num
        # build matrix
        matrix = self.get_matrix_gallery(label_images)
        # update image gallery
        self._image_gallery.update_widget(matrix)

        # set label names
        self._image_gallery.set_names(self.face.ids_label)

        # show images on the canvas
        for label, images in label_images.items():
            row_index =0
            id_column = int(label)
            for image in images:
                self._image_gallery.update_image( image,id_column ,row_index )
                row_index += 1
        pass

    @staticmethod
    def get_matrix_gallery(label_images:dict)->dict:

        row_nums = map(len, label_images.values())
        rows = max(list(row_nums))
        matrix = {"col": []}
        for col_count,keys in enumerate(list(label_images.keys())):
            matrix['col'].append({'row': [col_count] * rows} )

        return matrix

    def open_folders(self):

        path_image_name = filedialog.askdirectory(title="Select the images folders")

        if len(path_image_name) != 0:
            try:
                self.face.collect_images(path_image_name)
                self.face.train_face_detection()
                self.show_images(self.face.label_images)
                self._button_face_recognition["state"] = "normal"

            except Exception as error:
                self._button_face_recognition["state"] = "disable"
                self.log.exception(error)

    def load_movie(self, movie_filename: str = ''):

        super().load_movie(movie_filename)

    def _camera_view(self):

        self.button_camera.config(relief='sunken')
        self.camera_capture()
        self.button_camera.config(relief='raised')

    def camera_capture(self):

        super().camera_capture()

    def play_movie(self, movie_filename: str):

        super().play_movie(movie_filename)

    def run_frames(self):

        self.log.info("run frame by frame")

        try:

            while self._cap.isOpened():

                if self._play:

                    # update the frame number
                    ret, image = self._cap.read()

                    if ret:
                        self.frame.image = image
                        # take the image and sand it to the list of function to analyze process
                        algo_list = self.algo_stack
                        algo_nums = len(algo_list)

                        if algo_nums:

                            if self.set_gray_image:
                                image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY )

                            for n in range(0, algo_nums):
                                algo_list[n](image, self.frame.image)

                        # self.face_detection(frame_gray)
                        # convert matrix image to pillow image object
                        # display image and plot
                        cv2.imshow('frame', self.frame.image)
                        # press quite to Exit the loop
                        if cv2.waitKey(20) & 0xFF == ord('q'):
                            break

                        # refresh image display
                    elif not ret:
                        break

        except Exception as error:
            self.log.exception(error)
        finally:
            self.stop_video()

    def stop_video(self):

        if self._play:
            self._play = False
            self._cap.release()
            self._out.release()

        cv2.destroyAllWindows()

        pass


def main():
    trainer = Trainer()
    trainer.mainloop()


if __name__ == "__main__":
    main()



