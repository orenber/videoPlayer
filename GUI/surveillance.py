from GUI.videoPlayer import VideoPlayer
from GUI.frameImg import FrameImg
from GUI.dynamic_panel import DynamicPanel
import numpy as np
import cv2
from tkinter import *
from tkinter import ttk, messagebox
import keyboard
import copy as copy

from Utility.file_location import *
from skimage import morphology


class Surveillance(VideoPlayer):

    COLOR = {'red':   (0, 0, 255),
             'blue':  (255, 0, 0),
             'green': (0, 255, 0)}

    FILE_TYPE = {".AVI", 0,
                 ".MP4", 1}

    def __init__(self):
        super().__init__(image=True, play=True, camera=True, record=True)

        self.algo_stack = []
        self.frame_take = 0
        self.frame_number = 0

        self._file_name_record = "movement_detect"
        self._output_path_record = full_file(['Resources', 'Record', self._file_name_record])

        self.pri_frame = FrameImg(np.zeros(self.STD_DIMS.get('0.3MP'), float))
        self.face = [{'detect': False, 'pos_label': (None, None), 'ROI': {'x': [None, None], 'y': [None, None]}}]


        # segment path
        path = os.path.dirname(cv2.__file__)
        face_frontal = os.path.join(path, 'data', 'haarcascade_frontalface_default.xml')
        face_profile = os.path.join(path, 'data', "haarcascade_profileface.xml")

        # cascade classifier
        self.face_cascade = cv2.CascadeClassifier(face_frontal)
        self.profile_cascade = cv2.CascadeClassifier(face_profile)

    def _build_widget(self, parent: ttk.Frame = None, setup: dict = dict):

        self.master.geometry("950x720+0+0")
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        # main panel

        self.main_panel = Frame(width=1000, height=720, bg="gray24", relief="raised", name="main_panel")
        self.main_panel.pack(side=TOP)
        self.main_panel.place(relx=0, rely=0, relwidth=1, relheight=1)

        super()._build_widget(self.main_panel, setup)

        self.canvas_image.unbind("<Configure>")

        # control panel
        matrix = {"row": [{"col": [0, 0]}]}
        self.dynamic_panel = DynamicPanel(self.canvas_image, matrix)

        self.board.place_forget()
        self.board.destroy()
        self.board = self.dynamic_panel.current_label_image
        self.board.pack(fill=BOTH, expand=True)

        self.dynamic_panel.command = lambda: self._focus_label()
        [can.bind("<Configure>", self._resize) for can in self.dynamic_panel.canvas_image]

        # load image button button_load_image
        # self.icon_algo = PhotoImage( file=os.path.join( icons_path, 'algo.PNG' ) )
        self.button_movement_detection = Button(self.control_frame, padx=10, pady=10, bd=8, fg="white",
                                                font=('arial', 12, 'bold'),
                                                text="movement", bg="black", height=1, width=8,
                                                name="button_movement_detection",
                                                command=lambda: self._button_movement_detection_view())
        self.button_movement_detection.pack(side='left')

        # load image button_load_image
        # self.icon_algo = PhotoImage( file=os.path.join( icons_path, 'algo.PNG' ) )
        self.button_face_detection = Button(self.control_frame, padx=10, pady=10, bd=8, fg="white",
                                            font=('arial', 12, 'bold'),
                                            text="face", bg="black", height=1, width=8,
                                            name="button_face_detection",
                                            command=lambda: self._button_face_detection_view())
        self.button_face_detection.pack(side='left')

        # load image button button_load_image
        # self.icon_algo = PhotoImage( file=os.path.join( icons_path, 'algo.PNG' ) )
        self.button_profile_face_detection = Button(self.control_frame, padx=10, pady=10, bd=8, fg="white",
                                                    font=('arial', 12, 'bold'),
                                                    text="body", bg="black", height=1, width=8,
                                                    name='button_profile_face_detection',
                                                    command=lambda: self._button_profile_face_detection_view())
        self.button_profile_face_detection.pack(side='left')

    def _focus_label(self):

        self.board = self.dynamic_panel.current_label_image

    def _button_movement_detection_view(self):

        if self.button_movement_detection.cget('relief') == 'raised':
            self.algo_list(True, self.movement_detection)
            self.button_movement_detection.config(bg='white', relief='sunken')

        elif self.button_movement_detection.cget('relief') == 'sunken':
            self.algo_list(False, self.movement_detection)
            self.button_movement_detection.config(bg='black', relief='raised')

    def _button_face_detection_view(self):

        if self.button_face_detection.cget('relief') == 'raised':

            self.algo_list(True, self.face_detection)
            self.button_face_detection.config(bg='white', relief='sunken')

        elif self.button_face_detection.cget('relief') == 'sunken':

            self.algo_list(False, self.face_detection)
            self.button_face_detection.config(bg='black', relief='raised')

    def _button_profile_face_detection_view(self):

        if self.button_profile_face_detection.cget('relief') == 'raised':

            self.algo_list(True, self.profile_detection)
            self.button_profile_face_detection.config(bg='white', relief='sunken')

        elif self.button_profile_face_detection.cget('relief') == 'sunken':

            self.algo_list(False, self.profile_detection)
            self.button_profile_face_detection.config(bg='black', relief='raised')

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

            # if face detect and ther is labeling mode

            # write on the image lable
            cv2.setMouseCallback(self.lable_image())

        # creat/open folder and insert image inside

    def lable_image(self):

        lable_position = list(self.face[0]['pos_label'])
        frame = copy.copy(self.frame)
        text = []
        while self.face[0]['detect']:

            self.resize_image_show(frame)

            # wait for keypress
            key = keyboard.read_key()
            if key == 'BackSpace':
               text.pop[-1]

            if key == 'Enter':
                # in the case Enter press

                if messagebox.askokcancel("Cancel", "Do you want to Crop ROI Image?"):
                    pass
                    # crop face ROI and ask the user for permission

    def run_frames(self):

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

                            # convert two images to gray scale
                            gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

                            for n in range(0, algo_nums):
                                algo_list[n](gray_image)

                        # self.face_detection(frame_gray)
                        # convert matrix image to pillow image object
                        self.resize_image_show(self.frame)
                       
                        # refresh image display
                    elif not ret:
                        break
                self.board.update()
        except Exception as error:
            print(error)
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
        self.face = [{'detect': False, 'pos_label': (None, None), 'ROI': {'x': [None, None], 'y': [None, None]}} for k
                     in range(len(faces))]
        # Draw the rectangle around each face
        for count, (x, y, w, h) in enumerate(faces):

            self.face[count] = {'detect': True, 'ROI': {'x': (x, x + w), 'y': (y, y + h)}, 'pos_label': (x + 6, y - 6)}
            cv2.rectangle(self.frame.image, (x, y), (x+w, y+h), self.COLOR['blue'], 2)
            cv2.putText(self.frame.image, 'Face', self.face[count]['pos_label'],
                        cv2.FONT_HERSHEY_DUPLEX, 0.5, self.COLOR['green'], 1)
            # Display

    def profile_detection(self, gray_image: np.array):

        profile = self.profile_cascade.detectMultiScale(gray_image, 1.1, 1)
        # To draw a rectangle on each profile_faces
        for (x, y, w, h) in profile:
            cv2.rectangle(self.frame.image, (x, y), (x+w, y+h), self.COLOR['blue'], 2)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(self.frame.image, 'Profile', (x + 6, y - 6), font, 0.5, self.COLOR['green'], 1)
            # Display frames in a window

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

        self._out.write(frame)


def main():
    vid = Surveillance()
    vid.mainloop()


if __name__ == "__main__":
    main()