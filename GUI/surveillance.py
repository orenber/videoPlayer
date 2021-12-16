import logging
from GUI.videoPlayer import VideoPlayer
from GUI.frameImg import FrameImg
from GUI.dynamic_panel import DynamicPanel
from GUI.training import Trainer


import numpy as np
import cv2
from tkinter import *
from tkinter import ttk

from tkinter.simpledialog import askstring

from Utility.file_location import *
from Utility.text_to_spech import TextToSpeech
from Utility.logger_setup import setup_logger
from Utility.color_names import COLOR
from skimage import morphology
import Pmw


class Surveillance(VideoPlayer):

    FILE_TYPE = {".AVI", 0,
                 ".MP4", 1}

    def __init__(self, parent: ttk.Frame = None, **kwargs):

        self.log = setup_logger("Surveillance Camera")

        super().__init__(parent,image=True, play=True, camera=True, record=True)

        self.algo_stack = []
        self.frame_take = 0
        self.frame_number = 0
        self.set_gray_image = True
        self.trainer = Trainer

        self._file_name_record = "movement_detect"
        self._output_path_record = full_file(['Resources', 'Record', self._file_name_record])
        self._resolution = '0.02MP'
        self.pri_frame = FrameImg(np.zeros(self.STD_DIMS.get(self._resolution), float))
        self.face = [{'detect': False, 'pos_label': (None, None), 'ROI': {'x': [None, None], 'y': [None, None]}}]
        self.faces_names = []
        self._last_id = None
        self._event_count = 0
        self._threshold_event = 120

        # segment path
        path = os.path.dirname(cv2.__file__)
        face_frontal = os.path.join(path, 'data', 'haarcascade_frontalface_default.xml')
        face_profile = os.path.join(path, 'data', "haarcascade_profileface.xml")

        # cascade classifier
        self.face_cascade = cv2.CascadeClassifier(face_frontal)
        self.profile_cascade = cv2.CascadeClassifier(face_profile)
        self.speak = TextToSpeech()

    def call_event_counter(self, trigger_id:int=123):

        if self._last_id == trigger_id:
            self._event_count += 1

        else:
            # restart counter
            self._event_count -= 1

        if self._threshold_event < self._event_count:
            # restart counter
            self._event_count = 0
            # call event
            name = self.faces_names[trigger_id]
            self.speak.greeting(name)
            self.speak.ask()
            self.speak.run()

        # remember the last id
        self._last_id = trigger_id

    def _build_widget(self, parent: ttk.Frame = None, setup: dict = dict):

       # self.hide()
        self.log.info("start build widget")
        if parent is None:

            self.master.geometry( "950x720+0+0" )
            self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
            # Title bar Title
            self.master.title( "SurveillanceCamera" )
            # Title Bar Icon
            self.icons_path = full_file( ["Icons", "webcamera.ico"] )
            self.master.iconbitmap( self.icons_path )
            # main panel

            self.main_frame = Frame(self.master, relief='sunken',
                                     width=1000,
                                     height=720,
                                     bg="gray24",
                                     name="main_frame" )
            self.main_frame.pack( side=TOP )
            self.main_frame.place( relx=0, rely=0, relwidth=1, relheight=1 )

        else:
            self.main_frame = parent

        super()._build_widget(self.main_frame,setup)

        self.canvas_image.unbind("<Configure>")

        # control panel
        matrix = {"row": [{"col": [0, 0]}]}
        self.dynamic_panel = DynamicPanel(self.canvas_image, matrix)

        self.board.place_forget()
        self.board.destroy()
        self.board = self.dynamic_panel.current_label_image

        self.dynamic_panel.command = lambda: self._focus_label()
        [can.bind("<Configure>", self._resize) for can in self.dynamic_panel.canvas_image]

        # load image button button_load_image
        self.icon_movement_detect = PhotoImage(file=os.path.join(self.icons_path, 'motion-sensor.PNG'))
        self.button_movement_detection = Button(self.control_frame, padx=10, pady=10, bd=8,
                                                fg="white",
                                                font=('arial', 12, 'bold'),
                                                text="movement", bg="black",
                                                image=self.icon_movement_detect,
                                                height=self.icon_height,
                                                width=self.icon_width,
                                                name="button_movement_detection",
                                                command=lambda: self._button_movement_detection_view())
        self.button_movement_detection.pack(side='left')
        button_movement_detection_tooltip = Pmw.Balloon( self.control_frame )
        button_movement_detection_tooltip.bind( self.button_movement_detection, "Movement  detection")

        # load image button_face_detect
        self.icon_face_detect = PhotoImage(file=os.path.join(self.icons_path, 'face_detection.PNG'))
        self.button_face_detection = Button(self.control_frame,
                                            padx=10, pady=10, bd=8,
                                            fg="white",
                                            font=('arial', 12, 'bold'),
                                            text="face", bg="black",
                                            image=self.icon_face_detect,
                                            height=self.icon_height,
                                            width=self.icon_width,
                                            name="button_face_detection",
                                            command=lambda: self._button_face_detection_view())
        self.button_face_detection.pack(side='left')
        button_face_detection_tooltip = Pmw.Balloon(self.control_frame)
        button_face_detection_tooltip.bind(self.button_face_detection, "Face detection")

        # load image button button_ace_recognition
        self.icon_face_recognition = PhotoImage(file=os.path.join(self.icons_path, 'face_recognition.PNG'))
        self.button_face_recognition = Button(self.control_frame,
                                              padx=10, pady=10, bd=8,
                                              fg="white",
                                              font=('arial', 12, 'bold'),
                                              text="body", bg="black",
                                              image=self.icon_face_recognition,
                                              height=self.icon_height,
                                              width=self.icon_width,
                                              name='button_face_recognition',
                                              command=lambda: self._button_face_recognition_view())
        self.button_face_recognition.pack(side='left')
        button_face_recognition_tooltip = Pmw.Balloon(self.control_frame)
        button_face_recognition_tooltip.bind(self.button_face_recognition, "Face recognition")
        #self.button_face_recognition["state"] = "disabled"

        # load image button button_ace_recognition
        self.icon_mask_detection = PhotoImage(file=os.path.join(self.icons_path, 'mask.PNG'))
        self.button_mask_detection = Button(self.control_frame,
                                            padx=10, pady=10, bd=8,
                                            fg="white",
                                            font=('arial', 12, 'bold'),
                                            text="body", bg="black",
                                            image=self.icon_mask_detection,
                                            height=self.icon_height,
                                            width=self.icon_width,
                                            name='button_mask_detection',
                                            command=lambda: self._button_mask_detection_view())
        self.button_mask_detection.pack(side='left')
        button_mask_detection_tooltip = Pmw.Balloon(self.control_frame)
        button_mask_detection_tooltip.bind(self.button_mask_detection, "Mask detection")
        #self.show()

    def _focus_label(self):

        self.board = self.dynamic_panel.current_label_image

    def _button_mask_detection_view(self):

        if self.button_mask_detection.cget('relief') == 'raised':

            self.set_gray_image = False
            self.algo_list(True, self.mask_detection)
            self.button_mask_detection.config(bg='white', relief='sunken')
            self.log.info("Mask detection is On")

        elif self.button_mask_detection.cget('relief') == 'sunken':

            self.algo_list(False, self.mask_detection)
            self.set_gray_image = True
            self.button_mask_detection.config(bg='black', relief='raised')
            self.log.info("Mask detection is Off")

    def _button_movement_detection_view(self):

        if self.button_movement_detection.cget('relief') == 'raised':
            self.algo_list(True, self.movement_detection)
            self.button_movement_detection.config(bg='white', relief='sunken')
            self.log.info("Movement detection is On")

        elif self.button_movement_detection.cget('relief') == 'sunken':
            self.algo_list(False, self.movement_detection)
            self.button_movement_detection.config(bg='black', relief='raised')
            self.log.info("Movement detection is Off")

    def _button_face_detection_view(self):

        if self.button_face_detection.cget('relief') == 'raised':

            self.algo_list(True, self.face_detection)
            self.button_face_detection.config(bg='white', relief='sunken')
            self.log.info("Face detection is on")

        elif self.button_face_detection.cget('relief') == 'sunken':

            self.algo_list(False, self.face_detection)
            self.button_face_detection.config(bg='black', relief='raised')
            self.log.info("Face detection is Off")

    def _button_face_recognition_view(self):

        if self.button_face_recognition.cget('relief') == 'raised':
            self.faces_names = self.trainer.load_labels()
            self.algo_list(True, self.face_recognition)
            self.button_face_recognition.config(bg='white', relief='sunken')
            self.log.info("Face recognition is on")

        elif self.button_face_recognition.cget('relief') == 'sunken':

            self.algo_list(False, self.face_recognition)
            self.button_face_recognition.config(bg='black', relief='raised')
            self.log.info("Face recognition is off")

    def algo_list(self, add: bool = False, algo=None):

        if add:
            if algo not in self.algo_stack:
                self.algo_stack.append(algo)
        else:
            if algo is None:
                pass

            elif algo in self.algo_stack:
                self.algo_stack.remove(algo)

    def _pause_view(self):
        super()._pause_view()
        # condition for crop ROI
        if self.face[0]['detect']:
            self.log.info("detect Face")

            # if face detect and ther is labeling mode

            # write on the image lable
            self.board.bind("<Double-Button>", self.lable_image)

        # creat/open folder and insert image inside

    def lable_image(self, _):

        if self.face[0]['detect']:

            roi = self.face[0]['ROI']
            x = roi['x']
            y = roi['y']
            crop_image = self.frame.image[y[0]:y[1], x[0]:x[1]]
            cv2.imshow('ROI', crop_image)

            label_image = askstring("label", "label the ROI image")
            print(label_image)
            try:
                images_face_path = full_file(["Resources", "images", "faces", label_image])
                create_folder_if_not_exist(str(images_face_path))
                path_file = os.path.join(images_face_path, file_date(label_image, ".png"))
                cv2.imwrite(path_file, crop_image)
                cv2.destroyAllWindows()
            except Exception as error:
                self.log.error(error)
            finally:
                self.dynamic_panel.current_label_image.unbind("<Button>")

    def run_frames(self):

        self.log.info("run frame by frame")
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

                        self._update_progress(self.frame_number)

                        # take the image and sand it to the list of function to analyze process
                        algo_list = self.algo_stack
                        algo_nums = len(algo_list)

                        if algo_nums:

                            if self.set_gray_image:
                                # convert two images to gray scale
                                image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

                            for n in range(0, algo_nums):
                                algo_list[n](image)

                        # self.face_detection(frame_gray)
                        # convert matrix image to pillow image object
                        self.resize_image_show(self.frame)
                       
                        # refresh image display
                    elif not ret:
                        break
                self.board.update()
        except Exception as error:
            self.log.exception(error)
        finally:
            self._cap.release()
            self._out.release()
            cv2.destroyAllWindows()
            self._button_view_off()

    def movement_detection(self, gray_image: np.array):

        if self.frame_number == 1:
            self.pri_frame.image = gray_image

        # subtract one image from another
        sub = cv2.absdiff(gray_image, self.pri_frame.image)

        # convert the product image to binary image
        (thresh, blackAndWhiteImage) = cv2.threshold(sub, 30, 255, cv2.THRESH_BINARY)

        # save the last frame
        self.pri_frame.image = gray_image

        # label image
        label_image = morphology.label(blackAndWhiteImage)

        # remove noise
        image_clear = morphology.remove_small_objects(label_image, min_size=100, connectivity=1)

        # record if thar is movement
        self.record_movement(gray_image, image_clear)

    def face_detection(self, gray_image: np.array):

        # detect the faces
        faces = self.face_cascade.detectMultiScale(gray_image, 1.1, 4)
        self.face = [{'detect': False, 'pos_label': (None, None),
                      'ROI': {'x': [None, None], 'y': [None, None]}} for _ in range(len(faces))]
        # Draw the rectangle around each face
        for count, (x, y, w, h) in enumerate(faces):

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
            id_, conf = self.trainer.recognizer.predict(roi_gray)
            if conf >= self.trainer.confident:
                name = self.faces_names[id_]

                # take the roi corrdinet x and y
                points_start = (x, y)
                points_end = (x + w, y + h)
                cv2.putText(self.frame.image, name, points_start,
                            cv2.FONT_HERSHEY_SIMPLEX, 1, COLOR['white'], 2, cv2.LINE_AA)
                # draw rectangle around the faces
                cv2.rectangle(self.frame.image, points_start, points_end, COLOR['blue'], 2)
                self.call_event_counter(id_)

    def mask_detection(self, rgb_image: np.array):

        # detect faces in the frame and determine if they are wearing a
        # face mask or not
        (locs, preds) = self.trainer.mask_detector.detect_and_predict_mask(rgb_image)

        # loop over the detected face locations and their corresponding
        # locations
        for (box, pred) in zip(locs, preds):

            # unpack the bounding box and predictions
            (startX, startY, endX, endY) = box
            (mask, withoutMask) = pred

            # determine the class label and color we'll use to draw
            # the bounding box and text
            label = "Mask" if mask > withoutMask else "No Mask"
            color = (0, 255, 0) if label == "Mask" else (0, 0, 255)

            # include the probability in the label
            label = "{}: {:.2f}%".format(label, max( mask, withoutMask ) * 100)

            # display the label and bounding box rectangle on the output
            # frame
            cv2.putText(self.frame.image, label, (startX, startY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
            cv2.rectangle(self.frame.image, (startX, startY), (endX, endY), color, 2)

    def record_movement(self, frame: np.array, image_noise_movement: np.array):

        # in the case thar is blob above the threshold ->  trigger record function
        if np.any(image_noise_movement) and self.frame_take < 150:
            # record
            self.frame_take += 5

        if self.frame_take > 0:
            if self.button_record.cget("relief") == 'raised':
                self.camera_recording(file_date(self._output_path_record, self._file_type_record))
                self._record_view_state(True)

            self.save_frame(frame)
            self.frame_take -= 1
            cv2.imshow('record', frame)

        elif self.frame_take == 0:
            self._record_view_state(False)

    def save_frame(self, frame: np.array):
        try:

            self._out.write(frame)
        except Exception as error:
            self.log.error(error)


def main():
    vid = Surveillance()
    vid.mainloop()


if __name__ == "__main__":
    main()
