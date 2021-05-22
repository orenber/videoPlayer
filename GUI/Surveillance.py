from GUI.VideoPlayer import VideoPlayer
import numpy as np
import cv2
from time import sleep
from skimage import morphology, measure, segmentation


class Surveillance(VideoPlayer):

    def __init__(self):
        super().__init__(image=True, play=True, camera=True,record = True)

        self.__play = True

    def run_frames(self):

        self.movement_detection()

    def movement_detection(self):
        frame_number = 0
        frame_take = 0

        while self._cap.isOpened():

            if self.__play:
                # update the frame number
                ret, frame_rgb = self._cap.read()
                # self.frame = image_matrix
                if ret:
                    frame_number += 1
                    self.update_progress( frame_number )

                    # convert two images to gray scale
                    frame = cv2.cvtColor( frame_rgb, cv2.COLOR_RGB2GRAY )

                    # subtract one image from another
                    sub = cv2.absdiff( frame, pri_frame )

                    # convert the product image to binary image
                    (thresh, blackAndWhiteImage) = cv2.threshold( sub, 30, 255, cv2.THRESH_BINARY )

                    # save the last frame
                    pri_frame = frame

                    # label image
                    label_image = morphology.label( blackAndWhiteImage )

                    # remove noise
                    image_clear = morphology.remove_small_objects( label_image, min_size=100, connectivity=1 )

                    # check how much blob thar is in the image
                    cc = measure.regionprops( image_clear )

                    # in the case thar is blob above the threshold ->  trigger record function
                    if len( cc ) > 1 and frame_take < 150:
                        record = True
                        frame_take += 5

                    if frame_take > 0:
                        self.save_frame( frame )
                        frame_take -= 1
                        cv2.imshow( 'record', frame )

                    # convert matrix image to pillow image object
                    self.__frame = self.matrix_to_pillow(frame_rgb )
                    self.show_image( self.__frame )

                # refresh image display
            self.board.update()

        self._cap.release()
        self._out.release()
        cv2.destroyAllWindows()





def main():
    vid = Surveillance()
    vid.mainloop()


if __name__ == "__main__":
    main()