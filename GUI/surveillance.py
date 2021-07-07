from GUI.videoPlayer import VideoPlayer
from GUI.frameImg import FrameImg
import numpy as np
import cv2
from tkinter import *
from tkinter import ttk
import os
from skimage import morphology


class Surveillance(VideoPlayer):

    COLOR = {'red':   (0, 0, 255),
             'blue':  (255, 0, 0),
             'green': (0, 255, 0)}

    def __init__(self):

        super().__init__(image=True, play=True, camera=True, record=True)

        self.algo_stack = []
        self.frame_take = 0
        self.frame_number = 0

        self.pri_frame = FrameImg(np.zeros(self.STD_DIMS.get('0.3MP'), float))

        # segment path
        path = os.path.dirname(cv2.__file__)
        face_frontal = os.path.join(path, 'data', 'haarcascade_frontalface_default.xml')
        face_profile = os.path.join(path, 'data', "haarcascade_profileface.xml")

        # cascade classifier
        self.face_cascade = cv2.CascadeClassifier(face_frontal)
        self.profile_cascade = cv2.CascadeClassifier(face_profile)

    def _build_widget(self, parent: ttk.Frame = None, setup: dict = dict):

        self.master.geometry("950x720+0+0")
        # main panel

        self.main_panel = Frame(width=1000, height=720, bg="gray24", relief="raised", name="main_panel")
        self.main_panel.pack(side=TOP)
        self.main_panel.place(relx=0, rely=0, relwidth=1, relheight=1)


        # control panel
        matrix = {"col": [{"row": [0, 0, 0]}, {"row": [1, 1, 1]}, {"row": [2, 2, 2]}]}
        self.dynamic_panel = DynamicPanel(self.main_panel,matrix)

        super()._build_widget(self.dynamic_panel, setup)
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

                        # convert two images to gray scale
                        gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

                        # take the image and sand it to the list of function to analyze process
                        algo_list = self.algo_stack
                    
                        for n in range(0, len(algo_list)):
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

        # Detect the faces
        faces = self.face_cascade.detectMultiScale(gray_image, 1.1, 4)
        # Draw the rectangle around each face
        for (x, y, w, h) in faces:
            cv2.rectangle(self.frame.image, (x, y), (x+w, y+h), self.COLOR['blue'], 2)
            cv2.putText(self.frame.image, 'Face', (x + 6, y - 6), cv2.FONT_HERSHEY_DUPLEX, 0.5, self.COLOR['green'], 1)
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
                self.camera_recording()
                self.button_record.config(image=self.icon_record_on, relief='sunken')

            self.save_frame(frame)
            self.frame_take -= 1
            cv2.imshow('record', frame)

        elif self.frame_take == 0:
            self.button_record.config(image=self.icon_record_off, relief='raised')

    def save_frame(self, frame: np.array):

        self._out.write(frame)


def main():
    vid = Surveillance()
    vid.mainloop()


if __name__ == "__main__":
    main()
