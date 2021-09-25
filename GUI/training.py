
from GUI.dynamic_panel import DynamicPanel
from GUI.videoPlayer import VideoPlayer

from tkinter import *
from tkinter import ttk, filedialog
from Utility.file_location import *
from Utility.logger_setup import setup_logger
from Utility.color_names import COLOR
import cv2
from PIL import Image
import numpy as np
import pickle
import Pmw

try:
    from Algo.detect_mask_video import MaskDetection
except Exception as error:
    print(error)


class Trainer(VideoPlayer):

    def __init__(self, parent: ttk.Frame = None, **kwargs):
        self.log = setup_logger('Trainer')
        self.setup = self.set_setup(kwargs)
        super().__init__(play=True, camera=True)

        ttk.Frame.__init__(self, parent)

        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.path = os.path.dirname(cv2.__file__)
        self.face_frontal_path = os.path.join(self.path, 'data', 'haarcascade_frontalface_default.xml' )
        self.face_cascade = cv2.CascadeClassifier(self.face_frontal_path)
        self._path_images = full_file(["Resources", "images", "faces"])

        self.set_gray_image = True

        self.face = [{'detect': False, 'pos_label': (None, None), 'ROI': {'x': [None, None], 'y': [None, None]}}]
        self.faces_names = []
        self._last_id = None
        self.current_id = 0
        self.label_ids = {}
        self.ids_label = {}
        self.y_labels = []
        self.x_train = []
        self.label_images = {}
        self.algo_stack = []
        self._id = 0

        self._confident = 45
        self._training = False
        self._image_size = (200, 200)

        try:
            self.mask_detector = MaskDetection()
        except Exception as error:
            self.log.exception(error)

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
        self.hide()
        if parent == None:

            self.master.geometry("470x700+0+0")
        else:
            self.master = parent

        self._icons_path = full_file(["Icons"])

        # create Main Frame
        self._main_frame = Frame(self.master, bg="gray70")
        self._main_frame.pack(fill=BOTH, expand=1)

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
            self.button_play_video.pack( side=TOP )
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

        self.show()

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

            self.algo_list(True, self.face_detection)
            self.button_face_detection.config(bg='white', relief='sunken')
            self.log.info("Face detection is on")

        elif self.button_face_detection.cget('relief') == 'sunken':

            self.algo_list(False, self.face_detection)
            self.button_face_detection.config(bg='black', relief='raised')
            self.log.info("Face detection is Off")

    def _view_train_face_detection(self):
        if self._button_train.cget('relief') == 'raised':
            self.training = True
            self._button_train.config( relief=SUNKEN)
        elif self._button_train.cget('relief') == SUNKEN:
            self.training = False
            self._button_train.config( relief=RAISED)

    def _view_button_face_recognition(self):
        if self._button_face_recognition.cget('relief') == RAISED:
            self.faces_names = self.load_labels()
            self.algo_list(True, self.face_recognition)

            self._button_face_recognition.config(relief=SUNKEN)
            self.log.info("Face recognition is on")

        elif self._button_face_recognition.cget('relief') == SUNKEN:

            self.algo_list(False, self.face_recognition)

            self._button_face_recognition.config(relief=RAISED)
            self.log.info("Face recognition is off")

    def _view_button_mask_detection(self):
        if self._button_mask_detection.cget('relief') == RAISED:
            self.set_gray_image = False
            self.algo_list(True, self.mask_detection)

            self._button_mask_detection.config(relief=SUNKEN)
            self.log.info("Mask detection is on")

        elif self._button_mask_detection.cget('relief') == SUNKEN:
            self.algo_list(False, self.mask_detection)
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
        self._image_gallery.set_names(self.ids_label)

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
                self.collect_images(path_image_name)
                self.train_face_detection()
                self.show_images(self.label_images)
                self._button_face_recognition["state"] = "normal"

            except Exception as error:
                self._button_face_recognition["state"] = "disable"
                self.log.exception(error)

    def reset_parameters(self):
        self.current_id = 0
        self.label_ids = {}
        self.y_labels = []
        self.x_train = []
        self.label_images = {}
        self._id = 0
        self.ids_label = {}


    def collect_images(self, images_dir: str):

        self.reset_parameters()
        self._path_images = images_dir

        for root, dirs, files in os.walk(images_dir):
            for file in files:
                if file.endswith("png") or file.endswith("jpg"):
                    path = os.path.join(root, file)
                    label = os.path.basename(os.path.dirname(path)).replace(" ", ".").lower()

                    if label not in self.label_ids:

                        self.ids_label[self.current_id] = label
                        self.label_ids[label] = self.current_id
                        self.current_id += 1
                    self._id = self.label_ids[label]
                    self.label_images[str(self._id)] = []

                    # convert to gray scale
                    pil_image = Image.open(path).convert("L")
                    # resize images to the same size
                    image_resize = pil_image.resize(self._image_size, Image.ANTIALIAS)
                    # convert image to numpy array
                    image_array = np.array(image_resize, "uint8")

                    self.collect_faces(image_array)

        with open("labels.pickle", 'wb') as f:
            pickle.dump(self.label_ids, f)
        
        for label, image in zip(self.y_labels, self.x_train):
            self.label_images[str(label)].append(image)

    def crop_faces(self, image_array):

        faces = self.face_cascade.detectMultiScale(image_array, scaleFactor=1.5, minNeighbors=5)

        for (x, y, w, h) in faces:
            roi = image_array[y:y + h, x:x + w]
            self.x_train.append(roi)
            self.y_labels.append(self._id)

    def collect_faces(self, face_roi):

        self.x_train.append(face_roi)
        self.y_labels.append(self._id)

    def train_face_detection(self):

        try:
            self.recognizer.train(self.x_train, np.array(self.y_labels))
            self.recognizer.save("trainner.yml")
        except Exception as error:
            self.log.debug(error)

    def save_roi_faces(self, image: np.array, path: str=''):

        try:
            # crop the region of interest ( faces in the images)
            folder_unknown = full_file([self._path_images, 'unknown'])
            create_folder_if_not_exist(folder_unknown)
            cv2.imwrite(file_date(os.path.join(folder_unknown, "unknown"), '.png'), image)

        except Exception as error:
            self.log.debug(error)

    @staticmethod
    def load_labels()->list:

        with open("labels.pickle", 'rb') as f:
            og_labels = pickle.load(f)
            labels = {v: k for k, v in og_labels.items()}
        return labels

    def face_detection(self, gray_image: np.array):

        # detect the faces
        faces = self.face_cascade.detectMultiScale(gray_image, 1.1, 4)
        self.face = [{'detect': False, 'pos_label': (None, None),
                      'ROI': {'x': [None, None], 'y': [None, None]}} for _ in range(len(faces))]
        # Draw the rectangle around each face
        for count, (x, y, w, h) in enumerate(faces):

            if self._training:
                # detect ROI face
                roi = gray_image[y:y + h, x:x + w]
                self.crop_faces(roi)
                self.save_roi_faces(roi)

            self.face[count] = {'detect': True, 'ROI': {'x': (x, x + w), 'y': (y, y + h)}, 'pos_label': (x + 6, y - 6)}
            cv2.rectangle(self.frame.image, (x, y), (x+w, y+h), COLOR['blue'], 2)
            cv2.putText(self.frame.image, 'Face', self.face[count]['pos_label'],
                        cv2.FONT_HERSHEY_DUPLEX, 0.5, COLOR['green'], 1)

    def face_recognition(self, gray_image: np.array):

        # detect faces in the image
        faces = self.face_cascade.detectMultiScale(gray_image, scaleFactor=1.5, minNeighbors=5)
        # go over all the face and plot the rectangle around
        for (x, y, w, h) in faces:

            # detect ROI face
            roi_gray = gray_image[y:y + h, x:x + w]

            # recognizer deep learned model predict keras tensorflow pytorch scikit learn
            id_, conf = self.recognizer.predict(roi_gray)

            if conf >= self._confident:
                name = self.faces_names[id_]

                # take the roi corrdinet x and y
                points_start = (x, y)
                points_end = (x + w, y + h)
                cv2.putText(self.frame.image, name, points_start,
                             cv2.FONT_HERSHEY_SIMPLEX, 1, COLOR['white'], 2, cv2.LINE_AA )
                # draw rectangle around the faces
                cv2.rectangle( self.frame.image, points_start, points_end, COLOR['blue'], 2 )



    def mask_detection(self, rgb_image: np.array):

        # detect faces in the frame and determine if they are wearing a
        # face mask or not
        (locs, preds) = self.mask_detector.detect_and_predict_mask(rgb_image)

        # loop over the detected face locations and their corresponding
        # locations
        for (box, pred) in zip(locs, preds):

            # unpack the bounding box and predictions
            (startX, startY, endX, endY) = box
            (mask, withoutMask) = pred

            # determine the class label and color we'll use to draw
            # the bounding box and text
            label = "Mask" if mask > withoutMask else "No Mask"
            color = COLOR["green"] if label == "Mask" else COLOR["red"]

            # include the probability in the label
            label = "{}: {:.2f}%".format(label, max( mask, withoutMask ) * 100)

            # display the label and bounding box rectangle on the output
            # frame
            cv2.putText(self.frame.image, label, (startX, startY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
            cv2.rectangle(self.frame.image, (startX, startY), (endX, endY), color, 2)

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
                                algo_list[n](image)

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



