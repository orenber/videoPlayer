from GUI.VideoPlayer import VideoPlayer
import numpy as np
import cv2
from tkinter import *
import os
from skimage import morphology, measure, segmentation


class Surveillance(VideoPlayer):

    def __init__(self):
        super().__init__(image=True, play=True, camera=True,record = True)

        self.__play = True

        self.algo_stack = []
        self.frame_take = 0
        self.image_size_camera = '480p'
        self.pri_frame = np.zeros((480,640), np.uint8)

        # segment path
        path = os.path.dirname( cv2.__file__ )
        face_frontal = os.path.join( path, 'data', 'haarcascade_frontalface_default.xml' )
        upper_body = os.path.join( path, 'data', "haarcascade_upperbody.xml" )


        # cascade classifier
        self.face_cascade = cv2.CascadeClassifier(face_frontal)
        self.pedestrian_cascade = cv2.CascadeClassifier(upper_body)

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
        self.button_face_value = False

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
            self.algo_list(False, self.pedestrian_detection)

    def algo_list(self, add: bool=False, algo=None):

        if add:
            if algo not in self.algo_stack:
                self.algo_stack.append(algo)
        else:
            if algo is None:
                pass

            elif algo in self.algo_stack:
                self.algo_stack.remove(algo)

    def run_frames(self):

        frame_number = 0
        self.frame_take = 0

        self.camera_recording()
        try:
            while self._cap.isOpened():

                if self.__play:
                    # update the frame number
                    ret, self.__frame = self._cap.read()

                    if ret:
                        frame_number += 1
                        self.update_progress(frame_number)

                        # convert two images to gray scale
                        gray_image = cv2.cvtColor(self.__frame, cv2.COLOR_RGB2GRAY)

                        # take the image and sand it to the list of function to analize proces 
                        algo_list = self.algo_stack
                    
                        for n in range(0,len(algo_list)):
                            algo_list[n](gray_image)
                       
                       
                        # self.face_detection(frame_gray)
                        # convert matrix image to pillow image object
                        self.__frame = self.matrix_to_pillow(self.__frame)
                        self.show_image(self.__frame)
                       
                               # refresh image display
                self.board.update()
        except Exception as e:
            print(e)
        finally:
            self._cap.release()
            cv2.destroyAllWindows()
            self._button_view_off()

    def save_frame(self, frame):
        # convert two images to gray scale

        self._out.write(frame)

    def face_detection(self, gray_image):

        # Detect the faces
        faces = self.face_cascade.detectMultiScale(gray_image, 1.1, 4)
        # Draw the rectangle around each face
        for (x, y, w, h) in faces:
            cv2.rectangle(self.__frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.putText(self.__frame, 'Face', (x + 6, y - 6), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 0, 0), 1)
        # Display

    def pedestrian_detection(self, gray_image):
        
        pedestrians = self.pedestrian_cascade.detectMultiScale(gray_image, 1.1, 1)
        # To draw a rectangle on each pedestrians
        for (x, y, w, h) in pedestrians:
            cv2.rectangle(self.__frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(self.__frame, 'Person', (x + 6, y - 6), font, 0.5, (0, 255, 0), 1)
            # Display frames in a window

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
            self.save_frame(frame)
            self.frame_take -= 1
            cv2.imshow( 'record', frame)



def main():
    vid = Surveillance()
    vid.mainloop()


if __name__ == "__main__":
    main()