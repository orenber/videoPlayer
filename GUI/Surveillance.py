from GUI.VideoPlayer import VideoPlayer
import numpy as np
import cv2
from tkinter import *
import os
from time import sleep
from skimage import morphology, measure, segmentation


class Surveillance(VideoPlayer):

    def __init__(self):
        super().__init__(image=True, play=True, camera=True,record = True)

        self.__play = True

        self.algo_stack = set({})
        self.frame_take = 0
        self.pri_frame = np.zeros(self.image_size, np.uint8)

        # segment path
        path = os.path.abspath(os.path.join(os.pardir, 'xml'))
        face_frontal = os.path.join(path, 'haarcascade_frontalface_default.xml')
        #full_body = os.path.join(path,"haarcascade_fullbody.xml")

        # cascade classifier
        self.face_cascade = cv2.CascadeClassifier(face_frontal)
        #self.pedestrian_cascade = cv2.CascadeClassifier(full_body)

        # load image button button_load_image
        # self.icon_algo = PhotoImage( file=os.path.join( icons_path, 'algo.PNG' ) )
        self.button_movement_detection = Button(self.control_frame, padx=10, pady=10, bd=8, fg="white", font=('arial', 12, 'bold'),
                                        text="movment", bg="black", height=1, width=8,
                                        command=lambda: self._button_movement_detection_view())
        self.button_movement_detection.pack(side='left')
        self.button_movement_value = False

        # load image button_load_image
        # self.icon_algo = PhotoImage( file=os.path.join( icons_path, 'algo.PNG' ) )
        self.button_face_detection = Button(self.control_frame, padx=10, pady=10, bd=8, fg="white", font=('arial', 12, 'bold'),
                                            text="face", bg="black", height=1, width=8,
                                            command=lambda: self._button_face_detection_view())
        self.button_face_detection.pack(side='left')
        self.button_face_value =False

        # load image button button_load_image
        # self.icon_algo = PhotoImage( file=os.path.join( icons_path, 'algo.PNG' ) )
        self.button_pedestrian_detection = Button(self.control_frame, padx=10, pady=10, bd=8, fg="white", font=('arial', 12, 'bold'),
                                                  text="body", bg="black", height=1, width=8,
                                                  command=lambda: self._button_pedestrian_detection_view() )
        self.button_pedestrian_detection.pack(side='left')
        self.button_pedestrian_value = False

    def _button_movement_detection_view(self):

        self.button_movement_value = not self.button_movement_value
        if self.button_movement_value:
            self.button_movement_detection.config(bg='white', relief='sunken')
            run_algo = True
        else:    
            run_algo = False
            self.button_movement_detection.config(bg='black', relief='raised')
        self.algo_list(run_algo, self.movement_detection)

    def _button_face_detection_view(self):

        self.button_face_value = not self.button_face_value
        if self.button_face_value :

            self.button_face_detection.config(bg='white', relief='sunken')
            self.algo_list( True, self.face_detection)
        else:    
            self.algo_list( False, self.face_detection)
            self.button_face_detection.config(bg='black', relief='raised')

    def _button_pedestrian_detection_view(self):

        self.button_pedestrian_value = not self.button_pedestrian_value
        if self.button_pedestrian_value:
            self.button_pedestrian_detection.config(bg='white', relief='sunken')
            self.algo_list(True, self.pedestrian_detection)
        else:
            self.button_pedestrian_detection.config(bg='black', relief='raised')
            self.algo_list( False, self.pedestrian_detection)

    def algo_list(self, add:bool=False, algo=None):
        if add:
            if algo not in self.algo_stack:
                self.algo_stack.add(algo)
        else:
            if algo==None:
               pass
            elif algo in self.algo_stack:
               self.algo_stack.discard(algo)

    def run_frames(self):

        frame_number = 0
        self.frame_take = 0

        while self._cap.isOpened():

            if self.__play:
                # update the frame number
                ret, frame_rgb = self._cap.read()
                # self.frame = image_matrix
                if ret:
                    frame_number += 1
                    self.update_progress(frame_number)

                    # convert two images to gray scale
                    frame = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2GRAY)

                    # take the image and sand it to the list of function to analize proces 
                    (y(frame) for y in self.algo_stack)
                    # convert matrix image to pillow image object
                    self.__frame = self.matrix_to_pillow(frame_rgb )
                    self.show_image(self.__frame)

                # refresh image display
            self.board.update()

        self._cap.release()
        self._out.release()
        cv2.destroyAllWindows()

    def face_detection(self,gray_image):

        # Detect the faces
        faces = self.face_cascade.detectMultiScale(gray_image, 1.1, 4)
        # Draw the rectangle around each face
        for (x, y, w, h) in faces:
            cv2.rectangle(self.frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        # Display
        cv2.imshow('img', self.frame)

    def pedestrian_detection(self, gray_image):
        
        pedestrians = self.pedestrian_cascade.detectMultiScale(gray_image, 1.1, 1)
        # To draw a rectangle on each pedestrians
        for (x, y, w, h) in pedestrians:
            cv2.rectangle(self.frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(self.frame, 'Person', (x + 6, y - 6), font, 0.5, (0, 255, 0), 1)
            # Display frames in a window
        return self.frame

    def movement_detection(self, frame):

        # subtract one image from another
        sub = cv2.absdiff(frame, self.pri_frame)

        # convert the product image to binary image
        (thresh, blackAndWhiteImage) = cv2.threshold( sub, 30, 255, cv2.THRESH_BINARY )
        
        # save the last frame
        self.pri_frame = frame
    
        # label image
        label_image = morphology.label( blackAndWhiteImage )
    
        # remove noise
        image_clear = morphology.remove_small_objects( label_image, min_size=100, connectivity=1 )
    
        # check how much blob thar is in the image
        cc = measure.regionprops( image_clear )
    
        # in the case thar is blob above the threshold ->  trigger record function
        if len( cc ) > 1 and self.frame_take < 150:
            record = True
            self.frame_take += 5
    
        if self.frame_take > 0:
            self.save_frame( frame )
            self.frame_take -= 1
            cv2.imshow( 'record', frame )


def main():
    vid = Surveillance()
    vid.mainloop()


if __name__ == "__main__":
    main()