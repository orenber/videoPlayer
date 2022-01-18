from GUI.videoPlayer import VideoPlayer
from GUI.frameImg import FrameImg
from GUI.dynamic_panel import DynamicPanel
from Algo.face_trainer import FaceTrainer

import numpy as np
import cv2
from skimage import morphology

from tkinter import *
from tkinter import ttk
from tkinter.simpledialog import askstring
import Pmw

from Utility.file_location import *
from Utility.text_to_spech import TextToSpeech
from Utility.logger_setup import setup_logger
from Utility.display_widget import center_widget
from Utility.image_procesing import test_camera_device

import threading


class Surveillance(VideoPlayer):

    FILE_TYPE = {".AVI", 0,
                 ".MP4", 1}

    def __init__(self, parent: ttk.Frame = None, **kwargs):

        self.log = setup_logger("Surveillance Camera")

        self.frame_rate_option = [24, 30, 40, 45]

        super().__init__(parent,image=True, play=True, camera=True, record=True)

        self.algo_stack = []
        self.frame_take = 0
        self.frame_number = 0

        self.set_gray_image = True
        self.trainer = FaceTrainer()

        self._file_name_record = "movement_detect"
        self._output_path_record = full_file(['Resources', 'Record', self._file_name_record])
        self._record_color = 1
        self._resolution = '0.02MP'
        self.pri_frame = FrameImg(np.zeros(self.STD_DIMS.get(self._resolution), float))
        self.faces_names = []
        self._event_count = 0
        self._threshold_event = 120


        # segment path
        # cascade classifier
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

    def _show_menu(self, e):

        self.menu_camera.post(e.x_root, e.y_root)

    def _show_video_capture_device(self, camera_ports):
        self.camera_port_num = IntVar(value=0)
        for device in range(0,camera_ports,1):
            exist = test_camera_device(device)
            if exist:

                self.menu_camera.add_checkbutton(label="Camera: " + str(device),
                                          onvalue = device, variable=self.camera_port_num,
                                          command=lambda: self.connect_camera_device(self.camera_port_num))
                self.menu_camera.add_cascade(menu = self.menu_frame_rate,label="Frame Rate")

                self.menu_camera.add_cascade(label="Resolution", menu=self.menu_res)
                self.menu_camera.add_separator()


    def connect_camera_device(self, cam):

        self._camera_port = cam.get()
        self.log.info("connect to camera port:" + str(self._camera_port))


    def _build_widget(self, parent: ttk.Frame = None, setup: dict = dict):

        #self.hide()
        self.log.info("start build widget")
        if parent is None:

            self.master.geometry(center_widget(self.master,950,720))
            self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
            # Title bar Title
            self.master.title("SurveillanceCamera")
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

        self.menu_camera = Menu(self.board, tearoff=0)
        self.menu_frame_rate = Menu(self.board, tearoff=0)
        self.menu_res = Menu(self.board, tearoff=0)

        self.frame_rate_value = StringVar()

        for frame_rate in self.frame_rate_option:
            self.menu_frame_rate.add_checkbutton(label=str(frame_rate), onvalue=frame_rate,
                                            command=self.select_frame_rate, variable=self.frame_rate_value)

            # resolution

        self.resolution_value = StringVar()

        for res, value in self.STD_DIMS.items():
            self.menu_res.add_checkbutton( label=str( res ) + ': ' + str( value ), onvalue=str( res ),
                                             command=self.select_resolution,
                                             variable=self.resolution_value )

        self._show_video_capture_device(5)

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

    def select_frame_rate(self):
        self.frame_rate = int(self.frame_rate_value.get())
        self.log.info("Frame rate selected :" + self.frame_rate_value.get())


    def select_resolution(self):

        self.resolution = self.resolution_value.get()
        self.image_size_camera = self.resolution
        self._size_image = self.STD_DIMS.get(self._resolution)
        self.log.info("Resolution selected :" + self.resolution)


    def _focus_label(self):

        self.board = self.dynamic_panel.current_label_image
        self.board.bind("<Button-3>", self._show_menu)
        self.pack()

    def _button_mask_detection_view(self):

        if self.button_mask_detection.cget('relief') == 'raised':

            self.set_gray_image = False
            self.algo_list(True, self.trainer.mask_detection)
            self.button_mask_detection.config(bg='white', relief='sunken')
            self.log.info("Mask detection is On")

        elif self.button_mask_detection.cget('relief') == 'sunken':

            self.algo_list(False, self.trainer.mask_detection)
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

            self.algo_list(True, self.trainer.face_detection)
            self.button_face_detection.config(bg='white', relief='sunken')
            self.log.info("Face detection is on")

        elif self.button_face_detection.cget('relief') == 'sunken':

            self.algo_list(False, self.trainer.face_detection)
            self.button_face_detection.config(bg='black', relief='raised')
            self.log.info("Face detection is Off")

    def _button_face_recognition_view(self):

        if self.button_face_recognition.cget('relief') == 'raised':
            self.faces_names = self.trainer.load_labels()
            self.algo_list(True, self.trainer.face_recognition)
            self.button_face_recognition.config(bg='white', relief='sunken')
            self.log.info("Face recognition is on")

        elif self.button_face_recognition.cget('relief') == 'sunken':

            self.algo_list(False, self.trainer.face_recognition)
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

                        if self._record:
                            self.save_frame( image )

                        # take the image and sand it to the list of function to analyze process
                        algo_list = self.algo_stack
                        algo_nums = len(algo_list)

                        if algo_nums:

                            if self.set_gray_image:
                                # convert two images to gray scale
                                image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

                            for n in range(0, algo_nums):
                                algo_list[n](image, self.frame.image)

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

    def movement_detection(self, gray_image: np.ndarray, _):

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

    def record_movement(self, frame: np.array, image_noise_movement: np.array):

        # in the case thar is blob above the threshold ->  trigger record function
        if np.any(image_noise_movement) and self.frame_take < 150:
            # record
            self.frame_take += 5

        if self.frame_take > 0:
            if self.button_record.cget("relief") == 'raised':
                self.camera_recording(file_date(self._output_path_record, self._file_type_record))
                self._record_view_state(True)

            self.save_frame(self.frame.image)
            self.frame_take -= 1
            cv2.imshow('record', frame)

        elif self.frame_take == 0:
            self._record_view_state(False)


def main():
    vid = Surveillance()
    vid.mainloop()


if __name__ == "__main__":
    main()
